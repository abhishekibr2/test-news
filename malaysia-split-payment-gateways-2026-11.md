# Malaysia Payment Gateways: Split Payment + DuitNow Comparison (Nov 2026)

**Requirement:** a local Malaysian gateway that supports **split payment / split settlement** and at least **DuitNow** (QR or Online Banking).

> **How this was researched:** official pricing pages, API docs and T&Cs of each gateway, read through web-search indexing. The gateway sites could not be opened directly from the research environment.
> - Every figure comes from an official domain unless marked *(3rd-party)*.
> - "?" means it was not published or could not be verified.
> - Several vendors' pages contradict each other; the conflicts are noted.
> - **Confirm all rates with sales before signing.** Most vendors negotiate on volume, and SST at 8% applies to fees.

---

## 1. Shortlist summary (split + DuitNow)

| Gateway | Split payment feature | How the split works | Extra fee for split | DuitNow support | Verdict |
|---|---|---|---|---|---|
| **Razorpay Curlec** | ✅ **Route** | Linked Accounts, each with its own bank account. Transfers can be **fixed amounts** from an order, from a captured payment, or as a direct transfer. API, dashboard and batch upload. Reversible. | ⚠️ **Yes**: a per-transfer fee on top of the MDR. The docs' example uses 0.25%; the actual rate is negotiated. | DuitNow Pay (early access only). FPX is migrating to DuitNow Online Banking/Wallets with no merchant changes needed. DuitNow QR online: ? | Most complete marketplace split. Pricier. |
| **Billplz** | ✅ **Split Rule** (all plans) | Per Collection. Up to **2 recipients** in V4, which must be **Billplz accounts** identified by email. Fixed (sen) and/or % cut. **FPX payments only.** | None listed | DuitNow QR ✅ 1.5%. DuitNow Transfer used for payouts. | Cheap and simple. Splits limited to FPX and 2 recipients. |
| **CHIP** | ✅ **Split settlement** | Split to **multiple bank accounts** and/or CHIP modules, with custom speed and rate per recipient. Probably set up via sales; no public API docs for it. | None listed | DuitNow QR ✅ 1.0% (min RM0.15) | Lowest published rates. Confirm split mechanics with sales. |
| **toyyibPay** | ✅ `billSplitPayment` (API) | Recipients must be **toyyibPay users**. Fixed amounts in cents. **FPX only**, and not on dynamic-price bills. A dashboard report is available. | None listed | DuitNow QR ✅ 1% or RM1 | Cheapest overall. Basic features. |
| **senangPay** (senangPay-DOKU) | ✅ **Split Payment / Split Settlement** | Real-time % sharing (for example, agent commissions). Mass payouts are also available. Appears to be an **Enterprise** feature. | ? (Enterprise quote) | DuitNow QR only priced for softPOS (1.0%). Online DuitNow: ? | OK if on the Enterprise plan. |
| **Fiuu** (ex-Razer MS / MOLPay) | ✅ **Marketplace Payment** | One payment is split into sub-merchant transactions. Operator sees all; each sub-merchant sees its own. | ? (quote) | ✅ **DuitNow QR + DuitNow Online Banking/Wallets** + Cross-Border QR | Best DuitNow coverage. Weekly settlement. |
| **HitPay** | ✅ **Platform Partners** | Each sub-merchant has its own HitPay account with KYC. Platform commission (% or fixed) is auto-deducted, and funds go straight to the sub-merchant's bank. | None (no platform fee) | DuitNow QR ✅ 1.2% | Good for SaaS/marketplace. Higher FPX cost. |
| **Xendit MY** | ✅ **xenPlatform Split Rules** | Sub-accounts. Flat or % split, calculated after fees. Not auto-reversed on refund. | ⚠️ Pricing page: **USD 10k setup + USD 7.5k/month** + USD 5 per sub-account. A blog says ~USD 1.50 per sub-account. | ✅ DuitNow Online Banking (MYR 2.00 + 0.90). DuitNow QR ✅ (rate ?) | Enterprise-grade. Expensive. |
| **Revenue Monster** | ✅ "Split" method (web) | ? | ? | ✅ DuitNow QR | Rates not published (quote only) |
| **Stripe MY** | ✅ Connect | Destination charges, transfers, application fees | USD 2 per active account + 0.25% + 25¢ per payout (when the platform prices) | ❌ **No DuitNow** (FPX only) | ❌ Fails the DuitNow requirement |
| **iPay88** | ❌ Not found ("split" = BNPL/instalments) | n/a | n/a | DuitNow QR ✅ | ❌ No split settlement found |
| **2C2P** | ? | ? | ? | DuitNow QR ✅ | Enterprise. Nothing public. |

---

## 2. Per-transaction cost (MDR)

