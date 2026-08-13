#!/usr/bin/env python3
"""
Listing data for larissamayfield.com property landing pages.

ONE DICT PER LISTING. generate.py turns each into /listings/<slug>.html.
The `new-listing` skill appends to LISTINGS — you can also hand-edit.

────────────────────────────────────────────────────────────────────────────
GROUND RULE: every value here must come from the MLS sheet, the county
assessor, the seller's disclosures, or Larissa's own eyes. Nothing on a
listing page may be invented. If a fact is unknown, leave it None and the
generator omits the row rather than guessing. A wrong square-footage or
septic claim on a public page is a licensing problem, not a typo.
────────────────────────────────────────────────────────────────────────────

STATUS VALUES
  "draft"       — builds the page for preview only. noindex, kept out of the
                  sitemap and the listings index, shows a PREVIEW banner.
                  New listings start here until the facts are checked.
  "coming-soon" — public, indexed, no showings yet.
  "active"      — public, indexed, showings open.
  "pending"     — public, indexed, banner says pending, form still live.
  "sold"        — public, indexed, keeps the page as an SEO/authority asset.
                  Set sold_price + sold_date.

PHOTOS
  Drop them in  images/listings/<slug>/  named so they sort in tour order:
      01-front.jpg  02-living.jpg  03-kitchen.jpg  ...
  The generator globs that folder — it never references a file that isn't
  there. First photo is the hero. Captions are optional (see photo_captions).
  Shoot/export landscape 3:2 at ~2000px wide. A draft with no photos falls
  back to stock so you can preview the layout; any non-draft status with no
  photos fails the build on purpose.
"""

# ── Required-ish keys (None = omit that row/section entirely) ────────────────
#   slug address city state zip county price beds baths sqft status
# Everything else is optional. Sections with no data don't render.

