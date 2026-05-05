#!/bin/bash
# Site generator for Larissa Mayfield Heritage Editorial website
# Generates 50+ static HTML pages from templates

SITE="/Users/derikbannister9/larissa-mayfield-website"
cd "$SITE"

# Depth helper: how many ../ for CSS/JS/images paths
depth_prefix() {
  local d="$1"
  case "$d" in
    0) echo "." ;;
    1) echo ".." ;;
    2) echo "../.." ;;
  esac
}

# Header partial
header_html() {
  local prefix="$1"
  local active="$2"
  cat <<HEADER
<header class="site-header">
  <div class="header-left">
    <a href="${prefix}/index.html">
      <img src="${prefix}/images/larissa-headshot-square.jpg" alt="Larissa Mayfield">
      <span class="name">Larissa Mayfield</span>
      <span class="broker">&middot; Real Broker</span>
    </a>
  </div>
  <nav class="header-nav">
    <a href="${prefix}/about.html"$([ "$active" = "about" ] && echo ' class="active"')>About</a>
    <a href="${prefix}/sellers.html"$([ "$active" = "sellers" ] && echo ' class="active"')>Sellers</a>
    <a href="${prefix}/rural-acreage.html"$([ "$active" = "rural" ] && echo ' class="active"')>Rural &amp; Acreage</a>
    <a href="${prefix}/buyers.html"$([ "$active" = "buyers" ] && echo ' class="active"')>Buyers</a>
    <a href="${prefix}/communities/index.html"$([ "$active" = "communities" ] && echo ' class="active"')>Communities</a>
    <a href="${prefix}/resources.html"$([ "$active" = "resources" ] && echo ' class="active"')>Resources</a>
    <a href="${prefix}/contact.html"$([ "$active" = "contact" ] && echo ' class="active"')>Contact</a>
  </nav>
  <div class="header-phone"><a href="tel:5417847745">541.784.7745</a></div>
  <button class="menu-toggle" id="menuToggle"><span></span><span></span><span></span></button>
</header>
<div class="mobile-menu" id="mobileMenu">
  <a href="${prefix}/index.html">Home</a>
  <a href="${prefix}/about.html">About</a>
  <a href="${prefix}/sellers.html">Sellers</a>
  <a href="${prefix}/rural-acreage.html">Rural &amp; Acreage</a>
  <a href="${prefix}/buyers.html">Buyers</a>
  <a href="${prefix}/communities/index.html">Communities</a>
  <a href="${prefix}/resources.html">Resources</a>
  <a href="${prefix}/testimonials.html">Testimonials</a>
  <a href="${prefix}/contact.html">Contact</a>
</div>
HEADER
}

# Footer partial
footer_html() {
  local prefix="$1"
  cat <<FOOTER
<footer class="site-footer">
  <div class="footer-grid">
    <div>
      <div class="footer-name">Larissa Mayfield</div>
      <div class="footer-license">REAL BROKER &middot; LIC. 201231874</div>
      <p class="footer-desc">Licensed throughout Oregon. Primary service area: Lane, Linn, Benton, and Douglas counties.</p>
    </div>
    <div class="footer-col">
      <div class="footer-col-title">Pages</div>
      <ul>
        <li><a href="${prefix}/about.html">About</a></li>
        <li><a href="${prefix}/sellers.html">Sellers</a></li>
        <li><a href="${prefix}/rural-acreage.html">Rural &amp; Acreage</a></li>
        <li><a href="${prefix}/buyers.html">Buyers</a></li>
        <li><a href="${prefix}/communities/index.html">Communities</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <div class="footer-col-title">Resources</div>
      <ul>
        <li><a href="${prefix}/guides/first-time-buyer-guide.html">First-Time Guide</a></li>
        <li><a href="${prefix}/guides/rural-buyer-playbook.html">Rural Guide</a></li>
        <li><a href="${prefix}/guides/lane-county-market-notes.html">Market Reports</a></li>
        <li><a href="${prefix}/blog/index.html">Blog</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <div class="footer-col-title">Contact</div>
      <ul>
        <li><a href="tel:5417847745">541.784.7745</a></li>
        <li><a href="mailto:larissa@theoperativegroup.com">larissa@theoperativegroup.com</a></li>
        <li><a href="${prefix}/contact.html">Schedule a call</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 LARISSA MAYFIELD &middot; REAL BROKER LLC</span>
    <span>EQUAL HOUSING OPPORTUNITY</span>
  </div>
</footer>
FOOTER
}

