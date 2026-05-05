#!/usr/bin/env python3
"""Generate 50+ static HTML pages for Larissa Mayfield Heritage Editorial website."""
import os, textwrap

SITE = "/Users/derikbannister9/larissa-mayfield-website"

# ── Helpers ──────────────────────────────────────────────────────────────────

def prefix(depth):
    if depth == 0: return "."
    return "/".join([".."] * depth)

def header(pfx, active=""):
    links = [
        ("about.html", "about", "About"),
        ("sellers.html", "sellers", "Sellers"),
        ("rural-acreage.html", "rural", "Rural &amp; Acreage"),
        ("buyers.html", "buyers", "Buyers"),
        ("communities/index.html", "communities", "Communities"),
        ("resources.html", "resources", "Resources"),
        ("contact.html", "contact", "Contact"),
    ]
    nav = "\n    ".join(
        f'<a href="{pfx}/{href}"' + (' class="active"' if key == active else '') + f'>{label}</a>'
        for href, key, label in links
    )
    mobile = "\n  ".join(
        f'<a href="{pfx}/{href}">{label}</a>'
        for href, key, label in [("index.html","home","Home")] + links + [("testimonials.html","testimonials","Testimonials")]
    )
    return f'''<header class="site-header">
  <div class="header-left">
    <a href="{pfx}/index.html">
      <img src="{pfx}/images/larissa-headshot-square.jpg" alt="Larissa Mayfield" width="36" height="36">
      <span class="name">Larissa Mayfield</span>
      <span class="broker">&middot; Real Broker</span>
    </a>
  </div>
  <nav class="header-nav">
    {nav}
  </nav>
  <div class="header-phone"><a href="tel:5417847745">541.784.7745</a></div>
  <button class="menu-toggle" id="menuToggle" aria-label="Menu"><span></span><span></span><span></span></button>
</header>
<div class="mobile-menu" id="mobileMenu">
  {mobile}
</div>'''

def footer(pfx):
    return f'''<footer class="site-footer">
  <div class="footer-grid">
    <div>
      <div class="footer-name">Larissa Mayfield</div>
      <div class="footer-license">REAL BROKER &middot; LIC. 201231874</div>
      <p class="footer-desc">Licensed throughout Oregon. Primary service area: Lane, Linn, Benton, and Douglas counties.</p>
    </div>
    <div class="footer-col">
      <div class="footer-col-title">Pages</div>
      <ul>
        <li><a href="{pfx}/about.html">About</a></li>
        <li><a href="{pfx}/sellers.html">Sellers</a></li>
        <li><a href="{pfx}/rural-acreage.html">Rural &amp; Acreage</a></li>
        <li><a href="{pfx}/buyers.html">Buyers</a></li>
        <li><a href="{pfx}/communities/index.html">Communities</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <div class="footer-col-title">Resources</div>
      <ul>
        <li><a href="{pfx}/guides/first-time-buyer-guide.html">First-Time Guide</a></li>
        <li><a href="{pfx}/guides/rural-buyer-playbook.html">Rural Playbook</a></li>
        <li><a href="{pfx}/blog/index.html">Blog</a></li>
        <li><a href="{pfx}/testimonials.html">Testimonials</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <div class="footer-col-title">Contact</div>
      <ul>
        <li><a href="tel:5417847745">541.784.7745</a></li>
        <li><a href="mailto:larissa@theoperativegroup.com">larissa@theoperativegroup.com</a></li>
        <li><a href="{pfx}/contact.html">Schedule a Call</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 LARISSA MAYFIELD &middot; REAL BROKER LLC</span>
    <span>EQUAL HOUSING OPPORTUNITY</span>
  </div>
</footer>'''

def breadcrumb(pfx, crumbs):
    """crumbs = list of (href_or_none, label). Last is current."""
    parts = [f'<a href="{pfx}/index.html">HOME</a>']
    for i, (href, label) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append(f'<span class="current">{label}</span>')
        else:
            parts.append(f'<a href="{pfx}/{href}">{label}</a>')
    return '<div class="breadcrumb">' + ' <span class="sep">/</span> '.join(parts) + '</div>'