| Gateway | FPX (online banking) | DuitNow QR | Local cards | Foreign cards | E-wallets (TNG / GrabPay / Boost / ShopeePay) |
|---|---|---|---|---|---|
| **Billplz** Basic / Standard | **RM1.25 / RM0.75** flat (deducted from prepaid credit) | 1.5% | 1.8% / 1.5% | 3.8% / 3.5% | 1.5% all |
| **Curlec** | 1.5% or RM1, whichever is higher | DuitNow Pay: 1.2% or RM0.30, whichever is higher | Visa 2.40%, MC 2.00% | Visa 3.30%, MC 3.10% | TNG 1.5% / Grab 1.5% / Boost 1.3% / Shopee ? |
| **CHIP** | **RM1.00** (B2B RM2.00) | **1.0%** (min RM0.15) | Credit 2.0%, debit 1.0% | 3.0% | 0.95%–1.15% (pricing page) vs 1.40% (Collect page): conflicting |
| **toyyibPay** | **RM1.00** (B2B RM2.00). Non-profit "Santai" plan: RM0 | 1% or RM1 | 1.5%? (old page; another source says 2.0%) | 3.5% | ? (likely via DuitNow QR) |
| **senangPay** | 1.5% or RM1, whichever is higher | 1.0% (softPOS only) | 2.5% or RM0.65, whichever is higher | Package-based | 1.5% or RM0.65, whichever is higher |
| **Fiuu** *(Apr 2024 rate sheet)* | 1.00%, min RM1.20, max RM2.00 *(3rd-party)* | 1.00% online, 0.80% offline | ~2.40% online | ~3.15% online | Grab 1.40% / Boost 1.40% / Shopee 1.30% / TNG ? |
| **HitPay** | 1.8% + RM0.40 | 1.2% | 1.2% + RM1 | 3% + RM1 (+2% FX) | TNG 1.9% / Grab 2% / Shopee 2.2% / Boost ? |
| **Xendit** | RM1.20 personal / RM2.00 corp. **+ RM0.90** | ? + RM0.90 | Debit 1.9%, credit 2.0% + RM0.90 | 3.8% + RM0.90 | TNG 1.8% / Grab 2.0% / Shopee 2.5% + RM0.90 |
| **Stripe** | ~3% + RM1 (low confidence) | ❌ | 3% + RM1 | +1% (+2% FX) | GrabPay 3% |
| **iPay88** *(3rd-party)* | 1.9–2.7% (min RM0.60) | ? | 2.3–3.2% | ? | ~1.5% |
| **Revenue Monster** | Quote | Quote | Quote | Quote | Quote |

---

## 3. Plans, setup and annual fees

| Gateway | Plans | Setup / registration | Subscription |
|---|---|---|---|
| **Billplz** | Basic, Standard | None. Card activation RM50 per the T&C, but the pricing page says no fee (conflict). | Basic **RM0**. Standard **RM999/yr + SST** (~RM1,079) |
| **Curlec** | Basic, Standard, Enterprise | Conflicting: RM0 / RM99 / RM500 across official pages | No monthly or annual fee found |
| **CHIP** | Single pay-as-you-go | **RM0** | **RM0** |
| **toyyibPay** | Standard, Santai (non-profit) | RM100 onboarding (the manual says none: conflict) | RM100/yr from year 2 |
| **senangPay** | Starter, Advance, Enterprise | None stated now (old page: RM450) | Starter **RM199/yr** (promo 149). Advance **RM349/yr** (promo 299; adds cards and BNPL). Enterprise: quote |
| **Fiuu** | Tiered (2024) | RM99 or RM999 one-time | RM99/yr maintenance, first year waived |
| **HitPay** | Pay-as-you-go | RM0 | RM0. Add-on surcharges: +0.2% for links/invoices/store, +0.5% for the Shopify app |
| **Xendit** | Standard; xenPlatform | RM0 standard. xenPlatform USD 10k | RM0 standard. xenPlatform USD 7.5k/month |
| **Revenue Monster** | Advanced, Corporate+ | RM499 + RM99 per extra settlement account | ? |
| **iPay88** *(3rd-party)* | Start Up, SME, Corporate | RM488–RM2,579 | ~RM500/yr (SME) |

---

## 4. Settlement, payout, deposit, refund and chargeback costs