# Page wrapper function
# Usage: make_page output_file depth title description active_nav breadcrumb_html body_html schema_type
make_page() {
  local outfile="$1" depth="$2" title="$3" desc="$4" active="$5" crumb="$6" body="$7" schema_type="${8:-WebPage}"
  local prefix
  prefix=$(depth_prefix "$depth")
  local canonical_path="${outfile#$SITE/}"

  cat > "$outfile" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${title} | Larissa Mayfield — Real Broker, Oregon</title>
<meta name="description" content="${desc}">
<meta property="og:title" content="${title} | Larissa Mayfield">
<meta property="og:description" content="${desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="${prefix}/images/larissa-hat.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://larissamayfield.com/${canonical_path}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="${prefix}/css/style.css">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "${schema_type}",
  "name": "${title}",
  "description": "${desc}",
  "url": "https://larissamayfield.com/${canonical_path}",
  "author": {
    "@type": "RealEstateAgent",
    "name": "Larissa Mayfield",
    "telephone": "+1-541-784-7745",
    "email": "larissa@theoperativegroup.com",
    "address": {
      "@type": "PostalAddress",
      "addressRegion": "OR",
      "addressCountry": "US"
    },
    "areaServed": ["Lane County","Linn County","Benton County","Douglas County"],
    "license": "201231874"
  }
}
</script>
</head>
<body>
$(header_html "$prefix" "$active")
${crumb}
${body}
$(footer_html "$prefix")
<script src="${prefix}/js/main.js"></script>
</body>
</html>
EOF
  echo "  Created: $canonical_path"
}

echo "=== Generating Larissa Mayfield Website ==="
echo ""

##############################
# HOME PAGE
##############################
echo "--- Core Pages ---"
make_page "$SITE/index.html" 0 "Every Home Tells a Story" "Rural acreage and first homes across the Willamette Valley. Larissa Mayfield, Real Broker — 20+ years in banking, Lane County specialist." "home" "" '
<section class="hero-split">
  <div>
    <div class="tag reveal" style="margin-bottom:24px">Lane &middot; Linn &middot; Benton &middot; Douglas Counties</div>
    <h1 class="reveal reveal-d1">Every<br>home<br>tells a<br><em>story.</em></h1>
    <p class="body-text reveal reveal-d2" style="max-width:460px;margin:40px 0 36px">Rural acreage and first homes across the Willamette Valley &mdash; represented with the patience and rigor of two decades in commercial lending.</p>
    <div class="reveal reveal-d3" style="display:flex;gap:14px;flex-wrap:wrap">
      <a class="btn-primary" href="sellers.html">What&rsquo;s your land worth?</a>
      <a class="btn-link" href="about.html">Meet Larissa &rarr;</a>
    </div>
  </div>
  <div class="parallax-wrap reveal reveal-d2">
    <img class="parallax-img" src="images/larissa-hat.jpg" alt="Larissa Mayfield, Oregon Realtor" style="height:620px;object-position:center 30%">
  </div>
</section>

<section class="meta-strip reveal">
  <span>License #201231874</span>
  <span>Native Oregonian</span>
  <span>20+ Yrs &middot; Banking &amp; Finance</span>
  <span>4-H Volunteer &middot; Lane County</span>
  <span>Real Broker &middot; OR</span>
</section>

<section class="feature-section">
  <div class="feature-sticky">
    <div class="tag tag-purple reveal">Issue 01 &middot; Sellers</div>
    <h2 class="section-heading reveal reveal-d1" style="font-size:60px;line-height:1;margin-top:18px">Listing land is <em style="color:var(--purple)">not</em> like listing a house.</h2>
  </div>
  <div>
    <p class="body-text reveal" style="font-size:19px;margin-bottom:36px">Wells. Septic. Easements. Comparable sales five miles apart. Rural pricing is its own discipline &mdash; and it&rsquo;s how I built my book of business.</p>
    <div class="feature-grid-2x2">
      <div class="feature-card reveal"><div class="num">01</div><h3>Honest valuation</h3><p>I price from comparable land sales &mdash; not Zillow estimates that ignore acreage.</p></div>
      <div class="feature-card reveal reveal-d1"><div class="num">02</div><h3>Buyer financing</h3><p>Two decades in lending means I know which buyers can actually close on rural property.</p></div>
      <div class="feature-card reveal reveal-d2"><div class="num">03</div><h3>Drone &amp; lifestyle media</h3><p>Land is sold by light, line, and possibility &mdash; not by a phone snapshot.</p></div>
      <div class="feature-card reveal reveal-d3"><div class="num">04</div><h3>Title &amp; easement work</h3><p>Encroachments, water rights, and access roads are due diligence &mdash; not surprises.</p></div>
    </div>
  </div>