def make_page(path, depth, title, desc, active, crumbs, body, schema_type="WebPage", extra_schema=""):
    pfx = prefix(depth)
    canonical = path.replace(SITE + "/", "")
    schema = f'''{{"@context":"https://schema.org","@type":"{schema_type}","name":"{title}","description":"{desc}","url":"https://larissamayfield.com/{canonical}","author":{{"@type":"RealEstateAgent","name":"Larissa Mayfield","telephone":"541-784-7745","email":"larissa@theoperativegroup.com","url":"https://larissamayfield.com","areaServed":[{{"@type":"AdministrativeArea","name":"Lane County, Oregon"}},{{"@type":"AdministrativeArea","name":"Linn County, Oregon"}},{{"@type":"AdministrativeArea","name":"Benton County, Oregon"}},{{"@type":"AdministrativeArea","name":"Douglas County, Oregon"}}]}}{extra_schema}}}'''
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Larissa Mayfield &mdash; Real Broker, Oregon</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} | Larissa Mayfield">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://larissamayfield.com/{canonical}">
<meta property="og:image" content="https://larissamayfield.com/images/og-share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} | Larissa Mayfield">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://larissamayfield.com/images/og-share.jpg">
<link rel="canonical" href="https://larissamayfield.com/{canonical}">
<link rel="icon" href="{pfx}/favicon.ico" sizes="any">
<link rel="icon" href="{pfx}/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pfx}/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pfx}/css/style.css">
<script type="application/ld+json">{schema}</script>
</head>
<body>
{header(pfx, active)}
{breadcrumb(pfx, crumbs) if crumbs else ""}
{body}
{footer(pfx)}
<script src="{pfx}/js/main.js"></script>
</body>
</html>'''
    os.makedirs(os.path.dirname(path) if "/" in path[len(SITE)+1:] else SITE, exist_ok=True)
    with open(path, "w") as f:
        f.write(html)
    print(f"  ✓ {canonical}")

# Unsplash photo URLs used as placeholders
IMG = {
    "valley": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1600&q=80",
    "farmhouse": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=1600&q=80",
    "rural": "https://images.unsplash.com/photo-1500076656116-558758c991c1?w=1600&q=80",
    "house": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=1600&q=80",
    "creek": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1600&q=80",
    "cottage": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=1600&q=80",
    "mountain": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1600&q=80",
    "meadow": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1600&q=80",
    "barn": "https://images.unsplash.com/photo-1595880723089-69855e0e3a5a?w=1600&q=80",
    "vineyard": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1600&q=80",
    "keys": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=1600&q=80",
    "couple": "https://images.unsplash.com/photo-1516455590571-18256e5bb9ff?w=1600&q=80",
    "aerial": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1600&q=80",
    "town": "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1600&q=80",
    "forest": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1600&q=80",
    "well": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=1600&q=80",
    "septic": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=1600&q=80",
    "docs": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1600&q=80",
    "contract": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1600&q=80",
}

# ── Testimonials data ────────────────────────────────────────────────────────
TESTIMONIALS = [
    ("Alan N. Gray", "Umpqua Seller, 2025", "I have bought and sold 26 homes since 1974 and I can honestly say that Larissa Mayfield is the best Realtor I&rsquo;ve ever had the pleasure of working with."),
    ("Sara &amp; Ben W.", "First-Time Buyers, Veneta, 2024", "Larissa was incredible from start to finish. She answered every single question, walked us through each step, and never made us feel rushed. We found our dream home on five acres."),
    ("Michael Torres", "Rural Seller, Junction City, 2024", "Our property had well and septic complications. Larissa handled everything calmly, found a qualified buyer, and closed on time. Couldn&rsquo;t have done it without her."),
    ("Lynn &amp; David M.", "Cottage Grove Buyers, 2024", "We relocated from California not knowing the area at all. Larissa gave us an honest, thorough tour of every community. She wasn&rsquo;t pushy and really listened to what mattered to us."),
    ("Jennifer Schultz", "Elmira Seller, 2025", "Larissa&rsquo;s market analysis was spot on. She priced our property perfectly and we had multiple offers within a week. Professional, honest, and incredibly hardworking."),
    ("Tom K.", "Land Buyer, Lane County, 2024", "Finding buildable acreage is harder than people think. Larissa understands wells, septic feasibility, access easements &mdash; the stuff most agents gloss over."),
    ("Patricia Nguyen", "Springfield Buyer, 2025", "As a single mom buying my first house, I was terrified. Larissa made the entire process feel manageable. She even coordinated with my lender when things got complicated."),
    ("Robert &amp; Jean H.", "Eugene Sellers, 2024", "Third time selling a home and the first time it didn&rsquo;t feel stressful. Larissa&rsquo;s staging suggestions, professional photos, and negotiation got us $18K over asking."),
    ("Derek Sullivan", "Investor, Lane County, 2024", "Larissa understands the numbers. She helped me evaluate three rural parcels and walked me through the zoning and timber rights on each. Data-driven and no nonsense."),
    ("Maria &amp; Carlos R.", "Creswell Buyers, 2025", "Our English isn&rsquo;t perfect and Larissa was so patient explaining every document. She found us a beautiful home near good schools. We recommend her to everyone."),
    ("Amy Chen", "Veneta Seller, 2024", "Larissa sold our property in 11 days. The drone photography made our land look stunning online. She knows rural marketing better than anyone we interviewed."),
    ("James Patterson", "Acreage Buyer, Drain, 2024", "Bought 40 acres with a creek and existing well. Larissa brought in the right inspectors, handled the title work on the easement, and made sure we knew exactly what we were getting."),
    ("Susan Walsh", "First-Time Buyer, Eugene, 2025", "I was pre-approved but still nervous. Larissa helped me understand every line of the purchase agreement and negotiated the seller to cover closing costs. She&rsquo;s a real advocate."),
    ("Kevin &amp; Lisa B.", "Oakridge Sellers, 2024", "We thought our cabin would be hard to sell. Larissa positioned it as a getaway retreat, did beautiful lifestyle photos, and found a Portland buyer within three weeks."),
    ("Rachel Dominguez", "Springfield Seller, 2025", "I interviewed three agents. Larissa was the only one who actually walked my property, pointed out what to fix, and gave me a realistic timeline. Honest and effective."),
    ("Frank Novak", "Land Seller, Linn County, 2024", "Selling bare land is tricky. Larissa understood timber value, soil reports, and how to market to the right buyer pool. Closed at 98% of asking."),
    ("The Harrison Family", "Cottage Grove Buyers, 2025", "Moving from out of state with three kids. Larissa coordinated everything remotely until we could visit. She shortlisted homes that actually matched our needs, not just our price range."),
    ("Diana Moore", "Eugene Buyer, 2024", "I work 60-hour weeks and needed an agent who could handle things independently. Larissa kept me informed without overwhelming me and made smart decisions throughout."),
    ("Greg &amp; Pam T.", "Junction City Sellers, 2025", "Our property had a shared well agreement that scared off two agents. Larissa knew exactly how to disclose it, documented the agreement properly, and we closed without issue."),
    ("Olivia Tran", "First-Time Buyer, Veneta, 2025", "Larissa helped me use a USDA loan to buy my first home on two acres. She knew which properties qualified and walked me through the extra paperwork. I&rsquo;m so grateful."),
]

# ── Community data ───────────────────────────────────────────────────────────
COMMUNITIES = [
    {
        "slug": "veneta",
        "name": "Veneta",
        "tagline": "Small-town roots, ten minutes from Eugene.",
        "desc": "Veneta sits at the western edge of the Willamette Valley where farmland meets the foothills of the Coast Range. It is one of the most affordable communities in Lane County with strong demand for acreage properties.",
        "bullets": ["Median home ~$385K", "Strong acreage market", "Fern Ridge Lake access", "Elmira-Veneta school district", "10 min to west Eugene"],
        "img": IMG["valley"],
        "seo_desc": "Explore Veneta, Oregon real estate with Larissa Mayfield. Affordable acreage, rural homes, and land near Eugene. Fern Ridge Lake, Elmira-Veneta schools."
    },
    {
        "slug": "elmira",
        "name": "Elmira",
        "tagline": "Quiet acreage living, close to everything.",
        "desc": "Elmira is an unincorporated community northwest of Eugene known for its larger lot sizes and rural character. Hobby farms, horse properties, and quiet residential acreages define the area.",
        "bullets": ["Average lot 2-10 acres", "Equestrian-friendly", "Elmira-Veneta schools", "15 min to downtown Eugene", "Fern Ridge Lake nearby"],
        "img": IMG["farmhouse"],
        "seo_desc": "Elmira, Oregon homes and acreage for sale. Horse properties, hobby farms, and rural living near Eugene. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "eugene",
        "name": "Eugene",
        "tagline": "Oregon&rsquo;s second city &mdash; culture meets nature.",
        "desc": "Eugene is the cultural and economic hub of Lane County. From the University of Oregon campus to Skinner Butte, Eugene offers walkable neighborhoods, excellent schools, and a vibrant food and arts scene.",
        "bullets": ["Population ~176K", "University of Oregon", "Strong rental market", "Bikeable infrastructure", "Gateway to the Cascades"],
        "img": IMG["town"],
        "seo_desc": "Eugene, Oregon real estate — homes, condos, investment properties. University of Oregon area. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "springfield",
        "name": "Springfield",
        "tagline": "Affordable homes, growing opportunity.",
        "desc": "Springfield has experienced significant revitalization with a growing downtown, the Glenwood riverfront district, and strong residential demand. It remains one of the most affordable markets adjacent to Eugene.",
        "bullets": ["Median home ~$365K", "Glenwood riverfront growth", "PeaceHealth medical hub", "Springfield school district", "McKenzie River access"],
        "img": IMG["house"],
        "seo_desc": "Springfield, Oregon homes for sale. Affordable real estate near Eugene, Glenwood riverfront, McKenzie River. Agent Larissa Mayfield."
    },
    {
        "slug": "junction-city",
        "name": "Junction City",
        "tagline": "Farmland and heritage in the heart of the valley.",
        "desc": "Junction City occupies some of the richest agricultural land in the Willamette Valley. Known for its Scandinavian Festival and strong farming community, it offers a quieter alternative to the Eugene-Springfield metro.",
        "bullets": ["Small-town community", "Excellent farmland", "Scandinavian heritage", "Junction City schools", "20 min to Eugene"],
        "img": IMG["meadow"],
        "seo_desc": "Junction City, Oregon real estate — farmland, acreage, rural homes in the Willamette Valley. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "cottage-grove",
        "name": "Cottage Grove",
        "tagline": "Covered bridges and forested hills.",
        "desc": "Cottage Grove sits along the Coast Fork of the Willamette River, surrounded by forested hills and famous covered bridges. It offers some of the most affordable housing in Lane County with a charming historic downtown.",
        "bullets": ["Historic downtown core", "Covered bridge capital", "Dorena Lake recreation", "Affordable entry prices", "Row River Trail"],
        "img": IMG["creek"],
        "seo_desc": "Cottage Grove, Oregon homes and land for sale. Covered bridges, Dorena Lake, affordable living. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "oakridge",
        "name": "Oakridge",
        "tagline": "Mountain biking capital of the Northwest.",
        "desc": "Oakridge is a mountain community at the edge of the Cascade Range, known globally for world-class mountain biking trails. It offers cabin retreats, timber properties, and a small-town pace of life.",
        "bullets": ["World-class MTB trails", "Cascade Range gateway", "Cabin & retreat market", "National forest access", "Growing tourism economy"],
        "img": IMG["mountain"],
        "seo_desc": "Oakridge, Oregon cabins, retreats, and mountain homes. Cascade Range gateway, world-class mountain biking. Agent Larissa Mayfield."
    },
    {
        "slug": "creswell",
        "name": "Creswell",
        "tagline": "Family-friendly and freeway-close.",
        "desc": "Creswell offers an appealing balance of small-town livability and convenient I-5 access. It is one of the fastest-growing communities in Lane County with strong schools and new residential development.",
        "bullets": ["Fast-growing community", "Creswell school district", "I-5 corridor access", "New construction market", "10 min to south Eugene"],
        "img": IMG["cottage"],
        "seo_desc": "Creswell, Oregon homes for sale — new construction, family-friendly, I-5 access. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "drain",
        "name": "Drain",
        "tagline": "Timber country with room to breathe.",
        "desc": "Drain is a small timber town in Douglas County along Highway 99. It offers very affordable large-acreage properties, rolling hills, and a genuine rural lifestyle that draws buyers seeking self-sufficiency.",
        "bullets": ["Affordable large acreage", "Timber & ranch properties", "Douglas County schools", "40 min to Roseburg", "Off-grid potential"],
        "img": IMG["barn"],
        "seo_desc": "Drain, Oregon land, acreage, and rural homes. Affordable timber country in Douglas County. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "lane-county",
        "name": "Lane County",
        "tagline": "From the ocean to the Cascades.",
        "desc": "Lane County stretches from the Oregon Coast to the Cascade Range, encompassing Eugene-Springfield and dozens of rural communities. It offers the widest range of property types in western Oregon.",
        "bullets": ["Population ~385K", "Eugene-Springfield metro", "Coast to Cascades geography", "Strong agricultural base", "University of Oregon"],
        "img": IMG["aerial"],
        "seo_desc": "Lane County, Oregon real estate overview — cities, rural communities, acreage, farmland. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "linn-county",
        "name": "Linn County",
        "tagline": "Grass seed capital and Cascade foothills.",
        "desc": "Linn County is one of Oregon&rsquo;s top agricultural counties, anchored by Albany and Lebanon. The eastern foothills offer recreational properties near the Santiam corridor.",
        "bullets": ["Albany & Lebanon hubs", "Top agricultural county", "Santiam Canyon access", "Affordable rural land", "Strong hobby farm market"],
        "img": IMG["vineyard"],
        "seo_desc": "Linn County, Oregon farms, acreage, and rural homes. Albany, Lebanon, Santiam Canyon. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "benton-county",
        "name": "Benton County",
        "tagline": "Corvallis, Oregon State, and rolling hills.",
        "desc": "Benton County is home to Corvallis and Oregon State University. It offers a highly educated population, excellent schools, and a mix of in-town homes and surrounding rural properties.",
        "bullets": ["Corvallis hub", "Oregon State University", "High quality of life", "Mary&rsquo;s Peak area", "Strong school districts"],
        "img": IMG["rural"],
        "seo_desc": "Benton County, Oregon real estate — Corvallis homes, rural acreage, Oregon State University area. Agent Larissa Mayfield."
    },
    {
        "slug": "douglas-county",
        "name": "Douglas County",
        "tagline": "Umpqua Valley &mdash; wine, timber, and wide open land.",
        "desc": "Douglas County stretches from the Umpqua Valley to the Coast Range, offering some of the most affordable acreage in western Oregon. Roseburg is the county seat and economic center.",
        "bullets": ["Roseburg county seat", "Umpqua Valley wine region", "Affordable large acreage", "Timber industry base", "South Umpqua River"],
        "img": IMG["forest"],
        "seo_desc": "Douglas County, Oregon land, acreage, and rural homes. Umpqua Valley, Roseburg, timber country. Agent Larissa Mayfield, Real Broker."
    },
]

# ── Blog data ────────────────────────────────────────────────────────────────
BLOGS = [
    {
        "slug": "well-flow-tests-oregon",
        "title": "Understanding Well Flow Tests in Oregon",
        "tag": "RURAL &middot; WELLS",
        "date": "APR 2026",
        "excerpt": "A well flow test tells you how much water a property can reliably deliver. Here is what to expect, what the numbers mean, and when to walk away.",
        "img": IMG["well"],
        "seo_desc": "What is a well flow test in Oregon? Learn GPM standards, testing procedures, and red flags for rural property buyers. Guide by Larissa Mayfield.",
        "body_sections": [
            ("What Is a Well Flow Test?", "A well flow test measures the sustained yield of a water well in gallons per minute (GPM). In Oregon, this is not legally required for a residential sale, but most lenders require one, and any buyer of rural property should insist on it. The test typically runs for two to four hours, drawing water at a steady rate while monitoring the static water level and the recovery rate."),
            ("What GPM Do You Need?", "The general rule for a single-family home is a minimum of 5 GPM sustained. However, if you plan to irrigate a garden, water livestock, or run an accessory dwelling unit, you may need 10 GPM or more. Properties below 3 GPM often require a storage tank and pressure system, which adds $5,000 to $15,000 to your setup costs."),
            ("Red Flags to Watch For", "A well that recovers slowly after drawdown may indicate a declining aquifer or seasonal limitations. Wells drilled during wet months can test well in spring and fail in August. Always ask for historical flow data if available, and request a test during the driest part of the season when possible."),
            ("Oregon Well Regulations", "The Oregon Water Resources Department (OWRD) maintains well logs for every permitted well in the state. You can look up any property&rsquo;s well log online for free. The log shows depth, casing, and the original driller&rsquo;s reported yield &mdash; though yields can change over decades."),
            ("What I Tell My Clients", "If a property has a well, the flow test is non-negotiable. I schedule it early in the inspection period so we have time to negotiate or walk away. A bad well does not always kill a deal &mdash; sometimes the seller will drill a new well or credit the cost &mdash; but you have to know what you are working with before you commit."),
        ]
    },
    {
        "slug": "oregon-bond-vs-fha",
        "title": "Oregon Bond vs. FHA: Which Loan Fits You?",
        "tag": "FINANCING &middot; FIRST-TIME BUYERS",
        "date": "MAR 2026",
        "excerpt": "Oregon&rsquo;s Bond program and FHA loans both serve first-time buyers, but the differences matter. Down payment, PMI, income limits &mdash; here is how they compare.",
        "img": IMG["docs"],
        "seo_desc": "Oregon Bond loan vs FHA loan for first-time buyers. Compare down payments, income limits, PMI, and eligibility. Guide by Larissa Mayfield.",
        "body_sections": [
            ("Oregon Bond Program Basics", "Oregon Housing and Community Services (OHCS) offers the Oregon Bond Residential Loan through approved lenders. It provides below-market interest rates and can be combined with down payment assistance. Income limits apply based on county and household size &mdash; for Lane County in 2026, the limit is approximately $110,000 for a household of two."),
            ("FHA Loan Basics", "FHA loans are insured by the Federal Housing Administration and available through most lenders. The minimum down payment is 3.5% with a credit score of 580 or higher. There are no income limits, but the property must meet FHA appraisal standards, which can be stricter than conventional appraisals."),
            ("Down Payment Comparison", "Oregon Bond can be paired with the Cash Advantage program, offering 3% of the purchase price as a forgivable grant after five years. This means you could potentially close with almost nothing out of pocket. FHA requires a flat 3.5% down payment with no state-level grant program attached."),
            ("Mortgage Insurance", "FHA carries both an upfront mortgage insurance premium (1.75% of the loan) and a monthly MIP that lasts the life of the loan for most borrowers. Oregon Bond loans structured as conventional mortgages carry PMI that drops off at 80% loan-to-value, saving you money long term."),
            ("Which Should You Choose?", "If you meet the income limits and plan to stay in the home for at least five years, Oregon Bond with Cash Advantage is almost always the better deal. If your income is above the limit or you need a faster, more flexible close, FHA is the reliable fallback. I walk every first-time buyer through both options before we start shopping."),
        ]
    },
    {
        "slug": "pricing-acreage-2026",
        "title": "How to Price Acreage in the Willamette Valley (2026)",
        "tag": "SELLERS &middot; RURAL",
        "date": "FEB 2026",
        "excerpt": "Pricing rural land is not like pricing a subdivision home. Comps are sparse, improvements vary wildly, and the buyer pool is different. Here is how it works.",
        "img": IMG["valley"],
        "seo_desc": "How to price acreage and rural land in Oregon's Willamette Valley in 2026. CMA methods, comps, and rural pricing strategy by Larissa Mayfield.",
        "body_sections": [
            ("Why Standard CMAs Fall Short", "A traditional comparative market analysis works well in subdivisions where homes share floor plans and lot sizes. On rural acreage, no two properties are alike. One parcel might have a well, a barn, and timber rights; the next might be bare pasture with a seasonal creek. You cannot simply adjust price per square foot."),
            ("The Components of Rural Value", "I break rural property value into components: the home itself, the land per acre, outbuildings and improvements, water rights or well capacity, timber value, and any income-producing features like rental units or grazing leases. Each component is analyzed separately, then combined for a total market estimate."),
            ("Finding Meaningful Comps", "In a rural market, you often have to look back 12 to 18 months and expand the radius to 15 or 20 miles. I also look at pending and withdrawn listings for price signals. A property that sat for 120 days and was withdrawn often tells you more about the market than one that sold quickly."),
            ("Pricing Strategy for 2026", "As of early 2026, rural Lane County properties between 5 and 20 acres are moving well when priced correctly. Overpriced listings are sitting, especially above $600K. The buyer pool for acreage is serious but cautious &mdash; most are cash or conventional, and they do their homework."),
            ("The Appraisal Challenge", "Even if a buyer agrees to your asking price, the lender&rsquo;s appraiser may not. Rural appraisals are notoriously conservative because appraisers face the same comp problem you do. I prepare a detailed pricing package that I share with the appraiser, including component breakdowns and comparable explanations."),
        ]
    },
    {
        "slug": "veneta-market-update",
        "title": "Veneta &amp; West Lane County: Market Snapshot",
        "tag": "MARKET &middot; VENETA",
        "date": "APR 2026",
        "excerpt": "What is happening in the Veneta and west Lane County real estate market right now? Inventory, pricing, and what buyers and sellers should expect.",
        "img": IMG["valley"],
        "seo_desc": "Veneta, Oregon and west Lane County real estate market update 2026. Inventory, pricing, trends for buyers and sellers. By Larissa Mayfield.",
        "body_sections": [
            ("Inventory Snapshot", "As of spring 2026, active residential listings in the Veneta-Elmira area hover around 25 to 35 homes at any given time, with a roughly even split between in-town properties and acreage. This represents a slight increase from the lows of 2023 and 2024, but demand remains strong for properties under $450K."),
            ("Pricing Trends", "The median sale price for Veneta proper is approximately $385K, up about 4% year over year. Acreage properties outside city limits command a premium, with 5+ acre parcels averaging $475K to $600K depending on improvements. The highest demand is for turnkey homes on 2 to 5 acres with a good well."),
            ("Buyer Profile", "Most buyers in west Lane County fall into three categories: first-time buyers using USDA or Oregon Bond loans, move-up families seeking more space, and retirees from the Portland metro or California. Cash buyers represent roughly 20% of transactions and tend to dominate the acreage market above $500K."),
            ("What Sellers Should Know", "Properly priced homes with good photos and accurate disclosures are still selling within 20 to 30 days. The key word is properly priced. Overpriced listings are sitting 60+ days, and price reductions are becoming more common. If you are thinking of selling, get a realistic CMA before you list."),
            ("Looking Ahead", "Interest rates in the mid-6% range are keeping some buyers on the sideline, but local demand fundamentals remain solid. West Lane County benefits from being one of the most affordable corridors within commuting distance of Eugene. I expect steady, moderate appreciation through 2026."),
        ]
    },
    {
        "slug": "septic-101-oregon-buyers",
        "title": "Septic Systems 101 for Oregon Buyers",
        "tag": "RURAL &middot; SEPTIC",
        "date": "JAN 2026",
        "excerpt": "Buying a property with a septic system? Here is what you need to know about inspections, permits, and what can go wrong.",
        "img": IMG["septic"],
        "seo_desc": "Septic system guide for Oregon home buyers. Inspections, permits, DEQ rules, and costs. Rural property guide by Larissa Mayfield.",
        "body_sections": [
            ("How Septic Systems Work", "A standard septic system has two main components: a tank that collects and partially treats wastewater, and a drain field that disperses the effluent into the soil. Oregon&rsquo;s Department of Environmental Quality (DEQ) regulates all onsite sewage systems. The system must be designed for the property&rsquo;s soil type and expected usage."),
            ("Inspections and Reports", "Oregon does not require a septic inspection at the time of sale, but most buyers should get one. A qualified inspector will pump the tank, check for structural damage, and evaluate the drain field. The cost is typically $400 to $600 and can reveal problems that would cost $15,000 to $30,000 to fix."),
            ("Common Issues", "The most frequent problems I see on rural properties are failing drain fields, root intrusion, and tanks that have not been pumped in years. A soggy spot in the yard near the drain field is a major red flag. Older systems installed before current DEQ standards may not meet modern code and could need complete replacement."),
            ("Replacement Costs", "A new standard septic system in Lane County costs $12,000 to $25,000 depending on soil conditions and system type. Alternative systems like sand filter or pressure-dosed systems run $20,000 to $40,000. If the property has difficult soil (heavy clay, high water table), costs can be higher."),
            ("My Advice for Buyers", "Always get a septic inspection. Always. Even on newer systems. I have seen two-year-old systems with installation defects. If the system needs replacement, we negotiate with the seller or adjust the offer. A septic problem does not have to kill a deal, but you need to know the numbers before you commit."),
        ]
    },
    {
        "slug": "pre-approval-letters-explained",
        "title": "Pre-Approval Letters: What Sellers Actually See",
        "tag": "BUYERS &middot; FINANCING",
        "date": "MAR 2026",
        "excerpt": "A pre-approval letter is your ticket to writing competitive offers. But not all pre-approvals are created equal. Here is what matters.",
        "img": IMG["contract"],
        "seo_desc": "What is a pre-approval letter? How it works, what sellers look for, and how to get a strong one. Guide by Oregon Realtor Larissa Mayfield.",
        "body_sections": [
            ("Pre-Qualification vs. Pre-Approval", "A pre-qualification is a quick estimate based on self-reported income and debt. A pre-approval involves a full credit pull, income verification, and underwriter review. In a competitive market, only a pre-approval carries weight. Sellers and listing agents can tell the difference immediately."),
            ("What the Letter Says", "A strong pre-approval letter states the loan type, the approved amount, and the expiration date. Some lenders include the buyer&rsquo;s name only; others add property-specific details. I work with lenders who will customize the letter for each offer to match the offer price exactly."),
            ("Why It Matters in Multiple Offers", "When a seller receives three offers at similar prices, the pre-approval letter is often the deciding factor. A letter from a reputable local lender with full underwriting carries more credibility than a generic online pre-qualification. It signals that the buyer is real and the financing is solid."),
            ("Getting Pre-Approved Early", "I recommend my buyers get pre-approved before we tour a single home. It sets realistic expectations, prevents heartbreak on properties you cannot afford, and lets us move fast when the right home appears. The process takes two to three business days with most lenders."),
            ("Choosing the Right Lender", "For rural properties, lender choice matters even more. Not all lenders do USDA loans. Not all appraisers know how to comp acreage. I maintain relationships with lenders who specialize in rural Oregon and can close on time even with well and septic contingencies."),
        ]
    },
    {
        "slug": "easements-explained",
        "title": "Easements Explained: What Every Buyer Must Know",
        "tag": "RURAL &middot; LEGAL",
        "date": "FEB 2026",
        "excerpt": "An easement gives someone else a right to use part of your property. Here is how to read them, what they mean, and when to worry.",
        "img": IMG["docs"],
        "seo_desc": "Understanding easements on rural property in Oregon. Access, utility, conservation easements explained. Guide by Larissa Mayfield.",
        "body_sections": [
            ("What Is an Easement?", "An easement is a legal right to use another person&rsquo;s property for a specific purpose. Common examples include access easements (a neighbor drives across your land to reach theirs), utility easements (power lines, water lines), and conservation easements (restrictions on development to protect habitat or farmland)."),
            ("Types You Will Encounter", "In rural Oregon, the most common easements are access and utility easements. Many rural properties are accessed via a shared driveway or private road with a recorded easement. These should spell out maintenance responsibilities, who can use the road, and any cost-sharing agreements."),
            ("How to Read a Title Report", "Every property purchase includes a preliminary title report that lists all recorded easements, liens, and encumbrances. I review every title report line by line with my clients. Some easements are routine (power company utility easement along the road); others can significantly affect how you use the property."),
            ("When Easements Become Problems", "An unrecorded access easement is a lawsuit waiting to happen. A blanket utility easement that covers the only buildable portion of the lot can prevent construction. A conservation easement might prohibit the barn you planned to build. These are things we check before you write an offer, not after."),
            ("Protecting Yourself", "If an easement concerns you, request a copy of the actual easement document (not just the title report summary). Have a real estate attorney review it if the language is ambiguous. In my experience, most easement issues can be resolved through negotiation or by purchasing title insurance endorsements, but you have to identify them early."),
        ]
    },
    {
        "slug": "water-rights-oregon",
        "title": "Water Rights in Oregon: A Buyer&rsquo;s Primer",
        "tag": "RURAL &middot; WATER",
        "date": "JAN 2026",
        "excerpt": "Oregon&rsquo;s water law is different from most states. If the property has irrigation, a pond, or diverts from a stream, water rights matter.",
        "img": IMG["creek"],
        "seo_desc": "Oregon water rights for rural property buyers. Permits, transfers, and what to check before buying land. Guide by Larissa Mayfield.",
        "body_sections": [
            ("Oregon&rsquo;s Prior Appropriation System", "Oregon follows the doctrine of prior appropriation, meaning water rights are separate from land ownership and are allocated based on who filed first. If you buy a property with water rights, those rights transfer with the land only if they are properly documented and have been used regularly."),
            ("Domestic Well Exemption", "Most residential wells in Oregon fall under the domestic well exemption, which allows up to 15,000 gallons per day for household use without a water right permit. However, if you plan to irrigate more than half an acre or use water for commercial purposes, you likely need a water right."),
            ("Checking Water Right Status", "The Oregon Water Resources Department (OWRD) maintains a searchable database of all water rights. I check this for every rural property with irrigation or water features. A water right that has not been used for five consecutive years may be subject to forfeiture, which means the buyer could lose it."),
            ("Transfer and Change of Use", "If you want to change how a water right is used (for example, switching from agricultural irrigation to a pond), you need to apply for a transfer with OWRD. This process can take six months to a year. It is important to understand the current authorized use before closing."),
            ("What This Means for Your Purchase", "Water rights add value to rural property, but only if they are valid and usable. I advise my clients to verify the right, confirm it has been exercised recently, and understand any conditions or limitations. If the water right is critical to your plans for the property, make the sale contingent on verification."),
        ]
    },
    {
        "slug": "usda-loans-lane-county",
        "title": "USDA Loans in Lane County: The Zero-Down Option",
        "tag": "FINANCING &middot; RURAL",
        "date": "DEC 2025",
        "excerpt": "USDA Rural Development loans offer zero down payment for qualifying properties. Many Lane County homes are eligible &mdash; here is how it works.",
        "img": IMG["keys"],
        "seo_desc": "USDA loan eligibility in Lane County, Oregon. Zero down payment, income limits, eligible areas. Guide by Larissa Mayfield, Real Broker.",
        "body_sections": [
            ("What Is a USDA Loan?", "The USDA Rural Development Guaranteed Loan program offers 100% financing (zero down payment) for homes in eligible rural areas. The program is designed to help moderate-income buyers purchase homes in communities that the USDA designates as rural. Despite the name, many suburban areas qualify."),
            ("Lane County Eligible Areas", "Much of Lane County outside the Eugene-Springfield urban growth boundary is USDA-eligible. This includes Veneta, Elmira, Cottage Grove, Creswell, Junction City, Oakridge, and most unincorporated areas. You can check any address on the USDA eligibility map at rd.usda.gov."),
            ("Income Limits", "USDA loans have income limits that vary by county and household size. For Lane County in 2026, the limit for a 1-4 person household is approximately $110,100. The limit for a 5-8 person household is approximately $145,350. These limits are adjusted annually and are higher than many people expect."),
            ("Advantages Over FHA", "USDA loans have no down payment requirement (FHA requires 3.5%), lower mortgage insurance costs, and often competitive interest rates. The upfront guarantee fee is 1% (versus 1.75% for FHA), and the annual fee is 0.35% (versus 0.55% for FHA). Over a 30-year loan, these savings add up significantly."),
            ("Working With the Right Lender", "Not all lenders offer USDA loans, and fewer still are experienced with rural properties that require well and septic. Processing times can be longer than conventional loans. I work with lenders who close USDA loans regularly in Lane County and know how to navigate the additional requirements without delays."),
        ]
    },
    {
        "slug": "closing-costs-explained",
        "title": "Closing Costs in Oregon: What to Expect",
        "tag": "BUYERS &middot; FINANCE",
        "date": "NOV 2025",
        "excerpt": "Beyond the down payment, buyers in Oregon face closing costs that typically run 2% to 4% of the purchase price. Here is the breakdown.",
        "img": IMG["docs"],
        "seo_desc": "Oregon closing costs for home buyers explained. Title insurance, escrow, recording fees, and how to negotiate. Guide by Larissa Mayfield.",
        "body_sections": [
            ("Typical Closing Cost Range", "In Oregon, buyer closing costs generally fall between 2% and 4% of the purchase price. On a $400,000 home, that means $8,000 to $16,000 in addition to your down payment. The exact amount depends on your loan type, lender fees, and whether you negotiate seller concessions."),
            ("Line-Item Breakdown", "Common buyer closing costs include: loan origination fee (0.5% to 1%), appraisal ($500 to $800), title insurance ($1,000 to $2,000), escrow fees ($500 to $1,200), recording fees ($100 to $200), home inspection ($400 to $600), and prepaid items like property tax and insurance reserves."),
            ("Oregon-Specific Costs", "Oregon does not have a general sales tax, but it does have transfer taxes in some counties and a statewide real estate transfer fee of $1 per $1,000 of sale price. Title insurance in Oregon is competitively priced compared to many states. Escrow is typically handled by a title company rather than an attorney."),
            ("Negotiating Seller Concessions", "In many transactions, the buyer can negotiate for the seller to cover some or all closing costs, typically up to 3% of the purchase price for conventional loans and 6% for FHA and USDA. This is especially common in a buyer&rsquo;s market or when the property has been listed for a while."),
            ("How I Help My Clients Prepare", "I provide a detailed closing cost estimate before we write any offer so there are no surprises. I also connect buyers with lenders who offer credits or promotions that can offset costs. My goal is to make sure you know your total out-of-pocket number, not just the down payment, before you commit."),
        ]
    },
    {
        "slug": "rural-financing-options",
        "title": "Financing a Rural Property: Your Options in Oregon",
        "tag": "FINANCING &middot; RURAL",
        "date": "JAN 2026",
        "excerpt": "Rural properties have financing quirks that standard loans do not cover. From USDA to portfolio lenders, here are your options.",
        "img": IMG["farmhouse"],
        "seo_desc": "How to finance rural property in Oregon. USDA, conventional, portfolio, and land loans. Guide by Larissa Mayfield, Real Broker.",
        "body_sections": [
            ("Why Rural Financing Is Different", "Standard Fannie Mae and Freddie Mac guidelines have rules about acreage, outbuildings, and property condition that can disqualify rural properties. A home on 40 acres with a large barn may not fit conventional underwriting. Road access, water source, and land use can all affect eligibility."),
            ("USDA Rural Development Loans", "For qualifying properties and buyers, USDA offers zero-down financing at competitive rates. Eligible areas in Lane County include Veneta, Elmira, Cottage Grove, Creswell, Junction City, and most unincorporated areas. Income limits apply but are higher than most people think."),
            ("Conventional Loans on Acreage", "Some conventional lenders will finance homes on up to 20 acres. Beyond that, they may only appraise and finance the home plus a few acres, leaving the excess land unfinanced. This means you may need a larger down payment or a separate land loan for the additional acreage."),
            ("Portfolio and Local Lenders", "Portfolio lenders are banks or credit unions that keep loans on their own books rather than selling them to the secondary market. This gives them flexibility to finance properties that do not fit standard guidelines. I work with several local portfolio lenders in the Eugene area who specialize in rural properties."),
            ("Seller Financing and Land Contracts", "For properties that are difficult to finance through traditional channels, seller financing can be an option. The seller acts as the lender and the buyer makes payments directly. This requires a willing seller and should always involve a real estate attorney. It is most common for bare land and unique rural properties."),
        ]
    },
    {
        "slug": "first-time-buyer-mistakes",
        "title": "7 First-Time Buyer Mistakes I See Every Month",
        "tag": "BUYERS &middot; TIPS",
        "date": "MAR 2026",
        "excerpt": "After hundreds of transactions, these are the mistakes first-time buyers make most often. All of them are preventable.",
        "img": IMG["couple"],
        "seo_desc": "Common first-time home buyer mistakes in Oregon and how to avoid them. Tips from experienced Realtor Larissa Mayfield.",
        "body_sections": [
            ("Skipping Pre-Approval", "Touring homes without a pre-approval letter is like test-driving cars you cannot afford. You fall in love with something outside your budget, waste time, and lose credibility with sellers. Get pre-approved before you look at a single property."),
            ("Choosing the Wrong Loan", "Many first-time buyers default to FHA when they might qualify for Oregon Bond with down payment assistance, or a USDA loan with zero down. The right loan can save you tens of thousands of dollars over the life of the mortgage. Compare at least three options."),
            ("Waiving Inspections to Compete", "In a competitive market, some buyers waive inspections to make their offer more attractive. This is risky, especially on older homes and rural properties. A $500 inspection can save you from a $30,000 septic replacement or a foundation problem."),
            ("Underestimating Closing Costs", "The down payment is not the only cash you need at closing. Budget an additional 2% to 4% of the purchase price for closing costs, plus reserves for moving, repairs, and the first few months of ownership. Running out of cash at closing is a preventable disaster."),
            ("Making Big Purchases Before Closing", "Do not buy furniture, a car, or open new credit cards between pre-approval and closing. Your lender will pull your credit again before funding, and new debt can change your debt-to-income ratio enough to kill the loan."),
            ("Ignoring the Neighborhood", "Visit the property at different times of day. Drive the commute during rush hour. Check the school ratings. Talk to the neighbors. The house itself might be perfect, but the location is permanent."),
            ("Not Using a Buyer&rsquo;s Agent", "In Oregon, the seller typically pays both the listing and buyer&rsquo;s agent commissions. Using an experienced buyer&rsquo;s agent costs you nothing and gives you someone advocating exclusively for your interests throughout the transaction."),
        ]
    },
    {
        "slug": "sellers-playbook-2026",
        "title": "The Seller&rsquo;s Playbook: Listing in 2026",
        "tag": "SELLERS &middot; STRATEGY",
        "date": "APR 2026",
        "excerpt": "The 2026 market rewards preparation. Here is the playbook I use with every seller to maximize price and minimize time on market.",
        "img": IMG["house"],
        "seo_desc": "How to sell your home in Oregon in 2026. Pricing strategy, staging, photography, and marketing. Seller's guide by Larissa Mayfield.",
        "body_sections": [
            ("Start With Honest Pricing", "Overpricing is the number one mistake sellers make. A home priced 5% too high will sit, accumulate days on market, and eventually sell for less than it would have at the correct price. I provide a detailed CMA with real comps and an honest conversation about where your home fits."),
            ("Pre-Listing Preparation", "Small investments yield outsized returns. A deep clean, declutter, fresh paint on scuffed walls, and basic landscaping can add thousands to your sale price. I provide a room-by-room preparation checklist tailored to your specific property."),
            ("Professional Photography and Media", "Over 95% of buyers start their search online. The first photo they see determines whether they click or scroll past. I invest in professional photography, drone aerials for acreage properties, and lifestyle-focused marketing that tells a story about how people live in the home."),
            ("Strategic Marketing", "Listing on the MLS is the bare minimum. I syndicate to Zillow, Realtor.com, and Redfin, run targeted social media campaigns, and leverage my network of active buyers and agents. For unique or rural properties, I also use direct mail and community-specific marketing."),
            ("Negotiation and Closing", "Multiple offers sound great, but managing them requires discipline. I evaluate each offer holistically: price, terms, financing strength, timeline, and contingencies. The highest price is not always the best offer. I guide you through every decision point from offer acceptance through closing."),
        ]
    },
    {
        "slug": "credit-improvement-tips",
        "title": "Improve Your Credit Score Before Buying a Home",
        "tag": "BUYERS &middot; FINANCE",
        "date": "DEC 2025",
        "excerpt": "A higher credit score means a lower interest rate, which means lower monthly payments. Here is how to improve your score before you apply.",
        "img": IMG["docs"],
        "seo_desc": "How to improve your credit score before buying a home. Practical tips for Oregon buyers. Guide by Larissa Mayfield, Real Broker.",
        "body_sections": [
            ("Why Your Score Matters", "Your credit score directly affects your mortgage interest rate. The difference between a 680 and a 740 score can mean 0.5% to 1% in rate difference. On a $350,000 loan over 30 years, that is $35,000 to $70,000 in additional interest. A few months of credit work can save you real money."),
            ("Check Your Reports First", "Pull your free credit reports from all three bureaus at annualcreditreport.com. Look for errors: incorrect balances, accounts that are not yours, and late payments that were actually on time. Disputing errors is the fastest way to improve your score."),
            ("Pay Down Credit Card Balances", "Credit utilization (how much of your available credit you are using) accounts for about 30% of your score. Getting your utilization below 30% helps; below 10% is ideal. If you have $10,000 in available credit, keep your balances under $1,000."),
            ("Do Not Close Old Accounts", "The length of your credit history matters. Closing an old credit card shortens your average account age and reduces your available credit, both of which can lower your score. Keep old accounts open, even if you do not use them regularly."),
            ("Avoid New Credit Applications", "Every hard inquiry (credit application) can lower your score by a few points. In the six months before you plan to buy, avoid opening new credit cards, financing furniture, or co-signing loans. The exception is mortgage shopping: multiple mortgage inquiries within a 45-day window count as a single inquiry."),
        ]
    },
]

# ── Guide data ───────────────────────────────────────────────────────────────
GUIDES = [
    {
        "slug": "first-time-buyer-guide",
        "title": "The First-Time Buyer&rsquo;s Guide to Oregon",
        "tag": "GUIDE &middot; 2026 EDITION",
        "desc": "Everything you need to know about buying your first home in Oregon. From pre-approval to closing day, this guide walks you through every step.",
        "img": IMG["keys"],
        "seo_desc": "Complete first-time home buyer guide for Oregon. Pre-approval, loan types, inspections, closing process. By Larissa Mayfield, Real Broker.",
        "sections": [
            ("Step 1: Check Your Financial Readiness", "Before you start touring homes, assess your financial position. Check your credit score, calculate your debt-to-income ratio, and review your savings. Most lenders want to see a DTI below 43% and at least two months of reserves after closing. If your score is below 620, consider spending three to six months improving it before applying."),
            ("Step 2: Get Pre-Approved", "A pre-approval is not optional in today&rsquo;s market. Work with a lender who can evaluate your full financial picture and issue a letter within a few days. Compare at least two or three lenders. I have relationships with local lenders who specialize in first-time buyer programs and can walk you through Oregon Bond, FHA, USDA, and conventional options."),
            ("Step 3: Define Your Must-Haves", "Make two lists: must-haves and nice-to-haves. Be honest about what you can compromise on. Location, school district, and commute are the hardest things to change. Kitchens and bathrooms can be updated over time. A clear list helps me find the right homes faster and prevents decision fatigue."),
            ("Step 4: Tour Homes Strategically", "I limit home tours to five to seven homes per outing. Seeing too many in one day causes everything to blur together. I schedule tours in order of priority and provide a comparison sheet so you can evaluate each property against your criteria objectively."),
            ("Step 5: Write a Competitive Offer", "When you find the right home, we move quickly. I will prepare a comparative analysis to guide your offer price, advise on terms and contingencies, and write the offer that night. In a competitive market, speed and preparation win. Your pre-approval letter and proof of funds go in with every offer."),
            ("Step 6: Navigate Inspections", "Once your offer is accepted, the inspection period begins. I coordinate a home inspection, and for rural properties, well and septic inspections as well. If the inspection reveals issues, we negotiate repairs or credits. This is where having an experienced agent makes the biggest difference."),
            ("Step 7: Close and Get Your Keys", "The final two to three weeks involve appraisal, final underwriting, and closing preparation. I monitor every deadline, coordinate with your lender and the title company, and make sure nothing falls through the cracks. On closing day, you sign the documents, the funds transfer, and you get the keys to your new home."),
        ]
    },
    {
        "slug": "rural-buyer-playbook",
        "title": "The Rural Buyer&rsquo;s Playbook",
        "tag": "GUIDE &middot; ACREAGE &amp; LAND",
        "desc": "Buying rural property in Oregon is not like buying in a subdivision. Wells, septic, easements, zoning, and more &mdash; this playbook covers everything.",
        "img": IMG["valley"],
        "seo_desc": "Complete guide to buying rural property and acreage in Oregon. Wells, septic, easements, zoning, financing. By Larissa Mayfield.",
        "sections": [
            ("Why Rural Is Different", "Rural property transactions involve complexities that suburban sales do not. Water comes from a well, not a city line. Wastewater goes to a septic system, not a sewer. Roads may be private with shared maintenance agreements. Zoning can restrict what you build and how you use the land. This guide prepares you for all of it."),
            ("Water: Wells and Water Rights", "The well is the property&rsquo;s water supply. Get a flow test (minimum 5 GPM for a single-family home), review the well log with OWRD, and inspect the well head and pump system. If the property has irrigation rights, verify they are current and transferable. Water is the single most important infrastructure element on rural property."),
            ("Wastewater: Septic Systems", "A septic inspection should be performed on every property with an onsite system. The inspector will pump the tank, check the drain field, and assess the system&rsquo;s remaining life. Replacement costs range from $12,000 to $40,000 depending on soil conditions and system type. Factor this into your offer if needed."),
            ("Access: Roads and Easements", "How do you get to the property? If the road is private, who maintains it? Is there a recorded road maintenance agreement? Are there easements that affect where you can build? Review the preliminary title report carefully and walk the property boundaries if possible."),
            ("Zoning and Land Use", "Lane County has multiple zoning designations for rural land: EFU (Exclusive Farm Use), F-1 and F-2 (Forest), RR (Rural Residential), and others. Each has different rules about what you can build, how many dwellings are allowed, and what activities are permitted. I check zoning before we write an offer."),
            ("Financing Rural Properties", "Not all lenders finance rural properties, and not all appraisers know how to comp them. USDA loans work for qualifying properties and buyers. Conventional loans may limit acreage. Portfolio lenders offer the most flexibility. I connect you with lenders who specialize in rural Oregon and can close on time."),
            ("Due Diligence Checklist", "Before closing on rural property, verify: well flow test results, septic inspection report, recorded easements and access rights, zoning designation and allowed uses, flood zone status, soil type and buildability, timber rights (if applicable), water rights (if applicable), and any HOA or CCR restrictions. I track every item on this list for my clients."),
        ]
    },
    {
        "slug": "lane-county-market-notes",
        "title": "Lane County Real Estate: Market Notes",
        "tag": "MARKET &middot; 2026",
        "desc": "Current market conditions, trends, and outlook for Lane County, Oregon real estate. Updated for 2026.",
        "img": IMG["aerial"],
        "seo_desc": "Lane County, Oregon real estate market report 2026. Median prices, inventory, trends, and outlook. By Larissa Mayfield, Real Broker.",
        "sections": [
            ("Market Overview", "Lane County&rsquo;s real estate market in 2026 is characterized by moderate appreciation, improving inventory, and steady demand. The median home price across the county is approximately $410,000, up about 3.5% year over year. Urban Eugene-Springfield and rural communities are performing differently, and understanding those differences is key."),
            ("Eugene-Springfield Metro", "The Eugene-Springfield metro area remains the most active market in Lane County. Median sale prices hover around $425,000 for Eugene and $365,000 for Springfield. Inventory has improved from the extremely low levels of 2021 through 2023, but well-priced homes in desirable neighborhoods still receive multiple offers."),
            ("Rural and Acreage Market", "Rural properties and acreage parcels continue to attract strong interest from both local and out-of-state buyers. The market is bifurcated: turnkey homes on small acreage (2 to 10 acres) move quickly, while larger parcels and fixer-uppers require more patience. Correct pricing is critical in this segment."),
            ("Interest Rate Impact", "Mortgage rates in the mid-6% range are keeping some entry-level buyers on the sideline. However, Oregon Bond and USDA programs offer rate advantages that bring many of these buyers back into the market. Buyers who locked rates during brief dips in early 2026 are particularly well-positioned."),
            ("Outlook for the Rest of 2026", "I expect moderate, steady appreciation of 3% to 5% for Lane County through the remainder of 2026. The fundamentals are solid: job growth at the University of Oregon and PeaceHealth, quality of life driving in-migration, and limited buildable land constraining supply. The biggest risk is a sustained rate increase above 7%, which would cool demand noticeably."),
        ]
    },
]

# ── Service/specialty pages ──────────────────────────────────────────────────
SERVICES = [
    {
        "slug": "home-valuation",
        "title": "Free Home Valuation",
        "tag": "SELLERS &middot; NO OBLIGATION",
        "desc": "Get a free, no-obligation valuation of your Oregon home or land based on real comparable sales and local market knowledge.",
        "seo_desc": "Free home valuation in Lane County, Oregon. Honest pricing based on real comps. Request yours from Larissa Mayfield, Real Broker.",
        "body": '''<section class="section-dark">
  <div class="valuation-grid">
    <div>
      <div class="tag reveal" style="margin-bottom:24px">Sellers &middot; No-Obligation Valuation</div>
      <h1 class="page-title reveal reveal-d1" style="color:var(--cream)">What is your property<br><em style="color:var(--cream)"><i>worth today?</i></em></h1>
      <p class="body-text reveal reveal-d2" style="color:rgba(244,239,230,.85);margin-top:32px;max-width:460px">I provide a detailed, honest valuation based on actual comparable sales in your area &mdash; not automated estimates. Every valuation includes a conversation about your property&rsquo;s unique features and the current market conditions in your neighborhood.</p>
      <p class="body-text reveal reveal-d3" style="color:rgba(244,239,230,.65);margin-top:24px;max-width:460px;font-size:14px">Free. No obligation. No pressure. Just the information you need to make an informed decision.</p>
    </div>
    <form class="valuation-form reveal reveal-d2" onsubmit="event.preventDefault()">
      <label><div class="label-text">PROPERTY ADDRESS</div><input type="text" placeholder="24500 Hwy 126, Veneta OR"></label>
      <label><div class="label-text">APPROXIMATE ACREAGE</div><input type="text" placeholder="12.5"></label>
      <label><div class="label-text">PROPERTY TYPE</div><input type="text" placeholder="Rural / Acreage / Residential"></label>
      <label><div class="label-text">YOUR NAME</div><input type="text" placeholder="Your name"></label>
      <label><div class="label-text">EMAIL OR PHONE</div><input type="text" placeholder="you@email.com"></label>
      <button type="submit">REQUEST VALUATION &rarr;</button>
    </form>
  </div>