| Gateway | Settlement timeline | Payout / withdrawal fee | Deposit / reserve / prepaid | Min. payout | Refund fee | Chargeback |
|---|---|---|---|---|---|---|
| **Billplz** | FPX **T+1** (full amount, fees taken from credit). Wallets next day incl. weekends. Cards T+2. | "Free" (unclear). DuitNow Transfer payouts RM1.25 / RM0.75 | **Prepaid Credit Balance** for FPX fees, auto-reloaded from FPX collections in RM100 blocks | ? | ? | ? |
| **Curlec** | **T+2** (risk-based). Instant settlement available. | ? (instant settlement fee: ?) | ? | ? | **RM0.50** + original fee not returned | Amount + fines deducted |
| **CHIP** | FPX and DuitNow QR **T+1**. Cards and e-wallets T+2. | Own settlement: none found. CHIP Send payouts **RM1.00 each** + RM1 one-time bank verification | None found | ? | FPX RM1 (B2B RM2). Others free. | ? |
| **toyyibPay** | 1–4 business days. DuitNow QR 2 days. Santai up to 10 days. | ? | Settlements held until KYC is approved. Fees netted from payouts. | ? | ? | ? |
| **senangPay** | FPX **T+1**. Others T+2 (the T&C says twice weekly). | ? | ? | **RM100** | ? | **RM90** if contested. Scheme fees at arbitration. |
| **Fiuu** | **Weekly (Thursday)** for cards and DuitNow. T+2 for local e-wallets. | Telegraphic transfer charges borne by merchant | Reserve / settlement charge: N/A | **RM100** | FPX refund RM0.70 | N/A on the 2024 sheet |
| **HitPay** | FPX and cards **T+1**. DuitNow and e-wallets T+2. | None found | None | ? | No extra fee (original fee kept) | MYR 200? (doc may be outdated) |
| **Xendit** | Varies by method. Instant payout available for a fee. | Own-bank withdrawal **free**. Disbursements 1% (min RM1.50) + RM0.90 | ? | ? | **RM0.90** + original fees kept | **USD 25** regardless of outcome |
| **Stripe** | Daily / weekly. First payout 7–14 days. FPX T+5. | Standard free. Instant 1% (min RM2) | ? | RM2 (instant) | Fees not returned | **RM90** + RM90 if countered |

---

## 5. Recommendation

1. **Best overall for split + DuitNow on a budget: CHIP.**
   - Lowest published FPX and DuitNow QR rates.
   - No setup or annual fee, and T+1 settlement for FPX and QR.
   - Split settlement goes **directly to multiple bank accounts**, so recipients don't need gateway accounts.
   - *Action:* ask CHIP sales for the split-settlement API, whether splits are fixed or %, and the fee.
2. **Most mature split API (marketplace / platform): Razorpay Curlec Route.**
   - Linked accounts with their own bank accounts, transfers via API or batch, and reversals.
   - The trade-offs are an extra per-transfer fee, T+2 settlement and higher FPX cost. DuitNow is via FPX→DuitNow Online Banking/Wallets migration, and DuitNow Pay is early access only.
3. **Cheapest if split is FPX-only and recipients can open their own accounts:** **Billplz Standard** (RM0.75 FPX) or **toyyibPay** (RM1 FPX).
   - Neither can split DuitNow QR, card or e-wallet payments.
4. **Widest DuitNow coverage (QR + Online Banking/Wallets): Fiuu.**
   - It also has a Marketplace Payment split.
   - The trade-offs are weekly settlement, an RM100 minimum payout and no current public rate card.
5. **Exclude:**
   - **Stripe** has no DuitNow support.
   - **iPay88** has no split settlement product found.
   - **Xendit xenPlatform** is enterprise pricing, unless volume justifies it.

### Questions to send every shortlisted vendor
- Does the split work on **DuitNow QR / DuitNow Online Banking**, not just FPX?
- Can the split go to a **plain bank account**, or must recipients hold an account with the gateway?
- Is the split **fixed, %, or both**, and set per transaction via the API?
- What is the **split / transfer fee**, the **payout fee** and any **reserve or deposit**?
- What happens to splits on **refunds and chargebacks** (auto-reversal)?
- Can a **non-SSM individual** be a split recipient?

### Key sources
- Billplz: main.billplz.com/pricing, billplz.github.io/api_slate
- Curlec: curlec.com/pricing, curlec.com/docs/payments/route
- CHIP: chip-in.asia/pricing, chip-in.asia/collect
- toyyibPay: toyyibpay.com/pricing-plans, toyyibpay.com/apireference
- senangPay: senangpay.com/pricing, senangpay.com/faq
- Fiuu: fiuu.com/marketplace-payment, fiuu.com/duitnow, booster.fiuu.com/assets/Appendix_20240419.pdf
- HitPay: hitpayapp.com/my/pricing, hitpayapp.com/platform-partners-payments-api
- Xendit: xendit.co/en-my/pricing, docs.xendit.co/docs/split-payments
- Stripe: stripe.com/en-my/pricing, docs.stripe.com/payments/fpx
- Revenue Monster: revenuemonster.my/pricing
