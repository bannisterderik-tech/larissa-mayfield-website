# Listing build notes — 13 Aug 2026

Five listing pages built from the RMLS input forms and photo sets in the
"Active Listings" Google Drive folder.

> **Status update — 14 Aug 2026: all five are now `status: "active"`.**
> `SHOW_LISTINGS_NAV` is `True`, the Listings nav item is live, and all five
> plus the index are in the sitemap. The only remaining draft is the
> `1234-example-road` template placeholder. The "To publish" checklist at the
> bottom of this file has been carried out — it is kept for reference on the
> next listing, not as outstanding work.

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

## Verified against the live RMLS feed — 13 Aug 2026

Every price, MLS number and status below was read off the property's own
listing page (Zillow, `Source: RMLS (OR)`), not off the input form.

| Listing | Price | MLS # | Status |
|---|---|---|---|
| 1009 Royal Saint Georges Dr, Florence | $710,000 | 132439191 | Active |
| 88790 Faulhaber Rd, Elmira | $525,000 | 243596637 | Active |
| 1219 Pleasant St, Springfield | $325,000 | 553006363 | Active |
| 310 Pitney Ln Unit 71, Junction City | $189,000 | 547423009 | Active |
| 0 10th St, Veneta | $59,000 | 573861003 | Active |

**All five are co-listed: Daniel Gandee and Larissa Mayfield, both Real Broker.**
That answers the earlier attribution question — Larissa is a listing agent on
every one. The pages currently present them under her name and agent card only.
That is accurate but not complete; if you want Daniel named too, say so.

### The input forms were stale, and it mattered

310 Pitney Ln was on the site at **$225,000**, taken from its 23 Apr input form.
The live listing is **$189,000** after two cuts:

    23 Apr 2026   listed         $225,000
     5 Jun 2026   price change   $199,900   (-11.2%)
    11 Jul 2026   price change   $189,000   (-5.5%)

The site was advertising a live listing $36,000 above its actual price. 0 10th
St had also been cut ($11K on 21 Jun) but happened to already be correct.

**Lesson for the `new-listing` skill: the RMLS input form is a point-in-time
document, not current state. Price and status must be confirmed against the
live listing before publishing, and re-checked whenever a listing has been on
market a while.**

### Also resolved

- **Faulhaber year built = 1965.** The published listing text reads "This 1965
  ranch-style home", agreeing with the form's YEAR BUILT field over the 1966 in
  its own remarks. Now on the page.
- **310 Pitney has 2 bathrooms.** Was blank.
- **MLS numbers added to all five** — they were missing entirely.

## Still open

1. **Faulhaber bathrooms.** Larissa's own description says "1.5 bathrooms";
   Zillow's summary field says 2. The page shows **1.5**, following her copy.
   Worth a glance.
2. **Faulhaber water and septic.** Still unknown, so that page still has no
   rural panel. On a 0.78-acre Elmira property this is the first thing an
   acreage buyer asks.
3. **555 N Danebo Ave Spc 7 has no page.** Listing paperwork only — no RMLS
   input form, no photos. Needs shooting and RMLS entry first.

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

## To publish (done for these five — the recipe for the next one)

1. Larissa confirms the facts on each page and fills the gaps above.
2. Update `listings_data.py`, set `status: "active"`.
3. Set `SHOW_LISTINGS_NAV = True` in `generate.py` to put "Listings" in the nav
   and the index into the sitemap.
4. `python3 generate.py`, then commit and push.