</section>
<section style="padding:96px 56px">
  <div class="tag tag-purple reveal">How It Works</div>
  <h2 class="section-heading reveal reveal-d1" style="margin-top:18px">Three steps to your valuation.</h2>
  <div class="timeline-grid" style="grid-template-columns:repeat(3,1fr)">
    <div class="timeline-step reveal"><div class="num">01</div><h3>Request</h3><p>Fill out the form above or call me directly. I will confirm receipt within 24 hours.</p></div>
    <div class="timeline-step reveal reveal-d1"><div class="num">02</div><h3>Research</h3><p>I pull comparable sales, review tax records, and analyze current market conditions for your area.</p></div>
    <div class="timeline-step reveal reveal-d2"><div class="num">03</div><h3>Deliver</h3><p>You receive a detailed valuation report with my assessment and a no-obligation conversation about your options.</p></div>
  </div>
</section>'''
    },
    {
        "slug": "first-time-buyer-program",
        "title": "First-Time Buyer Program",
        "tag": "BUYERS &middot; SPECIALIZED SUPPORT",
        "desc": "Dedicated support for first-time home buyers in Oregon. From loan selection to closing day, I guide you through every step.",
        "seo_desc": "First-time home buyer program in Oregon. Pre-approval, Oregon Bond, USDA loans, step-by-step guidance. Larissa Mayfield, Real Broker.",
    },
    {
        "slug": "acreage-specialist",
        "title": "Acreage &amp; Land Specialist",
        "tag": "RURAL &middot; SPECIALTY",
        "desc": "Specialized expertise in buying and selling acreage properties in Oregon&rsquo;s Willamette Valley. Wells, septic, easements, zoning &mdash; I handle the complexity.",
        "seo_desc": "Oregon acreage and land specialist. Wells, septic, easements, rural pricing. Expert agent Larissa Mayfield, Real Broker.",
    },
    {
        "slug": "relocation-guide",
        "title": "Relocating to Oregon",
        "tag": "BUYERS &middot; RELOCATION",
        "desc": "Moving to Oregon from out of state? This guide covers communities, cost of living, climate, schools, and how to buy remotely.",
        "seo_desc": "Relocating to Oregon guide. Cost of living, communities, schools, climate, and remote buying process. By Larissa Mayfield, Real Broker.",
    },
    {
        "slug": "investment-property",
        "title": "Investment Property in Lane County",
        "tag": "INVESTORS &middot; LANE COUNTY",
        "desc": "Lane County offers strong rental demand, affordable entry points, and appreciation potential. Here is what investors need to know.",
        "seo_desc": "Investment property in Lane County, Oregon. Rental demand, cap rates, and market analysis. Guide by Larissa Mayfield, Real Broker.",
    },
    {
        "slug": "downsizing-guide",
        "title": "Downsizing in Oregon",
        "tag": "SELLERS &middot; LIFESTYLE",
        "desc": "Thinking about downsizing? From selling your current home to finding the right fit, this guide covers the emotional and practical sides.",
        "seo_desc": "Downsizing your home in Oregon. Selling, buying smaller, and making the transition. Guide by Larissa Mayfield, Real Broker.",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def gen_home():
    body = f'''<section class="hero-split">
  <div>
    <div class="tag reveal">LARISSA MAYFIELD &middot; REAL BROKER &middot; OREGON</div>
    <h1 class="reveal reveal-d1">Every home<br>tells a<br><em>story.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:36px;max-width:420px">Licensed throughout Oregon with deep roots in Lane, Linn, Benton, and Douglas counties. I specialize in rural properties, acreage, and first-time buyers.</p>
    <div style="margin-top:36px;display:flex;gap:14px;flex-wrap:wrap" class="reveal reveal-d3">
      <a class="btn-primary" href="contact.html">Schedule a Call &rarr;</a>
      <a class="btn-link" href="sellers.html">Sell Your Home</a>
    </div>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="images/larissa-hat.jpg" alt="Larissa Mayfield in the Willamette Valley"></div>