</section>

<section class="section-dark">
  <div class="tag reveal" style="margin-bottom:18px">Valuation &middot; No Obligation</div>
  <div class="valuation-grid">
    <div>
      <h2 class="reveal reveal-d1" style="font-size:clamp(48px,6vw,84px);line-height:.95;letter-spacing:-.03em">What is<br>your land<br><em>worth today?</em></h2>
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
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:40px" class="reveal">
    <h2 class="section-heading">The territory.</h2>
    <span class="tag">05 Communities</span>
  </div>
  <div class="community-grid">
    <article class="reveal"><a href="communities/veneta.html"><img src="https://images.unsplash.com/photo-1500076656116-558758c991c1?w=900&q=80" alt="Veneta Oregon"></a><h3><a href="communities/veneta.html">Veneta</a></h3><p>Small-town pace, big lots</p></article>
    <article class="reveal reveal-d1"><a href="communities/elmira.html"><img src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=900&q=80" alt="Elmira Oregon"></a><h3><a href="communities/elmira.html">Elmira</a></h3><p>Schools &amp; quiet acreage</p></article>
    <article class="reveal reveal-d2"><a href="communities/eugene.html"><img src="https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=900&q=80" alt="Eugene Oregon"></a><h3><a href="communities/eugene.html">Eugene</a></h3><p>University &amp; culture</p></article>
    <article class="reveal reveal-d3"><a href="communities/springfield.html"><img src="https://images.unsplash.com/photo-1449844908441-8829872d2607?w=900&q=80" alt="Springfield Oregon"></a><h3><a href="communities/springfield.html">Springfield</a></h3><p>Value &amp; growth</p></article>
    <article class="reveal"><a href="communities/lane-county.html"><img src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=900&q=80" alt="Lane County Oregon"></a><h3><a href="communities/lane-county.html">Lane County</a></h3><p>Coast to Cascades</p></article>
  </div>
</section>

<section class="about-teaser">
  <div class="reveal">
    <div class="tag" style="margin-bottom:18px">A Little About Me</div>
    <blockquote>&ldquo;Before I sold homes, I funded them &mdash; twenty years in banking and commercial lending. I know exactly what a clean transaction looks like, and I know how to close one.&rdquo;</blockquote>
    <div class="tag" style="margin-top:32px">&mdash; Larissa Mayfield</div>
  </div>
  <div class="photo-grid-2x2 reveal reveal-d1">
    <img src="images/larissa-yellow.jpg" alt="Larissa Mayfield">
    <img src="images/larissa-laptop.jpg" alt="Larissa Mayfield working">
    <img src="images/larissa-hat-smile.jpg" alt="Larissa Mayfield">
    <img src="images/larissa-couch.jpg" alt="Larissa Mayfield">
  </div>
</section>

<section class="section-alt">
  <h2 class="section-heading reveal" style="margin-bottom:32px">Take something with you.</h2>
  <div class="lead-grid">
    <article class="lead-card reveal"><div class="meta">32 PP &middot; PDF</div><h3>First-Time Buyer Guide</h3><p>A walkthrough from pre-approval to closing, written for the Willamette Valley.</p><a class="download" href="guides/first-time-buyer-guide.html">Download &rarr;</a></article>
    <article class="lead-card reveal reveal-d1"><div class="meta">24 PP &middot; PDF</div><h3>Rural Buyer Guide</h3><p>Wells, septic, easements, financing &mdash; what to check before you fall in love.</p><a class="download" href="guides/rural-buyer-playbook.html">Download &rarr;</a></article>
    <article class="lead-card reveal reveal-d2"><div class="meta">Monthly &middot; Email</div><h3>Lane County Market Notes</h3><p>Rural &amp; residential trends, hand-curated. No spam, no fluff.</p><a class="download" href="guides/lane-county-market-notes.html">Subscribe &rarr;</a></article>
  </div>
