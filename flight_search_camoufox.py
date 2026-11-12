#!/usr/bin/env python3
"""
Indore (IDR) <-> Kuala Lumpur (KUL) fare finder using Camoufox.

Rules:
  - Outbound: any day next week (2026-11-16 .. 2026-11-22)
  - Return:   7-15 days after the outbound date
  - Max 1 stop, total journey (incl. layover) < 10 h
  - Rank by cheapest total (outbound + return), one-way legs combined

Sources:
  - Google Flights: parsed automatically (prices, airline, duration, layover)
  - Skyscanner + EaseMyTrip: screenshot + page text saved to ./out for
    cross-checking the best dates (their layouts change too often to parse)

Usage:  python3 flight_search_camoufox.py            # full run
        python3 flight_search_camoufox.py --quick    # 2 outbound dates only
Output: ./out/results.csv, ./out/best_combos.txt, screenshots/text per search
"""
import csv
import re
import sys
import time
import random
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

from camoufox.sync_api import Camoufox

OUT = Path("out")
OUT.mkdir(exist_ok=True)

ORIG, DEST = "IDR", "KUL"
OUT_DATES = [date(2026, 11, 16) + timedelta(d) for d in range(7)]
MAX_MINUTES = 10 * 60
QUICK = "--quick" in sys.argv
if QUICK:
    OUT_DATES = OUT_DATES[2:4]
RET_DATES = sorted({o + timedelta(d) for o in OUT_DATES for d in range(7, 16)})


def minutes(text):
    h = re.search(r"(\d+)\s*hr", text)
    m = re.search(r"(\d+)\s*min", text)
    return (int(h.group(1)) if h else 0) * 60 + (int(m.group(1)) if m else 0)


def parse_google(page, frm, to, d):
    """Google Flights result rows carry a full aria-label sentence."""
    rows = []
    for el in page.query_selector_all('div[aria-label^="From "]'):
        label = el.get_attribute("aria-label") or ""
        price = re.search(r"From ([\d,]+) Indian rupees", label)
        dur = re.search(r"Total duration ([^.]+)\.", label)
        if not price or not dur:
            continue
        stops = 0 if "Nonstop" in label else int(re.search(r"(\d+) stops?", label).group(1)) if re.search(r"(\d+) stops?", label) else 9
        airline = re.search(r"flight with ([^.]+)\.", label)
        leave = re.search(r"Leaves (.+?) at ([\d:]+\s*[AP]M)", label)
        arrive = re.search(r"arrives at (.+?) at ([\d:]+\s*[AP]M)", label)
        lay = re.search(r"is a ([^.]+?) layover at ([^.]+?)\.", label)
        rows.append({
            "date": d.isoformat(), "route": f"{frm}-{to}",
            "price_inr": int(price.group(1).replace(",", "")),
            "airline": airline.group(1) if airline else "",
            "stops": stops, "duration_min": minutes(dur.group(1)),
            "departs": leave.group(2) if leave else "",
            "arrives": arrive.group(2) if arrive else "",
            "layover": f"{lay.group(1)} at {lay.group(2)}" if lay else "",
        })
    return rows


def google_search(page, frm, to, d):
    q = f"Flights from {frm} to {to} on {d.isoformat()} one way"
    url = f"https://www.google.com/travel/flights?hl=en&gl=IN&curr=INR&q={quote(q)}"
    page.goto(url, timeout=90000)
    page.wait_for_timeout(8000)
    # expand "other flights" if present
    for txt in ("View more flights", "more flights"):
        btn = page.query_selector(f'button:has-text("{txt}")')
        if btn:
            try:
                btn.click(); page.wait_for_timeout(4000)
            except Exception:
                pass
            break
    tag = f"google_{frm}{to}_{d:%m%d}"
    page.screenshot(path=str(OUT / f"{tag}.png"), full_page=True)
    rows = parse_google(page, frm, to, d)
    if not rows:
        (OUT / f"{tag}.txt").write_text(page.inner_text("body"))
        print(f"  ! no rows parsed for {tag} (CAPTCHA/layout?) - see {tag}.png")
    return rows


