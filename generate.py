#!/usr/bin/env python3
"""Generate 50+ static HTML pages for Larissa Mayfield Heritage Editorial website."""
import os
import re, textwrap

SITE = "/Users/derikbannister9/larissa-mayfield-website"

# Listing pages are built and reachable by direct URL, but the "Listings" nav
# item and the listings index stay out of the site until Larissa signs off on
# the design. Flip to True to surface them everywhere (nav, footer, sitemap).
SHOW_LISTINGS_NAV = True

# Live host. The site is served from larissamayfieldre.com; the old
# larissamayfield.com does not resolve. Change here, not in 11 places.
DOMAIN = "https://larissamayfieldre.com"

# ── Helpers ──────────────────────────────────────────────────────────────────

def prefix(depth):
    if depth == 0: return "."
    return "/".join([".."] * depth)

# Cache-bust CSS/JS by content hash. Without this, a returning visitor keeps the
# stylesheet and script the browser cached last time — so a deploy that changes
# the calculator colour or adds a gallery control simply doesn't reach them.
# ── Responsive images ────────────────────────────────────────────────────────
# build_images.py writes a manifest of the WebP derivatives it made. Rather than
# rewriting every <img> call site by hand (and missing some), make_page runs
# every finished page through enhance_images(), which upgrades each <img> into a
# <picture> with a WebP srcset. One choke point, 100% coverage.
_MANIFEST = None
def img_manifest():
    global _MANIFEST
    if _MANIFEST is None:
        try:
            with open(f"{SITE}/images/derivatives.json") as f:
                _MANIFEST = __import__("json").load(f)
        except Exception:
            _MANIFEST = {}
    return _MANIFEST


# How wide the image actually renders, so the browser fetches that tier and not
# a 2048px file for a 318px slot. Keyed by a data-sizes hint on the tag.
SIZES = {
    "tile":  "(max-width:768px) 50vw,(max-width:1024px) 33vw,25vw",
    "hero":  "100vw",
    "card":  "(max-width:768px) 100vw,(max-width:1024px) 50vw,33vw",
    "half":  "(max-width:1024px) 100vw,50vw",
    "avatar": "48px",
}


def enhance_images(html, depth):
    """Rewrite <img> -> <picture> with WebP srcset, intrinsic size and lazy hints."""
    man = img_manifest()
    if not man:
        return html
    base = os.path.dirname(f"{SITE}/{'/'.join(['x'] * depth)}/page.html") if depth else SITE
    state = {"first": True}

    def repl(m):
        tag = m.group(0)
        src = re.search(r'\bsrc="([^"]*)"', tag)
        if not src:
            return tag
        raw = src.group(1)
        if not raw or raw.startswith(("http://", "https://", "data:")):
            return tag
        # Resolve the page-relative src back to a repo-relative key.
        rel = os.path.normpath(os.path.join(base, raw.split("?")[0]))
        rel = os.path.relpath(rel, SITE)
        info = man.get(rel)
        if not info or not info.get("widths"):
            return tag

        key = re.search(r'\bdata-sizes="([^"]*)"', tag)
        sizes = SIZES.get(key.group(1) if key else "", SIZES["half"])
        stem, _ = os.path.splitext(raw.split("?")[0])
        srcset = ", ".join(f"{stem}-{w}.webp {w}w" for w in info["widths"])

        attrs = re.sub(r'\sdata-sizes="[^"]*"', "", tag[4:-1] if tag.endswith("/>") else tag[4:-1])
        if "width=" not in attrs:
            attrs += f' width="{info["w"]}" height="{info["h"]}"'
        if "decoding=" not in attrs:
            attrs += ' decoding="async"'
        # The first image on a page is almost always the LCP element — never
        # lazy-load it, and tell the browser it matters.
        if state["first"]:
            attrs = re.sub(r'\sloading="lazy"', "", attrs) + ' fetchpriority="high"'
            state["first"] = False
        elif "loading=" not in attrs:
            attrs += ' loading="lazy"'
        return (f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
                f'<img{attrs}></picture>')

    return re.sub(r"<img\b[^>]*>", repl, html)


def add_faq_schema(html):
    """Any page rendering .faq-item blocks gets FAQPage markup built from the
    questions actually on the page. AI answer engines lift Q&A pairs directly,
    and Google can show them as expandable results."""
    qs = re.findall(r'<div class="faq-item[^"]*">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', html, re.S)
    if len(qs) < 2:
        return html
    import json as _j
    def clean(t):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).replace("&amp;", "&").strip()
    blob = _j.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                     "mainEntity": [{"@type": "Question", "name": clean(q),
                                     "acceptedAnswer": {"@type": "Answer", "text": clean(a)}}
                                    for q, a in qs]}).replace("<", "\\u003c")
    return html.replace("</head>", f'<script type="application/ld+json">{blob}</script>\n</head>', 1)


def add_breadcrumb_schema(html, canonical, crumbs):
    """68 pages showed a breadcrumb trail with no markup behind it. This turns
    each one into a BreadcrumbList so the trail appears in the search result
    instead of a bare URL."""
    if not crumbs:
        return html
    import json as _j
    items = [{"@type": "ListItem", "position": 1, "name": "Home",
              "item": f"{DOMAIN}/index.html"}]
    for i, (href, label) in enumerate(crumbs, start=2):
        node = {"@type": "ListItem", "position": i,
                "name": label.replace("&amp;", "&").title()}
        # The last crumb is the current page; Google wants no `item` on it.
        if i - 2 < len(crumbs) - 1:
            node["item"] = f"{DOMAIN}/{href}"
        items.append(node)
    blob = _j.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                     "itemListElement": items}).replace("<", "\\u003c")
    return html.replace("</head>",
                        f'<script type="application/ld+json">{blob}</script>\n</head>', 1)


_ASSET_VER = {}
def asset_ver(rel):
    if rel not in _ASSET_VER:
        import hashlib
        with open(f"{SITE}/{rel}", "rb") as f:
            _ASSET_VER[rel] = hashlib.md5(f.read()).hexdigest()[:8]
    return _ASSET_VER[rel]