</section>

<section class="testimonial-hero reveal">
  <div class="stars">&star; &star; &star; &star; &star;</div>
  <blockquote>&ldquo;I have bought and sold 26 homes since 1974 and I can honestly say that Larissa Mayfield is the best Realtor I&rsquo;ve ever had the pleasure of working with. Her knowledge and attention to detail set her apart.&rdquo;</blockquote>
  <div class="attr">&mdash; ALAN N. GRAY &middot; UMPQUA SELLER, 2025</div>
</section>
' "RealEstateAgent"

echo "  HOME done"

# We'll continue generating pages with a simpler approach — write the body inline
# For brevity in this script, the remaining pages use the same make_page function

##############################
# ABOUT
##############################
make_page "$SITE/about.html" 0 "About Larissa Mayfield" "Native Oregonian, 20+ years in banking and commercial lending. Licensed throughout Oregon with deep expertise in Lane, Linn, Benton, and Douglas counties." "about" \
'<div class="breadcrumb"><a href="index.html">HOME</a><span class="sep">/</span><span class="current">About</span></div>' \
'
<section class="inner-hero">
  <div>
    <div class="tag reveal">Native Oregonian &middot; Lic. 201231874</div>
    <h1 class="page-title reveal reveal-d1" style="margin-top:24px">A practiced<br>hand on either<br><em>side of the table.</em></h1>
    <p class="body-text reveal reveal-d2" style="max-width:540px;margin-top:36px;font-size:19px">I&rsquo;m Larissa &mdash; a born-and-raised Oregonian who came to real estate after twenty years in banking, finance, and commercial lending. I represent buyers and sellers across Lane, Linn, Benton, and Douglas counties.</p>
  </div>
  <div class="parallax-wrap reveal reveal-d1">
    <img class="parallax-img" src="images/larissa-hat.jpg" alt="Larissa Mayfield, Oregon Realtor" style="width:100%;height:620px;object-fit:cover;object-position:center 30%">
  </div>
</section>
<section class="meta-strip reveal">
  <span>20+ Yrs &middot; Lending</span><span>Native Oregonian</span><span>4-H Volunteer</span><span>Lane &middot; Linn &middot; Benton &middot; Douglas</span><span>Real Broker</span>
</section>
<section class="chapter">
  <div class="chapter-sticky"><div class="tag tag-purple reveal">Chapter 01</div><h2 class="section-heading reveal reveal-d1" style="margin-top:18px">My story.</h2></div>
  <div class="chapter-body">
    <p class="reveal">As a proud native Oregonian, I became a realtor because I&rsquo;m passionate about helping clients achieve their dreams of homeownership. Every home tells a story &mdash; and I&rsquo;m dedicated to helping you start the next chapter in yours.</p>
    <p class="reveal reveal-d1">Before transitioning to real estate, I spent over twenty years in banking, finance, and commercial lending. That experience equips me with a unique perspective and a comprehensive set of tools to meet your real estate needs &mdash; whether you&rsquo;re buying your first home, upgrading, or selling to embrace a new opportunity.</p>
    <p class="reveal reveal-d2">To me, buying or selling a home is more than just a transaction &mdash; it&rsquo;s a life-changing experience. I take pride in providing exceptional, personalized service and building strong, lasting relationships. You can count on me to work relentlessly on your behalf, always keeping your goals at the forefront.</p>
  </div>
</section>
<section class="photo-grid-section">
  <div class="photo-grid-inner">
    <div class="photo-grid-4 reveal">
      <img src="images/larissa-hat-seated.jpg" alt="Larissa Mayfield"><img src="images/larissa-laptop.jpg" alt="Larissa working">
      <img src="images/larissa-couch.jpg" alt="Larissa Mayfield"><img src="images/larissa-hat-smile.jpg" alt="Larissa smiling">
    </div>
    <div class="reveal reveal-d1">
      <div class="tag tag-purple" style="margin-bottom:18px">Chapter 02 &middot; Community</div>
      <h2 class="section-heading" style="margin-bottom:24px">Beyond the listings.</h2>
      <p class="body-text" style="max-width:480px">I&rsquo;m deeply involved in the community as a volunteer with the Lane County 4-H program, where I help local youth develop valuable skills by raising and caring for various farm animals. The same neighbors who built this place are the ones I get to serve.</p>
    </div>
  </div>