LISTINGS = [

    # ═══════════════════════════════════════════════════════════════════════
    # TEMPLATE / REFERENCE LISTING — status "draft" so it never goes public.
    # Copy this whole block for a new listing, replace every value, or let
    # the `new-listing` skill do it. Do NOT flip this one to "active".
    # ═══════════════════════════════════════════════════════════════════════
    {
        "slug": "1234-example-road",
        "status": "draft",

        # ── Identity ────────────────────────────────────────────────────────
        "address": "1234 Example Road",
        "city": "Veneta",
        "state": "OR",
        "zip": "97487",
        "county": "Lane County",
        "map_query": "Veneta, OR 97487",   # what the map iframe searches
        "lat": None,                        # decimal degrees, from the MLS
        "lng": None,

        # ── Headline numbers ────────────────────────────────────────────────
        "price": 675000,
        "sold_price": None,
        "sold_date": None,                  # "2026-09-14"
        "beds": 4,
        "baths": 2.5,
        "sqft": 2233,
        "acres": 3.67,
        "year_built": 1978,
        "property_type": "Single-Family Residence",
        "mls": None,                        # "24123456"
        "taxes_annual": 3842,               # feeds the payment estimator
        "tax_year": "2025&ndash;26",
        "hoa": None,                        # "$45/mo" or None

        # ── Editorial voice ─────────────────────────────────────────────────
        # kicker sits above the address; tagline is the one-line hook in the
        # hero aside. Write like a person who has stood on the property.
        "kicker": "Template Listing",
        "tagline": "A worked example showing every section this template can render.",
        "description": [
            "This is the template listing. It exists so you can see the full page "
            "before a real property goes on it &mdash; every section below is driven "
            "by the dictionary in listings_data.py, and any section with no data "
            "simply does not render.",
            "Write the real description the way Larissa talks: what the place "
            "actually is, who it suits, and what a buyer should walk in knowing. "
            "Three or four paragraphs. Lead with the thing that makes it "
            "different, not with &ldquo;welcome home.&rdquo;",
            "For rural parcels, say the quiet part out loud in the copy &mdash; "
            "the well&rsquo;s output, the septic&rsquo;s permit, the zoning minimum, "
            "what the outbuildings are actually good for. That is the information "
            "buyers are hunting for and almost no listing page gives them.",
        ],

        # Six short hero bullets. (label, detail)
        "highlights": [
            ("Single level", "No stairs anywhere in the main house"),
            ("3.67 acres", "Fenced pasture, mature trees, seasonal pond"),
            ("Dual-living potential", "Oversized garage, partially converted"),
            ("New roof", "Replaced 2024, transferable warranty"),
            ("RR5 zoning", "2-acre minimum &mdash; second dwelling may be permitted"),
            ("I-5 in 9 minutes", "Commutable to Eugene without feeling like it"),
        ],

        # ── The fact table. (Group title, [(label, value), ...]) ────────────
        # Rows whose value is None are dropped. Keep labels short.
        "fact_groups": [
            ("Structure", [
                ("Style", "Single level ranch"),
                ("Year built", "1978"),
                ("Living area", "2,233 sq ft"),
                ("Bedrooms", "4"),
                ("Bathrooms", "2 full, 1 half"),
                ("Garage", "Oversized 2-car, partially converted"),
                ("Roof", "Composition, replaced 2024"),
                ("Heating", "Heat pump with electric backup"),
                ("Cooling", "Central"),
                ("Flooring", "Engineered hardwood, tile, carpet"),
            ]),
            ("Land &amp; water", [
                ("Lot size", "3.67 acres"),
                ("Zoning", "RR5 &mdash; rural residential, 2-acre minimum"),
                ("Water", "Private well"),
                ("Well output", "Ask &mdash; see well log in documents"),
                ("Septic", "Standard system, county permit on file"),
                ("Irrigation", "None of record"),
                ("Fencing", "Perimeter and cross-fenced pasture"),
                ("Outbuildings", "Lean-to barn with two stalls"),
                ("Water features", "Seasonal pond"),
            ]),
            ("Financial &amp; legal", [
                ("List price", "$675,000"),
                ("Property taxes", "$3,842 (2025&ndash;26)"),
                ("Tax account", "Ask"),
                ("HOA", "None"),
                ("County", "Lane County"),
                ("Flood zone", "Ask &mdash; see RLID report"),
            ]),
        ],

        # ── Rural panel. Set to None for in-town listings. ───────────────────
        # This is the section that beats every other listing page in the valley.
        "rural": {
            "intro": "Acreage is bought and sold on infrastructure, not adjectives. "
                     "Here is what governs this parcel.",
            "items": [
                ("Water", "Private well",
                 "Well log is in the documents below. A flow test is worth ordering "
                 "during inspection &mdash; it is the single most expensive thing to "
                 "get wrong on a rural buy."),
                ("Septic", "Standard system, permitted",
                 "County permit on file. Budget for a pump-and-inspect; Lane County "
                 "records tell you the tank size and the drainfield location."),
                ("Zoning", "RR5, 2-acre minimum",
                 "At 3.67 acres this parcel exceeds the minimum, which is what opens "
                 "the door to an additional dwelling permit. Confirm with Lane County "
                 "Land Management before you count on it."),
                ("Access", "County-maintained road frontage",
                 "No shared-road maintenance agreement to negotiate."),
                ("Outbuildings", "Lean-to barn, two stalls",
                 "Suits horses, 4-H stock, or storage. Not a permitted dwelling."),
                ("Financing note", "Conventional, VA and USDA may all fit",
                 "Acreage and outbuilding value can affect appraisal &mdash; worth "
                 "a conversation with your lender before you write."),
            ],
        },

        # ── Room dimensions. (Room, dimensions, level) — or None ─────────────
        "rooms": [
            ("Primary bedroom", "16&prime; &times; 14&prime;", "Main"),
            ("Bedroom 2", "12&prime; &times; 11&prime;", "Main"),
            ("Bedroom 3", "12&prime; &times; 11&prime;", "Main"),
            ("Bedroom 4", "11&prime; &times; 10&prime;", "Main"),
            ("Living room", "20&prime; &times; 16&prime;", "Main"),
            ("Kitchen", "15&prime; &times; 13&prime;", "Main"),
            ("Dining", "13&prime; &times; 11&prime;", "Main"),
            ("Bonus / flex", "22&prime; &times; 12&prime;", "Garage conversion"),
        ],

        # ── Feature columns. {Column title: [items]} — or None ───────────────
        "features": {
            "Interior": [
                "Open kitchen to living",
                "Wood-burning stove insert",
                "Walk-in primary closet",
                "Laundry room with utility sink",
                "Pantry",
            ],
            "Exterior": [
                "Covered back patio",
                "Raised garden beds",
                "Mature oak and fir",
                "Gravel RV parking",
                "Two-stall lean-to barn",
            ],
            "Land": [
                "Fenced and cross-fenced",
                "Seasonal pond",
                "Level to gently sloping",
                "County road frontage",
                "No CC&amp;Rs of record",
            ],
        },

        # ── Schools. (Level, School, District, Distance) — or None ───────────
        # Pull from the district, not from a portal. Note the boundary caveat.
        "schools": [
            ("Elementary", "Verify with district", "Fern Ridge SD 28J", "&mdash;"),
            ("Middle", "Verify with district", "Fern Ridge SD 28J", "&mdash;"),
            ("High", "Elmira High School", "Fern Ridge SD 28J", "&mdash;"),
        ],

        # ── Drive times. (Destination, Time) — or None ───────────────────────
        "nearby": [
            ("Veneta", "6 min"),
            ("Fern Ridge Lake", "10 min"),
            ("Eugene / I-5", "25 min"),
            ("PeaceHealth RiverBend", "30 min"),
            ("Florence &amp; the coast", "50 min"),
            ("Eugene Airport (EUG)", "30 min"),
        ],

        # ── Open houses. (Weekday date label, time window) — or None ─────────
        "open_houses": None,

        # ── Documents. (Label, href, note) — or None ─────────────────────────
        # Put real files in  documents/<slug>/  and link relatively, or link
        # out to a Drive folder. Never link a document you have not opened.
        "documents": None,

        # ── Media. YouTube ID and a tour embed URL — or None ─────────────────
        "video_id": None,          # e.g. "dQw4w9WgXcQ"
        "tour_url": None,          # Matterport / Zillow 3D embed URL

        # ── Photo captions, keyed by filename in images/listings/<slug>/ ─────
        "photo_captions": {},

        # Draft-only stand-ins so the layout previews without real photos.
        # Keys come from STOCK_FILES in generate.py. Ignored once real photos
        # exist in images/listings/<slug>/.
        "sample_stock": ["parcelaerial", "whitehome", "interior", "staged",
                         "pasture", "barn", "adu", "forestpath"],

        # ── SEO ──────────────────────────────────────────────────────────────
        "seo_desc": "Template listing page for larissamayfield.com. Not a real "
                    "property &mdash; replace before publishing.",
    },


]


# ── Derived helpers used by generate.py ─────────────────────────────────────

PUBLIC_STATUSES = ("coming-soon", "active", "pending", "sold")

STATUS_LABEL = {
    "draft":       "Preview",
    "coming-soon": "Coming Soon",
    "active":      "For Sale",
    "pending":     "Sale Pending",
    "sold":        "Sold",
}


def public_listings():
    """Listings that may appear in the index, the sitemap, and search results."""
    return [l for l in LISTINGS if l.get("status") in PUBLIC_STATUSES]
