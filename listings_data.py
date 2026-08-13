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


    # ═══════════════════════════════════════════════════════════════════════
    # REAL LISTINGS — built 2026-08-13 from the RMLS input forms and photo
    # sets in the "Active Listings" Drive folder. Facts come from the form or
    # from Larissa's own PUBLIC REMARKS on that form; nothing is inferred.
    # All start as "draft" — Larissa checks each against the sheet, then flip.
    # Fields left None are ones the form did not answer. See BUILD-NOTES.md.
    # ═══════════════════════════════════════════════════════════════════════

    {
        "slug": "1009-royal-saint-georges-dr",
        "status": "draft",
        "address": "1009 Royal Saint Georges Dr",
        "city": "Florence", "state": "OR", "zip": "97439", "county": "Lane County",
        "map_query": "1009 Royal Saint Georges Dr, Florence, OR 97439",
        "lat": None, "lng": None,
        "price": 710000, "sold_price": None, "sold_date": None,
        "beds": 3, "baths": 2.5, "sqft": 2047, "acres": None,
        "year_built": 1993, "property_type": "Single-Family Residence",
        "mls": None, "taxes_annual": None, "tax_year": None, "hoa": None,
        "kicker": "Sandpines West \u00b7 Gated",
        "tagline": "An updated Craftsman inside the gates at Sandpines West, a few minutes from the dunes.",
        "description": [
            "Nestled within the gated community of Sandpines West, this beautifully updated "
            "3-bedroom plus bonus room, 2.5-bath Craftsman offers an exceptional blend of luxury, "
            "privacy, and thoughtful upgrades throughout.",
            "Recent improvements include new interior and exterior paint, professional landscaping, "
            "new carpeting, new siding, updated lighting, new blinds, and a new HVAC system installed "
            "in December 2025. Additional major updates include a new roof in 2022, luxury vinyl plank "
            "flooring, and upgraded kitchen and bathroom countertops.",
            "The chef&rsquo;s kitchen is designed to impress with stainless steel appliances, including "
            "a range with air fry mode, wall oven, built-in microwave, and wine refrigerator. Vaulted "
            "ceilings create an open and airy feel in the spacious living room. The main-level primary "
            "suite offers seclusion with vaulted ceilings, fireplace, soaking tub, dual vanities, and "
            "generous space to unwind.",
        ],
        "highlights": [
            ("Gated community", "Sandpines West, Florence"),
            ("Main-level primary", "Vaulted ceilings, fireplace, soaking tub"),
            ("New HVAC", "Installed December 2025"),
            ("New roof", "2022"),
            ("Chef&rsquo;s kitchen", "Wall oven, wine fridge, air-fry range"),
            ("3 bed + bonus", "2,047 sq ft over two levels"),
        ],
        "fact_groups": [
            ("Structure", [
                ("Style", "Craftsman"), ("Year built", "1993"),
                ("Living area", "2,047 sq ft"), ("Levels", "2"),
                ("Bedrooms", "3 plus bonus room"), ("Bathrooms", "2.5"),
                ("Roof", "Replaced 2022"), ("HVAC", "New system, December 2025"),
                ("Flooring", "Luxury vinyl plank and new carpet"),
            ]),
            ("Community &amp; legal", [
                ("Community", "Sandpines West &mdash; gated"),
                ("City", "Florence"), ("County", "Lane County"),
                ("Property taxes", None), ("HOA", None),
            ]),
        ],
        "rural": None,
        "rooms": None,
        "features": {
            "Interior": ["Vaulted ceilings", "Main-level primary suite", "Primary fireplace",
                         "Soaking tub and dual vanities", "Wine refrigerator", "Wall oven",
                         "Range with air fry mode", "Bonus room"],
            "Recent updates": ["New HVAC (Dec 2025)", "New roof (2022)", "New siding",
                               "New interior and exterior paint", "New carpeting",
                               "Updated lighting and blinds", "Upgraded countertops"],
            "Exterior": ["Gated community", "Professional landscaping"],
        },
        "schools": None,
        "nearby": None,
        "open_houses": None, "documents": None, "video_id": None, "tour_url": None,
        "photo_captions": {}, "sample_stock": [],
        "seo_desc": "1009 Royal Saint Georges Dr, Florence OR 97439. Updated 3 bed, 2.5 bath "
                    "Craftsman with bonus room in gated Sandpines West. $710,000. Larissa Mayfield, Real Broker.",
    },

    {
        "slug": "310-pitney-ln-71",
        "status": "draft",
        "address": "310 Pitney Ln, Space 71",
        "city": "Junction City", "state": "OR", "zip": "97448", "county": "Lane County",
        "map_query": "310 Pitney Ln, Junction City, OR 97448",
        "lat": None, "lng": None,
        "price": 225000, "sold_price": None, "sold_date": None,
        "beds": 3, "baths": None, "sqft": 1337, "acres": None,
        "year_built": 2018, "property_type": "Manufactured Home in Park &mdash; home only, no land",
        "mls": None, "taxes_annual": None, "tax_year": None, "hoa": None,
        "kicker": "Manufactured Home \u00b7 Home Only",
        "tagline": "A 2018 Palm Harbor in an all-ages park \u2014 the home is for sale, the land is not.",
        "description": [
            "Immaculately maintained 2018 Palm Harbor manufactured home, offered as home only with "
            "no land included. Attractive curb appeal welcomes you in, along with a large covered "
            "porch that creates a great space to enjoy your morning coffee.",
            "Inside, the home feels fresh and inviting with an open floor plan, vaulted ceilings, and "
            "large windows that bring in plenty of natural light. Newer vinyl flooring has been added "
            "in the living room and primary bedroom. The primary suite features a walk-in closet and "
            "a spacious bathroom.",
            "Outside, the home is very nicely landscaped and shows pride of ownership throughout. "
            "Located in an all-ages manufactured home park. Space rent is $750 per month. Park "
            "approval is required to complete the purchase. Land is not included in the sale.",
        ],
        "highlights": [
            ("Home only", "The land is not included in the sale"),
            ("Space rent $750/mo", "Park approval required to purchase"),
            ("All-ages park", "No age restriction"),
            ("Built 2018", "Palm Harbor, 1,337 sq ft"),
            ("Vaulted ceilings", "Open plan, large windows"),
            ("Covered porch", "Landscaped and well kept"),
        ],
        "fact_groups": [
            ("Structure", [
                ("Make", "Palm Harbor"), ("Year built", "2018"),
                ("Living area", "1,337 sq ft"), ("Levels", "1"),
                ("Bedrooms", "3"), ("Bathrooms", None),
                ("Flooring", "Newer vinyl in living room and primary"),
            ]),
            ("Park &amp; ownership", [
                ("Ownership", "Home only &mdash; land not included"),
                ("Space rent", "$750 per month"),
                ("Park approval", "Required to complete the purchase"),
                ("Park type", "All ages"),
                ("City", "Junction City"), ("County", "Lane County"),
            ]),
        ],
        "rural": None, "rooms": None,
        "features": {
            "Interior": ["Open floor plan", "Vaulted ceilings", "Large windows",
                         "Walk-in closet in primary", "Spacious primary bathroom",
                         "Newer vinyl flooring"],
            "Exterior": ["Large covered porch", "Nicely landscaped", "Attractive curb appeal"],
        },
        "schools": None, "nearby": None,
        "open_houses": None, "documents": None, "video_id": None, "tour_url": None,
        "photo_captions": {}, "sample_stock": [],
        "seo_desc": "310 Pitney Ln Space 71, Junction City OR. 2018 Palm Harbor manufactured home, "
                    "3 bed, 1,337 sq ft, all-ages park, home only. $225,000. Larissa Mayfield, Real Broker.",
    },

    {
        "slug": "88790-faulhaber-rd",
        "status": "draft",
        "address": "88790 Faulhaber Rd",
        "city": "Elmira", "state": "OR", "zip": "97437", "county": "Lane County",
        "map_query": "88790 Faulhaber Rd, Elmira, OR 97437",
        "lat": None, "lng": None,
        "price": None, "sold_price": None, "sold_date": None,
        "beds": 4, "baths": 1.5, "sqft": 1910, "acres": 0.78,
        "year_built": None,   # form says 1965, public remarks say 1966 — Larissa to confirm
        "property_type": "Single-Family Residence",
        "mls": None, "taxes_annual": None, "tax_year": None, "hoa": None,
        "kicker": "Country Living \u00b7 Dead-End Road",
        "tagline": "Three quarters of an acre on a private dead-end road, minutes from Fern Ridge.",
        "description": [
            "Enjoy country living on this 0.78-acre property located on a private dead-end road, "
            "offering added privacy while remaining just minutes from Fern Ridge Reservoir, "
            "Highway 126, and the Oregon Coast.",
            "This ranch-style home offers approximately 1,900 square feet with 4 bedrooms, "
            "1.5 bathrooms, an updated kitchen, newer hardwood flooring, and an open living area. "
            "Recent updates include remodeled bathrooms, updated lighting, Decora switches and "
            "outlets, and a two-zone ductless mini-split system for heating and cooling. The home "
            "also features a pellet stove for supplemental heat.",
            "Outside, you&rsquo;ll find an attached two-car garage with loft storage, RV parking, two "
            "storage sheds, a chicken coop with a fenced kennel area, an 11&prime; x 20&prime; carport, "
            "landscaped grounds, and a producing mini-orchard. A new roof was installed in 2025.",
        ],
        "highlights": [
            ("0.78 acres", "Private dead-end road"),
            ("New roof", "Installed 2025"),
            ("Ductless mini-split", "Two zones, heating and cooling"),
            ("Mini-orchard", "Producing, plus landscaped grounds"),
            ("RV parking", "Plus 11&prime; x 20&prime; carport and two sheds"),
            ("Minutes to Fern Ridge", "Hwy 126 and the coast beyond"),
        ],
        "fact_groups": [
            ("Structure", [
                ("Style", "Single-level ranch"), ("Year built", None),
                ("Living area", "1,910 sq ft (RLID)"), ("Levels", "1"),
                ("Bedrooms", "4"), ("Bathrooms", "1.5"),
                ("Roof", "New in 2025"),
                ("Heating &amp; cooling", "Two-zone ductless mini-split"),
                ("Supplemental heat", "Pellet stove"),
                ("Flooring", "Newer hardwood"),
                ("Garage", "Attached two-car with loft storage"),
            ]),
            ("Land &amp; outbuildings", [
                ("Lot size", "0.78 acres"),
                ("Road", "Private dead-end, gravel"),
                ("Carport", "11&prime; x 20&prime;"),
                ("Storage", "Two sheds"),
                ("Animals", "Chicken coop with fenced kennel area"),
                ("Orchard", "Producing mini-orchard"),
                ("RV parking", "Yes"),
                ("Water", None), ("Septic", None), ("Zoning", None),
            ]),
            ("Location &amp; legal", [
                ("City", "Elmira"), ("County", "Lane County"),
                ("Tax account", "0514883"),
                ("Property taxes", None),
            ]),
        ],
        "rural": None,
        "rooms": None,
        "features": {
            "Interior": ["Updated kitchen", "Remodeled bathrooms", "Newer hardwood flooring",
                         "Open living area", "Pellet stove", "Updated lighting",
                         "Decora switches and outlets"],
            "Exterior": ["Attached two-car garage with loft", "RV parking",
                         "11&prime; x 20&prime; carport", "Two storage sheds",
                         "Chicken coop with fenced kennel", "Landscaped grounds"],
            "Land": ["0.78 acres", "Private dead-end road", "Producing mini-orchard"],
        },
        "schools": [
            ("Elementary", "Elmira Elementary", "Fern Ridge SD 28J", "&mdash;"),
            ("Middle", "Fern Ridge Middle", "Fern Ridge SD 28J", "&mdash;"),
            ("High", "Elmira High School", "Fern Ridge SD 28J", "&mdash;"),
        ],
        "nearby": None,
        "open_houses": None, "documents": None, "video_id": None, "tour_url": None,
        "photo_captions": {}, "sample_stock": [],
        "seo_desc": "88790 Faulhaber Rd, Elmira OR 97437. Ranch home on 0.78 acres, 4 bed, 1.5 bath, "
                    "1,910 sq ft, new roof 2025, minutes from Fern Ridge. Larissa Mayfield, Real Broker.",
    },

    {
        "slug": "1219-pleasant-st",
        "status": "draft",
        "address": "1219 Pleasant St",
        "city": "Springfield", "state": "OR", "zip": "97477", "county": "Lane County",
        "map_query": "1219 Pleasant St, Springfield, OR 97477",
        "lat": None, "lng": None,
        "price": None,   # form reads "325.00" in an 8-char field — Larissa to confirm
        "sold_price": None, "sold_date": None,
        "beds": 3, "baths": 1, "sqft": 874, "acres": None,
        "year_built": 1954, "property_type": "Single-Family Residence",
        "mls": None, "taxes_annual": None, "tax_year": None, "hoa": None,
        "kicker": "First Home or Investment",
        "tagline": "A tidy 1954 Springfield house with good bones and room to add value.",
        "description": [
            "Opportunity awaits in this 3-bedroom, 1-bath Springfield home, offering an affordable "
            "entry into homeownership. Whether you&rsquo;re a first-time buyer, investor, or simply "
            "looking for a place to make your own, this home provides a solid foundation with the "
            "opportunity to build equity over time.",
            "The home features hardwood floors, a brick fireplace with a pellet stove insert, maple "
            "kitchen cabinets, and central heating and air conditioning. A 2006 remodel included "
            "updated plumbing, electrical, and energy-efficient vinyl windows.",
            "Outside, you&rsquo;ll find a fully fenced backyard with a covered patio, an outdoor fire "
            "pit, mature plum, cherry, and apple trees, a storage shed, and an attached single-car "
            "garage. Conveniently located with easy access to shopping, dining, parks, and everyday "
            "amenities.",
        ],
        "highlights": [
            ("2006 remodel", "Plumbing, electrical, vinyl windows"),
            ("Hardwood floors", "Original character throughout"),
            ("Pellet stove insert", "In a brick fireplace"),
            ("Central heat &amp; air", "Not common at this price"),
            ("Fully fenced yard", "Covered patio and fire pit"),
            ("Fruit trees", "Mature plum, cherry and apple"),
        ],
        "fact_groups": [
            ("Structure", [
                ("Year built", "1954"), ("Living area", "874 sq ft (RLID)"),
                ("Levels", "1"), ("Bedrooms", "3"), ("Bathrooms", "1"),
                ("Heating &amp; cooling", "Central heat and air conditioning"),
                ("Fireplace", "Brick with pellet stove insert"),
                ("Flooring", "Hardwood"), ("Kitchen", "Maple cabinets"),
                ("Garage", "Attached single-car"),
                ("Windows", "Energy-efficient vinyl (2006)"),
            ]),
            ("Yard &amp; legal", [
                ("Fencing", "Fully fenced backyard"),
                ("Outdoor", "Covered patio, fire pit, storage shed"),
                ("Trees", "Mature plum, cherry and apple"),
                ("City", "Springfield"), ("County", "Lane County"),
                ("Property taxes", None),
            ]),
        ],
        "rural": None, "rooms": None,
        "features": {
            "Interior": ["Hardwood floors", "Brick fireplace with pellet insert",
                         "Maple kitchen cabinets", "Central heat and air",
                         "Vinyl windows (2006)"],
            "Exterior": ["Fully fenced backyard", "Covered patio", "Outdoor fire pit",
                         "Storage shed", "Attached single-car garage"],
            "Updated in 2006": ["Plumbing", "Electrical", "Energy-efficient vinyl windows"],
        },
        "schools": None, "nearby": None,
        "open_houses": None, "documents": None, "video_id": None, "tour_url": None,
        "photo_captions": {}, "sample_stock": [],
        "seo_desc": "1219 Pleasant St, Springfield OR 97477. 3 bed, 1 bath, 874 sq ft home built 1954 "
                    "with 2006 updates and a fully fenced yard. Larissa Mayfield, Real Broker.",
    },

    {
        "slug": "0-10th-st-veneta",
        "status": "draft",
        "address": "0 10th St",
        "city": "Veneta", "state": "OR", "zip": "97487", "county": "Lane County",
        "map_query": "Aspen Heights, Veneta, OR 97487",
        "lat": None, "lng": None,
        "price": None, "sold_price": None, "sold_date": None,
        "beds": None, "baths": None, "sqft": None, "acres": 0.18,
        "year_built": None, "property_type": "Residential Lot",
        "mls": None, "taxes_annual": None, "tax_year": None, "hoa": None,
        "kicker": "Building Lot \u00b7 Aspen Heights",
        "tagline": "A serviced 0.18-acre lot in Aspen Heights \u2014 bring your own builder.",
        "description": [
            "Discover this 0.18-acre lot located in the desirable Aspen Heights Subdivision in "
            "Veneta. This parcel offers an excellent opportunity to create your new home, with "
            "water, electric, and sewer connections available at the street.",
            "Bring your preferred builder and design a residence that fits your vision. The "
            "established neighborhood provides a welcoming setting while still being conveniently "
            "close to local amenities.",
        ],
        "highlights": [
            ("0.18 acres", "Aspen Heights Subdivision"),
            ("Water at the street", "Connection available"),
            ("Sewer at the street", "No septic to engineer"),
            ("Power available", "Electricity at the street"),
            ("Bring your builder", "No builder tie-in"),
            ("Established neighbourhood", "Close to Veneta amenities"),
        ],
        "fact_groups": [
            ("The parcel", [
                ("Lot size", "0.18 acres"),
                ("Subdivision", "Aspen Heights"),
                ("Manufactured home", "Permitted &mdash; see CC&amp;Rs"),
                ("City", "Veneta"), ("County", "Lane County"),
                ("Zoning", None), ("Property taxes", None),
            ]),
            ("Utilities at the street", [
                ("Water", "Available"),
                ("Sewer", "Available"),
                ("Electricity", "Available"),
                ("Natural gas", None),
            ]),
        ],
        "rural": None, "rooms": None,
        "features": {
            "The opportunity": ["Serviced building lot", "Bring your preferred builder",
                                "Design to your own plan"],
            "Utilities": ["Water available at street", "Sewer available at street",
                          "Electricity available at street"],
            "Setting": ["Aspen Heights Subdivision", "Established neighbourhood",
                        "Close to Veneta amenities"],
        },
        "schools": None, "nearby": None,
        "open_houses": None, "documents": None, "video_id": None, "tour_url": None,
        "photo_captions": {}, "sample_stock": [],
        "seo_desc": "0 10th St, Veneta OR 97487. A 0.18-acre building lot in Aspen Heights with "
                    "water, sewer and power at the street. Larissa Mayfield, Real Broker.",
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