</section>
<section class="cta-centered reveal">
  <h2>Let&rsquo;s work together to make your real estate dreams a reality.</h2>
  <div class="cta-buttons"><a class="btn-primary" href="contact.html">Schedule a conversation</a><a class="btn-link" href="tel:5417847745">541.784.7745 &rarr;</a></div>
</section>
' "AboutPage"

echo "  ABOUT done"

##############################
# SELLERS
##############################
make_page "$SITE/sellers.html" 0 "Sell Your Home or Land" "Free no-obligation property valuation. 5-step selling process from consultation to closing. Lane County rural and residential specialist." "sellers" \
'<div class="breadcrumb"><a href="index.html">HOME</a><span class="sep">/</span><span class="current">Sellers &amp; Valuation</span></div>' \
'
<section class="section-dark" style="padding-top:96px">
  <div style="display:grid;grid-template-columns:1.1fr 1fr;gap:56px;align-items:end">
    <div>
      <div class="tag reveal" style="margin-bottom:24px">Sellers &middot; No-Obligation Valuation</div>
      <h1 class="page-title reveal reveal-d1" style="color:var(--cream)">What is your<br>property<br><em style="color:var(--cream)"><i>worth today?</i></em></h1>
      <p class="body-text reveal reveal-d2" style="color:rgba(244,239,230,.85);margin-top:32px;max-width:460px">A free, no-obligation valuation built from real comparable sales &mdash; and an honest conversation about what your home or land would list for in today&rsquo;s market.</p>
    </div>
    <form class="valuation-form reveal reveal-d2" style="background:rgba(255,255,255,.04);padding:32px;border:1px solid rgba(244,239,230,.2)" onsubmit="event.preventDefault()">
      <label><div class="label-text">PROPERTY ADDRESS</div><input type="text" placeholder="24500 Hwy 126, Veneta OR"></label>
      <label><div class="label-text">APPROXIMATE ACREAGE</div><input type="text" placeholder="12.5"></label>
      <label><div class="label-text">PROPERTY TYPE</div><input type="text" placeholder="Rural / Acreage"></label>
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
    <img class="reveal parallax-img" src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1600&q=80" alt="Willamette Valley acreage">
    <div>
      <div class="tag tag-purple reveal" style="margin-bottom:18px">Specialty &middot; Rural &amp; Land</div>
      <h2 class="section-heading reveal reveal-d1" style="margin-bottom:28px">Selling land is <em style="color:var(--purple)">not</em> like selling a house.</h2>
      <p class="body-text reveal reveal-d2" style="font-size:16px;margin-bottom:32px">Wells. Septic. Easements. Comparable sales five miles apart. Rural pricing is its own discipline. Two decades in commercial lending taught me how rural transactions actually close.</p>
      <div class="split-pills reveal reveal-d3"><div class="split-pill">Honest valuation</div><div class="split-pill">Buyer financing</div><div class="split-pill">Drone &amp; lifestyle media</div><div class="split-pill">Title &amp; easement work</div></div>
      <div class="reveal" style="margin-top:32px"><a class="tag tag-purple" href="rural-acreage.html" style="cursor:pointer">See Rural &amp; Acreage Page &rarr;</a></div>
    </div>
  </div>
</section>
<section class="testimonial-hero reveal">
  <div class="stars">&star; &star; &star; &star; &star;</div>
  <blockquote style="font-size:40px">&ldquo;I have bought and sold 26 homes since 1974 and I can honestly say that Larissa Mayfield is the best Realtor I&rsquo;ve ever had the pleasure of working with.&rdquo;</blockquote>
  <div class="attr">&mdash; ALAN N. GRAY &middot; UMPQUA SELLER &middot; 2025</div>
</section>
'

echo "  SELLERS done"

echo ""
echo "=== Shell generator complete — continuing with Python for remaining 47+ pages ==="
