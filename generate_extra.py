#!/usr/bin/env python3
"""Generate additional pages to bring total above 50."""
import sys
sys.path.insert(0, "/Users/derikbannister9/larissa-mayfield-website")
from generate import *

EXTRA_BLOGS = [
    {
        "slug": "home-inspection-checklist",
        "title": "The Home Inspection Checklist Every Buyer Needs",
        "tag": "BUYERS &middot; INSPECTIONS",
        "date": "APR 2026",
        "excerpt": "A home inspection is your best protection against expensive surprises. Here is what inspectors look for and what you should ask about.",
        "img_key": "house",
        "seo_desc": "Home inspection checklist for Oregon buyers. What inspectors check, common issues, and how to use the report. Guide by Larissa Mayfield.",
        "body_sections": [
            ("What a Home Inspection Covers", "A standard home inspection evaluates the structure, roof, foundation, electrical, plumbing, HVAC, windows, doors, insulation, and visible components of the property. The inspector produces a detailed written report, typically 30 to 50 pages, with photos and descriptions of any concerns."),
            ("What It Does Not Cover", "A standard inspection does not include well tests, septic evaluations, radon testing, mold testing, or pest inspections. These are separate inspections that I recommend scheduling concurrently during the inspection period for rural properties."),
            ("Common Issues in Oregon Homes", "The most frequent findings in Lane County homes include aging roofs (especially moss damage), moisture intrusion in crawl spaces, outdated electrical panels, and deferred maintenance on decks and siding. Homes built before 1978 may have lead paint. Homes with basements often show signs of water management issues."),
            ("How to Use the Report", "The inspection report is a negotiation tool, not a deal-killer. I help clients prioritize findings into three categories: safety concerns that must be addressed, significant defects that warrant repair credits, and maintenance items that are normal for the home&rsquo;s age. We then negotiate repairs or credits based on the serious items."),
            ("Choosing an Inspector", "I recommend inspectors who are ASHI-certified, carry errors and omissions insurance, and have experience with the specific property type. For rural properties, I use inspectors who understand well houses, septic systems, and outbuilding construction. The inspection fee ($400 to $600) is the best money you will spend in the transaction."),
        ]
    },
    {
        "slug": "staging-tips-sellers",
        "title": "Staging Your Home to Sell: What Actually Works",
        "tag": "SELLERS &middot; STAGING",
        "date": "MAR 2026",
        "excerpt": "Professional staging can increase your sale price by 5% to 10%. But you do not always need a professional &mdash; here is what works on any budget.",
        "img_key": "cottage",
        "seo_desc": "Home staging tips for Oregon sellers. DIY and professional staging strategies that increase sale price. By Larissa Mayfield, Real Broker.",
        "body_sections": [
            ("Why Staging Works", "Staging helps buyers visualize themselves living in the space. A well-staged home photographs better, shows better in person, and creates an emotional connection that translates to higher offers. The National Association of Realtors reports that staged homes sell for 1% to 5% more than unstaged comparable properties."),
            ("The Free Stuff: Declutter and Deep Clean", "The most impactful staging step costs nothing: remove personal items, declutter surfaces, and deep clean every room. Pack away family photos, clear kitchen counters to two or three items, and make sure every surface sparkles. Buyers need to see the home, not your life in it."),
            ("Low-Cost High-Impact Improvements", "Fresh white towels in bathrooms, new doormat, updated light fixtures in dated rooms, and a fresh coat of paint in neutral tones. Budget $500 to $1,500 and focus on the kitchen, primary bathroom, and entryway. These are the rooms that sell houses."),
            ("Professional Staging", "For vacant homes or properties above $500K, professional staging is often worth the investment. A staging company brings furniture, art, and accessories to create a lifestyle presentation. Costs range from $1,500 to $4,000 for a 30-day staging period. I have relationships with local stagers who know the Lane County market."),
            ("What I Provide for My Sellers", "Every listing client receives a room-by-room preparation checklist, a staging consultation, and professional photography. I walk the property with you, point out what to address, and help you prioritize. The goal is to maximize your sale price while minimizing your out-of-pocket preparation costs."),
        ]
    },
    {
        "slug": "moving-to-oregon-from-california",
        "title": "Moving to Oregon From California: What to Know",
        "tag": "RELOCATION &middot; CALIFORNIA",
        "date": "FEB 2026",
        "excerpt": "Oregon is attracting California transplants at record rates. Here is what to expect about housing, taxes, climate, and culture.",
        "img_key": "valley",
        "seo_desc": "Guide to moving from California to Oregon. Housing costs, taxes, climate, culture differences. By Oregon Realtor Larissa Mayfield.",
        "body_sections": [
            ("Housing Cost Comparison", "The median home price in Lane County is approximately $410,000, compared to $750,000 or more in most California metros. Your California equity can buy significantly more property here. Many transplants use their proceeds to purchase acreage or upgrade to a larger home."),
            ("Tax Differences", "Oregon has no sales tax, which is immediately noticeable. However, Oregon&rsquo;s income tax rates are among the highest in the nation (up to 9.9%). Property tax rates are generally lower than California&rsquo;s. The net tax impact depends on your income and spending patterns."),
            ("Climate and Lifestyle", "The Willamette Valley has mild, wet winters and warm, dry summers. Average rainfall in Eugene is about 47 inches per year, mostly between October and April. Summers are stunning &mdash; 80s and sunny with low humidity. If you are coming from Southern California, the winter rain is an adjustment."),
            ("Cultural Differences", "Oregon&rsquo;s culture is more casual, outdoors-oriented, and community-focused than most California metros. Eugene in particular has a strong arts, food, and sustainability culture. The pace is slower, which most transplants grow to love. Traffic is minimal by California standards."),
            ("Buying Remotely", "Many California buyers start their search remotely. I conduct video tours, provide detailed neighborhood summaries, and handle the legwork until you can visit in person. Once you arrive, I have a curated list of homes ready to tour. I have helped dozens of families relocate successfully from California."),
        ]
    },
    {
        "slug": "property-tax-oregon",
        "title": "Understanding Property Tax in Oregon",
        "tag": "BUYERS &middot; TAXES",
        "date": "JAN 2026",
        "excerpt": "Oregon&rsquo;s property tax system is unique. Measure 50, assessed value caps, and compression &mdash; here is what homeowners need to know.",
        "img_key": "docs",
        "seo_desc": "Oregon property tax explained. Measure 50, assessed value, tax rates, and how it affects home buyers. Guide by Larissa Mayfield.",
        "body_sections": [
            ("How Oregon Property Tax Works", "Oregon&rsquo;s property tax system is governed by Measure 50, passed in 1997. Unlike most states, your tax is based on assessed value, not market value. Assessed value can only increase by 3% per year, regardless of how much the market value increases. This means long-held properties often have assessed values well below market value."),
            ("Assessed Value vs. Market Value", "When you buy a property, the assessed value resets to the lesser of the purchase price or the real market value, then grows by up to 3% annually. This means a home that was assessed at $200,000 for a longtime owner might reset to $400,000 when you buy it, significantly increasing the tax bill."),
            ("Tax Rates by Area", "Tax rates vary by location and the tax districts that serve the property. In Lane County, rates typically range from $12 to $18 per $1,000 of assessed value. Eugene properties tend toward the higher end; rural unincorporated areas tend toward the lower end."),
            ("Compression", "Oregon law caps the total tax rate, causing compression when the combined rates of all districts exceed the limit. This effectively reduces your actual tax bill below what the rates would suggest. Compression benefits properties in areas with many overlapping tax districts."),
            ("What This Means for Buyers", "When evaluating a property, look at the current tax bill and understand that your bill may be different once the assessed value resets. I include a tax estimate in my analysis for every property. For rural properties with special assessments (like farm deferral), the tax picture can change significantly at sale."),
        ]
    },
    {
        "slug": "drone-photography-listings",
        "title": "Why Drone Photography Sells Rural Listings Faster",
        "tag": "SELLERS &middot; MARKETING",
        "date": "DEC 2025",
        "excerpt": "Aerial photography shows buyers what a property truly offers. For acreage and rural listings, drone photos are not optional &mdash; they are essential.",
        "img_key": "aerial",
        "seo_desc": "Drone photography for rural real estate listings in Oregon. Why aerial photos sell acreage faster. By Larissa Mayfield, Real Broker.",
        "body_sections": [
            ("The Problem With Ground-Level Photos", "A ground-level photo of a 20-acre property shows you a house, some grass, and maybe a tree line. It does not communicate the scale, layout, boundaries, or landscape features that make the property special. Buyers scrolling online have no way to understand what they are looking at."),
            ("What Drone Photos Reveal", "An aerial view shows the full property boundary, the relationship between the home and outbuildings, the topography, water features, timber coverage, and the surrounding landscape. It answers questions that buyers have before they visit: How far is the barn from the house? How much of the land is usable? What do the neighbors look like?"),
            ("Video Walkthroughs", "Beyond still photos, drone video creates a cinematic property tour that tells a story. I use slow flyover footage to show the approach, the setting, and the lifestyle. These videos perform extremely well on social media and generate significantly more engagement than static posts."),
            ("ROI for Sellers", "Properties listed with professional drone photography sell faster and for higher prices than comparable listings without aerial media. The cost of professional drone photography ($300 to $600) is one of the highest-ROI investments a seller can make, especially on acreage properties."),
            ("What I Include", "Every acreage listing I represent includes professional drone photography and video as a standard part of my marketing package. I work with FAA-certified drone operators who specialize in real estate and know how to capture Oregon&rsquo;s landscapes at their best."),
        ]
    },
    {
        "slug": "multigenerational-homes-oregon",
        "title": "Multigenerational Living: ADUs and Dual-Living in Oregon",
        "tag": "BUYERS &middot; LIFESTYLE",
        "date": "NOV 2025",
        "excerpt": "Oregon&rsquo;s ADU-friendly laws make multigenerational living more accessible than ever. Here is what buyers need to know.",
        "img_key": "farmhouse",
        "seo_desc": "Multigenerational homes and ADUs in Oregon. Zoning, financing, and finding properties for extended families. By Larissa Mayfield.",
        "body_sections": [
            ("Oregon&rsquo;s ADU Laws", "Oregon is one of the most ADU-friendly states in the country. House Bill 2001, effective since 2021, requires cities with populations over 25,000 to allow at least two dwelling units on residential lots. This means you can build an accessory dwelling unit on most urban residential properties in Eugene and Springfield."),
            ("Rural ADU Options", "On rural land zoned EFU or Rural Residential, the rules are different. Lane County allows certain accessory structures and may permit a second dwelling for family members or farm workers under specific conditions. The details depend on the zoning designation and the county&rsquo;s current interpretation of state law."),
            ("Finding the Right Property", "For multigenerational buyers, I search for properties that already have a second dwelling, a converted garage, or the space and zoning to add one. Some rural properties have existing guest houses, manufactured homes, or separate living quarters that are ideal for extended family."),
            ("Financing Considerations", "Financing a property with an ADU can be straightforward if the unit is already built and permitted. For properties where you plan to add an ADU, some lenders offer renovation loans (like the FHA 203k) that finance the construction. I connect clients with lenders experienced in ADU financing."),
            ("Making It Work", "Multigenerational living works best when everyone has appropriate privacy and shared spaces are well-designed. Properties with separate entrances, separate utility connections, or enough distance between dwellings tend to work best. I help families think through the practical aspects before they commit to a property."),
        ]
    },
]