def snapshot(page, name, url):
    try:
        page.goto(url, timeout=90000)
        page.wait_for_timeout(25000)
        page.screenshot(path=str(OUT / f"{name}.png"), full_page=True)
        (OUT / f"{name}.txt").write_text(page.inner_text("body"))
        print(f"  saved {name}")
    except Exception as e:
        print(f"  {name} failed: {e}")


def sky_url(frm, to, d):
    return (f"https://www.skyscanner.co.in/transport/flights/{frm.lower()}/{to.lower()}/"
            f"{d:%y%m%d}/?adultsv2=1&cabinclass=economy&stops=!twoPlusStops&currency=INR")


def emt_url(frm, to, d):
    names = {"IDR": "Indore-India", "KUL": "Kuala Lumpur-Malaysia"}
    return (f"https://flight.easemytrip.com/FlightList/Index?srch={frm}-{quote(names[frm])}|"
            f"{to}-{quote(names[to])}|{d:%d/%m/%Y}&px=1-0-0&cbn=0&ar=undefined&isow=true"
            f"&isdm=false&lang=en-us&CCODE=IN&curr=INR&apptype=B2C")


def main():
    all_rows = []
    with Camoufox(headless=True, humanize=True, locale="en-IN", geoip=True) as browser:
        page = browser.new_page()
        legs = [(ORIG, DEST, d) for d in OUT_DATES] + [(DEST, ORIG, d) for d in RET_DATES]
        for frm, to, d in legs:
            print(f"Google {frm}->{to} {d}")
            try:
                all_rows += google_search(page, frm, to, d)
            except Exception as e:
                print(f"  error: {e}")
            time.sleep(random.uniform(4, 9))

        ok = [r for r in all_rows if r["stops"] <= 1 and r["duration_min"] < MAX_MINUTES]
        with open(OUT / "results.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()) + ["ok"] if all_rows else ["none"])
            w.writeheader()
            for r in all_rows:
                w.writerow({**r, "ok": r in ok})

        best_out = {}
        best_ret = {}
        for r in ok:
            tgt = best_out if r["route"] == f"{ORIG}-{DEST}" else best_ret
            if r["date"] not in tgt or r["price_inr"] < tgt[r["date"]]["price_inr"]:
                tgt[r["date"]] = r
        combos = []
        for od, o in best_out.items():
            for rd, rr in best_ret.items():
                gap = (date.fromisoformat(rd) - date.fromisoformat(od)).days
                if 7 <= gap <= 15:
                    combos.append((o["price_inr"] + rr["price_inr"], gap, o, rr))
        combos.sort(key=lambda c: c[0])

        lines = []
        for total, gap, o, rr in combos[:15]:
            def fmt(x):
                return (f"{x['date']} {x['airline']} {x['departs']}->{x['arrives']} "
                        f"{x['duration_min']//60}h{x['duration_min']%60:02d}m "
                        f"{'nonstop' if x['stops']==0 else 'via ' + x['layover']}  Rs {x['price_inr']:,}")
            lines.append(f"Rs {total:,}  ({gap} days)\n  OUT: {fmt(o)}\n  RET: {fmt(rr)}")
        report = "\n\n".join(lines) or "No combos met the rules - check screenshots in ./out"
        (OUT / "best_combos.txt").write_text(report)
        print("\n=== CHEAPEST COMBOS (Google Flights) ===\n" + report)

        # Cross-check top 3 outbound/return dates on Skyscanner + EaseMyTrip
        check = []
        for _, _, o, rr in combos[:3]:
            check += [(ORIG, DEST, date.fromisoformat(o["date"])), (DEST, ORIG, date.fromisoformat(rr["date"]))]
        for frm, to, d in dict.fromkeys(check):
            snapshot(page, f"sky_{frm}{to}_{d:%m%d}", sky_url(frm, to, d))
            snapshot(page, f"emt_{frm}{to}_{d:%m%d}", emt_url(frm, to, d))


if __name__ == "__main__":
    main()