def header(pfx, active=""):
    links = [
        ("about.html", "about", "About"),
    ] + ([("listings/index.html", "listings", "Listings")] if SHOW_LISTINGS_NAV else []) + [
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
      <img src="{pfx}/images/larissa-headshot-square.jpg" alt="Larissa Mayfield" width="36" height="36" data-sizes="avatar">
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
        {f'<li><a href="{pfx}/listings/index.html">Listings</a></li>' if SHOW_LISTINGS_NAV else ''}
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
        <li>PO Box 161, Elmira, OR 97437</li>
        <li><a href="{pfx}/contact.html">Schedule a Call</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 LARISSA MAYFIELD &middot; REAL BROKER, LLC</span>
    <span><a href="{pfx}/terms.html">TERMS OF SERVICE</a> &middot; <a href="{pfx}/privacy.html">PRIVACY POLICY</a> &middot; <a href="{pfx}/do-not-sell.html">YOUR PRIVACY CHOICES</a> &middot; <a href="{pfx}/photo-credits.html">PHOTO CREDITS</a></span>
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

def make_page(path, depth, title, desc, active, crumbs, body, schema_type="WebPage", extra_schema="",
              extra_head="", og_image=None):
    pfx = prefix(depth)
    canonical = path.replace(SITE + "/", "")
    # Listing pages pass their hero photo so a shared link previews the house
    # rather than the generic brand card.
    og = og_image or "https://larissamayfieldre.com/images/og-share.jpg"
    schema = f'''{{"@context":"https://schema.org","@type":"{schema_type}","name":"{title}","description":"{desc}","url":"https://larissamayfieldre.com/{canonical}","author":{{"@type":"RealEstateAgent","name":"Larissa Mayfield","telephone":"541-784-7745","email":"larissa@theoperativegroup.com","url":"https://larissamayfieldre.com","areaServed":[{{"@type":"City","name":"Veneta, Oregon"}},{{"@type":"City","name":"Elmira, Oregon"}},{{"@type":"AdministrativeArea","name":"Lane County, Oregon"}},{{"@type":"AdministrativeArea","name":"Linn County, Oregon"}},{{"@type":"AdministrativeArea","name":"Benton County, Oregon"}},{{"@type":"AdministrativeArea","name":"Douglas County, Oregon"}}]}}{extra_schema}}}'''
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
<meta property="og:url" content="https://larissamayfieldre.com/{canonical}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} | Larissa Mayfield">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og}">
<link rel="canonical" href="https://larissamayfieldre.com/{canonical}">
<link rel="icon" href="{pfx}/favicon.ico" sizes="any">
<link rel="icon" href="{pfx}/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pfx}/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pfx}/css/style.css?v={asset_ver("css/style.css")}">
<script type="application/ld+json">{schema}</script>
{extra_head}</head>
<body>
{header(pfx, active)}
{breadcrumb(pfx, crumbs) if crumbs else ""}
{body}
{footer(pfx)}
<script src="{pfx}/js/main.js?v={asset_ver("js/main.js")}"></script>
</body>
</html>'''
    html = enhance_images(html, depth)
    html = add_breadcrumb_schema(html, canonical, crumbs)
    html = add_faq_schema(html)
    os.makedirs(os.path.dirname(path) if "/" in path[len(SITE)+1:] else SITE, exist_ok=True)
    with open(path, "w") as f:
        f.write(html)
    print(f"  ✓ {canonical}")

# Unsplash photo URLs used as placeholders
# Local stock photos — verified Pacific Northwest / Willamette Valley appropriate
# All photos live in /images/stock/ — never linking to remote Unsplash URLs again.
# Every key maps to ONE distinct file whose actual contents match the copy it
# sits next to. Do not point two keys at the same file — the duplicate-image
# check in verify_site() will fail the build.
STOCK_FILES = {
    # ── Places (real, verified photographs of the actual location) ──────────
    "fernridge":    ("stock", "veneta-fern-ridge"),          # Fern Ridge Lake, Lane County
    "eugene":       ("stock", "eugene-skinner-butte"),       # Eugene from Skinner Butte
    "springfield":  ("stock", "springfield-home"),           # modest single-storey home
    "coveredbridge":("stock", "cottage-grove-bridge"),       # Centennial Covered Bridge
    "osu":          ("stock", "corvallis-osu"),              # OSU lower campus quad
    "creswell":     ("stock", "creswell-home"),              # two-storey suburban home
    "pasture":      ("stock", "junction-city-farms"),        # cattle pasture at dawn
    "coast":        ("stock", "lane-county-coast-cascade"),  # Oregon coast headland
    "heritagebarn": ("stock", "heritage-barn-lane-county"),  # Cochran-Rice barn, Cottage Grove
    # ── Landscape ───────────────────────────────────────────────────────────
    "wheat":        ("stock", "wheat-field"),
    "barn":         ("stock", "barn-sunset"),
    "cascades":     ("stock", "mountain-valley"),
    "mistyforest":  ("stock", "misty-forest"),
    "fog":          ("stock", "cascade-fog"),
    "canopy":       ("stock", "aerial-forest"),
    "ridge":        ("stock", "valley-vista"),
    "forestpath":   ("stock", "forest-path"),
    "acreageaerial":("stock", "willamette-acreage-aerial"),
    "parcelaerial": ("stock", "rural-property-with-house"),
    # ── Homes & transactions ────────────────────────────────────────────────
    "whitehome":    ("stock", "white-home"),
    "suburban":     ("stock", "suburban-home"),
    "forsale":      ("stock", "sellers-hero-acreage-home"),
    "staged":       ("stock", "staged-home-listing"),
    "interior":     ("stock", "interior"),
    "keys":         ("stock", "handing-keys"),
    "buyers":       ("stock", "happy-home-buyers"),
    "adu":          ("stock", "adu-backyard"),
    # ── Rural infrastructure & paperwork ────────────────────────────────────
    "well":         ("stock", "water-well-pump"),
    "septic":       ("stock", "septic-inspection"),
    "inspector":    ("stock", "home-inspector"),
    "docs":         ("stock", "documents"),
    "contract":     ("stock", "signing"),
}

# Alt text describes WHAT IS IN THE PHOTOGRAPH — never the headline it sits
# under. A screen-reader user hears the article title from the heading already.
STOCK_ALT = {
    "fernridge":    "Fern Ridge Lake near Veneta, Oregon, with moored boats and the Coast Range beyond",
    "eugene":       "Eugene, Oregon, and the surrounding hills seen from Skinner Butte",
    "springfield":  "A modest single-storey home on a quiet Springfield, Oregon street",
    "coveredbridge":"The white Centennial Covered Bridge in Cottage Grove, Oregon",
    "osu":          "A tree-lined path across the lower campus quad at Oregon State University in Corvallis",
    "creswell":     "A two-storey suburban home with a wide lawn and mature hedges",
    "pasture":      "Cattle grazing in a misty Willamette Valley pasture at sunrise",
    "coast":        "Surf breaking below a forested headland on the Oregon coast",
    "heritagebarn": "A weathered heritage barn with a painted advertisement, Cottage Grove, Oregon",
    "wheat":        "A golden grain field at sunset in the Willamette Valley",
    "barn":         "A barn and grain silo silhouetted against a sunset",
    "cascades":     "Snow-capped Cascade peaks above a conifer-lined valley",
    "mistyforest":  "Mist drifting through a dense stand of Pacific Northwest conifers",
    "fog":          "Fog settling over forested hills in the Oregon Cascades",
    "canopy":       "An overhead view of an evergreen forest canopy",
    "ridge":        "A green ridge line falling away to a broad valley",
    "forestpath":   "A dirt path winding through tall Douglas firs",
    "acreageaerial":"An aerial view of Willamette Valley farmland divided into cultivated parcels",
    "parcelaerial": "An aerial view of a rural property showing the house, outbuildings, pond and fence lines",
    "whitehome":    "A white farmhouse with a wraparound porch on a green lawn",
    "suburban":     "A two-storey brick suburban home with a double garage",
    "forsale":      "A red 'Home For Sale' sign in the front yard of an Oregon house",
    "staged":       "A staged living room with light furnishings and natural daylight",
    "interior":     "An open-plan dining and living area with large windows",
    "keys":         "A hand holding a set of new house keys in an open doorway",
    "buyers":       "A couple celebrating outside the home they have just bought",
    "adu":          "A small accessory dwelling unit with a covered porch in a back garden",
    "well":         "An old stone well head with a bucket and winch on a rural property",
    "septic":       "A plumber tightening a drain line during a property inspection",
    "inspector":    "A home inspector in a hard hat and hi-vis vest examining a ceiling",
    "docs":         "Mortgage and tax paperwork spread out beside a calculator",
    "contract":     "A hand signing a real estate contract",
}

def stock_path(key, depth=0):
    """Build a relative path to a stock photo from given page depth."""
    pfx = "." if depth == 0 else "/".join([".."] * depth)
    kind, name = STOCK_FILES[key]
    if kind == "portrait":
        return f"{pfx}/images/{name}.jpg"
    return f"{pfx}/images/stock/{name}.jpg"

def stock_alt(key):
    """Alt text for a stock photo, describing the photo itself."""
    return STOCK_ALT[key]

# Backward-compat shim — IMG[key] returns depth-0 path used by root-level pages.
IMG = {k: stock_path(k, 0) for k in STOCK_FILES}

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
        "img_key": "fernridge",
        "seo_desc": "Explore Veneta, Oregon real estate with Larissa Mayfield. Affordable acreage, rural homes, and land near Eugene. Fern Ridge Lake, Elmira-Veneta schools."
    },
    {
        "slug": "elmira",
        "name": "Elmira",
        "tagline": "Quiet acreage living, close to everything.",
        "desc": "Elmira is an unincorporated community northwest of Eugene known for its larger lot sizes and rural character. Hobby farms, horse properties, and quiet residential acreages define the area.",
        "bullets": ["Average lot 2-10 acres", "Equestrian-friendly", "Elmira-Veneta schools", "15 min to downtown Eugene", "Fern Ridge Lake nearby"],
        "img_key": "barn",
        "seo_desc": "Elmira, Oregon homes and acreage for sale. Horse properties, hobby farms, and rural living near Eugene. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "eugene",
        "name": "Eugene",
        "tagline": "Oregon&rsquo;s second city &mdash; culture meets nature.",
        "desc": "Eugene is the cultural and economic hub of Lane County. From the University of Oregon campus to Skinner Butte, Eugene offers walkable neighborhoods, excellent schools, and a vibrant food and arts scene.",
        "bullets": ["Population ~176K", "University of Oregon", "Strong rental market", "Bikeable infrastructure", "Gateway to the Cascades"],
        "img_key": "eugene",
        "seo_desc": "Eugene, Oregon real estate — homes, condos, investment properties. University of Oregon area. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "springfield",
        "name": "Springfield",
        "tagline": "Affordable homes, growing opportunity.",
        "desc": "Springfield has experienced significant revitalization with a growing downtown, the Glenwood riverfront district, and strong residential demand. It remains one of the most affordable markets adjacent to Eugene.",
        "bullets": ["Median home ~$365K", "Glenwood riverfront growth", "PeaceHealth medical hub", "Springfield school district", "McKenzie River access"],
        "img_key": "springfield",
        "seo_desc": "Springfield, Oregon homes for sale. Affordable real estate near Eugene, Glenwood riverfront, McKenzie River. Agent Larissa Mayfield."
    },
    {
        "slug": "junction-city",
        "name": "Junction City",
        "tagline": "Farmland and heritage in the heart of the valley.",
        "desc": "Junction City occupies some of the richest agricultural land in the Willamette Valley. Known for its Scandinavian Festival and strong farming community, it offers a quieter alternative to the Eugene-Springfield metro.",
        "bullets": ["Small-town community", "Excellent farmland", "Scandinavian heritage", "Junction City schools", "20 min to Eugene"],
        "img_key": "pasture",
        "seo_desc": "Junction City, Oregon real estate — farmland, acreage, rural homes in the Willamette Valley. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "cottage-grove",
        "name": "Cottage Grove",
        "tagline": "Covered bridges and forested hills.",
        "desc": "Cottage Grove sits along the Coast Fork of the Willamette River, surrounded by forested hills and famous covered bridges. It offers some of the most affordable housing in Lane County with a charming historic downtown.",
        "bullets": ["Historic downtown core", "Covered bridge capital", "Dorena Lake recreation", "Affordable entry prices", "Row River Trail"],
        "img_key": "coveredbridge",
        "seo_desc": "Cottage Grove, Oregon homes and land for sale. Covered bridges, Dorena Lake, affordable living. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "oakridge",
        "name": "Oakridge",
        "tagline": "Mountain biking capital of the Northwest.",
        "desc": "Oakridge is a mountain community at the edge of the Cascade Range, known globally for world-class mountain biking trails. It offers cabin retreats, timber properties, and a small-town pace of life.",
        "bullets": ["World-class MTB trails", "Cascade Range gateway", "Cabin & retreat market", "National forest access", "Growing tourism economy"],
        "img_key": "cascades",
        "seo_desc": "Oakridge, Oregon cabins, retreats, and mountain homes. Cascade Range gateway, world-class mountain biking. Agent Larissa Mayfield."
    },
    {
        "slug": "creswell",
        "name": "Creswell",
        "tagline": "Family-friendly and freeway-close.",
        "desc": "Creswell offers an appealing balance of small-town livability and convenient I-5 access. It is one of the fastest-growing communities in Lane County with strong schools and new residential development.",
        "bullets": ["Fast-growing community", "Creswell school district", "I-5 corridor access", "New construction market", "10 min to south Eugene"],
        "img_key": "creswell",
        "seo_desc": "Creswell, Oregon homes for sale — new construction, family-friendly, I-5 access. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "drain",
        "name": "Drain",
        "tagline": "Timber country with room to breathe.",
        "desc": "Drain is a small timber town in Douglas County along Highway 99. It offers very affordable large-acreage properties, rolling hills, and a genuine rural lifestyle that draws buyers seeking self-sufficiency.",
        "bullets": ["Affordable large acreage", "Timber & ranch properties", "Douglas County schools", "40 min to Roseburg", "Off-grid potential"],
        "img_key": "fog",
        "seo_desc": "Drain, Oregon land, acreage, and rural homes. Affordable timber country in Douglas County. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "lane-county",
        "name": "Lane County",
        "tagline": "From the ocean to the Cascades.",
        "desc": "Lane County stretches from the Oregon Coast to the Cascade Range, encompassing Eugene-Springfield and dozens of rural communities. It offers the widest range of property types in western Oregon.",
        "bullets": ["Population ~385K", "Eugene-Springfield metro", "Coast to Cascades geography", "Strong agricultural base", "University of Oregon"],
        "img_key": "coast",
        "seo_desc": "Lane County, Oregon real estate overview — cities, rural communities, acreage, farmland. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "linn-county",
        "name": "Linn County",
        "tagline": "Grass seed capital and Cascade foothills.",
        "desc": "Linn County is one of Oregon&rsquo;s top agricultural counties, anchored by Albany and Lebanon. The eastern foothills offer recreational properties near the Santiam corridor.",
        "bullets": ["Albany & Lebanon hubs", "Top agricultural county", "Santiam Canyon access", "Affordable rural land", "Strong hobby farm market"],
        "img_key": "wheat",
        "seo_desc": "Linn County, Oregon farms, acreage, and rural homes. Albany, Lebanon, Santiam Canyon. Agent Larissa Mayfield, Real Broker."
    },
    {
        "slug": "benton-county",
        "name": "Benton County",
        "tagline": "Corvallis, Oregon State, and rolling hills.",
        "desc": "Benton County is home to Corvallis and Oregon State University. It offers a highly educated population, excellent schools, and a mix of in-town homes and surrounding rural properties.",
        "bullets": ["Corvallis hub", "Oregon State University", "High quality of life", "Mary&rsquo;s Peak area", "Strong school districts"],
        "img_key": "osu",
        "seo_desc": "Benton County, Oregon real estate — Corvallis homes, rural acreage, Oregon State University area. Agent Larissa Mayfield."
    },
    {
        "slug": "douglas-county",
        "name": "Douglas County",
        "tagline": "Umpqua Valley &mdash; wine, timber, and wide open land.",
        "desc": "Douglas County stretches from the Umpqua Valley to the Coast Range, offering some of the most affordable acreage in western Oregon. Roseburg is the county seat and economic center.",
        "bullets": ["Roseburg county seat", "Umpqua Valley wine region", "Affordable large acreage", "Timber industry base", "South Umpqua River"],
        "img_key": "mistyforest",
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
        "img_key": "well",
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
        "img_key": "docs",
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
        "img_key": "acreageaerial",
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
        "img_key": "wheat",
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
        "img_key": "septic",
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
        "img_key": "contract",
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
        "img_key": "parcelaerial",
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
        "img_key": "fernridge",
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
        "img_key": "springfield",
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
        "img_key": "keys",
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
        "img_key": "heritagebarn",
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
        "img_key": "buyers",
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
        "img_key": "staged",
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
        "img_key": "suburban",
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
        "img_key": "buyers",
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
        "img_key": "parcelaerial",
        "title": "The Rural Buyer&rsquo;s Playbook",
        "tag": "GUIDE &middot; ACREAGE &amp; LAND",
        "desc": "Buying rural property in Oregon is not like buying in a subdivision. Wells, septic, easements, zoning, and more &mdash; this playbook covers everything.",
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
        "img_key": "ridge",
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
        "img_key": "forsale",
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
    <form class="valuation-form reveal reveal-d2" data-form-type="valuation">
      <label><div class="label-text">PROPERTY ADDRESS</div><input type="text" name="property_address" placeholder="24500 Hwy 126, Veneta OR" required></label>
      <label><div class="label-text">APPROXIMATE ACREAGE</div><input type="text" name="acreage" placeholder="12.5"></label>
      <label><div class="label-text">PROPERTY TYPE</div><input type="text" name="property_type" placeholder="Rural / Acreage / Residential"></label>
      <label><div class="label-text">YOUR NAME</div><input type="text" name="name" placeholder="Your name" required></label>
      <label><div class="label-text">EMAIL OR PHONE</div><input type="text" name="contact" placeholder="you@email.com" required></label>
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
        "img_key": "buyers",
        "title": "First-Time Buyer Program",
        "tag": "BUYERS &middot; SPECIALIZED SUPPORT",
        "desc": "Dedicated support for first-time home buyers in Oregon. From loan selection to closing day, I guide you through every step.",
        "seo_desc": "First-time home buyer program in Oregon. Pre-approval, Oregon Bond, USDA loans, step-by-step guidance. Larissa Mayfield, Real Broker.",
    },
    {
        "slug": "acreage-specialist",
        "img_key": "acreageaerial",
        "title": "Acreage &amp; Land Specialist",
        "tag": "RURAL &middot; SPECIALTY",
        "desc": "Specialized expertise in buying and selling acreage properties in Oregon&rsquo;s Willamette Valley. Wells, septic, easements, zoning &mdash; I handle the complexity.",
        "seo_desc": "Oregon acreage and land specialist. Wells, septic, easements, rural pricing. Expert agent Larissa Mayfield, Real Broker.",
    },
    {
        "slug": "relocation-guide",
        "img_key": "coast",
        "title": "Relocating to Oregon",
        "tag": "BUYERS &middot; RELOCATION",
        "desc": "Moving to Oregon from out of state? This guide covers communities, cost of living, climate, schools, and how to buy remotely.",
        "seo_desc": "Relocating to Oregon guide. Cost of living, communities, schools, climate, and remote buying process. By Larissa Mayfield, Real Broker.",
    },
    {
        "slug": "investment-property",
        "img_key": "suburban",
        "title": "Investment Property in Lane County",
        "tag": "INVESTORS &middot; LANE COUNTY",
        "desc": "Lane County offers strong rental demand, affordable entry points, and appreciation potential. Here is what investors need to know.",
        "seo_desc": "Investment property in Lane County, Oregon. Rental demand, cap rates, and market analysis. Guide by Larissa Mayfield, Real Broker.",
    },
    {
        "slug": "downsizing-guide",
        "img_key": "creswell",
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
    <p class="body-text reveal reveal-d2" style="margin-top:36px;max-width:420px">Licensed throughout Oregon with deep roots in west Lane County &mdash; Veneta, Elmira, and the Fern Ridge area. I specialize in rural properties, acreage, and first-time buyers across Lane, Linn, Benton, and Douglas counties.</p>
    <div style="margin-top:36px;display:flex;gap:14px;flex-wrap:wrap" class="reveal reveal-d3">
      <a class="btn-primary" href="contact.html">Schedule a Call &rarr;</a>
      <a class="btn-link" href="sellers.html">Sell Your Home</a>
    </div>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="images/larissa-hat.jpg" alt="Larissa Mayfield, Oregon real estate broker, in the Willamette Valley"></div>
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
    <form class="valuation-form reveal reveal-d2" data-form-type="valuation">
      <label><div class="label-text">PROPERTY ADDRESS</div><input type="text" name="property_address" placeholder="24500 Hwy 126, Veneta OR" required></label>
      <label><div class="label-text">APPROXIMATE ACREAGE</div><input type="text" name="acreage" placeholder="12.5"></label>
      <label><div class="label-text">YOUR NAME</div><input type="text" name="name" placeholder="Your name" required></label>
      <label><div class="label-text">EMAIL OR PHONE</div><input type="text" name="contact" placeholder="you@email.com" required></label>
      <button type="submit">REQUEST VALUATION &rarr;</button>
    </form>
  </div>
</section>
<section style="padding:96px 56px">
  <div class="tag tag-purple reveal">Communities</div>
  <h2 class="section-heading reveal reveal-d1" style="margin-top:18px;margin-bottom:40px">Where I work.</h2>
  <div class="community-grid">
    <article class="reveal"><a href="communities/veneta.html"><img src="{IMG['fernridge']}" alt="{stock_alt('fernridge')}"><h3>Veneta</h3><p>Small-town roots, ten minutes from Eugene.</p></a></article>
    <article class="reveal reveal-d1"><a href="communities/elmira.html"><img src="{IMG['barn']}" alt="{stock_alt('barn')}"><h3>Elmira</h3><p>Quiet acreage living, close to everything.</p></a></article>
    <article class="reveal reveal-d2"><a href="communities/eugene.html"><img src="{IMG['eugene']}" alt="{stock_alt('eugene')}"><h3>Eugene</h3><p>Oregon&rsquo;s second city.</p></a></article>
    <article class="reveal reveal-d3"><a href="communities/springfield.html"><img src="{IMG['springfield']}" alt="{stock_alt('springfield')}"><h3>Springfield</h3><p>Affordable homes, growing fast.</p></a></article>
    <article class="reveal"><a href="communities/cottage-grove.html"><img src="{IMG['coveredbridge']}" alt="{stock_alt('coveredbridge')}"><h3>Cottage Grove</h3><p>Covered bridges and forested hills.</p></a></article>
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
    <img src="images/larissa-hat-smile.jpg" alt="Larissa Mayfield, Oregon real estate broker">
    <img src="images/larissa-family-outdoor.jpg?v=3" alt="Larissa Mayfield with her family outdoors in rural Oregon">
    <img src="images/larissa-horse.jpg" alt="Larissa Mayfield with her horse in the Willamette Valley">
    <img src="images/larissa-family.jpg?v=2" alt="Larissa Mayfield with her family">
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
        "Larissa Mayfield is a licensed Oregon Realtor with Real Broker specializing in rural properties, acreage, and first-time buyers in Veneta, Elmira, and throughout Lane, Linn, Benton, and Douglas counties.",
        "home", [], body, "RealEstateAgent")

def gen_about():
    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">About Larissa</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Roots in<br>the <em>valley.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">I grew up in a 4-H family in rural Oregon. Before real estate, I spent two decades in commercial lending &mdash; underwriting rural transactions, working with appraisers, and learning how complex deals actually close.</p>
    <p class="body-text reveal reveal-d3" style="margin-top:16px;max-width:440px">That background is why my clients hire me. I understand wells, septic systems, easements, and the financing structures that make rural property sales work. I don&rsquo;t learn on the job &mdash; I brought the expertise with me.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal is-portrait" src="images/larissa-hat-seated.jpg" alt="Larissa Mayfield, Oregon real estate broker, seated in a wide-brimmed hat"></div>
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
      <img src="images/larissa-horse.jpg" alt="Larissa Mayfield with her horse in the Willamette Valley">
      <img src="images/larissa-family-outdoor.jpg?v=3" alt="Larissa Mayfield with her family outdoors in rural Oregon">
      <img src="images/larissa-laptop.jpg" alt="Larissa Mayfield working on a client&rsquo;s rural listing">
      <img src="images/larissa-family.jpg?v=2" alt="Larissa Mayfield with her family">
    </div>
    <div>
      <div class="tag tag-purple reveal" style="margin-bottom:18px">Community &amp; Values</div>
      <h2 class="section-heading reveal reveal-d1">4-H roots,<br>real values.</h2>
      <p class="body-text reveal reveal-d2" style="margin-top:24px">Community, honesty, hard work, and showing up &mdash; those are not marketing slogans. They are how I was raised, and they are how I run my business. Every client is a neighbor, and every transaction is a handshake.</p>
      <img src="images/larissa-4h-swine.jpg" alt="Champion show pig at the Lane County Youth Livestock Auction &mdash; carrying on the 4-H and FFA tradition" class="reveal reveal-d3" style="width:100%;height:auto;margin-top:28px;border-radius:2px">
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
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{IMG['forsale']}" alt="{stock_alt('forsale')}"></div>
</section>
<section class="section-dark">
  <div class="valuation-grid">
    <div>
      <div class="tag reveal" style="margin-bottom:24px">Sellers &middot; No-Obligation Valuation</div>
      <h2 class="section-heading reveal reveal-d1" style="color:var(--cream)">What is your property<br><em style="color:var(--cream)"><i>worth today?</i></em></h2>
      <p class="body-text reveal reveal-d2" style="color:rgba(244,239,230,.85);margin-top:24px;max-width:420px">A free, no-obligation valuation built from real comparable sales and an honest conversation about your property in today&rsquo;s market.</p>
    </div>
    <form class="valuation-form reveal reveal-d2" data-form-type="valuation">
      <label><div class="label-text">PROPERTY ADDRESS</div><input type="text" name="property_address" placeholder="24500 Hwy 126, Veneta OR" required></label>
      <label><div class="label-text">APPROXIMATE ACREAGE</div><input type="text" name="acreage" placeholder="12.5"></label>
      <label><div class="label-text">PROPERTY TYPE</div><input type="text" name="property_type" placeholder="Rural / Acreage / Residential"></label>
      <label><div class="label-text">YOUR NAME</div><input type="text" name="name" placeholder="Your name" required></label>
      <label><div class="label-text">EMAIL OR PHONE</div><input type="text" name="contact" placeholder="you@email.com" required></label>
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
    <img class="reveal parallax-img" src="{IMG['parcelaerial']}" alt="{stock_alt('parcelaerial')}">
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
  <img src="{IMG['acreageaerial']}" alt="{stock_alt('acreageaerial')}">
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
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{IMG['keys']}" alt="{stock_alt('keys')}"></div>
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
    <img class="reveal parallax-img" src="{IMG['buyers']}" alt="{stock_alt('buyers')}">
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
        cards += f'''    <article class="reveal{delay}"><a href="{c['slug']}.html"><img src="{stock_path(c['img_key'], 1)}" alt="{stock_alt(c['img_key'])}"><h3>{c['name']}</h3><p>{c['tagline']}</p></a></article>\n'''
    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">Communities</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Where I<br><em>work.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">From Eugene to Drain, the Willamette Valley to the Coast Range &mdash; I serve buyers and sellers across Lane, Linn, Benton, and Douglas counties.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{stock_path('acreageaerial', 1)}" alt="{stock_alt('acreageaerial')}"></div>
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
  <img src="{stock_path(c['img_key'], 1)}" alt="{stock_alt(c['img_key'])}">
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
        guide_cards += f'''    <div class="guide-card reveal"><img src="{stock_path(g['img_key'], 0)}" alt="{stock_alt(g['img_key'])}"><div class="guide-card-body"><div class="tag tag-purple" style="margin-bottom:12px">{g['tag']}</div><h3 style="font-size:26px;letter-spacing:-.01em;margin-bottom:8px;font-weight:400">{g['title']}</h3><p class="body-text" style="font-size:14px;margin-bottom:auto">{g['desc']}</p><a class="btn-link" href="guides/{g['slug']}.html" style="margin-top:20px">Read &rarr;</a></div></div>\n'''

    blog_cards = ""
    for i, b in enumerate(BLOGS[:6]):
        blog_cards += f'''    <div class="blog-card reveal"><img src="{stock_path(b['img_key'], 0)}" alt="{stock_alt(b['img_key'])}"><div class="meta">{b['tag']} &middot; {b['date']}</div><h3><a href="blog/{b['slug']}.html">{b['title']}</a></h3><p>{b['excerpt'][:120]}...</p></div>\n'''

    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">Resources</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Guides &amp;<br><em>insights.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">Free guides, market reports, and blog articles to help you make informed real estate decisions in Oregon.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{IMG['forestpath']}" alt="{stock_alt('forestpath')}"></div>
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
  <div class="parallax-wrap"><img class="parallax-img reveal" src="images/larissa-headshot.jpg" alt="Portrait of Larissa Mayfield, Real Broker, Oregon"></div>
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
    import json as _j
    reviews = [{"@type": "Review",
                "author": {"@type": "Person", "name": re.sub(r"&[a-z]+;", "&", t[0])},
                "reviewRating": {"@type": "Rating", "ratingValue": 5, "bestRating": 5},
                "reviewBody": re.sub(r"&[a-z]+;", "'", t[2])[:500],
                "itemReviewed": {"@type": "RealEstateAgent", "name": "Larissa Mayfield"}}
               for t in TESTIMONIALS]
    review_schema = ',"aggregateRating":' + _j.dumps({
        "@type": "AggregateRating", "ratingValue": 5, "bestRating": 5,
        "reviewCount": len(TESTIMONIALS)}) + ',"review":' + _j.dumps(reviews)
    make_page(f"{SITE}/testimonials.html", 0,
        "Client Testimonials — Larissa Mayfield Reviews",
        "Read reviews from Larissa Mayfield's real estate clients in Oregon. Verified testimonials from buyers, sellers, and rural property transactions.",
        "testimonials", [("testimonials.html", "TESTIMONIALS")], body,
        schema_type="RealEstateAgent", extra_schema=review_schema)

def gen_contact():
    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">Contact</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Let&rsquo;s<br><em>connect.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">Whether you are ready to buy, thinking about selling, or just have questions &mdash; I am here. No pressure, no obligation.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal is-portrait" src="images/larissa-hat-smile.jpg" alt="Larissa Mayfield smiling, wearing a wide-brimmed hat"></div>
</section>
<section>
  <div class="contact-grid">
    <form class="contact-form reveal" data-form-type="contact">
      <div><div class="form-label">YOUR NAME</div><input type="text" name="name" placeholder="Full name" required></div>
      <div><div class="form-label">EMAIL</div><input type="email" name="email" placeholder="you@email.com" required></div>
      <div><div class="form-label">PHONE</div><input type="tel" name="phone" placeholder="541-000-0000"></div>
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
      <div><div class="form-label">MESSAGE</div><textarea name="message" rows="5" placeholder="Tell me a little about your situation..."></textarea></div>
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
        <div style="font-family:var(--mono);font-size:10px;letter-spacing:.2em;color:var(--muted);margin-bottom:16px">MAILING</div>
        <div style="font-family:var(--sans);font-size:16px;line-height:1.7;color:var(--muted)">PO Box 161<br>Elmira, OR 97437</div>
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
        cards += f'''    <div class="blog-card reveal{delay}"><img src="{stock_path(b['img_key'], 1)}" alt="{stock_alt(b['img_key'])}"><div class="meta">{b['tag']} &middot; {b['date']}</div><h3><a href="{b['slug']}.html">{b['title']}</a></h3><p>{b['excerpt']}</p></div>\n'''
    body = f'''<section class="inner-hero">
  <div>
    <div class="tag tag-purple reveal">Blog</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px">Articles &amp;<br><em>insights.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:440px">Practical advice on buying, selling, and owning real estate in Oregon. Written by Larissa Mayfield.</p>
  </div>
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{stock_path('ridge', 1)}" alt="{stock_alt('ridge')}"></div>
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
  <div class="parallax-wrap"><img class="parallax-img reveal" src="{stock_path(s.get('img_key','keys'), 1)}" alt="{stock_alt(s.get('img_key','keys'))}"></div>
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