EXTRA_SERVICES = [
    {
        "slug": "wells-septic-guide",
        "title": "Wells &amp; Septic: The Complete Buyer&rsquo;s Guide",
        "tag": "RURAL &middot; INFRASTRUCTURE",
        "desc": "Everything you need to know about wells and septic systems when buying rural property in Oregon. Inspections, costs, and what to look for.",
        "seo_desc": "Complete guide to wells and septic systems for Oregon rural property buyers. Inspections, costs, regulations. By Larissa Mayfield.",
    },
    {
        "slug": "oregon-land-for-sale",
        "title": "Oregon Land for Sale — Finding the Right Parcel",
        "tag": "BUYERS &middot; LAND",
        "desc": "Looking for land in Oregon? From buildable lots to timber parcels, here is how to evaluate and purchase land in the Willamette Valley.",
        "seo_desc": "Oregon land for sale guide. How to find, evaluate, and buy land in the Willamette Valley. By Larissa Mayfield, Real Broker.",
    },
]

print("Generating extra pages...")

print("\n── Extra Blog Articles ──")
for b in EXTRA_BLOGS:
    gen_blog_article(b)
    BLOGS.append(b)

print("\n── Extra Service Pages ──")
for s in EXTRA_SERVICES:
    gen_service(s)
    SERVICES.append(s)

# Regenerate blog index with all articles
print("\n── Regenerating Blog Index ──")
gen_blog_index()

# Regenerate sitemap with all pages
print("\n── Regenerating Sitemap ──")
gen_sitemap()

print(f"\n✅ {6 + 2} extra files generated. Total HTML pages now: {46 + 6 + 2}")
