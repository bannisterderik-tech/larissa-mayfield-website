#!/usr/bin/env python3
"""
Market pages — one per city, at /markets/<slug>.html.

WHY THESE ARE NOT DOORWAY PAGES
The thing that makes a programmatic local page legitimate rather than spam is
whether each one carries data the others don't. Every city below has its own
verified median, its own days-on-market, its own year-over-year move and its
own sale count, pulled from that city's own Redfin market page. No two of
these say the same thing, because no two of these markets are doing the same
thing — Riddle sells in 6 days, Oakridge takes 198.

Deliberately separate from /communities/, which are hand-written pages about
places Larissa actually knows. These make no claim to local knowledge. They
report numbers and say what the numbers mean. Inventing local colour for
thirty towns would be exactly the fabrication we have avoided everywhere else.

HOW THIS DATA WAS COLLECTED
Fetched 14 Aug 2026 from each city's Redfin housing-market page, covering the
three months ending June 2026. 56 cities were attempted, 41 verified, 15
rejected — the rejects failed on their own merits and are listed in REJECTED
below so nobody wastes time re-fetching them.

Every record passed three checks:
  1. the page title actually names that city (Redfin id 5844 looks like Eugene
     and is in fact Encinitas, California)
  2. the trend paragraph is for the CURRENT period, not a stale one
  3. a median and a days-on-market figure were both present

REFRESH QUARTERLY. Bump PERIOD and ASOF when you do. Stale market data on a
licensed broker's site is worse than no market data.
"""

PERIOD = "three months ending June 2026"
SOURCE = "Redfin"
ASOF = "14 August 2026"

# name, county, median, yoy, dom, dom_prev, sold
# yoy is None where the source phrasing could not be parsed with confidence —
# three cities produced an identical suspicious value and were nulled rather
# than published.
PLACES = [
    # ── Lane County ─────────────────────────────────────────────────────────
    ("Eugene",        "Lane",     "$499,000", "-1.2%",  14, 17,  499),
    ("Springfield",   "Lane",     "$440,000", "+2.3%",  15, 14,  175),
    ("Florence",      "Lane",     "$425,000", "-15.8%", 43, 51,  50),
    ("Veneta",        "Lane",     "$421,000", "-3.3%",  19, 11,  28),
    ("Dunes City",    "Lane",     "$697,000", "+33.4%", 53, 11,  4),
    ("Coburg",        "Lane",     "$595,000", None,     19, 35,  4),
    ("Lowell",        "Lane",     "$465,000", "+7.5%",  51, 100, 7),
    ("Junction City", "Lane",     "$405,000", "-13.2%", 36, 16,  31),
    ("Creswell",      "Lane",     "$455,000", "+6.2%",  5,  31,  13),
    ("Cottage Grove", "Lane",     "$367,000", "-4.6%",  24, 38,  41),
    ("Oakridge",      "Lane",     "$260,000", "-8.7%",  198, 44, 10),
    # ── Lincoln County ──────────────────────────────────────────────────────
    ("Yachats",       "Lincoln",  "$790,000", "+28.4%", 165, 104, 5),
    ("Lincoln City",  "Lincoln",  "$535,000", "+9.2%",  68, 44,  50),
    ("Depoe Bay",     "Lincoln",  "$521,000", "-8.6%",  65, 95,  18),
    ("Newport",       "Lincoln",  "$518,000", "-2.8%",  57, 66,  29),
    ("Waldport",      "Lincoln",  "$408,000", "-19.0%", 100, 33, 12),
    ("Toledo",        "Lincoln",  "$375,000", "+19.0%", 49, 140, 11),
    # ── Benton County ───────────────────────────────────────────────────────
    ("Corvallis",     "Benton",   "$594,000", "+1.0%",  42, 46,  121),
    ("Adair Village", "Benton",   "$582,000", "+8.4%",  59, 50,  12),
    ("Philomath",     "Benton",   "$443,000", "+0.6%",  57, 36,  8),
    # ── Linn County ─────────────────────────────────────────────────────────
    ("Millersburg",   "Linn",     "$604,000", "-3.7%",  62, 79,  18),
    ("Brownsville",   "Linn",     "$465,000", "+25.6%", 56, 91,  7),
    ("Albany",        "Linn",     "$440,000", None,     65, 53,  202),
    ("Lyons",         "Linn",     "$430,000", "-26.7%", 33, 186, 5),
    ("Harrisburg",    "Linn",     "$384,000", "+6.8%",  17, 28,  5),
    ("Halsey",        "Linn",     "$375,000", "+58.5%", 93, 58,  4),
    ("Lebanon",       "Linn",     "$372,000", "-3.4%",  61, 47,  66),
    ("Sweet Home",    "Linn",     "$342,000", "+5.2%",  69, 63,  47),
    # ── Deschutes County ────────────────────────────────────────────────────
    ("Bend",          "Deschutes","$725,000", None,     24, 32,  584),
    ("Sisters",       "Deschutes","$652,000", "-10.4%", 40, 37,  33),
    ("Redmond",       "Deschutes","$471,000", "-10.2%", 26, 34,  207),
    ("La Pine",       "Deschutes","$370,000", "-3.2%",  56, 121, 29),
    # ── Klamath County ──────────────────────────────────────────────────────
    ("Klamath Falls", "Klamath",  "$289,000", "-4.7%",  72, 24,  75),
    # ── Douglas County ──────────────────────────────────────────────────────
    ("Sutherlin",     "Douglas",  "$375,000", "+3.4%",  32, 30,  35),
    ("Canyonville",   "Douglas",  "$372,000", "+69.2%", 109, 96, 2),
    ("Winston",       "Douglas",  "$353,000", "+2.7%",  59, 22,  15),
    ("Roseburg",      "Douglas",  "$322,000", "-0.82%", 22, 25,  109),
    ("Reedsport",     "Douglas",  "$305,000", "-8.4%",  72, 50,  13),
    ("Drain",         "Douglas",  "$292,000", "+10.2%", 97, 84,  6),
    ("Myrtle Creek",  "Douglas",  "$255,000", "-3.0%",  34, 32,  6),
    ("Riddle",        "Douglas",  "$248,000", "-11.0%", 6,  67,  4),
]

# Attempted and rejected, with the reason. Do not "fix" these by loosening the
# checks — a page is better absent than wrong.
REJECTED = {
    "Elkton": "most recent data July 2024", "Siletz": "August 2025",
    "Waterloo": "October 2025", "Sodaville": "November 2025",
    "Yoncalla": "March 2026", "Monroe": "April 2026", "Merrill": "April 2026",
    "Malin": "April 2026", "Chiloquin": "May 2026", "Westfir": "May 2026",
    "Scio": "incomplete", "Tangent": "incomplete", "Bonanza": "incomplete",
    "Oakland": "incomplete", "Glendale": "incomplete",
}

COUNTIES = {
    "Lane":      "Larissa's home county and primary market.",
    "Lincoln":   "The coast, north-west of Lane County.",
    "Benton":    "North of Lane County, centred on Corvallis.",
    "Linn":      "North-east of Lane County, across the valley floor.",
    "Deschutes": "East over the Cascades, the Bend and Redmond market.",
    "Klamath":   "South-east of Lane County, high desert.",
    "Douglas":   "South of Lane County, the Umpqua valley.",
}


def slugify(name):
    return name.lower().replace(" ", "-")
