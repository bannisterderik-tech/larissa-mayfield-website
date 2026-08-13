# Listing build notes — 13 Aug 2026

Five listing pages built from the RMLS input forms and photo sets in the
"Active Listings" Google Drive folder. **All five are `status: "draft"`** —
noindex, kept out of the sitemap and the listings index, and carrying a red
PREVIEW banner. Larissa checks each against her sheet, then we flip to `active`.

## What each page was built from

Facts come from two places only: the **RMLS input form** for that property, and
the **PUBLIC REMARKS** section of that same form (Larissa's own already-public
marketing copy). Nothing was inferred, and nothing was taken from the private
agent remarks or from any of the transaction paperwork in those folders.

| Listing | Price | Beds/Baths | Sq ft | Photos |
|---|---|---|---|---|
| 1009 Royal Saint Georges Dr, Florence | $710,000 | 3+bonus / 2.5 | 2,047 | 56 |
| 310 Pitney Ln Space 71, Junction City | $225,000 | 3 / — | 1,337 | 41 |
| 88790 Faulhaber Rd, Elmira | — | 4 / 1.5 | 1,910 | 48 |
| 1219 Pleasant St, Springfield | — | 3 / 1 | 874 | 41 |
| 0 10th St, Veneta (lot) | — | — | 0.18 ac | 15 |

## Open items — Larissa needs to answer these before any page goes public

1. **Three prices are missing.** The list-price field is blank on the Faulhaber
   and 0 10th St forms. On the 1219 Pleasant St form it reads `325.00` in an
   8-character field — almost certainly $325,000, but "almost certainly" is not
   good enough for a published price, so it is left blank.
2. **88790 Faulhaber Rd year built.** The form says **1965**; the public remarks
   on the same form say "this **1966** ranch-style home". Left blank until she
   confirms which is right.
3. **310 Pitney Ln bathrooms.** Not stated on the form or in the remarks.
4. **Faulhaber water and septic.** A 0.78-acre Elmira property will be on well
   and/or septic, but the form fields did not extract cleanly and I would not
   guess. These are the two facts rural buyers ask about first — worth adding.
5. **0 10th St is dated.** Its paperwork is from Sep–Oct 2025. Confirm it is
   still on the market before publishing.
6. **555 N Danebo Ave Spc 7 was not built.** That folder has listing paperwork
   only (dated 9–11 Aug 2026) — no RMLS input form and no photos yet. Nothing to
   build a page from. It needs to be shot and entered into RMLS first.

## Deliberate choices

- **No documents are linked on any page.** Those Drive folders hold listing
  contracts, CMAs, pricing matrices and agency agreements — seller-confidential
  material. 1009 Royal Saint Georges and 1219 Pleasant St *do* contain genuine
  buyer-facing disclosures (SPDS, lead-based paint, stucco/EIFS), and those could
  be published if Larissa wants; say the word and I'll wire them up.
- **"All-ages park", not "family park".** The Pitney public remarks use both
  phrases. "Family park" reads as familial-status steering under fair housing;
  "all-ages" says the same thing safely. Space rent ($750/mo) and the park
  approval requirement are in the public remarks, so they are on the page.
- **Photos** are the photographer's `images-for-web-or-mls` export where one
  existed, renumbered `01.jpg`…`NN.jpg` so they sort in the shot order. Brochure
  pages were dropped; the dimensioned floor plan is kept and placed last.
- **No rural panel on Faulhaber** despite the acreage — that section is only
  honest when the well/septic/zoning facts are in hand. See item 4.

## To publish

1. Larissa confirms the facts on each page and fills the gaps above.
2. Update `listings_data.py`, set `status: "active"`.
3. Set `SHOW_LISTINGS_NAV = True` in `generate.py` to put "Listings" in the nav
   and the index into the sitemap.
4. `python3 generate.py`, then commit and push.