</section>
<div class="meta-strip">
  <span>REAL BROKER</span><span>LIC. 201231874</span><span>LANE &middot; LINN &middot; BENTON &middot; DOUGLAS</span><span>541.784.7745</span>
</div>
<section class="feature-section">
  <div class="feature-sticky">
    <div class="tag tag-purple reveal">Why Larissa</div>
    <h2 class="section-heading reveal reveal-d1" style="margin-top:18px">Built for rural&nbsp;sellers.</h2>
    <p class="body-text reveal reveal-d2" style="margin-top:24px;max-width:380px">Two decades in commercial lending taught me how rural transactions actually close. Wells. Septic. Easements. Comparable sales five miles apart. I handle the complexity so you don&rsquo;t have to.</p>
    <a class="btn-primary reveal reveal-d3" href="about.html" style="margin-top:28px">Read My Story &rarr;</a>
  </div>
  <div class="feature-grid-2x2">
    <div class="feature-card reveal"><div class="num">01</div><h3>Rural Pricing</h3><p>Component-based valuations that account for land, improvements, water, and timber &mdash; not Zillow estimates.</p></div>
    <div class="feature-card reveal reveal-d1"><div class="num">02</div><h3>Buyer Financing</h3><p>USDA, Oregon Bond, conventional, portfolio &mdash; I match the right loan to the right property.</p></div>
    <div class="feature-card reveal reveal-d2"><div class="num">03</div><h3>Due Diligence</h3><p>Well flow tests, septic inspections, easement review, title work &mdash; managed from day one.</p></div>
    <div class="feature-card reveal reveal-d3"><div class="num">04</div><h3>Lifestyle Media</h3><p>Drone aerials, lifestyle photography, and storytelling that shows buyers how they will live on the property.</p></div>
  </div>