# ══════════════════════════════════════════════════════════════════════════════
# LISTING PAGES
# ══════════════════════════════════════════════════════════════════════════════
# One landing page per property, driven entirely by listings_data.LISTINGS.
# Every section is conditional: if the data isn't there, the section doesn't
# render. That is deliberate — a half-filled listing page reads as neglect, and
# an invented fact on a licensed broker's site is a real problem. Better to show
# eight tight sections than sixteen with "TBD" in them.

import glob as _glob
import json as _json
from listings_data import LISTINGS, STATUS_LABEL, PUBLIC_STATUSES


def fmt_money(n):
    return None if n is None else "$" + f"{int(round(n)):,}"


def fmt_dec(n):
    """3.67 -> '3.67', 2.0 -> '2', 4 -> '4'."""
    if n is None:
        return None
    if isinstance(n, float):
        return f"{n:g}"
    return f"{n:,}"


def fmt_int(n):
    return None if n is None else f"{int(n):,}"


def listing_addr(l, full=True):
    a = f"{l['address']}, {l['city']}, {l['state']}"
    return f"{a} {l['zip']}" if full and l.get("zip") else a


def listing_photos(l):
    """[(src_relative_to_listings_dir, alt, caption)] in filename order.

    Globs the folder rather than trusting a hand-written list, so the page can
    never point at a photo that isn't on disk. Add photos by dropping files in
    and re-running — no code change.
    """
    slug = l["slug"]
    d = f"{SITE}/images/listings/{slug}"
    # build_images.py writes its WebP derivatives alongside the sources as
    # <name>-<width>.webp. Those are not photographs of the property — without
    # this filter the gallery counts every derivative as another photo.
    files = sorted(f for ext in ("jpg", "jpeg", "png", "webp")
                   for f in (os.path.basename(p) for p in _glob.glob(f"{d}/*.{ext}"))
                   if not re.search(r"-\d+\.webp$", f))
    caps = l.get("photo_captions") or {}
    addr = listing_addr(l, full=False)
    out = []
    for i, fn in enumerate(files):
        cap = caps.get(fn)
        # Alt text describes the photograph. A caption, when the photographer
        # or Larissa wrote one, is always the better description.
        alt = cap or f"{addr} &mdash; photo {i + 1} of {len(files)}"
        out.append((f"../images/listings/{slug}/{fn}", alt, cap))
    if out:
        return out
    # A draft with no photos yet still previews, using stock stand-ins, so the
    # layout can be reviewed before the shoot. Anything public must have real ones.
    if l.get("status") == "draft":
        return [(stock_path(k, 1), stock_alt(k), None)
                for k in (l.get("sample_stock") or ["parcelaerial", "whitehome", "interior"])]
    raise SystemExit(
        f"\n❌ Listing '{slug}' is status '{l['status']}' but images/listings/{slug}/ is empty.\n"
        f"   Add photos (01-front.jpg, 02-living.jpg, ...) or set status back to 'draft'.")


def _rows(pairs):
    """Fact rows, dropping any whose value is None/blank."""
    return "".join(
        f'<div class="fact-row"><dt>{k}</dt><dd>{v}</dd></div>'
        for k, v in pairs if v not in (None, "", "&mdash;")
    )


def listing_price_block(l):
    """Headline price, with the sold price taking over once it closes."""
    if l.get("status") == "sold" and l.get("sold_price"):
        return (fmt_money(l["sold_price"]),
                f"Sold{' &middot; ' + l['sold_date'] if l.get('sold_date') else ''}")
    if l.get("price"):
        return fmt_money(l["price"]), STATUS_LABEL.get(l.get("status"), "For Sale")
    return None, STATUS_LABEL.get(l.get("status"), "")


def listing_schema(l, photos):
    """RealEstateListing + Residence + Offer graph. The reference site ships
    none of this; it's the cheapest rich-result win on the page."""
    base = f"https://larissamayfieldre.com/listings/{l['slug']}.html"
    avail = {"active": "InStock", "coming-soon": "PreOrder",
             "pending": "LimitedAvailability", "sold": "SoldOut"}.get(l.get("status"), "InStock")
    prop = {
        "@type": "SingleFamilyResidence",
        "@id": base + "#property",
        "name": listing_addr(l, full=False),
        "address": {"@type": "PostalAddress", "streetAddress": l["address"],
                    "addressLocality": l["city"], "addressRegion": l["state"],
                    "postalCode": l.get("zip"), "addressCountry": "US"},
        "url": base,
    }
    if l.get("beds"):
        prop["numberOfBedrooms"] = l["beds"]
    if l.get("baths"):
        prop["numberOfBathroomsTotal"] = l["baths"]
    if l.get("sqft"):
        prop["floorSize"] = {"@type": "QuantitativeValue", "value": l["sqft"], "unitCode": "FTK"}
    if l.get("acres"):
        prop["lotSize"] = {"@type": "QuantitativeValue", "value": l["acres"], "unitText": "acre"}
    if l.get("year_built"):
        prop["yearBuilt"] = l["year_built"]
    if l.get("lat") and l.get("lng"):
        prop["geo"] = {"@type": "GeoCoordinates", "latitude": l["lat"], "longitude": l["lng"]}
    if photos:
        prop["photo"] = [f"https://larissamayfieldre.com/{p[0].replace('../', '')}" for p in photos[:12]]

    agent = {"@type": "RealEstateAgent", "name": "Larissa Mayfield",
             "telephone": "541-784-7745", "email": "larissa@theoperativegroup.com",
             "url": "https://larissamayfieldre.com", "parentOrganization": {
                 "@type": "Organization", "name": "Real Broker, LLC"}}

    graph = [{
        "@type": "RealEstateListing", "@id": base, "url": base,
        "name": listing_addr(l, full=False),
        "description": re.sub(r"<[^>]+>", "", l["description"][0])[:300] if l.get("description") else "",
        "about": {"@id": base + "#property"},
        "provider": agent,
    }, prop]
    price = l.get("sold_price") if l.get("status") == "sold" else l.get("price")
    if price:
        graph.append({"@type": "Offer", "itemOffered": {"@id": base + "#property"},
                      "price": price, "priceCurrency": "USD",
                      "availability": f"https://schema.org/{avail}", "seller": agent})
    js = _json.dumps({"@context": "https://schema.org", "@graph": graph}).replace("<", "\\u003c")
    return f'<script type="application/ld+json">{js}</script>\n'