</section>
<section class="section-dark">
  <div class="valuation-grid">
    <div>
      <div class="tag reveal" style="margin-bottom:24px">Sellers &middot; No-Obligation Valuation</div>
      <h2 class="section-heading reveal reveal-d1" style="color:var(--cream)">What is your property<br><em style="color:var(--cream)"><i>worth today?</i></em></h2>
      <p class="body-text reveal reveal-d2" style="color:rgba(244,239,230,.85);margin-top:24px;max-width:420px">A free, no-obligation valuation built from real comparable sales and an honest conversation about today&rsquo;s market.</p>
    </div>
    <form class="valuation-form reveal reveal-d2" onsubmit="event.preventDefault()">
      <label><div class="label-text">PROPERTY ADDRESS</div><input type="text" placeholder="24500 Hwy 126, Veneta OR"></label>
      <label><div class="label-text">APPROXIMATE ACREAGE</div><input type="text" placeholder="12.5"></label>
      <label><div class="label-text">YOUR NAME</div><input type="text" placeholder="Your name"></label>
      <label><div class="label-text">EMAIL OR PHONE</div><input type="text" placeholder="you@email.com"></label>
      <button type="submit">REQUEST VALUATION &rarr;</button>
    </form>
  </div>
</section>
<section style="padding:96px 56px">
  <div class="tag tag-purple reveal">Communities</div>
  <h2 class="section-heading reveal reveal-d1" style="margin-top:18px;margin-bottom:40px">Where I work.</h2>
  <div class="community-grid">
    <article class="reveal"><a href="communities/veneta.html"><img src="{IMG['valley']}" alt="Veneta Oregon"><h3>Veneta</h3><p>Small-town roots, ten minutes from Eugene.</p></a></article>
    <article class="reveal reveal-d1"><a href="communities/elmira.html"><img src="{IMG['farmhouse']}" alt="Elmira Oregon"><h3>Elmira</h3><p>Quiet acreage living, close to everything.</p></a></article>
    <article class="reveal reveal-d2"><a href="communities/eugene.html"><img src="{IMG['town']}" alt="Eugene Oregon"><h3>Eugene</h3><p>Oregon&rsquo;s second city.</p></a></article>
    <article class="reveal reveal-d3"><a href="communities/springfield.html"><img src="{IMG['house']}" alt="Springfield Oregon"><h3>Springfield</h3><p>Affordable homes, growing fast.</p></a></article>
    <article class="reveal"><a href="communities/cottage-grove.html"><img src="{IMG['creek']}" alt="Cottage Grove Oregon"><h3>Cottage Grove</h3><p>Covered bridges and forested hills.</p></a></article>
  </div>
  <div style="text-align:center;margin-top:36px"><a class="btn-primary reveal" href="communities/index.html">View All Communities &rarr;</a></div>
</section>
<section class="about-teaser">
  <div>
    <div class="tag tag-purple reveal" style="margin-bottom:24px">About</div>
    <blockquote class="reveal reveal-d1">&ldquo;I grew up in a 4-H family. Community, honesty, and showing up &mdash; those aren&rsquo;t values I adopted for marketing. They&rsquo;re how I was raised.&rdquo;</blockquote>
    <div style="margin-top:28px" class="reveal reveal-d2">
      <a class="btn-link" href="about.html">Read Larissa&rsquo;s Story &rarr;</a>
    </div>
  </div>
  <div class="photo-grid-2x2 reveal">
    <img src="images/larissa-hat-smile.jpg" alt="Larissa Mayfield">
    <img src="images/larissa-couch.jpg" alt="Larissa Mayfield at home">
    <img src="images/larissa-laptop.jpg" alt="Larissa working">
    <img src="images/larissa-yellow.jpg" alt="Larissa Mayfield portrait">
  </div>
</section>
<section class="section-alt">
  <div class="tag tag-purple reveal" style="margin-bottom:18px">Free Resources</div>
  <h2 class="section-heading reveal reveal-d1" style="margin-bottom:32px">Guides &amp; downloads.</h2>
  <div class="lead-grid">
    <div class="lead-card reveal"><div class="meta">GUIDE &middot; 2026 EDITION</div><h3>First-Time Buyer&rsquo;s Guide</h3><p>Pre-approval to closing &mdash; everything first-time buyers in Oregon need to know.</p><a class="download" href="guides/first-time-buyer-guide.html">Read the Guide &rarr;</a></div>
    <div class="lead-card reveal reveal-d1"><div class="meta">GUIDE &middot; ACREAGE &amp; LAND</div><h3>Rural Buyer&rsquo;s Playbook</h3><p>Wells, septic, easements, zoning, and financing &mdash; the rural checklist.</p><a class="download" href="guides/rural-buyer-playbook.html">Read the Playbook &rarr;</a></div>
    <div class="lead-card reveal reveal-d2"><div class="meta">MARKET &middot; 2026</div><h3>Lane County Market Notes</h3><p>Current conditions, median prices, and what to expect through 2026.</p><a class="download" href="guides/lane-county-market-notes.html">Read the Report &rarr;</a></div>
  </div>
</section>
<section class="testimonial-hero reveal">
  <div class="stars">&star; &star; &star; &star; &star;</div>
  <blockquote>&ldquo;{TESTIMONIALS[0][2]}&rdquo;</blockquote>
  <div class="attr">&mdash; {TESTIMONIALS[0][0].upper()} &middot; {TESTIMONIALS[0][1].upper()}</div>
</section>'''
    make_page(f"{SITE}/index.html", 0,
        "Oregon Real Estate Agent — Rural, Acreage &amp; First-Time Buyers",
        "Larissa Mayfield is a licensed Oregon Realtor with Real Broker specializing in rural properties, acreage, and first-time buyers in Lane, Linn, Benton, and Douglas counties.",
        "home", [], body, "RealEstateAgent")

def gen_about():
    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">About Larissa</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Roots in<br>the <em>valley.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">I grew up in a 4-H family in rural Oregon. Before real estate, I spent two decades in commercial lending &mdash; underwriting rural transactions, working with appraisers, and learning how complex deals actually close.</p>
    <p class="body-text reveal reveal-d3" style="margin-top:16px;max-width:440px">That background is why my clients hire me. I understand wells, septic systems, easements, and the financing structures that make rural property sales work. I don&rsquo;t learn on the job &mdash; I brought the expertise with me.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="images/larissa-hat-seated.jpg" alt="Larissa Mayfield"></div>
</section>
<section class="chapter">
  <div class="chapter-sticky">
    <div class="tag tag-purple reveal">My Story</div>
    <h2 class="section-heading reveal reveal-d1" style="margin-top:18px">From lending<br>to listing.</h2>
  </div>
  <div class="chapter-body">
    <p class="reveal">My path to real estate was not typical. I spent over twenty years in commercial banking, specializing in agricultural and rural lending. I evaluated properties, assessed risk, and structured financing for farms, timber operations, and rural businesses across Oregon.</p>
    <p class="reveal reveal-d1">That experience gave me something most agents do not have: a deep understanding of how lenders think, what appraisers look for, and where rural transactions fall apart. When I transitioned to real estate, I brought that institutional knowledge with me.</p>
    <p class="reveal reveal-d2">Today I serve buyers and sellers throughout Lane, Linn, Benton, and Douglas counties. My specialty is rural and acreage properties, but I work with first-time buyers, relocating families, and investors across the region. Every client gets the same thing: honest advice, thorough preparation, and someone who shows up.</p>
    <p class="reveal reveal-d3">I am licensed with Real Broker LLC and live in the community I serve. When I am not working, you will find me with my family, volunteering at local events, or somewhere outdoors in the Willamette Valley.</p>
  </div>
</section>
<section class="photo-grid-section">
  <div class="photo-grid-inner">
    <div class="photo-grid-4 reveal">
      <img src="images/larissa-hat-smile.jpg" alt="Larissa Mayfield">
      <img src="images/larissa-couch.jpg" alt="Larissa at home">
      <img src="images/larissa-laptop.jpg" alt="Larissa working">
      <img src="images/larissa-yellow.jpg" alt="Larissa Mayfield">
    </div>
    <div>
      <div class="tag tag-purple reveal" style="margin-bottom:18px">Community &amp; Values</div>
      <h2 class="section-heading reveal reveal-d1">4-H roots,<br>real values.</h2>
      <p class="body-text reveal reveal-d2" style="margin-top:24px">Community, honesty, hard work, and showing up &mdash; those are not marketing slogans. They are how I was raised, and they are how I run my business. Every client is a neighbor, and every transaction is a handshake.</p>
    </div>
  </div>
</section>
<section class="cta-dark">
  <h2>Let&rsquo;s talk about your goals.</h2>
  <p>Whether you are buying your first home, selling acreage, or just exploring your options &mdash; I am here to help.</p>
  <a href="contact.html">SCHEDULE A CALL &rarr;</a>
</section>'''
    make_page(f"{SITE}/about.html", 0,
        "About Larissa Mayfield — Oregon Realtor, Rural Specialist",
        "Learn about Larissa Mayfield, a licensed Oregon Realtor with Real Broker specializing in rural properties and acreage in Lane, Linn, Benton, and Douglas counties.",
        "about", [("about.html", "ABOUT")], body)

def gen_sellers():
    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">Sellers</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Sell with<br><em>confidence.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">Whether you are selling a suburban home or a 40-acre parcel, I bring honest pricing, professional marketing, and a process built on transparency. No surprises, no pressure &mdash; just a clear path from consultation to closing.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{IMG['house']}" alt="Oregon home for sale"></div>
</section>
<section class="section-dark">
  <div class="valuation-grid">
    <div>
      <div class="tag reveal" style="margin-bottom:24px">Sellers &middot; No-Obligation Valuation</div>
      <h2 class="section-heading reveal reveal-d1" style="color:var(--cream)">What is your property<br><em style="color:var(--cream)"><i>worth today?</i></em></h2>
      <p class="body-text reveal reveal-d2" style="color:rgba(244,239,230,.85);margin-top:24px;max-width:420px">A free, no-obligation valuation built from real comparable sales and an honest conversation about your property in today&rsquo;s market.</p>
    </div>
    <form class="valuation-form reveal reveal-d2" onsubmit="event.preventDefault()">
      <label><div class="label-text">PROPERTY ADDRESS</div><input type="text" placeholder="24500 Hwy 126, Veneta OR"></label>
      <label><div class="label-text">APPROXIMATE ACREAGE</div><input type="text" placeholder="12.5"></label>
      <label><div class="label-text">PROPERTY TYPE</div><input type="text" placeholder="Rural / Acreage / Residential"></label>
      <label><div class="label-text">YOUR NAME</div><input type="text" placeholder="Your name"></label>
      <label><div class="label-text">EMAIL OR PHONE</div><input type="text" placeholder="you@email.com"></label>
      <button type="submit">REQUEST VALUATION &rarr;</button>
    </form>
  </div>
</section>
<section style="padding:96px 56px">
  <div class="tag tag-purple reveal">The Process &middot; 5 Steps</div>
  <h2 class="section-heading reveal reveal-d1" style="margin-top:18px">From handshake to keys.</h2>
  <div class="timeline-grid">
    <div class="timeline-step reveal"><div class="num">01</div><h3>Consultation</h3><p>A walk of the property. We discuss goals, timeline, and what is possible.</p></div>
    <div class="timeline-step reveal reveal-d1"><div class="num">02</div><h3>Pricing</h3><p>A comparative market analysis grounded in actual closed comps &mdash; not Zillow.</p></div>
    <div class="timeline-step reveal reveal-d2"><div class="num">03</div><h3>Preparation</h3><p>Photography, drone, staging guidance &mdash; and the paperwork groundwork.</p></div>
    <div class="timeline-step reveal reveal-d3"><div class="num">04</div><h3>Listing</h3><p>Strategic marketing to qualified buyers. MLS, social, syndication, networks.</p></div>
    <div class="timeline-step reveal"><div class="num">05</div><h3>Closing</h3><p>Negotiation, inspection, appraisal, and the path through escrow to keys.</p></div>
  </div>
</section>
<section class="split-alt">
  <div class="split-alt-inner">
    <img class="reveal parallax-img" src="{IMG['valley']}" alt="Willamette Valley acreage">
    <div>
      <div class="tag tag-purple reveal" style="margin-bottom:18px">Specialty &middot; Rural &amp; Land</div>
      <h2 class="section-heading reveal reveal-d1" style="margin-bottom:28px">Selling land is <em style="color:var(--purple)">not</em> like selling a house.</h2>
      <p class="body-text reveal reveal-d2" style="font-size:16px;margin-bottom:32px">Wells. Septic. Easements. Comparable sales five miles apart. Rural pricing is its own discipline. Two decades in commercial lending taught me how rural transactions actually close.</p>
      <div class="split-pills reveal reveal-d3"><div class="split-pill">Honest valuation</div><div class="split-pill">Buyer financing</div><div class="split-pill">Drone &amp; lifestyle media</div><div class="split-pill">Title &amp; easement work</div></div>
      <div class="reveal" style="margin-top:32px"><a class="btn-primary" href="rural-acreage.html">See Rural &amp; Acreage Page &rarr;</a></div>
    </div>
  </div>
</section>
<section class="testimonial-hero reveal">
  <div class="stars">&star; &star; &star; &star; &star;</div>
  <blockquote>&ldquo;{TESTIMONIALS[4][2]}&rdquo;</blockquote>
  <div class="attr">&mdash; {TESTIMONIALS[4][0].upper()} &middot; {TESTIMONIALS[4][1].upper()}</div>
</section>'''
    make_page(f"{SITE}/sellers.html", 0,
        "Sell Your Home or Land in Oregon",
        "Sell your Oregon home or rural property with Larissa Mayfield. Free home valuation, professional marketing, and expert negotiation. Real Broker.",
        "sellers", [("sellers.html", "SELLERS")], body)

def gen_rural():
    body = f'''<section class="hero-fullbleed">
  <img src="{IMG['valley']}" alt="Oregon rural acreage">
  <div class="overlay"></div>
  <div class="content">
    <div>
      <div class="tag reveal" style="color:rgba(244,239,230,.7)">Rural &amp; Acreage Specialist</div>
      <h1 class="reveal reveal-d1">Land is<br>different.</h1>
    </div>
    <div class="aside reveal reveal-d2">Wells. Septic. Easements. Timber rights. Water rights. Zoning. Rural property transactions involve complexities that most agents have never navigated. I have &mdash; for over two decades.</div>
  </div>
</section>
<section style="padding:96px 56px">
  <div class="tag tag-purple reveal">What Sets Rural Apart</div>
  <h2 class="section-heading reveal reveal-d1" style="margin-top:18px;margin-bottom:40px">Two things most agents get wrong.</h2>
  <div class="dual-grid">
    <div class="dual-card reveal">
      <div class="tag" style="color:rgba(244,239,230,.5)">PRICING</div>
      <h3>Rural pricing is component-based.</h3>
      <p>You cannot price a 20-acre property with a well, barn, and timber the same way you price a subdivision home. I break value into components &mdash; land, improvements, water, timber, income &mdash; and analyze each separately.</p>
      <ul><li><span class="dash">&mdash;</span> Land value per acre</li><li><span class="dash">&mdash;</span> Home &amp; improvements</li><li><span class="dash">&mdash;</span> Well capacity &amp; water rights</li><li><span class="dash">&mdash;</span> Timber &amp; income features</li></ul>
    </div>
    <div class="dual-card reveal reveal-d1">
      <div class="tag" style="color:rgba(244,239,230,.5)">DUE DILIGENCE</div>
      <h3>The inspection list is longer.</h3>
      <p>Beyond the standard home inspection, rural properties require well flow tests, septic evaluations, easement review, zoning verification, and sometimes environmental assessments. I manage every item.</p>
      <ul><li><span class="dash">&mdash;</span> Well flow testing</li><li><span class="dash">&mdash;</span> Septic inspection</li><li><span class="dash">&mdash;</span> Easement &amp; title review</li><li><span class="dash">&mdash;</span> Zoning &amp; land use verification</li></ul>
    </div>
  </div>