def gen_listing_page(l):
    slug, status = l["slug"], l.get("status", "draft")
    photos = listing_photos(l)
    addr_short = listing_addr(l, full=False)
    price, price_label = listing_price_block(l)
    is_draft = status == "draft"
    S = []  # section buffer

    # ── Draft banner ────────────────────────────────────────────────────────
    if is_draft:
        S.append('''<div class="draft-bar">
  <strong>PREVIEW &mdash; NOT PUBLISHED.</strong> This page is <code>noindex</code>, kept out of the
  sitemap, and hidden from the listings index. Verify every fact against the MLS sheet and the
  county record, then set <code>status</code> to <code>active</code> in <code>listings_data.py</code>.
</div>''')

    # ── Sticky action bar (slides in once the hero clears) ───────────────────
    stick_stats = " &middot; ".join(x for x in [
        f"{fmt_dec(l.get('beds'))} bd" if l.get("beds") else None,
        f"{fmt_dec(l.get('baths'))} ba" if l.get("baths") else None,
        f"{fmt_int(l.get('sqft'))} sq ft" if l.get("sqft") else None,
        f"{fmt_dec(l.get('acres'))} ac" if l.get("acres") else None] if x)
    S.append(f'''<div class="listing-stickybar" id="listingStickyBar">
  <div class="lsb-left">
    <span class="lsb-addr">{l['address']}</span>
    <span class="lsb-stats">{stick_stats}</span>
  </div>
  <div class="lsb-right">
    {f'<span class="lsb-price">{price}</span>' if price else ''}
    <a class="lsb-cta" href="#showing">Request a Showing</a>
  </div>
</div>''')

    # ── Hero ────────────────────────────────────────────────────────────────
    hero_src, hero_alt, _ = photos[0]
    stat_cells = "".join(
        f'<div class="lstat"><span class="n">{v}</span><span class="k">{k}</span></div>'
        for k, v in [
            ("Bedrooms", fmt_dec(l.get("beds"))),
            ("Bathrooms", fmt_dec(l.get("baths"))),
            ("Square Feet", fmt_int(l.get("sqft"))),
            ("Acres", fmt_dec(l.get("acres"))),
            ("Built", str(l["year_built"]) if l.get("year_built") else None),
        ] if v)
    S.append(f'''<section class="listing-hero">
  <img src="{hero_src}" alt="{hero_alt}" data-sizes="hero">
  <div class="lh-scrim"></div>
  <div class="lh-content">
    <div class="lh-main">
      <span class="status-pill status-{status}">{STATUS_LABEL.get(status, '')}</span>
      {f'<div class="lh-kicker">{l["kicker"]}</div>' if l.get("kicker") else ''}
      <h1>{l['address']}</h1>
      <div class="lh-city">{l['city']}, {l['state']} {l.get('zip', '')} &middot; {l.get('county', '')}</div>
    </div>
    <div class="lh-aside">
      {f'<div class="lh-price">{price}</div><div class="lh-price-label">{price_label}</div>' if price else ''}
      {f'<p class="lh-tagline">{l["tagline"]}</p>' if l.get("tagline") else ''}
      <div class="lh-actions">
        <button class="btn-mono" type="button" data-lightbox-open="0">VIEW {len(photos)} PHOTOS</button>
        <a class="btn-ghost" href="#showing">REQUEST A SHOWING</a>
      </div>
    </div>
  </div>
</section>''')

    # ── Meta strip ──────────────────────────────────────────────────────────
    meta_bits = [x for x in [
        f"MLS# {l['mls']}" if l.get("mls") else None,
        l.get("property_type"),
        f"{fmt_dec(l['acres'])} acres" if l.get("acres") else None,
        l.get("county"),
        f"Built {l['year_built']}" if l.get("year_built") else None,
        STATUS_LABEL.get(status, ""),
    ] if x]
    S.append('<div class="meta-strip">' + "".join(f"<span>{b}</span>" for b in meta_bits) + "</div>")

    # ── Gallery ─────────────────────────────────────────────────────────────
    # Hero already rendered photos[0]; the mosaic shows the rest, so every
    # photo appears exactly once in the HTML. The lightbox holds all of them.
    def _full(src):
        """Largest WebP derivative for the lightbox, falling back to the JPEG."""
        info = img_manifest().get(os.path.relpath(
            os.path.normpath(os.path.join(f"{SITE}/listings", src)), SITE))
        if not info or not info.get("widths"):
            return src
        return f"{os.path.splitext(src)[0]}-{max(info['widths'])}.webp"
    gallery_data = _json.dumps(
        [{"src": _full(s), "alt": a, "cap": c or ""} for s, a, c in photos]
    ).replace("<", "\\u003c")
    if len(photos) > 1:
        # Uniform tiles, every one the same 3:2 crop — a property gallery reads
        # as a considered set, not a ransom note. Only the first GALLERY_PREVIEW
        # are in the initial view; the rest ship in the HTML (so they are in the
        # page source for crawlers) but are display:none until expanded.
        GALLERY_PREVIEW = 12
        rest = photos[1:]
        tiles = ""
        for i, (src, alt, cap) in enumerate(rest, start=1):
            hidden = " is-hidden" if i > GALLERY_PREVIEW else ""
            tiles += (f'<figure class="gtile{hidden}" data-lightbox-open="{i}">'
                      f'<img src="{src}" alt="{alt}" loading="lazy" data-sizes="tile">'
                      + (f'<figcaption>{cap}</figcaption>' if cap else '')
                      + '</figure>')
        more = ""
        if len(rest) > GALLERY_PREVIEW:
            more = (f'<div class="gallery-more-wrap">'
                    f'<button class="gallery-more" type="button" data-gallery-more '
                    f'data-total="{len(photos)}">Show all {len(photos)} photos'
                    f'<span class="gm-count">+{len(rest) - GALLERY_PREVIEW} more</span></button></div>')
        S.append(f'''<section class="listing-gallery" id="gallery" data-photos="{len(photos)}">
  <script type="application/json" id="galleryPhotos">{gallery_data}</script>
  <div class="lg-head">
    <div>
      <div class="tag tag-purple">Gallery</div>
      <h2 class="section-heading" style="margin-top:12px">See it properly.</h2>
    </div>
    <button class="btn-link" type="button" data-lightbox-open="0">Open full screen &rarr;</button>
  </div>
  <div class="ggrid">{tiles}</div>
  {more}
</section>''')
    else:
        S.append(f'<script type="application/json" id="galleryPhotos">{gallery_data}</script>')

    # ── Description ─────────────────────────────────────────────────────────
    if l.get("description"):
        paras = "".join(f"<p>{p}</p>" for p in l["description"])
        hl = ""
        if l.get("highlights"):
            hl = '<div class="hl-grid">' + "".join(
                f'<div class="hl"><span class="hl-k">{k}</span><span class="hl-v">{v}</span></div>'
                for k, v in l["highlights"]) + "</div>"
        S.append(f'''<section class="chapter" id="about">
  <div class="chapter-sticky">
    <div class="tag tag-purple">The Property</div>
    <h2 class="section-heading" style="margin-top:18px">About<br>{l['city']}.</h2>
    <p class="body-text" style="margin-top:20px;font-size:15px;color:var(--muted)">
      Written by Larissa after walking the property &mdash; not copied off the MLS sheet.</p>
  </div>
  <div class="chapter-body">{paras}{hl}</div>
</section>''')

    # ── Fact table ──────────────────────────────────────────────────────────
    if l.get("fact_groups"):
        cols = ""
        for title, pairs in l["fact_groups"]:
            rows = _rows(pairs)
            if rows:
                cols += f'<div class="fact-col"><h3>{title}</h3><dl>{rows}</dl></div>'
        if cols:
            S.append(f'''<section class="section-alt" id="facts">
  <div class="tag tag-purple">The Numbers</div>
  <h2 class="section-heading" style="margin-top:18px;margin-bottom:36px">Every fact, in one place.</h2>
  <div class="fact-cols">{cols}</div>
  <p class="fine">Information from the seller, the MLS, and public record. Believed accurate but not
  guaranteed &mdash; buyer to verify all measurements, systems, permits, and zoning to their own
  satisfaction during the inspection period.</p>
</section>''')

    # ── Rural infrastructure panel ──────────────────────────────────────────
    if l.get("rural"):
        r = l["rural"]
        items = "".join(
            f'<div class="ru-item"><div class="ru-k">{k}</div><div class="ru-v">{v}</div>'
            f'<p class="ru-note">{note}</p></div>'
            for k, v, note in r["items"])
        S.append(f'''<section class="rural-panel" id="land">
  <div class="rp-head">
    <div class="tag" style="color:rgba(244,239,230,.6)">Land, Water &amp; Zoning</div>
    <h2>What actually governs this parcel.</h2>
    <p>{r.get('intro', '')}</p>
  </div>
  <div class="ru-grid">{items}</div>
  <div class="rp-foot">Rural due diligence is its own discipline. If any of this is unfamiliar,
    read the <a href="../guides/rural-buyer-playbook.html">Rural Buyer Playbook</a> or just call me
    &mdash; <a href="tel:5417847745">541.784.7745</a>.</div>
</section>''')

    # ── Rooms ───────────────────────────────────────────────────────────────
    if l.get("rooms"):
        rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in l["rooms"])
        S.append(f'''<section class="rooms-section" id="rooms">
  <div class="tag tag-purple">Room by Room</div>
  <h2 class="section-heading" style="margin-top:18px;margin-bottom:28px">Dimensions.</h2>
  <table class="rooms-table">
    <thead><tr><th>Room</th><th>Dimensions</th><th>Level</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <p class="fine">Dimensions are approximate and taken from the listing sheet. Measure anything a
  decision depends on.</p>
</section>''')

    # ── Features ────────────────────────────────────────────────────────────
    if l.get("features"):
        cols = "".join(
            f'<div class="feat-col"><h3>{t}</h3><ul>'
            + "".join(f'<li><span class="dash">&mdash;</span>{i}</li>' for i in items)
            + "</ul></div>"
            for t, items in l["features"].items() if items)
        S.append(f'''<section class="section-alt" id="features">
  <div class="tag tag-purple">Features</div>
  <h2 class="section-heading" style="margin-top:18px;margin-bottom:32px">What comes with it.</h2>
  <div class="feat-cols">{cols}</div>
</section>''')

    # ── Payment estimator ───────────────────────────────────────────────────
    if l.get("price") and status != "sold":
        tax_row = l.get("taxes_annual") or 0
        S.append(f'''<section class="calc-section" id="payment" data-price="{l['price']}"
         data-taxes="{tax_row}" data-hoa="0">
  <div class="calc-intro">
    <div class="tag" style="color:rgba(244,239,230,.6)">Run the Numbers</div>
    <h2>What would this cost a month?</h2>
    <p>Move the numbers around. Nothing is sent anywhere and nothing here is a loan offer &mdash;
      it is the same arithmetic your lender does, so you can walk into that conversation already
      knowing the shape of it.</p>
    <p class="calc-disclaim">Estimate only. Not a quote, a pre-approval, or financial advice.
      Rates, taxes, and insurance vary; your lender&rsquo;s number is the one that counts.</p>
  </div>
  <div class="calc-panel">
    <div class="calc-grid">
      <label><span>Purchase price</span><input type="text" id="calcPrice" inputmode="numeric" value="{l['price']}"></label>
      <label><span>Down payment &mdash; <b id="calcDownPct">20</b>%</span>
        <input type="range" id="calcDown" min="0" max="50" step="1" value="20">
        <em id="calcDownAmt"></em></label>
      <label><span>Interest rate &mdash; <b id="calcRatePct">6.5</b>%</span>
        <input type="range" id="calcRate" min="3" max="10" step="0.125" value="6.5"></label>
      <label><span>Term</span>
        <select id="calcTerm"><option value="30">30 years</option><option value="20">20 years</option>
        <option value="15">15 years</option></select></label>
      <label><span>Property tax / yr</span><input type="text" id="calcTax" inputmode="numeric" value="{tax_row}"></label>
      <label><span>Insurance / yr</span><input type="text" id="calcIns" inputmode="numeric" value="1800"></label>
    </div>
    <div class="calc-out">
      <div class="calc-total"><span class="co-n" id="calcTotal">&mdash;</span><span class="co-k">estimated / month</span></div>
      <ul class="calc-break">
        <li><span>Principal &amp; interest</span><b id="calcPI">&mdash;</b></li>
        <li><span>Property taxes</span><b id="calcTaxM">&mdash;</b></li>
        <li><span>Insurance</span><b id="calcInsM">&mdash;</b></li>
        <li class="calc-loan"><span>Loan amount</span><b id="calcLoan">&mdash;</b></li>
      </ul>
    </div>
  </div>
</section>''')

    # ── Tour + video ────────────────────────────────────────────────────────
    media = ""
    if l.get("tour_url"):
        media += (f'<div class="media-frame"><iframe src="{l["tour_url"]}" loading="lazy" '
                  f'title="3D virtual tour of {addr_short}" allowfullscreen></iframe></div>')
    if l.get("video_id"):
        # Facade: the real iframe only loads on click, so an unwatched video
        # costs the page nothing.
        media += (f'<div class="media-facade" data-yt="{l["video_id"]}" role="button" tabindex="0" '
                  f'aria-label="Play video tour of {addr_short}">'
                  f'<img src="https://i.ytimg.com/vi/{l["video_id"]}/maxresdefault.jpg" '
                  f'alt="Video tour thumbnail for {addr_short}" loading="lazy">'
                  f'<span class="mf-play">&#9654;</span></div>')
    if media:
        S.append(f'''<section class="media-section" id="tour">
  <div class="tag tag-purple">Walk It From Here</div>
  <h2 class="section-heading" style="margin-top:18px;margin-bottom:28px">Tour &amp; video.</h2>
  <div class="media-grid">{media}</div>
</section>''')

    # ── Location: map, drive times, schools ─────────────────────────────────
    loc = ""
    if l.get("map_query"):
        q = l["map_query"].replace(" ", "+").replace("&", "%26")
        loc += (f'<div class="map-frame"><iframe src="https://www.google.com/maps?q={q}&output=embed" '
                f'loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
                f'title="Map of {addr_short}"></iframe></div>')
    side = ""
    if l.get("nearby"):
        side += ('<div class="loc-block"><h3>Drive times</h3><dl class="drive-list">'
                 + "".join(f"<div><dt>{p}</dt><dd>{t}</dd></div>" for p, t in l["nearby"])
                 + "</dl></div>")
    if l.get("schools"):
        side += ('<div class="loc-block"><h3>Schools</h3><table class="school-table"><tbody>'
                 + "".join(f"<tr><td class='sl'>{lv}</td><td>{n}<span>{d}</span></td><td>{dist}</td></tr>"
                           for lv, n, d, dist in l["schools"])
                 + '</tbody></table><p class="fine">School assignment is set by the district and '
                   'can change. Confirm boundaries directly with the district before you rely on them.</p></div>')
    if loc or side:
        S.append(f'''<section class="loc-section" id="location">
  <div class="loc-head">
    <div class="tag tag-purple">Location</div>
    <h2 class="section-heading" style="margin-top:18px">Where it sits.</h2>
  </div>
  <div class="loc-grid">{loc}<div class="loc-side">{side}</div></div>
</section>''')

    # ── Open houses ─────────────────────────────────────────────────────────
    if l.get("open_houses"):
        rows = "".join(f'<div class="oh-row"><div class="oh-date">{d}</div>'
                       f'<div class="oh-time">{t}</div>'
                       f'<a class="oh-cta" href="#showing">Can&rsquo;t make it? Book a private showing &rarr;</a></div>'
                       for d, t in l["open_houses"])
        S.append(f'''<section class="oh-section">
  <div class="tag tag-purple">Open House</div>
  <h2 class="section-heading" style="margin-top:18px;margin-bottom:24px">Come walk through.</h2>
  {rows}
</section>''')

    # ── Documents ───────────────────────────────────────────────────────────
    if l.get("documents"):
        docs = "".join(
            f'<a class="doc-card" href="{href}"><span class="doc-k">{label}</span>'
            f'<span class="doc-n">{note}</span><span class="doc-arrow">&darr;</span></a>'
            for label, href, note in l["documents"])
        S.append(f'''<section class="section-alt" id="documents">
  <div class="tag tag-purple">Disclosures</div>
  <h2 class="section-heading" style="margin-top:18px;margin-bottom:12px">Read it before you write.</h2>
  <p class="body-text" style="max-width:620px;margin-bottom:32px">Everything the seller has provided,
    up front. No form, no email gate &mdash; a buyer who reads the disclosures early is a buyer who
    closes.</p>
  <div class="doc-grid">{docs}</div>
</section>''')

    # ── Showing request + agent card ────────────────────────────────────────
    S.append(f'''<section class="showing-section" id="showing">
  <div class="showing-grid">
    <form class="contact-form" data-form-type="showing">
      <div class="sf-head">
        <div class="tag tag-purple">Private Showing</div>
        <h2>See {l['address']}.</h2>
        <p>Tell me when works and I&rsquo;ll confirm by text, usually within a couple of hours.
          If you already have an agent, bring them &mdash; this form still gets you scheduled.</p>
      </div>
      <input type="hidden" name="listing_address" value="{listing_addr(l)}">
      <input type="hidden" name="listing_mls" value="{l.get('mls') or ''}">
      <div><div class="form-label">YOUR NAME</div><input type="text" name="name" placeholder="Full name" required></div>
      <div class="sf-two">
        <div><div class="form-label">EMAIL</div><input type="email" name="email" placeholder="you@email.com" required></div>
        <div><div class="form-label">PHONE</div><input type="tel" name="phone" placeholder="541-000-0000"></div>
      </div>
      <div><div class="form-label">WHEN WORKS?</div>
        <div class="interest-chips">
          <button class="chip" type="button">Weekday morning</button>
          <button class="chip" type="button">Weekday afternoon</button>
          <button class="chip" type="button">Weekday evening</button>
          <button class="chip" type="button">Saturday</button>
          <button class="chip" type="button">Sunday</button>
          <button class="chip" type="button">ASAP</button>
        </div>
      </div>
      <div><div class="form-label">ANYTHING I SHOULD KNOW?</div>
        <textarea name="message" rows="4" placeholder="Questions about the well, the zoning, the roof — ask now and I'll have answers ready."></textarea></div>
      <button class="btn-mono" type="submit">REQUEST SHOWING &rarr;</button>
      <p class="fine">Larissa Mayfield &middot; Real Broker, LLC &middot; License #201231874. Submitting
        this does not create an agency relationship.</p>
    </form>
    <aside class="showing-aside">
      <div class="agent-card">
        <img src="../images/larissa-headshot.jpg" alt="Portrait of Larissa Mayfield, Real Broker, Oregon">
        <div class="ac-body">
          <div class="ac-name">Larissa Mayfield</div>
          <div class="ac-lic">REAL BROKER &middot; LIC. 201231874</div>
          <p>I live and work out here. If you want to know what the road does in February, whether
            the well is going to hold up, or what the neighbours actually farm &mdash; ask me, not a
            portal.</p>
          <a class="ac-phone" href="tel:5417847745">541.784.7745</a>
          <a class="ac-mail" href="mailto:larissa@theoperativegroup.com">larissa@theoperativegroup.com</a>
        </div>
      </div>
      <div class="aside-links">
        <a href="#payment">Estimate the monthly payment</a>
        <a href="../guides/rural-buyer-playbook.html">Rural buyer playbook</a>
        <a href="../services/wells-septic-guide.html">Wells &amp; septic, explained</a>
        <a href="../buyers.html">How buying works with me</a>
        <button type="button" class="print-btn" data-print>Print this listing</button>
      </div>
    </aside>
  </div>
</section>''')

    # ── Other listings ──────────────────────────────────────────────────────
    others = [o for o in LISTINGS if o["slug"] != slug and o.get("status") in PUBLIC_STATUSES][:3]
    if others:
        cards = ""
        for o in others:
            op = listing_photos(o)[0][0]
            oprice, _ = listing_price_block(o)
            cards += (f'<a class="ol-card" href="{o["slug"]}.html">'
                      f'<img src="{op}" alt="{listing_addr(o, full=False)}" loading="lazy" data-sizes="card">'
                      f'<span class="ol-status status-{o.get("status")}">{STATUS_LABEL.get(o.get("status"))}</span>'
                      f'<span class="ol-addr">{o["address"]}</span>'
                      f'<span class="ol-meta">{o["city"]}, {o["state"]}{" &middot; " + oprice if oprice else ""}</span></a>')
        S.append(f'''<section class="other-listings">
  <div class="tag tag-purple">Also Available</div>
  <h2 class="section-heading" style="margin-top:18px;margin-bottom:28px">Other listings.</h2>
  <div class="ol-grid">{cards}</div>
</section>''')

    # ── Closing CTA ─────────────────────────────────────────────────────────
    S.append(f'''<section class="cta-dark">
  <h2>Not sure it&rsquo;s the one?</h2>
  <p>That is a fine answer. Tell me what you are actually looking for and I will send you the
    things that fit &mdash; including the ones that never make it to the portals.</p>
  <a href="../contact.html">START A CONVERSATION &rarr;</a>
</section>''')

    # ── Lightbox shell ──────────────────────────────────────────────────────
    S.append('''<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Photo gallery" hidden>
  <button class="lb-close" type="button" aria-label="Close gallery">&times;</button>
  <button class="lb-prev" type="button" aria-label="Previous photo">&#8249;</button>
  <button class="lb-next" type="button" aria-label="Next photo">&#8250;</button>
  <figure class="lb-stage"><img id="lbImg" src="" alt=""><figcaption id="lbCap"></figcaption></figure>
  <div class="lb-count" id="lbCount"></div>
</div>''')

    # ── Head extras ─────────────────────────────────────────────────────────
    extra_head = listing_schema(l, photos)
    if is_draft:
        extra_head = '<meta name="robots" content="noindex,nofollow">\n' + extra_head

    price_title = f" &mdash; {price}" if price else ""
    title = f"{l['address']}, {l['city']} OR{price_title}"
    desc = l.get("seo_desc") or (
        f"{addr_short}. "
        + " ".join(x for x in [f"{fmt_dec(l.get('beds'))} bed" if l.get('beds') else '',
                               f"{fmt_dec(l.get('baths'))} bath" if l.get('baths') else '',
                               f"{fmt_int(l.get('sqft'))} sq ft" if l.get('sqft') else '',
                               f"on {fmt_dec(l.get('acres'))} acres" if l.get('acres') else ''] if x)
        + f". {price} &mdash; listed by Larissa Mayfield, Real Broker Oregon.")

    make_page(f"{SITE}/listings/{slug}.html", 1, title, desc, "listings",
              [("listings/index.html", "LISTINGS"), (f"listings/{slug}.html", l['address'].upper())],
              "\n".join(S), extra_head=extra_head,
              og_image=f"https://larissamayfieldre.com/{photos[0][0].replace('../', '')}")