</section>
<section style="padding:0 56px 96px">
  <div class="tag tag-purple reveal">Due Diligence Checklist</div>
  <h2 class="section-heading reveal reveal-d1" style="margin-top:18px;margin-bottom:8px">What I verify on every rural transaction.</h2>
  <div class="checklist-grid">
    <div class="checklist-item reveal"><h3>Water</h3><p>Well flow test, well log review, water rights verification, and seasonal reliability assessment.</p></div>
    <div class="checklist-item reveal reveal-d1"><h3>Septic</h3><p>System inspection, pump history, drain field evaluation, and DEQ compliance check.</p></div>
    <div class="checklist-item reveal reveal-d2"><h3>Access</h3><p>Road maintenance agreements, recorded easements, private road status, and emergency access.</p></div>
    <div class="checklist-item reveal reveal-d3"><h3>Zoning</h3><p>Allowed uses, building restrictions, ADU eligibility, and any pending land use changes.</p></div>
  </div>
</section>
<section class="cta-dark">
  <h2>Buying or selling rural property?</h2>
  <p>Let&rsquo;s talk about your land, your goals, and the best path forward.</p>
  <a href="contact.html">SCHEDULE A CALL &rarr;</a>
</section>'''
    make_page(f"{SITE}/rural-acreage.html", 0,
        "Rural &amp; Acreage Specialist — Oregon Land Sales",
        "Larissa Mayfield specializes in rural property and acreage sales in Oregon. Wells, septic, easements, and rural pricing expertise. Real Broker.",
        "rural", [("rural-acreage.html", "RURAL &amp; ACREAGE")], body)

def gen_buyers():
    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">Buyers</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Find your<br><em>place.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">Whether it is your first home or your fifth, buying in Oregon&rsquo;s Willamette Valley requires local knowledge, financing expertise, and someone who advocates for your interests at every step.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{IMG['keys']}" alt="New home keys"></div>
</section>
<section class="step-list">
  <div class="tag tag-purple reveal" style="margin-bottom:18px;padding:0 0 0 80px">The Buyer&rsquo;s Process &middot; 7 Steps</div>
  <div class="step-row reveal"><div class="num">01</div><h3>Pre-Approval</h3><p>Get pre-approved with a lender who knows Oregon programs. I connect you with the right one.</p><div class="arrow">&rarr;</div></div>
  <div class="step-row reveal"><div class="num">02</div><h3>Define Criteria</h3><p>Must-haves, nice-to-haves, neighborhoods, commute, schools &mdash; we build your search strategy.</p><div class="arrow">&rarr;</div></div>
  <div class="step-row reveal"><div class="num">03</div><h3>Tour Homes</h3><p>Strategic tours, five to seven homes at a time, with a comparison sheet to evaluate objectively.</p><div class="arrow">&rarr;</div></div>
  <div class="step-row reveal"><div class="num">04</div><h3>Write an Offer</h3><p>Competitive pricing, strong terms, and a pre-approval letter that signals you are ready.</p><div class="arrow">&rarr;</div></div>
  <div class="step-row reveal"><div class="num">05</div><h3>Inspections</h3><p>Home, well, septic (if applicable) &mdash; coordinated and reviewed with you in detail.</p><div class="arrow">&rarr;</div></div>
  <div class="step-row reveal"><div class="num">06</div><h3>Negotiate</h3><p>Repairs, credits, and terms &mdash; I handle the back-and-forth so you get the best deal.</p><div class="arrow">&rarr;</div></div>
  <div class="step-row reveal"><div class="num">07</div><h3>Close &amp; Keys</h3><p>Final walkthrough, signing, funding, and keys. Welcome home.</p><div class="arrow">&rarr;</div></div>
</section>
<section style="padding:96px 56px">
  <div class="tag tag-purple reveal">Financing FAQ</div>
  <h2 class="section-heading reveal reveal-d1" style="margin-top:18px;margin-bottom:8px">Common questions about buying.</h2>
  <div class="faq-grid">
    <div class="faq-item reveal"><h3>What credit score do I need?</h3><p>Most conventional loans require 620+. FHA accepts 580+. USDA typically wants 640+. If your score needs work, we can discuss a timeline to improve it.</p></div>
    <div class="faq-item reveal reveal-d1"><h3>How much do I need for a down payment?</h3><p>USDA: 0%. Oregon Bond with Cash Advantage: as low as 0%. FHA: 3.5%. Conventional: 3% to 20%. I walk you through every option.</p></div>
    <div class="faq-item reveal reveal-d2"><h3>What is Oregon Bond?</h3><p>A state program offering below-market interest rates and up to 3% in forgivable down payment assistance for qualifying first-time buyers.</p></div>
    <div class="faq-item reveal reveal-d3"><h3>Can I buy acreage with a USDA loan?</h3><p>Yes, if the property is in a USDA-eligible area and meets program guidelines. Many Lane County properties outside the urban growth boundary qualify.</p></div>
  </div>
</section>
<section class="lead-inline">
  <div class="lead-inline-inner">
    <img class="reveal parallax-img" src="{IMG['couple']}" alt="Happy home buyers">
    <div>
      <div class="tag tag-purple reveal" style="margin-bottom:18px">Free Guide</div>
      <h2 class="section-heading reveal reveal-d1">First-Time Buyer&rsquo;s<br>Guide to Oregon.</h2>
      <p class="body-text reveal reveal-d2" style="margin-top:20px;margin-bottom:28px">Pre-approval to closing day &mdash; everything first-time buyers in Oregon need to know, in one comprehensive guide.</p>
      <a class="btn-primary reveal reveal-d3" href="guides/first-time-buyer-guide.html">Read the Guide &rarr;</a>
    </div>
  </div>
</section>
<section class="testimonial-hero reveal">
  <div class="stars">&star; &star; &star; &star; &star;</div>
  <blockquote>&ldquo;{TESTIMONIALS[1][2]}&rdquo;</blockquote>
  <div class="attr">&mdash; {TESTIMONIALS[1][0].upper()} &middot; {TESTIMONIALS[1][1].upper()}</div>
</section>'''
    make_page(f"{SITE}/buyers.html", 0,
        "Buy a Home in Oregon — First-Time &amp; Rural Buyers",
        "Buying a home in Oregon? Larissa Mayfield guides first-time and rural buyers through every step. Pre-approval, financing, inspections, and closing.",
        "buyers", [("buyers.html", "BUYERS")], body)

def gen_communities_index():
    cards = ""
    for i, c in enumerate(COMMUNITIES):
        delay = f" reveal-d{(i % 4) + 1}" if i % 4 else ""
        cards += f'''    <article class="reveal{delay}"><a href="{c['slug']}.html"><img src="{c['img']}" alt="{c['name']} Oregon"><h3>{c['name']}</h3><p>{c['tagline']}</p></a></article>\n'''
    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">Communities</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Where I<br><em>work.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">From Eugene to Drain, the Willamette Valley to the Coast Range &mdash; I serve buyers and sellers across Lane, Linn, Benton, and Douglas counties.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{IMG['aerial']}" alt="Willamette Valley aerial"></div>
</section>
<section style="padding:96px 56px">
  <div class="tag tag-purple reveal">Towns &amp; Counties</div>
  <h2 class="section-heading reveal reveal-d1" style="margin-top:18px;margin-bottom:40px">Explore each community.</h2>
  <div class="community-grid" style="grid-template-columns:repeat(3,1fr);gap:24px">
{cards}  </div>
</section>
<section class="cta-dark">
  <h2>Don&rsquo;t see your community?</h2>
  <p>I am licensed throughout Oregon. If you are buying or selling anywhere in the state, let&rsquo;s talk.</p>
  <a href="../contact.html">SCHEDULE A CALL &rarr;</a>
</section>'''
    make_page(f"{SITE}/communities/index.html", 1,
        "Oregon Communities — Lane, Linn, Benton &amp; Douglas Counties",
        "Explore Oregon communities served by Larissa Mayfield: Veneta, Elmira, Eugene, Springfield, Junction City, Cottage Grove, Oakridge, Creswell, Drain, and more.",
        "communities", [("communities/index.html", "COMMUNITIES")], body)

def gen_community_page(c):
    bullets = "\n      ".join(f'<li><span class="dash">&mdash;</span> {b}</li>' for b in c["bullets"])
    body = f'''<section class="hero-fullbleed">
  <img src="{c['img']}" alt="{c['name']} Oregon">
  <div class="overlay"></div>
  <div class="content">
    <div>
      <div class="tag reveal" style="color:rgba(244,239,230,.7)">Community Guide</div>
      <h1 class="reveal reveal-d1">{c['name']}.</h1>
    </div>
    <div class="aside reveal reveal-d2">{c['tagline']}</div>
  </div>
</section>
<section class="chapter">
  <div class="chapter-sticky">
    <div class="tag tag-purple reveal">About {c['name']}</div>
    <h2 class="section-heading reveal reveal-d1" style="margin-top:18px">Living in<br>{c['name']}.</h2>
  </div>
  <div class="chapter-body">
    <p class="reveal">{c['desc']}</p>
    <ul class="reveal reveal-d1" style="list-style:none;display:grid;gap:10px">
      {bullets}
    </ul>
  </div>
</section>
<section class="cta-dark">
  <h2>Interested in {c['name']}?</h2>
  <p>I know this community well. Let&rsquo;s talk about what&rsquo;s available and what fits your goals.</p>
  <a href="../contact.html">SCHEDULE A CALL &rarr;</a>
</section>'''
    make_page(f"{SITE}/communities/{c['slug']}.html", 1,
        f"{c['name']}, Oregon Real Estate — Homes &amp; Land for Sale",
        c["seo_desc"],
        "communities", [("communities/index.html", "COMMUNITIES"), (f"communities/{c['slug']}.html", c['name'].upper())], body)

def gen_resources():
    guide_cards = ""
    for g in GUIDES:
        guide_cards += f'''    <div class="guide-card reveal"><img src="{g['img']}" alt="{g['title']}"><div class="guide-card-body"><div class="tag tag-purple" style="margin-bottom:12px">{g['tag']}</div><h3 style="font-size:26px;letter-spacing:-.01em;margin-bottom:8px;font-weight:400">{g['title']}</h3><p class="body-text" style="font-size:14px;margin-bottom:auto">{g['desc']}</p><a class="btn-link" href="guides/{g['slug']}.html" style="margin-top:20px">Read &rarr;</a></div></div>\n'''

    blog_cards = ""
    for i, b in enumerate(BLOGS[:6]):
        blog_cards += f'''    <div class="blog-card reveal"><img src="{b['img']}" alt="{b['title']}"><div class="meta">{b['tag']} &middot; {b['date']}</div><h3><a href="blog/{b['slug']}.html">{b['title']}</a></h3><p>{b['excerpt'][:120]}...</p></div>\n'''

    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">Resources</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Guides &amp;<br><em>insights.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">Free guides, market reports, and blog articles to help you make informed real estate decisions in Oregon.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{IMG['docs']}" alt="Real estate resources"></div>
</section>
<section style="padding:96px 56px">
  <div class="tag tag-purple reveal">Guides</div>
  <h2 class="section-heading reveal reveal-d1" style="margin-top:18px;margin-bottom:32px">In-depth resources.</h2>
  <div class="guide-cards">
{guide_cards}  </div>
</section>
<section class="section-alt">
  <div class="tag tag-purple reveal" style="margin-bottom:18px">Blog</div>
  <h2 class="section-heading reveal reveal-d1" style="margin-bottom:32px">Recent articles.</h2>
  <div class="blog-grid">
{blog_cards}  </div>
  <div style="text-align:center;margin-top:36px"><a class="btn-primary reveal" href="blog/index.html">View All Articles &rarr;</a></div>
</section>'''
    make_page(f"{SITE}/resources.html", 0,
        "Real Estate Resources — Guides, Blog &amp; Market Reports",
        "Free real estate guides, market reports, and blog articles for Oregon buyers and sellers. By Larissa Mayfield, Real Broker.",
        "resources", [("resources.html", "RESOURCES")], body)

def gen_testimonials():
    featured = TESTIMONIALS[0]
    cards = ""
    for t in TESTIMONIALS:
        cards += f'''<div class="testimonial-card reveal">
  <div class="stars">&star;&star;&star;&star;&star;</div>
  <blockquote>&ldquo;{t[2]}&rdquo;</blockquote>
  <div class="name">{t[0]}</div>
  <div class="detail">{t[1].upper()}</div>
</div>\n'''
    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">Testimonials</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">What my<br>clients <em>say.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">Real reviews from real clients. Every testimonial below is from a verified Zillow review or direct client feedback.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="images/larissa-headshot.jpg" alt="Larissa Mayfield"></div>
</section>
<section class="testimonial-featured">
  <blockquote class="reveal">&ldquo;{featured[2]}&rdquo;<div class="attr">&mdash; {featured[0].upper()} &middot; {featured[1].upper()}</div></blockquote>
</section>
<section>
  <div class="testimonials-masonry">
{cards}</div>
</section>
<section class="cta-dark">
  <h2>Ready to add your story?</h2>
  <p>Let&rsquo;s talk about your goals and how I can help.</p>
  <a href="contact.html">SCHEDULE A CALL &rarr;</a>
</section>'''
    make_page(f"{SITE}/testimonials.html", 0,
        "Client Testimonials — Larissa Mayfield Reviews",
        "Read reviews from Larissa Mayfield's real estate clients in Oregon. Verified testimonials from buyers, sellers, and rural property transactions.",
        "testimonials", [("testimonials.html", "TESTIMONIALS")], body)

def gen_contact():
    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">Contact</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Let&rsquo;s<br><em>connect.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">Whether you are ready to buy, thinking about selling, or just have questions &mdash; I am here. No pressure, no obligation.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="images/larissa-hat-smile.jpg" alt="Larissa Mayfield"></div>
</section>
<section>
  <div class="contact-grid">
    <form class="contact-form reveal" onsubmit="event.preventDefault()">
      <div><div class="form-label">YOUR NAME</div><input type="text" placeholder="Full name"></div>
      <div><div class="form-label">EMAIL</div><input type="email" placeholder="you@email.com"></div>
      <div><div class="form-label">PHONE</div><input type="tel" placeholder="541-000-0000"></div>
      <div><div class="form-label">I AM INTERESTED IN</div>
        <div class="interest-chips">
          <button class="chip" type="button">Buying</button>
          <button class="chip" type="button">Selling</button>
          <button class="chip" type="button">Rural/Acreage</button>
          <button class="chip" type="button">First-Time Buyer</button>
          <button class="chip" type="button">Valuation</button>
          <button class="chip" type="button">Just Exploring</button>
        </div>
      </div>
      <div><div class="form-label">MESSAGE</div><textarea rows="5" placeholder="Tell me a little about your situation..."></textarea></div>
      <button class="btn-mono" type="submit">SEND MESSAGE &rarr;</button>
    </form>
    <div class="contact-sidebar reveal reveal-d1">
      <div class="contact-card-dark">
        <div style="font-family:var(--mono);font-size:10px;letter-spacing:.2em;color:rgba(244,239,230,.5);margin-bottom:16px">DIRECT LINE</div>
        <div style="font-family:var(--serif);font-size:36px;letter-spacing:-.02em"><a href="tel:5417847745" style="color:var(--cream)">541.784.7745</a></div>
        <div style="margin-top:16px;font-family:var(--sans);font-size:14px;color:rgba(244,239,230,.7)">Call or text. I respond within a few hours during business days.</div>
      </div>
      <div class="contact-card-light">
        <div style="font-family:var(--mono);font-size:10px;letter-spacing:.2em;color:var(--muted);margin-bottom:16px">EMAIL</div>
        <div style="font-family:var(--sans);font-size:16px"><a href="mailto:larissa@theoperativegroup.com" style="color:var(--purple)">larissa@theoperativegroup.com</a></div>
      </div>
      <div class="contact-card-light">
        <div style="font-family:var(--mono);font-size:10px;letter-spacing:.2em;color:var(--muted);margin-bottom:16px">SERVICE AREA</div>
        <div style="font-family:var(--sans);font-size:14px;line-height:1.7;color:var(--muted)">Lane County &middot; Linn County &middot; Benton County &middot; Douglas County<br>Licensed throughout Oregon</div>
      </div>
      <div class="contact-card-light">
        <div style="font-family:var(--mono);font-size:10px;letter-spacing:.2em;color:var(--muted);margin-bottom:16px">LICENSE</div>
        <div style="font-family:var(--sans);font-size:14px;color:var(--muted)">Real Broker LLC &middot; License #201231874</div>
      </div>
    </div>
  </div>
</section>'''
    make_page(f"{SITE}/contact.html", 0,
        "Contact Larissa Mayfield — Oregon Real Estate Agent",
        "Contact Larissa Mayfield for real estate help in Oregon. Phone 541.784.7745, email larissa@theoperativegroup.com. Lane, Linn, Benton, Douglas counties.",
        "contact", [("contact.html", "CONTACT")], body)

def gen_blog_index():
    cards = ""
    for i, b in enumerate(BLOGS):
        delay = f" reveal-d{(i % 3) + 1}" if i % 3 else ""
        cards += f'''    <div class="blog-card reveal{delay}"><img src="../{'' if b['img'].startswith('http') else ''}{b['img']}" alt="{b['title']}"><div class="meta">{b['tag']} &middot; {b['date']}</div><h3><a href="{b['slug']}.html">{b['title']}</a></h3><p>{b['excerpt']}</p></div>\n'''
    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">Blog</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Articles &amp;<br><em>insights.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">Practical advice on buying, selling, and owning real estate in Oregon. Written by Larissa Mayfield.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{IMG['docs']}" alt="Real estate blog"></div>
</section>
<section style="padding:96px 56px">
  <div class="blog-grid">
{cards}  </div>
</section>'''
    make_page(f"{SITE}/blog/index.html", 1,
        "Real Estate Blog — Oregon Buying &amp; Selling Advice",
        "Real estate articles and advice for Oregon buyers and sellers. Wells, septic, financing, market updates, and more. By Larissa Mayfield.",
        "resources", [("blog/index.html", "BLOG")], body)

def gen_blog_article(b):
    sections = ""
    for heading, text in b["body_sections"]:
        sections += f'''  <h2>{heading}</h2>
  <p>{text}</p>\n'''
    body = f'''<section class="article-header">
  <div class="tag tag-purple reveal">{b['tag']} &middot; {b['date']}</div>
  <h1 class="page-title reveal reveal-d1" style="margin-top:18px;font-size:clamp(36px,5vw,64px)">{b['title']}</h1>
  <p class="body-text reveal reveal-d2" style="margin-top:24px">{b['excerpt']}</p>
  <div class="article-meta reveal reveal-d3"><span>BY LARISSA MAYFIELD</span><span>{b['date']}</span><span>5 MIN READ</span></div>
</section>
<section class="article-body reveal">
{sections}
  <div class="article-author">
    <img src="../images/larissa-headshot-square.jpg" alt="Larissa Mayfield">
    <div>
      <div style="font-weight:600;font-family:var(--sans);font-size:15px">Larissa Mayfield</div>
      <div style="font-family:var(--mono);font-size:10px;letter-spacing:.18em;color:var(--muted);margin-top:4px">REAL BROKER &middot; LIC. 201231874</div>
    </div>
  </div>
  <div class="article-cta">
    <h3 style="font-family:var(--serif);font-size:28px;letter-spacing:-.01em;font-weight:400;margin-bottom:16px">Have questions about this topic?</h3>
    <a class="btn-primary" href="../contact.html">Ask Larissa &rarr;</a>
  </div>
</section>'''
    make_page(f"{SITE}/blog/{b['slug']}.html", 1,
        b['title'],
        b['seo_desc'],
        "resources", [("blog/index.html", "BLOG"), (f"blog/{b['slug']}.html", b['title'][:30].upper())], body, "BlogPosting")

def gen_guide(g):
    sections = ""
    for heading, text in g["sections"]:
        sections += f'''  <h2>{heading}</h2>
  <p>{text}</p>\n'''
    body = f'''<section class="article-header">
  <div class="tag tag-purple reveal">{g['tag']}</div>
  <h1 class="page-title reveal reveal-d1" style="margin-top:18px;font-size:clamp(36px,5vw,64px)">{g['title']}</h1>
  <p class="body-text reveal reveal-d2" style="margin-top:24px">{g['desc']}</p>
  <div class="article-meta reveal reveal-d3"><span>BY LARISSA MAYFIELD</span><span>2026</span><span>10 MIN READ</span></div>
</section>
<section class="article-body reveal">
{sections}
  <div class="article-author">
    <img src="../images/larissa-headshot-square.jpg" alt="Larissa Mayfield">
    <div>
      <div style="font-weight:600;font-family:var(--sans);font-size:15px">Larissa Mayfield</div>
      <div style="font-family:var(--mono);font-size:10px;letter-spacing:.18em;color:var(--muted);margin-top:4px">REAL BROKER &middot; LIC. 201231874</div>
    </div>
  </div>
  <div class="article-cta">
    <h3 style="font-family:var(--serif);font-size:28px;letter-spacing:-.01em;font-weight:400;margin-bottom:16px">Ready to take the next step?</h3>
    <a class="btn-primary" href="../contact.html">Schedule a Call &rarr;</a>
  </div>
</section>'''
    make_page(f"{SITE}/guides/{g['slug']}.html", 1,
        g['title'],
        g['seo_desc'],
        "resources", [("guides/" + g['slug'] + ".html", g['title'][:30].upper())], body)

def gen_service(s):
    custom_body = s.get("body", "")
    if not custom_body:
        custom_body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">{s['tag']}</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px;font-size:clamp(36px,5vw,64px)">{s['title']}</h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:500px">{s['desc']}</p>
    <a class="btn-primary reveal reveal-d3" href="contact.html" style="margin-top:32px">Schedule a Call &rarr;</a>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{IMG['keys']}" alt="{s['title']}"></div>
</section>
<section class="chapter">
  <div class="chapter-sticky">
    <div class="tag tag-purple reveal">Details</div>
    <h2 class="section-heading reveal reveal-d1" style="margin-top:18px">How I<br>can help.</h2>
  </div>
  <div class="chapter-body">
    <p class="reveal">{s['desc']}</p>
    <p class="reveal reveal-d1">Every client&rsquo;s situation is unique. I take the time to understand your goals, your timeline, and your concerns before recommending a strategy. There is no one-size-fits-all approach to real estate, and I do not pretend there is.</p>
    <p class="reveal reveal-d2">My background in commercial lending means I understand financing structures, appraisal processes, and what lenders need to close. I bring that institutional knowledge to every transaction, whether it is a first-time buyer in Springfield or a 40-acre sale in Drain.</p>
    <p class="reveal reveal-d3">If you are interested in learning more, let&rsquo;s schedule a no-obligation conversation. I will answer your questions honestly and help you decide on the best path forward.</p>
  </div>
</section>
<section class="cta-dark">
  <h2>Let&rsquo;s talk.</h2>
  <p>No pressure, no obligation. Just an honest conversation about your real estate goals.</p>
  <a href="contact.html">SCHEDULE A CALL &rarr;</a>
</section>'''
    make_page(f"{SITE}/services/{s['slug']}.html", 1,
        s['title'] + " — Larissa Mayfield, Real Broker",
        s['seo_desc'],
        "", [("services/" + s['slug'] + ".html", s['title'][:30].upper())], custom_body)

def gen_sitemap():
    urls = ["index.html", "about.html", "sellers.html", "rural-acreage.html", "buyers.html",
            "communities/index.html", "resources.html", "testimonials.html", "contact.html",
            "blog/index.html"]
    for c in COMMUNITIES:
        urls.append(f"communities/{c['slug']}.html")
    for b in BLOGS:
        urls.append(f"blog/{b['slug']}.html")
    for g in GUIDES:
        urls.append(f"guides/{g['slug']}.html")
    for s in SERVICES:
        urls.append(f"services/{s['slug']}.html")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml += f'  <url><loc>https://larissamayfield.com/{u}</loc></url>\n'
    xml += '</urlset>'
    with open(f"{SITE}/sitemap.xml", "w") as f:
        f.write(xml)
    print("  ✓ sitemap.xml")

def gen_robots():
    with open(f"{SITE}/robots.txt", "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://larissamayfield.com/sitemap.xml\n")
    print("  ✓ robots.txt")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs(f"{SITE}/communities", exist_ok=True)
    os.makedirs(f"{SITE}/blog", exist_ok=True)
    os.makedirs(f"{SITE}/guides", exist_ok=True)
    os.makedirs(f"{SITE}/services", exist_ok=True)

    print("Generating pages...")
    print("\n── Core Pages ──")
    gen_home()
    gen_about()
    gen_sellers()
    gen_rural()
    gen_buyers()
    gen_communities_index()
    gen_resources()
    gen_testimonials()
    gen_contact()

    print("\n── Community Pages ──")
    for c in COMMUNITIES:
        gen_community_page(c)

    print("\n── Blog Index ──")
    gen_blog_index()

    print("\n── Blog Articles ──")
    for b in BLOGS:
        gen_blog_article(b)

    print("\n── Guides ──")
    for g in GUIDES:
        gen_guide(g)

    print("\n── Service Pages ──")
    for s in SERVICES:
        gen_service(s)

    print("\n── SEO Files ──")
    gen_sitemap()
    gen_robots()

    total = 9 + len(COMMUNITIES) + 1 + len(BLOGS) + len(GUIDES) + len(SERVICES) + 2
    print(f"\n✅ {total} files generated.")