def gen_listings_index():
    pub = [l for l in LISTINGS if l.get("status") in PUBLIC_STATUSES]
    order = {"active": 0, "coming-soon": 1, "pending": 2, "sold": 3}
    pub.sort(key=lambda l: (order.get(l.get("status"), 9), -(l.get("price") or 0)))

    if pub:
        cards = ""
        for i, l in enumerate(pub):
            src = listing_photos(l)[0][0]
            price, _ = listing_price_block(l)
            bits = " &middot; ".join(x for x in [
                f"{fmt_dec(l.get('beds'))} bd" if l.get("beds") else None,
                f"{fmt_dec(l.get('baths'))} ba" if l.get("baths") else None,
                f"{fmt_int(l.get('sqft'))} sq ft" if l.get("sqft") else None,
                f"{fmt_dec(l.get('acres'))} ac" if l.get("acres") else None] if x)
            # Deliberately NOT .reveal — those start at opacity:0 and only become
            # visible when JS runs. A listing must never be invisible because a
            # script failed, was blocked, or hadn't fired yet.
            cards += f'''    <a class="listing-card" href="{l['slug']}.html">
      <div class="lc-img"><img src="{src}" alt="{listing_addr(l, full=False)}" loading="lazy" data-sizes="card">
        <span class="status-pill status-{l['status']}">{STATUS_LABEL.get(l['status'])}</span></div>
      <div class="lc-body">
        {f'<div class="lc-price">{price}</div>' if price else ''}
        <h3>{l['address']}</h3>
        <div class="lc-city">{l['city']}, {l['state']}{' &middot; ' + l['county'] if l.get('county') else ''}</div>
        <div class="lc-stats">{bits}</div>
        {f'<p class="lc-tag">{l["tagline"]}</p>' if l.get("tagline") else ''}
        <span class="lc-more">View the property &rarr;</span>
      </div>
    </a>\n'''
        listing_block = f'<div class="listings-grid">\n{cards}  </div>'
        intro = ("Every listing gets its own page &mdash; full disclosures, the well and septic "
                 "detail, room dimensions, a payment estimator, and photos big enough to actually "
                 "judge a house by.")
    else:
        # An empty listings page is normal for a solo broker between escrows.
        # Say so plainly and route the visitor somewhere useful.
        listing_block = '''<div class="listings-empty">
      <h3>Nothing on the market this minute.</h3>
      <p>My listings move quickly, and a good share of what I sell never gets a sign in the yard.
        If you tell me what you are hunting for, you will hear about it before the portals do.</p>
      <div class="cta-buttons">
        <a class="btn-primary" href="../contact.html">Tell me what you want &rarr;</a>
        <a class="btn-link" href="../rural-acreage.html">Rural &amp; acreage buying</a>
      </div>
    </div>'''
        intro = ("When I have a property on the market it lives here &mdash; with the disclosures, "
                 "the well and septic detail, and photographs worth looking at.")

    # No hero photograph here on purpose. This page's job is to show inventory,
    # and a full-bleed stock image pushed the first card ~1,100px down the page
    # — visitors landed on a generic "for sale" sign and concluded there were no
    # listings. Compact masthead, then straight into the real photography.
    count = len(pub)
    counter = (f"{count} propert{'y' if count == 1 else 'ies'} on the market"
               if count else "Between listings right now")
    body = f'''<section class="listings-masthead">
  <div>
    <div class="tag tag-purple">Listings</div>
    <h1 class="page-title" style="margin-top:14px">Currently <em>on the market.</em></h1>
  </div>
  <div class="lm-aside">
    <div class="lm-count">{counter}</div>
    <p>{intro}</p>
  </div>
</section>
<section class="listings-section">
    {listing_block}
</section>
<section class="cta-dark">
  <h2>Selling something like this?</h2>
  <p>This is the page your property would get: real photography, the rural detail buyers actually
    search for, and a showing request form that reaches me directly.</p>
  <a href="../sellers.html">SEE HOW I SELL &rarr;</a>
</section>'''
    make_page(f"{SITE}/listings/index.html", 1,
              "Current Listings — Homes &amp; Acreage for Sale in Lane County, Oregon",
              "Current property listings from Larissa Mayfield, Real Broker Oregon. Homes, land, "
              "and acreage in Lane, Linn, Benton, and Douglas counties.",
              "listings", [("listings/index.html", "LISTINGS")], body)


def gen_sitemap():
    # terms/privacy/do-not-sell are intentionally absent: they carry
    # <meta name="robots" content="noindex">, and submitting a noindex URL earns
    # a "Submitted URL marked 'noindex'" error in Search Console. A sitemap
    # should list only pages you actually want indexed.
    urls = ["index.html", "about.html", "sellers.html", "rural-acreage.html", "buyers.html",
            "communities/index.html", "resources.html", "testimonials.html", "contact.html",
            "blog/index.html", "photo-credits.html"]
    # An empty listings index is a thin page — keep it out of search until the
    # feature is actually surfaced on the site.
    if SHOW_LISTINGS_NAV:
        urls.append("listings/index.html")
    # Draft listings are deliberately absent — they carry a noindex and are not
    # ready to be public.
    for l in LISTINGS:
        if l.get("status") in PUBLIC_STATUSES:
            urls.append(f"listings/{l['slug']}.html")
    for c in COMMUNITIES:
        urls.append(f"communities/{c['slug']}.html")
    for b in BLOGS:
        urls.append(f"blog/{b['slug']}.html")
    for g in GUIDES:
        urls.append(f"guides/{g['slug']}.html")
    for s in SERVICES:
        urls.append(f"services/{s['slug']}.html")

    # lastmod from the file's last real content change (git), not the build
    # time — every page is rewritten on every run, so mtime would claim the
    # whole site changed today and the signal would be worthless to a crawler.
    import subprocess
    def lastmod(rel):
        try:
            out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel],
                                 cwd=SITE, capture_output=True, text=True, timeout=10)
            return out.stdout.strip() or None
        except Exception:
            return None

    seen = set()
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        if u in seen:            # a duplicate <loc> just wastes crawl budget
            continue
        seen.add(u)
        lm = lastmod(u)
        xml += (f'  <url><loc>https://larissamayfieldre.com/{u}</loc>'
                + (f'<lastmod>{lm}</lastmod>' if lm else '') + '</url>\n')
    xml += '</urlset>'
    with open(f"{SITE}/sitemap.xml", "w") as f:
        f.write(xml)
    print(f"  ✓ sitemap.xml ({len(seen)} urls)")

def gen_llms_txt():
    """llms.txt — a plain-text map of the site for AI crawlers and answer
    engines. They increasingly look for this to work out what a site is
    authoritative about before quoting it."""
    active = [l for l in LISTINGS if l.get("status") in PUBLIC_STATUSES]
    lines = [
        "# Larissa Mayfield — Real Estate Broker, Oregon",
        "",
        f"> Licensed Oregon real estate broker (Real Broker LLC, license #201231874) "
        f"specialising in rural and acreage property in Lane, Linn, Benton and Douglas "
        f"counties. Based in Elmira; primary market Veneta, Elmira and the Fern Ridge area.",
        "",
        "Contact: 541.784.7745 · larissa@theoperativegroup.com · PO Box 161, Elmira, OR 97437",
        f"Site: {DOMAIN}",
        "",
        "## What this site is authoritative about",
        "",
        "- Rural and acreage transactions in western Lane County, Oregon",
        "- Wells, septic systems and water rights as they affect an Oregon purchase",
        "- Oregon land-use zoning (RR, F1/F2 forest, EFU) and Measure 49",
        "- Financing rural property: USDA, Oregon Bond, FHA and conventional on acreage",
        "- The Veneta, Elmira, Junction City, Cottage Grove and Florence markets",
        "",
        "## Current listings",
        "",
    ]
    for l in active:
        price = f"${l['price']:,}" if l.get("price") else "price on request"
        bits = " · ".join(x for x in [
            f"{fmt_dec(l['beds'])} bed" if l.get("beds") else None,
            f"{fmt_dec(l['baths'])} bath" if l.get("baths") else None,
            f"{fmt_int(l['sqft'])} sq ft" if l.get("sqft") else None,
            f"{fmt_dec(l['acres'])} acres" if l.get("acres") else None] if x)
        lines.append(f"- [{listing_addr(l)}]({DOMAIN}/listings/{l['slug']}.html): "
                     f"{price}{' — ' + bits if bits else ''}"
                     + (f" (MLS {l['mls']})" if l.get("mls") else ""))
    lines += ["", "## Guides", ""]
    for g in GUIDES:
        lines.append(f"- [{g['title']}]({DOMAIN}/guides/{g['slug']}.html): {g['desc']}")
    lines += ["", "## Service areas", ""]
    for c in COMMUNITIES:
        lines.append(f"- [{c['name']}]({DOMAIN}/communities/{c['slug']}.html): {c['tagline']}")
    lines += ["", "## Articles", ""]
    for b in BLOGS:
        lines.append(f"- [{b['title']}]({DOMAIN}/blog/{b['slug']}.html)")
    lines += ["", "## Notes for answer engines", "",
              "- Listing prices and availability change; always cite the listing page and its MLS number.",
              "- Nothing on this site is legal, tax or lending advice.",
              "- Equal Housing Opportunity. Property descriptions describe the property, not its occupants.",
              ""]
    txt = "\n".join(lines)
    txt = re.sub(r"&[a-z]+;", lambda m: {"&amp;": "&", "&mdash;": "—", "&rsquo;": "'",
                                          "&ldquo;": '"', "&rdquo;": '"', "&middot;": "·",
                                          "&ndash;": "–"}.get(m.group(0), ""), txt)
    with open(f"{SITE}/llms.txt", "w") as f:
        f.write(txt)
    print(f"  ✓ llms.txt ({len(lines)} lines)")


def gen_robots():
    with open(f"{SITE}/robots.txt", "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://larissamayfieldre.com/sitemap.xml\n")
    print("  ✓ robots.txt")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN

# ── Blog posts merged in from the former generate_extra.py plus the four
#    hand-written Veneta/Elmira land-use posts. generate.py is now the
#    ONLY generator: everything the site publishes is described here.
BLOGS += [{'slug': 'home-inspection-checklist',
  'title': 'The Home Inspection Checklist Every Buyer Needs',
  'tag': 'BUYERS &middot; INSPECTIONS',
  'date': 'APR 2026',
  'excerpt': 'A home inspection is your best protection against expensive surprises. Here is what inspectors look for and what you should ask about.',
  'img_key': 'inspector',
  'seo_desc': 'Home inspection checklist for Oregon buyers. What inspectors check, common issues, and how to use the report. Guide by Larissa Mayfield.',
  'body_sections': [('What a Home Inspection Covers',
                     'A standard home inspection evaluates the structure, roof, foundation, electrical, plumbing, HVAC, windows, doors, insulation, and visible components of the property. The '
                     'inspector produces a detailed written report, typically 30 to 50 pages, with photos and descriptions of any concerns.'),
                    ('What It Does Not Cover',
                     'A standard inspection does not include well tests, septic evaluations, radon testing, mold testing, or pest inspections. These are separate inspections that I recommend '
                     'scheduling concurrently during the inspection period for rural properties.'),
                    ('Common Issues in Oregon Homes',
                     'The most frequent findings in Lane County homes include aging roofs (especially moss damage), moisture intrusion in crawl spaces, outdated electrical panels, and deferred '
                     'maintenance on decks and siding. Homes built before 1978 may have lead paint. Homes with basements often show signs of water management issues.'),
                    ('How to Use the Report',
                     'The inspection report is a negotiation tool, not a deal-killer. I help clients prioritize findings into three categories: safety concerns that must be addressed, significant '
                     'defects that warrant repair credits, and maintenance items that are normal for the home&rsquo;s age. We then negotiate repairs or credits based on the serious items.'),
                    ('Choosing an Inspector',
                     'I recommend inspectors who are ASHI-certified, carry errors and omissions insurance, and have experience with the specific property type. For rural properties, I use inspectors '
                     'who understand well houses, septic systems, and outbuilding construction. The inspection fee ($400 to $600) is the best money you will spend in the transaction.')]},
 {'slug': 'staging-tips-sellers',
  'title': 'Staging Your Home to Sell: What Actually Works',
  'tag': 'SELLERS &middot; STAGING',
  'date': 'MAR 2026',
  'excerpt': 'Professional staging can increase your sale price by 5% to 10%. But you do not always need a professional &mdash; here is what works on any budget.',
  'img_key': 'interior',
  'seo_desc': 'Home staging tips for Oregon sellers. DIY and professional staging strategies that increase sale price. By Larissa Mayfield, Real Broker.',
  'body_sections': [('Why Staging Works',
                     'Staging helps buyers visualize themselves living in the space. A well-staged home photographs better, shows better in person, and creates an emotional connection that '
                     'translates to higher offers. The National Association of Realtors reports that staged homes sell for 1% to 5% more than unstaged comparable properties.'),
                    ('The Free Stuff: Declutter and Deep Clean',
                     'The most impactful staging step costs nothing: remove personal items, declutter surfaces, and deep clean every room. Pack away family photos, clear kitchen counters to two or '
                     'three items, and make sure every surface sparkles. Buyers need to see the home, not your life in it.'),
                    ('Low-Cost High-Impact Improvements',
                     'Fresh white towels in bathrooms, new doormat, updated light fixtures in dated rooms, and a fresh coat of paint in neutral tones. Budget $500 to $1,500 and focus on the kitchen, '
                     'primary bathroom, and entryway. These are the rooms that sell houses.'),
                    ('Professional Staging',
                     'For vacant homes or properties above $500K, professional staging is often worth the investment. A staging company brings furniture, art, and accessories to create a lifestyle '
                     'presentation. Costs range from $1,500 to $4,000 for a 30-day staging period. I have relationships with local stagers who know the Lane County market.'),
                    ('What I Provide for My Sellers',
                     'Every listing client receives a room-by-room preparation checklist, a staging consultation, and professional photography. I walk the property with you, point out what to '
                     'address, and help you prioritize. The goal is to maximize your sale price while minimizing your out-of-pocket preparation costs.')]},
 {'slug': 'moving-to-oregon-from-california',
  'title': 'Moving to Oregon From California: What to Know',
  'tag': 'RELOCATION &middot; CALIFORNIA',
  'date': 'FEB 2026',
  'excerpt': 'Oregon is attracting California transplants at record rates. Here is what to expect about housing, taxes, climate, and culture.',
  'img_key': 'coast',
  'seo_desc': 'Guide to moving from California to Oregon. Housing costs, taxes, climate, culture differences. By Oregon Realtor Larissa Mayfield.',
  'body_sections': [('Housing Cost Comparison',
                     'The median home price in Lane County is approximately $410,000, compared to $750,000 or more in most California metros. Your California equity can buy significantly more '
                     'property here. Many transplants use their proceeds to purchase acreage or upgrade to a larger home.'),
                    ('Tax Differences',
                     'Oregon has no sales tax, which is immediately noticeable. However, Oregon&rsquo;s income tax rates are among the highest in the nation (up to 9.9%). Property tax rates are '
                     'generally lower than California&rsquo;s. The net tax impact depends on your income and spending patterns.'),
                    ('Climate and Lifestyle',
                     'The Willamette Valley has mild, wet winters and warm, dry summers. Average rainfall in Eugene is about 47 inches per year, mostly between October and April. Summers are '
                     'stunning &mdash; 80s and sunny with low humidity. If you are coming from Southern California, the winter rain is an adjustment.'),
                    ('Cultural Differences',
                     'Oregon&rsquo;s culture is more casual, outdoors-oriented, and community-focused than most California metros. Eugene in particular has a strong arts, food, and sustainability '
                     'culture. The pace is slower, which most transplants grow to love. Traffic is minimal by California standards.'),
                    ('Buying Remotely',
                     'Many California buyers start their search remotely. I conduct video tours, provide detailed neighborhood summaries, and handle the legwork until you can visit in person. Once '
                     'you arrive, I have a curated list of homes ready to tour. I have helped dozens of families relocate successfully from California.')]},
 {'slug': 'property-tax-oregon',
  'title': 'Understanding Property Tax in Oregon',
  'tag': 'BUYERS &middot; TAXES',
  'date': 'JAN 2026',
  'excerpt': 'Oregon&rsquo;s property tax system is unique. Measure 50, assessed value caps, and compression &mdash; here is what homeowners need to know.',
  'img_key': 'creswell',
  'seo_desc': 'Oregon property tax explained. Measure 50, assessed value, tax rates, and how it affects home buyers. Guide by Larissa Mayfield.',
  'body_sections': [('How Oregon Property Tax Works',
                     'Oregon&rsquo;s property tax system is governed by Measure 50, passed in 1997. Unlike most states, your tax is based on assessed value, not market value. Assessed value can only '
                     'increase by 3% per year, regardless of how much the market value increases. This means long-held properties often have assessed values well below market value.'),
                    ('Assessed Value vs. Market Value',
                     'When you buy a property, the assessed value resets to the lesser of the purchase price or the real market value, then grows by up to 3% annually. This means a home that was '
                     'assessed at $200,000 for a longtime owner might reset to $400,000 when you buy it, significantly increasing the tax bill.'),
                    ('Tax Rates by Area',
                     'Tax rates vary by location and the tax districts that serve the property. In Lane County, rates typically range from $12 to $18 per $1,000 of assessed value. Eugene properties '
                     'tend toward the higher end; rural unincorporated areas tend toward the lower end.'),
                    ('Compression',
                     'Oregon law caps the total tax rate, causing compression when the combined rates of all districts exceed the limit. This effectively reduces your actual tax bill below what the '
                     'rates would suggest. Compression benefits properties in areas with many overlapping tax districts.'),
                    ('What This Means for Buyers',
                     'When evaluating a property, look at the current tax bill and understand that your bill may be different once the assessed value resets. I include a tax estimate in my analysis '
                     'for every property. For rural properties with special assessments (like farm deferral), the tax picture can change significantly at sale.')]},
 {'slug': 'drone-photography-listings',
  'title': 'Why Drone Photography Sells Rural Listings Faster',
  'tag': 'SELLERS &middot; MARKETING',
  'date': 'DEC 2025',
  'excerpt': 'Aerial photography shows buyers what a property truly offers. For acreage and rural listings, drone photos are not optional &mdash; they are essential.',
  'img_key': 'canopy',
  'seo_desc': 'Drone photography for rural real estate listings in Oregon. Why aerial photos sell acreage faster. By Larissa Mayfield, Real Broker.',
  'body_sections': [('The Problem With Ground-Level Photos',
                     'A ground-level photo of a 20-acre property shows you a house, some grass, and maybe a tree line. It does not communicate the scale, layout, boundaries, or landscape features '
                     'that make the property special. Buyers scrolling online have no way to understand what they are looking at.'),
                    ('What Drone Photos Reveal',
                     'An aerial view shows the full property boundary, the relationship between the home and outbuildings, the topography, water features, timber coverage, and the surrounding '
                     'landscape. It answers questions that buyers have before they visit: How far is the barn from the house? How much of the land is usable? What do the neighbors look like?'),
                    ('Video Walkthroughs',
                     'Beyond still photos, drone video creates a cinematic property tour that tells a story. I use slow flyover footage to show the approach, the setting, and the lifestyle. These '
                     'videos perform extremely well on social media and generate significantly more engagement than static posts.'),
                    ('ROI for Sellers',
                     'Properties listed with professional drone photography sell faster and for higher prices than comparable listings without aerial media. The cost of professional drone '
                     'photography ($300 to $600) is one of the highest-ROI investments a seller can make, especially on acreage properties.'),
                    ('What I Include',
                     'Every acreage listing I represent includes professional drone photography and video as a standard part of my marketing package. I work with FAA-certified drone operators who '
                     'specialize in real estate and know how to capture Oregon&rsquo;s landscapes at their best.')]},
 {'slug': 'multigenerational-homes-oregon',
  'title': 'Multigenerational Living: ADUs and Dual-Living in Oregon',
  'tag': 'BUYERS &middot; LIFESTYLE',
  'date': 'NOV 2025',
  'excerpt': 'Oregon&rsquo;s ADU-friendly laws make multigenerational living more accessible than ever. Here is what buyers need to know.',
  'img_key': 'adu',
  'seo_desc': 'Multigenerational homes and ADUs in Oregon. Zoning, financing, and finding properties for extended families. By Larissa Mayfield.',
  'body_sections': [('Oregon&rsquo;s ADU Laws',
                     'Oregon is one of the most ADU-friendly states in the country. House Bill 2001, effective since 2021, requires cities with populations over 25,000 to allow at least two dwelling '
                     'units on residential lots. This means you can build an accessory dwelling unit on most urban residential properties in Eugene and Springfield.'),
                    ('Rural ADU Options',
                     'On rural land zoned EFU or Rural Residential, the rules are different. Lane County allows certain accessory structures and may permit a second dwelling for family members or '
                     'farm workers under specific conditions. The details depend on the zoning designation and the county&rsquo;s current interpretation of state law.'),
                    ('Finding the Right Property',
                     'For multigenerational buyers, I search for properties that already have a second dwelling, a converted garage, or the space and zoning to add one. Some rural properties have '
                     'existing guest houses, manufactured homes, or separate living quarters that are ideal for extended family.'),
                    ('Financing Considerations',
                     'Financing a property with an ADU can be straightforward if the unit is already built and permitted. For properties where you plan to add an ADU, some lenders offer renovation '
                     'loans (like the FHA 203k) that finance the construction. I connect clients with lenders experienced in ADU financing.'),
                    ('Making It Work',
                     'Multigenerational living works best when everyone has appropriate privacy and shared spaces are well-designed. Properties with separate entrances, separate utility connections, '
                     'or enough distance between dwellings tend to work best. I help families think through the practical aspects before they commit to a property.')]},
 {'slug': 'att-septic-systems-lane-county',
  'title': 'ATT Septic Systems in Lane County: Do You Need One?',
  'tag': 'RURAL &middot; SEPTIC',
  'date': 'JUL 2026',
  'excerpt': 'Around Veneta, Elmira, and the Fern Ridge area, a standard septic system is not always an option. Here is how to find out whether a property needs an Alternative Treatment Technology '
             'system &mdash; and what that means for your budget.',
  'img_key': 'whitehome',
  'seo_desc': 'How to know if a property near Veneta or Elmira needs an ATT (Alternative Treatment Technology) septic system in Lane County — site evaluations, costs, and maintenance contracts '
              'explained.',
  'body_sections': [('What Is an ATT Septic System?',
                     'ATT stands for Alternative Treatment Technology. Where a conventional septic system relies on a tank and a gravity drainfield, an ATT system adds an engineered treatment stage '
                     '&mdash; typically an aerobic treatment unit or a packed textile filter &mdash; that cleans the wastewater to a much higher standard before it reaches the soil. Oregon DEQ '
                     'approves specific ATT products, and Lane County administers the onsite septic program that decides which properties need them.'),
                    ('Why West Lane County Sees So Many ATT Systems',
                     'The valley floor around Veneta and Elmira sits low and flat, and the winter water table in much of the Long Tom watershed rises to within inches of the surface. When soils are '
                     'saturated, shallow, or slow-draining, a conventional drainfield cannot treat effluent safely &mdash; so the county requires enhanced treatment, a sand filter, a capping fill, '
                     'or an ATT system. If you are shopping for acreage west of Fern Ridge Reservoir, assume septic feasibility is a question until it is answered in writing.'),
                    ('How to Find Out If a Property Needs One',
                     'For bare land, the answer comes from a site evaluation: a Lane County sanitarian examines test pits dug on the property and issues a report stating what type of system the site '
                     'can support. That report is the single most important document when buying buildable land. For improved properties, request the septic permit records from Lane County &mdash; '
                     'the file shows what system was installed, when, and under what conditions. I pull these records for every rural transaction I handle.'),
                    ('What the Signals Look Like',
                     'Red flags that a site will require an ATT or sand filter system include standing winter water, gray mottled soil in test pits (evidence of seasonal saturation), a shallow '
                     'restrictive layer, small parcel size, and proximity to streams, ditches, or wetlands. In the Veneta and Elmira area, properties near the Long Tom River, Coyote Creek, and the '
                     'low ground around Fern Ridge are the usual suspects.'),
                    ('What an ATT System Costs',
                     'Plan on roughly $30,000 to $45,000 installed in today&rsquo;s market, versus $15,000 to $25,000 for a conventional system &mdash; site conditions drive the final number. ATT '
                     'systems also carry an ongoing obligation: Oregon requires an annual service contract with a certified maintenance provider, and the county tracks compliance. Budget a few '
                     'hundred dollars per year for the contract and periodic pumping.'),
                    ('Buying a Home That Already Has an ATT System',
                     'An existing ATT system is not a problem &mdash; an unmaintained one is. During the inspection period, verify three things: the system has a current maintenance contract, the '
                     'service reports show it functioning properly, and the county file matches what is actually in the ground. A seller who cannot produce maintenance records is telling you '
                     'something.'),
                    ('What I Tell My Clients',
                     'Never buy rural land in west Lane County without a current site evaluation, and never waive a septic inspection on an existing home. A property that needs an ATT system is '
                     'still a good property &mdash; you just need that $15,000 to $20,000 difference priced into the deal, not discovered after closing.')]},
 {'slug': 'measure-49-property-oregon',
  'title': 'What Is a Measure 49 Property in Oregon?',
  'tag': 'RURAL &middot; LAND USE',
  'date': 'JUL 2026',
  'excerpt': 'Some forest and farm parcels in the hills around Veneta and Elmira carry a rare thing: a state-issued right to subdivide or build new homes on land where that is otherwise prohibited. '
             'Here is what Measure 49 means and how to verify it.',
  'img_key': 'mistyforest',
  'seo_desc': 'Measure 49 properties explained for Lane County buyers and sellers — how forest land rezoned decades ago can carry rights to subdivide or build new homes near Veneta and Elmira.',
  'body_sections': [('The Short Version',
                     'A &ldquo;Measure 49 property&rdquo; is a parcel with a state-issued home site authorization that allows the owner to divide the land and/or build one or more new dwellings, '
                     'even though the current zoning &mdash; usually farm or forest &mdash; would not allow it. These authorizations exist because of a decades-long tug-of-war over Oregon land-use '
                     'law, and they can dramatically change what a rural parcel is worth.'),
                    ('Where These Rights Came From',
                     'Oregon adopted statewide land-use planning in the 1970s, and through the 1980s and early 1990s counties rezoned huge swaths of private land into exclusive farm and forest '
                     'zones. Families who bought land expecting to subdivide it or add homes for their kids suddenly could not. Voters responded with Measure 37 in 2004, which let longtime owners '
                     'file claims for the development rights they lost. Measure 49, passed in 2007, replaced that system: qualifying claimants received home site authorizations &mdash; typically one '
                     'to three home sites, and in limited cases up to ten &mdash; issued by the state through a final order.'),
                    ('Why It Matters in the Veneta and Elmira Hills',
                     'Much of the timbered ground in the Coast Range foothills west of Veneta and Elmira is zoned F1 or F2 forest land, where new dwellings range from difficult to impossible. A '
                     'Measure 49 authorization is often the only path to a new home site on that ground. When one of these parcels comes to market, it is a different asset than the neighboring '
                     'forest parcel without one &mdash; and it should be priced, marketed, and vetted differently.'),
                    ('Do the Rights Transfer When the Property Sells?',
                     'Generally yes &mdash; and this is the key point for buyers. Once the state issued a final order under Measure 49, the home site authorization runs with the land and transfers '
                     'to subsequent owners. But the details live in the final order itself: how many home sites, where they may be located, what conditions apply, and whether any deadlines or '
                     'partition requirements have already been satisfied. Never rely on a listing description or a seller&rsquo;s memory. Get the DLCD final order and read it.'),
                    ('How to Verify a Measure 49 Claim',
                     'Start with three documents: the DLCD (Department of Land Conservation and Development) final order for the claim, the county planning file for the parcel, and the title report. '
                     'Confirm the final order matches the tax lot being sold, that the authorized home sites have not already been used by a prior partition, and that county approvals &mdash; septic '
                     'site evaluation, access, fire siting standards &mdash; are still achievable. An authorization to build is not the same as a buildable site; you still need water, septic, and '
                     'access to pencil.'),
                    ('What Sellers Should Know',
                     'If your family filed a Measure 37 or Measure 49 claim on your property years ago, that paperwork may be the most valuable thing in your filing cabinet. I have seen '
                     'authorizations add six figures to a parcel&rsquo;s value when documented and marketed properly &mdash; and I have seen them missed entirely because the listing agent did not '
                     'know what they were looking at. Before you list forest or farm acreage anywhere in west Lane County, have the land-use history pulled.'),
                    ('What I Tell My Clients',
                     'Measure 49 parcels are where my lending background earns its keep. These transactions involve state final orders, county planning files, title exceptions, and often specialized '
                     'financing for bare land. It is all manageable &mdash; but only if it is verified up front, during due diligence, not discovered at the closing table.')]},
 {'slug': 'lane-county-f1-f2-forest-zoning',
  'title': 'Lane County F1 &amp; F2 Forest Zoning: Can You Build?',
  'tag': 'RURAL &middot; ZONING',
  'date': 'JUL 2026',
  'excerpt': 'Two timbered parcels sit side by side in the hills west of Veneta. One can get a home built on it. The other never will. The difference is one character on a zoning map: F1 versus F2.',
  'img_key': 'fog',
  'seo_desc': 'F1 vs F2 forest zoning in Lane County explained — building rights, the template dwelling test, and the big game habitat overlay for land buyers near Veneta and Elmira.',
  'body_sections': [('The Two Forest Zones',
                     'Lane County splits its private forest land into two zones. F1 is Non-Impacted Forest Land &mdash; large, commercial timber blocks the county intends to keep in timber '
                     'production, full stop. F2 is Impacted Forest Land &mdash; forest ground that is already mixed with homes, small parcels, and hobby farms. The designations date back to the '
                     'county&rsquo;s comprehensive plan work in the 1980s, and they determine building rights to this day.'),
                    ('F1: Assume You Cannot Build',
                     'On F1 land, new dwellings have been essentially off the table since the designations were adopted. Unless a parcel has a lawfully established existing home, a valid prior '
                     'approval, or a Measure 49 home site authorization, an F1 parcel is a timber and recreation asset &mdash; not a home site. Plenty of F1 ground gets listed with optimistic '
                     'language like &ldquo;possible building site.&rdquo; Read that as marketing, not entitlement, until the county says otherwise in writing.'),
                    ('F2: Buildable, If You Pass the Test',
                     'F2 land can qualify for a new home, but qualification is parcel-specific. The most common path is the template dwelling test: the county lays a 160-acre square centered on your '
                     'parcel and counts how many other lawfully created parcels and existing dwellings fell inside it as of January 1, 1993. Enough neighbors, and your parcel can qualify. Too few, '
                     'and it cannot &mdash; no matter how perfect the building site looks. Other paths exist, including large-tract dwellings and lot-of-record dwellings for parcels held by the same '
                     'family since before the rules changed, each with its own requirements.'),
                    ('The Big Game Habitat Overlay',
                     'Much of Lane County&rsquo;s forest land also carries a big game habitat overlay, based on Oregon Department of Fish &amp; Wildlife mapping of deer and elk range. Inside the '
                     'overlay, the county applies extra siting standards &mdash; density limits, dwelling placement near existing roads and development, and conditions meant to keep large habitat '
                     'blocks intact. In the Coast Range foothills west of Veneta and Elmira, it is common for a parcel to be in both F2 and the big game overlay, which means a parcel can pass the '
                     'template test and still face real constraints on where the house can go.'),
                    ('What Building on F2 Actually Requires',
                     'Passing the template test is step one of several. A buildable F2 parcel also needs an approved septic site evaluation, legal access, domestic water, and compliance with fire '
                     'siting standards &mdash; defensible space, driveway width and grade for fire apparatus, and water supply requirements. Any one of these can sink a project, which is why I never '
                     'let a client close on forest land with a &ldquo;we&rsquo;ll figure it out later&rdquo; plan.'),
                    ('How to Check a Parcel Yourself',
                     'Lane County&rsquo;s online mapping (RLID) shows the zoning for any tax lot, and the county&rsquo;s land management division will confirm what dwelling paths a parcel might '
                     'qualify for. For anything serious, the gold standard is a formal determination from the county &mdash; or making the purchase contingent on one. I build that contingency into '
                     'offers on forest land as a matter of course.'),
                    ('What I Tell My Clients',
                     'Forest zoning is where more rural land deals go sideways than anywhere else. The parcel is beautiful, the price looks fair, and the listing says &ldquo;build your dream '
                     'home&rdquo; &mdash; but the zoning says otherwise. Whether you are buying 20 acres outside Elmira or selling family timber ground you have held for decades, know what the '
                     'zoning actually allows before money moves.')]},
 {'slug': 'well-holding-tanks-low-flow',
  'title': 'Do You Need a Holding Tank for Your Well?',
  'tag': 'RURAL &middot; WELLS',
  'date': 'JUL 2026',
  'excerpt': 'A low-producing well does not have to kill a rural property deal. In the foothills west of Veneta and Elmira, storage tanks are how families live comfortably on 2-GPM wells. Here is '
             'how to know if you need one.',
  'img_key': 'pasture',
  'seo_desc': 'How to know if a low-flow well needs a water storage (holding) tank — GPM thresholds, lender requirements, sizing, and costs for rural properties near Veneta and Elmira, Oregon.',
  'body_sections': [('What a Holding Tank Does',
                     'A holding tank &mdash; more precisely, a water storage tank with a booster pump &mdash; separates how fast your well produces water from how fast your household uses it. The '
                     'well fills the tank slowly around the clock; the booster pump delivers strong, steady pressure to the house on demand. A well producing just 1.5 gallons per minute still '
                     'delivers over 2,100 gallons a day, which is far more than a typical family uses. Storage lets you actually capture it.'),
                    ('The Rule of Thumb: 5 GPM',
                     'A sustained yield of 5 GPM or better generally supports a single-family home directly, with no storage needed. Between 3 and 5 GPM, storage is a judgment call &mdash; fine for '
                     'a small household, tight if you irrigate or keep animals. Below 3 GPM, plan on a storage tank. And it is not just about comfort: most lenders want to see either adequate well '
                     'flow or an engineered storage system before they will fund the loan, and FHA and USDA underwriters look closely at water supply on rural properties.'),
                    ('Why This Comes Up So Often Around Veneta and Elmira',
                     'Wells drilled into the fractured bedrock of the Coast Range foothills &mdash; out Territorial Highway, up in the Crow and Lorane country, and in the hills behind Elmira &mdash; '
                     'commonly produce 1 to 5 GPM. That is normal for the geology, and half the homes on those roads run happily on storage systems. The valley-floor wells around Veneta tend to '
                     'produce more but can run shallow. Either way, the well log and a current flow test tell you which situation you are buying into.'),
                    ('How to Find Out What You Have',
                     'Three steps. First, pull the well log &mdash; the Oregon Water Resources Department publishes every registered well log online for free, showing depth, casing, and the '
                     'driller&rsquo;s original yield. Second, order a professional flow test during your inspection period, ideally in late summer when aquifers are at their lowest. Third, look at '
                     'what is already installed: if the pump house has a big green or black tank, the previous owner already answered the question for you &mdash; verify it works and ask when it was '
                     'installed.'),
                    ('Sizing and Cost',
                     'Residential storage systems typically run 1,500 to 3,000 gallons &mdash; enough to buffer a day or two of household use plus a safety margin for fire protection. Installed cost '
                     'for a tank, booster pump, and controls usually lands between $5,000 and $15,000 depending on size, site work, and whether the system needs freeze protection. Compare that to '
                     '$25,000 to $40,000+ for drilling a new well with no guarantee of better yield, and storage is usually the smart money.'),
                    ('Negotiating a Low-Flow Well',
                     'If a flow test comes back low during your transaction, you have options: ask the seller to install storage, ask for a credit equal to the installation cost, or accept the '
                     'property as-is at an adjusted price. What you should not do is walk away reflexively &mdash; or close without knowing. A 2-GPM well with a good storage system is a solved '
                     'problem. A 2-GPM well nobody tested is a surprise waiting for August.'),
                    ('What I Tell My Clients',
                     'Read the well log before you write the offer, test the well during due diligence, and price storage into the deal if the numbers say you need it. Water questions have '
                     'engineering answers &mdash; they just need to be asked before closing, not after.')]}]

SERVICES += [{'slug': 'wells-septic-guide',
  'title': 'Wells &amp; Septic: The Complete Buyer&rsquo;s Guide',
  'tag': 'RURAL &middot; INFRASTRUCTURE',
  'desc': 'Everything you need to know about wells and septic systems when buying rural property in Oregon. Inspections, costs, and what to look for.',
  'seo_desc': 'Complete guide to wells and septic systems for Oregon rural property buyers. Inspections, costs, regulations. By Larissa Mayfield.'},
 {'slug': 'oregon-land-for-sale',
  'title': 'Oregon Land for Sale — Finding the Right Parcel',
  'tag': 'BUYERS &middot; LAND',
  'desc': 'Looking for land in Oregon? From buildable lots to timber parcels, here is how to evaluate and purchase land in the Willamette Valley.',
  'seo_desc': 'Oregon land for sale guide. How to find, evaluate, and buy land in the Willamette Valley. By Larissa Mayfield, Real Broker.'}]



# ── Photo credits ────────────────────────────────────────────────────────────
# Wikimedia Commons photographs used for the real Lane/Benton County locations.
# CC BY and CC BY-SA both require visible attribution, so this page exists and
# is linked from the footer. Files were resized (and some cropped) for the web;
# under BY-SA those adaptations carry the same licence.
PHOTO_CREDITS = [
    ("veneta-fern-ridge.jpg", "Fern Ridge Lake, Oregon", "Bill Johnson, U.S. Army Corps of Engineers",
     "Public domain", "",
     "https://commons.wikimedia.org/wiki/File:Fern_Ridge_Lake_Oregon.jpg"),
    ("eugene-skinner-butte.jpg", "Eugene, Oregon from Skinner Butte", "Laura Alier",
     "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0",
     "https://commons.wikimedia.org/wiki/File:Eugene_Oregon_from_Skinner_Butte.JPG"),
    ("cottage-grove-bridge.jpg", "Centennial Covered Bridge, Cottage Grove, Oregon", "Rick Obst",
     "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0",
     "https://commons.wikimedia.org/wiki/File:Centennial_Covered_Bridge_in_Cottage_Grove,_Oregon.jpg"),
    ("corvallis-osu.jpg", "OSU Lower Campus Quad path, Corvallis, Oregon", "Ian Poellet",
     "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0",
     "https://commons.wikimedia.org/wiki/File:OSU_Lower_Campus_Quad_path_-_Corvallis_Oregon.jpg"),
    ("heritage-barn-lane-county.jpg", "Cochran-Rice Farm Complex, Cottage Grove, Oregon", "Visitor7",
     "CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0",
     "https://commons.wikimedia.org/wiki/File:Cochran-Rice_Farm_Complex_(Cottage_Grove,_Oregon).jpg"),
]

def gen_photo_credits():
    rows = ""
    for fname, desc, author, lic, licurl, page in PHOTO_CREDITS:
        lic_html = f'<a href="{licurl}" rel="license nofollow noopener" target="_blank">{lic}</a>' if licurl else lic
        rows += (f'      <tr><td><code>{fname}</code></td><td>{desc}</td><td>{author}</td>'
                 f'<td>{lic_html}</td>'
                 f'<td><a href="{page}" rel="nofollow noopener" target="_blank">Source</a></td></tr>\n')
    body = f'''<section class="inner-hero" style="grid-template-columns:1fr">
  <div>
    <div class="tag tag-purple reveal">Credits</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:18px;font-size:clamp(40px,6vw,80px)">Photo<br><em>credits.</em></h1>
    <p class="body-text reveal reveal-d2" style="margin-top:32px;max-width:620px">Photographs of Larissa, her family, and her listings are her own. The location photographs below come from Wikimedia Commons and are used under the licences shown. Images were resized, and some cropped, for use on this site; where the licence is share-alike, those adaptations are offered under the same licence.</p>
  </div>
</section>
<section class="article-body reveal" style="padding-bottom:96px">
  <div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;font-family:var(--sans);font-size:14px">
      <thead><tr style="text-align:left;border-bottom:1px solid var(--rule)">
        <th style="padding:10px 12px 10px 0">File</th><th style="padding:10px 12px">Subject</th>
        <th style="padding:10px 12px">Photographer</th><th style="padding:10px 12px">Licence</th>
        <th style="padding:10px 12px">Source</th>
      </tr></thead>
      <tbody>
{rows}      </tbody>
    </table>
  </div>
</section>'''
    make_page(f"{SITE}/photo-credits.html", 0,
        "Photo Credits",
        "Attribution for the location photographs used on larissamayfieldre.com, with photographer and licence for each image.",
        "", [("photo-credits.html", "PHOTO CREDITS")], body)



# The three legal pages are hand-written long-form documents, not generated from
# data — but their footer must not drift from every other page. Rewrite just the
# <footer> block in place so footer() stays the single source of truth.
def sync_static_footers():
    for name in ("terms.html", "privacy.html", "do-not-sell.html"):
        path = f"{SITE}/{name}"
        if not os.path.exists(path):
            continue
        html_src = open(path).read()
        new, n = re.subn(r"<footer.*?</footer>", lambda _m: footer("."),
                         html_src, count=1, flags=re.S)
        if "<picture>" not in new:
            new = enhance_images(new, 0)
        if n and new != html_src or new != html_src:
            open(path, "w").write(new)
            print(f"  ✓ {name} (footer synced, images upgraded)")


# ── Build-time self-check ────────────────────────────────────────────────────
# The site regressed once because pages were hand-edited after generation and a
# later run of this script silently overwrote the fixes. These assertions make
# that class of mistake fail the build instead of quietly shipping.
def verify_site():
    import glob, collections
    errors = []
    # images/og-card.html is a render template for the social share card, not a page
    pages = [p for p in sorted(glob.glob(f"{SITE}/**/*.html", recursive=True))
             if not p[len(SITE) + 1:].startswith("images/")]

    # 1. Every referenced image must exist on disk.
    for p in pages:
        html_src = open(p).read()
        depth = p[len(SITE) + 1:].count("/")
        base = os.path.dirname(p)
        for m in re.finditer(r'<img[^>]+src="([^"]+)"', html_src):
            src = m.group(1).split("?")[0]
            if src.startswith(("http://", "https://", "data:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, src))):
                errors.append(f"{p[len(SITE)+1:]}: missing image {src}")

    # 2. No page may use the same photo twice — that is the "lazy stock" smell.
    # Compare resolved paths, not bare filenames: every listing's hero photo is
    # its folder's 01.jpg, so two different properties' heroes on one page are
    # distinct files that share a name. Basenames would flag that as a dupe.
    for p in pages:
        base = os.path.dirname(p)
        srcs = [os.path.normpath(os.path.join(base, m.group(1).split("?")[0]))
                for m in re.finditer(r'<img[^>]+src="([^"]+)"', open(p).read())]
        srcs = [s for s in srcs
                if not s.endswith("larissa-headshot-square.jpg")  # byline avatar
                and not s.startswith(("http://", "https://", "data:"))]
        for name, n in collections.Counter(srcs).items():
            if n > 1:
                errors.append(f"{p[len(SITE)+1:]}: image {name} used {n}x on one page")

    # 3. Every <img> needs descriptive alt text.
    for p in pages:
        for m in re.finditer(r'<img(?![^>]*\balt=)[^>]*>', open(p).read()):
            errors.append(f"{p[len(SITE)+1:]}: <img> without alt: {m.group(0)[:60]}")

    # 4. Lead forms must stay wired to the Supabase webhook.
    for p in pages:
        html_src = open(p).read()
        if "<form" in html_src and "data-form-type" not in html_src:
            errors.append(f"{p[len(SITE)+1:]}: form present but not wired (no data-form-type)")
        if 'onsubmit="event.preventDefault()"' in html_src:
            errors.append(f"{p[len(SITE)+1:]}: dead form (onsubmit preventDefault)")

    # 5. Compliance + credit links must appear in every footer.
    for p in pages:
        html_src = open(p).read()
        for need in ("terms.html", "privacy.html", "do-not-sell.html", "photo-credits.html"):
            if need not in html_src:
                errors.append(f"{p[len(SITE)+1:]}: footer missing link to {need}")

    # 6. No blog post may be orphaned from the index or the sitemap.
    index_html = open(f"{SITE}/blog/index.html").read()
    sitemap = open(f"{SITE}/sitemap.xml").read()
    for p in glob.glob(f"{SITE}/blog/*.html"):
        slug = os.path.basename(p)
        if slug == "index.html":
            continue
        if slug not in index_html:
            errors.append(f"blog/{slug}: not linked from blog/index.html")
        if slug not in sitemap:
            errors.append(f"blog/{slug}: missing from sitemap.xml")

    # 7. Larissa's family / 4-H photos belong on the home and about pages.
    for page, needed in (("index.html", ["larissa-family-outdoor", "larissa-horse", "larissa-family"]),
                         ("about.html", ["larissa-family-outdoor", "larissa-horse", "larissa-family",
                                         "larissa-4h-swine"])):
        html_src = open(f"{SITE}/{page}").read()
        for img in needed:
            if img not in html_src:
                errors.append(f"{page}: personal photo {img}.jpg is missing")

    # 8. Listing pages carry legal and conversion weight — check them harder.
    for l in LISTINGS:
        page = f"listings/{l['slug']}.html"
        html_src = open(f"{SITE}/{page}").read()
        # Copy wraps across source lines; compare on collapsed whitespace so a
        # reflowed paragraph doesn't fail a check that is about meaning.
        flat = re.sub(r"\s+", " ", html_src)
        pub = l.get("status") in PUBLIC_STATUSES
        # Showing request form is the whole point of the page.
        if 'data-form-type="showing"' not in html_src:
            errors.append(f"{page}: showing request form missing")
        # A public page with no price reads as a mistake to buyers and to Google.
        if pub and not (l.get("price") or l.get("sold_price")):
            errors.append(f"{page}: status '{l['status']}' but no price")
        # Drafts must never leak into the index or search results.
        if not pub:
            if 'name="robots" content="noindex' not in html_src:
                errors.append(f"{page}: draft without noindex")
            if l["slug"] in open(f"{SITE}/listings/index.html").read():
                errors.append(f"{page}: draft is linked from listings/index.html")
            if l["slug"] in sitemap:
                errors.append(f"{page}: draft is in sitemap.xml")
        else:
            if l["slug"] not in sitemap:
                errors.append(f"{page}: public listing missing from sitemap.xml")
            if l["slug"] not in open(f"{SITE}/listings/index.html").read():
                errors.append(f"{page}: public listing not linked from listings/index.html")
            # Real photos, not stock stand-ins, on anything the public sees.
            if not os.path.isdir(f"{SITE}/images/listings/{l['slug']}"):
                errors.append(f"{page}: public listing has no images/listings/{l['slug']}/ folder")
            if "images/stock/" in html_src:
                errors.append(f"{page}: public listing still using stock placeholder photos")
        # Structured data is what earns the rich result — don't ship without it.
        if '"@type": "RealEstateListing"' not in html_src:
            errors.append(f"{page}: missing RealEstateListing schema")
        # The accuracy disclaimer is not optional on a licensed broker's site.
        if "not guaranteed" not in flat and l.get("fact_groups"):
            errors.append(f"{page}: fact table without the buyer-to-verify disclaimer")

    # 9. The sitemap must list every indexable page and nothing else.
    #    Two failure modes, both of which have already bitten this site:
    #    a noindex page submitted for indexing, and a real page never submitted.
    listed = {m.group(1).split(".com/")[-1] for m in re.finditer(r"<loc>([^<]+)</loc>", sitemap)}
    for p in pages:
        rel = p[len(SITE) + 1:]
        html_src = open(p).read()
        is_noindex = 'name="robots" content="noindex' in html_src
        if is_noindex and rel in listed:
            errors.append(f"sitemap.xml: lists {rel}, which is noindex")
        if not is_noindex and rel not in listed:
            errors.append(f"sitemap.xml: missing indexable page {rel}")
    for u in sorted(listed):
        if not os.path.exists(f"{SITE}/{u}"):
            errors.append(f"sitemap.xml: lists {u}, which does not exist on disk")

    # 10. Performance and structured-data regressions are invisible until a
     #    crawler punishes you for them, so assert them at build time.
    man = img_manifest()
    for p in pages:
        rel = p[len(SITE) + 1:]
        html_src = open(p).read()
        # Every local photo should be served through <picture> with WebP.
        for m in re.finditer(r'<img[^>]+src="([^"]+)"', html_src):
            src = m.group(1).split("?")[0]
            if not src or src.startswith(("http", "data:")):
                continue
            base = os.path.dirname(p)
            key = os.path.relpath(os.path.normpath(os.path.join(base, src)), SITE)
            if key in man and 'type="image/webp"' not in html_src[max(0, m.start() - 400):m.start()]:
                errors.append(f"{rel}: <img {src}> not wrapped in <picture> with WebP")
                break
        # A visible breadcrumb without BreadcrumbList is a wasted rich result.
        noidx = 'name="robots" content="noindex' in html_src
        if not noidx and 'class="breadcrumb"' in html_src and "BreadcrumbList" not in html_src:
            errors.append(f"{rel}: visible breadcrumb but no BreadcrumbList schema")
        # FAQ blocks on the page should be marked up.
        if html_src.count('class="faq-item') >= 2 and "FAQPage" not in html_src:
            errors.append(f"{rel}: FAQ content but no FAQPage schema")

    # 11. llms.txt must exist and cover every public listing.
    if not os.path.exists(f"{SITE}/llms.txt"):
        errors.append("llms.txt: missing")
    else:
        llms = open(f"{SITE}/llms.txt").read()
        for l in LISTINGS:
            if l.get("status") in PUBLIC_STATUSES and l["slug"] not in llms:
                errors.append(f"llms.txt: missing public listing {l['slug']}")

    if errors:
        print(f"\n❌ {len(errors)} problem(s):")
        for e in errors:
            print("   -", e)
        raise SystemExit(1)
    print(f"\n✅ verify_site: {len(pages)} pages clean "
          "(images exist, no dupes, alt text present, forms wired, no orphans).")


# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs(f"{SITE}/communities", exist_ok=True)
    os.makedirs(f"{SITE}/blog", exist_ok=True)
    os.makedirs(f"{SITE}/guides", exist_ok=True)
    os.makedirs(f"{SITE}/services", exist_ok=True)
    os.makedirs(f"{SITE}/listings", exist_ok=True)

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

    print("\n── Listings ──")
    gen_listings_index()
    for l in LISTINGS:
        gen_listing_page(l)

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
    gen_photo_credits()
    sync_static_footers()
    gen_sitemap()
    gen_llms_txt()
    gen_robots()

    verify_site()

    total = 9 + len(COMMUNITIES) + 1 + len(BLOGS) + len(GUIDES) + len(SERVICES) + 2 + 1 + len(LISTINGS)
    print(f"\n✅ {total} files generated.")
