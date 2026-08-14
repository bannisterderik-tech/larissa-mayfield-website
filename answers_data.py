#!/usr/bin/env python3
"""
Answer pages — one page per real question, at /answers/<slug>.html.

WHY THESE EXIST
The portals (Zillow, Redfin, LandSearch) own "homes for sale in Veneta" and
always will — they have live inventory feeds and decades of domain authority.
What they structurally cannot do is answer a question. Nobody at Zillow knows
what Oregon requires of a seller with a domestic well. That is the ground a
licensed local broker can own outright, and it is where the buying intent is:
someone searching "well test required to sell in Oregon" is in a transaction
right now.

THE RULE FOR THIS FILE
Every regulatory claim carries a primary source in `sources` — a statute, an
administrative rule, or a .gov page. If a fact cannot be sourced, it does not
go on the page. These are legal and regulatory statements published under an
active broker's licence; being confidently wrong here is a real problem, not
an SEO miss.

`short_answer` is the direct answer, written to stand alone. It is what a
featured snippet lifts and what an AI engine quotes, so it must be true and
complete without the rest of the page.

`verified` is the date a human last checked the cited sources. Rules change.
"""

ANSWERS = [

    {
        "slug": "oregon-well-test-required-to-sell",
        "question": "Does Oregon require a well test when you sell a house?",
        "nav_label": "Well test required to sell",
        "tag": "Wells",
        "verified": "13 August 2026",
        "short_answer":
            "Yes. Under ORS 448.271, if the property you are selling has a well that supplies "
            "ground water for domestic use, you must have it tested for <strong>arsenic, "
            "nitrate and total coliform bacteria</strong> once you accept an offer. The sample "
            "has to be analysed by an accredited laboratory, and you must give the results to "
            "the buyer <em>and</em> file them with the Oregon Health Authority within 90 days "
            "of receiving them. Results stay valid for one year, so if a sale falls through you "
            "can reuse them on the next offer. Spring wells, irrigation-only wells and wells on "
            "undeveloped land are exempt.",
        "sections": [
            ("What the law actually says", [
                "The requirement comes from ORS 448.271, usually called the Domestic Well "
                "Testing Act, with the detail filled in by Oregon Administrative Rules "
                "333-061-0305 through 333-061-0335. It applies to a sale or exchange of real "
                "estate that includes a well supplying ground water for domestic purposes.",
                "The trigger is <strong>accepting an offer</strong>, not listing. You do not "
                "need results in hand to go on the market, which is worth knowing if you are "
                "trying to get a listing live before a weekend.",
            ]),
            ("The three tests, and why each one is there", [
                "<strong>Total coliform bacteria</strong> is the indicator test for whether "
                "surface contamination is reaching the water — a bad seal, a damaged casing, a "
                "well head sitting too low. It is the one most likely to come back positive, "
                "and it is often fixable.",
                "<strong>Nitrate</strong> points at septic systems, livestock or fertiliser "
                "reaching the aquifer. It matters most for infants, and it is the reason some "
                "parts of the valley get watched closely.",
                "<strong>Arsenic</strong> is naturally occurring in parts of Oregon's "
                "groundwater. It is not a contamination story, it is a geology story, and it "
                "does not announce itself — arsenic has no taste, colour or smell.",
            ]),
            ("Who does what, and by when", [
                "The seller or the seller's representative collects the sample following OAR "
                "333-061-0335, and it must be analysed by an accredited laboratory under OAR "
                "333-061-0330. You cannot use a hardware-store kit for this.",
                "Once you have results you have <strong>90 days</strong> to get them to the "
                "buyer and to submit the Real Estate Transaction (RET) form plus the results to "
                "the Oregon Health Authority. OHA accepts them by email to "
                "Domestic.Wells@odhsoha.oregon.gov or by fax to 971-673-0457.",
                "Filing with the state is the step people forget. Handing results to the buyer "
                "satisfies the buyer; it does not satisfy the statute.",
            ]),
            ("What a bad result actually means", [
                "A positive coliform result is common and is not automatically a deal problem. "
                "It usually starts a conversation about shock chlorination, the well head, or "
                "the casing seal, followed by a re-test.",
                "Arsenic and nitrate are different — those are treated, not repaired. Treatment "
                "is a real cost and a real negotiation, which is exactly why you want the test "
                "done early rather than in the last week of an escrow.",
                "None of this is a reason to avoid a well. Most of rural Lane County is on one. "
                "It is a reason to know the numbers before somebody else does.",
            ]),
            ("What this does not cover", [
                "The statute is about water quality, not water quantity. Nothing here tells you "
                "how many gallons a minute the well produces — that is a flow test, it is not "
                "required by Oregon law, and it is usually a lender or buyer request rather "
                "than a state one.",
                "It also says nothing about the condition of the pump, the pressure tank or the "
                "plumbing. Those are inspection items.",
            ]),
        ],
        "sources": [
            ("ORS 448.271 — Transfer of property that includes well; testing; effect",
             "https://oregon.public.law/statutes/ors_448.271"),
            ("OAR 333-061-0325 — Domestic Well Tests",
             "https://oregon.public.law/rules/oar_333-061-0325"),
            ("Oregon Health Authority — Well Testing &amp; Regulations",
             "https://www.oregon.gov/oha/ph/healthyenvironments/drinkingwater/sourcewater/domesticwellsafety/pages/testing-regulations.aspx"),
        ],
        "seo_desc":
            "Oregon requires a seller with a domestic well to test for arsenic, nitrate and "
            "coliform on accepting an offer, and to file results with the state within 90 days. "
            "What ORS 448.271 requires, explained by an Oregon broker.",
    },

    {
        "slug": "septic-no-permit-on-file-lane-county",
        "question": "What if there's no septic permit on file for a property?",
        "nav_label": "No septic permit on file",
        "tag": "Septic",
        "verified": "13 August 2026",
        "short_answer":
            "You get an <strong>Existing System Evaluation Report</strong>. When a property has "
            "a septic system but no as-built drawing or permit in the county record, that report "
            "is how the system gets documented — completed by a licensed installer, on the DEQ "
            "form, and filed with Lane County Land Management. It is not a pass/fail inspection "
            "and it does not create a permit retroactively. It tells you what is in the ground, "
            "whether it appears to be functioning, and what you would be taking on.",
        "sections": [
            ("Why the record is missing in the first place", [
                "Lane County's permit records run back to roughly the 1970s. A system installed "
                "before then, or installed without a permit, simply will not be there. On older "
                "rural parcels around Elmira, Veneta and the Fern Ridge area this is common "
                "rather than alarming.",
                "You can check before you ever write an offer. Lane County's Property Records "
                "Online portal (LMD-PRO) carries sanitation, building and land use permits, and "
                "it is public. Knowing whether a record exists changes how you write the offer.",
            ]),
            ("What the evaluation is, and what it is not", [
                "An Existing System Evaluation Report has to be done by someone licensed to do "
                "it, on the DEQ form — a general home inspector's opinion does not substitute.",
                "What it gives you: what type of system is there, where the tank and drainfield "
                "are, and whether it appears to be operating as intended.",
                "What it does not give you: a permit. The report documents the system; it does "
                "not legalise an unpermitted one or guarantee future performance. Treat it as "
                "the beginning of your diligence, not the end of it.",
            ]),
            ("How this changes what you can do with the property", [
                "This is the part that costs people money. The septic record is what governs "
                "how many bedrooms the system is approved for. If you are buying a three-bedroom "
                "house intending to add a fourth, or add a shop with a bathroom, or put in a "
                "second dwelling, the septic capacity is often the binding constraint — not the "
                "zoning, not the lot size.",
                "Get that answered during your inspection period, in writing, from Lane County "
                "Land Management. Not from the listing, and not from the seller's memory.",
            ]),
            ("Where to actually go", [
                "Lane County Land Management Division, 3050 N. Delta Highway, Eugene, OR 97408. "
                "Phone (541) 682-4651, counter hours Monday to Friday, 9:00am to 3:00pm.",
                "Oregon DEQ also publishes a statewide onsite septic records lookup, which is "
                "worth checking alongside the county portal.",
            ]),
        ],
        "sources": [
            ("Lane County — On-Site Wastewater",
             "https://www.lanecounty.org/government/county_departments/public_works/land_management_division/on-_site_wastewater"),
            ("Existing System Evaluation Report form (Oregon DEQ)",
             "https://oregonrealtors.org/sites/default/files/Handout%201%20-%20ESERform.pdf"),
            ("Oregon DEQ — Locating Onsite Septic System Records Online",
             "https://www.oregon.gov/deq/Residential/Pages/Onsite-Records.aspx"),
        ],
        "seo_desc":
            "No septic permit on file in Lane County? An Existing System Evaluation Report by a "
            "licensed installer documents the system. What it covers, what it doesn't, and why "
            "septic capacity — not zoning — usually limits what you can build.",
    },

    {
        "slug": "farm-forest-deferral-additional-tax-when-you-sell",
        "question": "If I sell land that's in farm or forest deferral, do I owe the back taxes?",
        "title": "Farm Deferral Back Taxes When You Sell",
        "nav_label": "Deferral and the back-tax question",
        "tag": "Taxes",
        "verified": "14 August 2026",
        "short_answer":
            "Usually not, and this is the single most misunderstood thing about rural land in "
            "Oregon. <strong>Selling is not what triggers the additional tax &mdash; changing the "
            "use is.</strong> Under ORS 308A.706 the tax stays a <em>potential</em> liability, "
            "unimposed, as long as the land is not being converted to residential, commercial or "
            "industrial use. A buyer who keeps farming it or keeps it in forest simply carries "
            "the deferral forward. When it <em>is</em> disqualified and converted, ORS 308A.703 "
            "sets the reach-back: <strong>ten years</strong> for exclusive-farm-use farmland that "
            "stays outside an urban growth boundary, <strong>five</strong> if it is inside one, "
            "<strong>five</strong> for farmland in a non-EFU zone, and <strong>five</strong> for "
            "designated forestland &mdash; never more years than the land actually held the "
            "assessment.",
        "sections": [
            ("What the deferral actually is", [
                "Farm and forest special assessment taxes qualifying land on what it is worth as "
                "farm or forest ground rather than on what it would fetch on the open market. On "
                "acreage anywhere near Eugene or the Fern Ridge corridor that gap is not small, "
                "and the annual saving is often the difference between a property that pencils "
                "and one that does not.",
                "The state's side of the bargain is that the discount is conditional. It is not "
                "forgiveness &mdash; it is a deferral, and the untaxed difference trails the "
                "property as a liability that may or may not ever come due.",
            ]),
            ("Why a sale, by itself, does not trigger it", [
                "This is where deals go sideways for no reason. A buyer hears \"deferral\" and "
                "assumes a five-figure tax bill lands at closing. Read ORS 308A.706: the "
                "additional taxes are <strong>not imposed</strong>, and remain a potential "
                "liability, when the disqualified land is not being put to a use incompatible "
                "with returning it to farm use.",
                "The statute keys on the <em>use and status of the land</em> on the "
                "disqualification date, not on who owns it. Land that changes hands and keeps "
                "doing what it was doing generally keeps its assessment, and the new owner "
                "inherits the same conditional arrangement the old one had.",
                "What actually causes trouble is quieter: the buyer who stops farming, or lets "
                "the income test lapse, or splits the parcel. Those are use and qualification "
                "changes, and they are the ones that bite.",
            ]),
            ("What it costs when it is triggered", [
                "ORS 308A.703 sets the number of years of back tax by category, and the "
                "distinctions matter more than people expect:",
                "<strong>Exclusive farm use zone farmland &mdash; ten years</strong>, but only if "
                "the land stays outside an urban growth boundary after disqualification. Inside a "
                "UGB it is five.",
                "<strong>Farmland in a non-exclusive farm use zone &mdash; five years.</strong>",
                "<strong>Designated forestland, western or eastern Oregon &mdash; five years.</strong>",
                "One limit runs across all of them: the additional tax can never cover more years "
                "than the land consecutively held the special assessment. Ground that has been in "
                "deferral three years cannot be reached back ten.",
            ]),
            ("What to actually do before you sign", [
                "Ask the county assessor two questions in writing: what special assessment is "
                "this parcel under, and what is the potential additional tax liability as of "
                "today. Both are answerable and neither is a secret.",
                "Then be honest with yourself about your plans. If you intend to keep the ground "
                "in farm or forest use, the deferral is an asset you are inheriting. If you "
                "intend to build a house on it, subdivide it, or run a business off it, price "
                "the disqualification into your offer rather than discovering it afterward.",
                "If you are the seller, know the number before a buyer's agent finds it. A "
                "surprise at day 12 of an inspection period costs more than the same fact "
                "disclosed on day one.",
            ]),
            ("Where this stops being general information", [
                "Special assessment has more categories, more qualification routes and more "
                "exceptions than any one page should pretend to cover &mdash; wildlife habitat "
                "land, conservation easements, small tract forestland and homesite assessments "
                "each run on their own rules.",
                "The county assessor is the authority on what your specific parcel is under. For "
                "the tax consequence of a specific plan, that is a conversation for your CPA, and "
                "it is worth having before you write the offer rather than after.",
            ]),
        ],
        "sources": [
            ("ORS 308A.703 &mdash; Additional taxes upon disqualification",
             "https://oregon.public.law/statutes/ors_308a.703"),
            ("ORS 308A.706 &mdash; Circumstances when additional taxes are deferred; "
             "potential additional tax liability",
             "https://oregon.public.law/statutes/ors_308a.706"),
            ("ORS 308A.116 &mdash; Disqualification of nonexclusive farm use zone farmland",
             "https://oregon.public.law/statutes/ors_308a.116"),
            ("Oregon Revised Statutes Chapter 308A &mdash; Land Special Assessments",
             "https://www.oregonlegislature.gov/bills_laws/ors/ors308a.html"),
        ],
        "seo_desc":
            "Selling Oregon land in farm or forest deferral does not by itself trigger the back "
            "taxes — changing the use does. What ORS 308A.703 and 308A.706 actually say, and the "
            "ten-year and five-year reach-back rules, explained by an Oregon broker.",
    },

    {
        "slug": "find-well-log-oregon",
        "question": "How do I find the well log for a property?",
        "nav_label": "Finding a well log",
        "tag": "Wells",
        "verified": "14 August 2026",
        "short_answer":
            "Search the Oregon Water Resources Department's well report database at "
            "<strong>apps.wrd.state.or.us/apps/gw/well_log</strong>. It is free, it is public, and "
            "it holds drilling records for most wells drilled in Oregon since the mid-1950s. The "
            "easiest route is to enter the street address, which auto-fills the "
            "township-range-section, then browse the wells in that section. You can also search "
            "by county, by well log ID, by tax lot, or by the driller's name. What you get back is "
            "a scan of the report the driller filed when the well went in &mdash; depth, "
            "construction, what they hit, and what it produced <em>on the day it was drilled</em>.",
        "sections": [
            ("Why you want it before you write an offer", [
                "The well log is the only independent record of what is actually in the ground. "
                "The listing tells you there is a well. The log tells you it is 340 feet deep, "
                "cased to 80, and made 12 gallons a minute in 1998 &mdash; or that it made three.",
                "It costs nothing and takes about five minutes. On any rural property around "
                "Veneta, Elmira, Crow or Noti, it is the first thing I pull.",
            ]),
            ("How to actually search it", [
                "The database is organised by <strong>township, range and section</strong> rather "
                "than by address, which throws people. The tool has an address box that converts "
                "for you &mdash; type the street address, let it fill the TRS, then look at the "
                "wells listed in that section.",
                "If you already have the well log ID, that is the direct route. The ID is a "
                "four-letter county code plus a number &mdash; LANE 51234, for instance. It is "
                "assigned when the driller files the report and it is how the state indexes the "
                "well for good.",
                "There is also a map interface if the address lookup does not land, and you can "
                "filter by owner name, tax lot, completion date, depth or yield.",
            ]),
            ("What the log tells you", [
                "<strong>Total depth and casing depth.</strong> How far down they went, and how "
                "far the steel goes. Casing depth matters &mdash; it is a large part of what "
                "keeps surface water out of your drinking water.",
                "<strong>Static water level.</strong> Where the water stood in the hole when it "
                "was finished. Compared against a neighbouring well drilled twenty years later, "
                "this is how you start reading whether an area's water table is moving.",
                "<strong>Yield at completion.</strong> Gallons per minute the driller measured on "
                "the day. This is the number everyone looks at and the one most often "
                "misunderstood &mdash; see below.",
                "<strong>The lithology log.</strong> The driller's running note of what they cut "
                "through: clay, gravel, blue clay, fractured basalt. This is the part that tells "
                "you why the well behaves the way it does.",
            ]),
            ("What the log does not tell you", [
                "<strong>It is not current.</strong> A yield figure from 1998 describes 1998. "
                "Wells silt up, pumps age, water tables move, and a neighbour drilling into the "
                "same fracture can change what yours does. The log is history, not a condition "
                "report.",
                "<strong>It says nothing about water quality.</strong> Nothing on it addresses "
                "arsenic, nitrate or coliform &mdash; that is the separate testing obligation "
                "Oregon puts on the seller once an offer is accepted.",
                "<strong>It says nothing about the pump, pressure tank or plumbing.</strong> "
                "Those are inspection items and they are frequently the actual expense.",
                "<strong>And sometimes there is no log at all.</strong> Wells predating the "
                "reporting requirement, or drilled without one, simply are not there. On older "
                "parcels that absence is common and is not by itself alarming &mdash; it just "
                "means the flow test and the water test carry all the weight.",
            ]),
        ],
        "sources": [
            ("Oregon Water Resources Department &mdash; Well Report Query",
             "https://apps.wrd.state.or.us/apps/gw/well_log/"),
            ("Oregon Water Resources Department &mdash; Access Data and Maps",
             "https://www.oregon.gov/owrd/access_data/pages/default.aspx"),
            ("OSU Well Water Program &mdash; Private Well Management Resources",
             "https://wellwater.oregonstate.edu/well-water/wells"),
        ],
        "seo_desc":
            "Find any Oregon property's well log free at the Water Resources Department database — "
            "depth, casing, static water level and yield. How to search by address or well log ID, "
            "what the log proves, and what it can't tell you.",
    },

    {
        "slug": "septic-bedrooms-approved-add-a-bedroom",
        "question": "How many bedrooms is my septic approved for, and can I add one?",
        "title": "Septic Bedroom Capacity in Oregon",
        "nav_label": "Septic bedroom capacity",
        "tag": "Septic",
        "verified": "14 August 2026",
        "short_answer":
            "Your septic permit states the design capacity, and that number &mdash; not the "
            "zoning, not the lot size &mdash; is usually what caps the bedroom count. Oregon sizes "
            "residential systems by bedrooms: under OAR 340-071-0220 a dwelling with four or fewer "
            "bedrooms needs a septic tank of at least <strong>1,000 gallons</strong>, and more "
            "than four bedrooms requires at least <strong>1,500</strong>. You cannot simply add a "
            "bedroom. Under OAR 340-071-0210 nobody may alter or increase an existing system's "
            "design capacity without a permit first &mdash; an <strong>alteration permit</strong> "
            "if the increase stays within the greater of 300 gallons per day or 50% of existing "
            "capacity, and a full <strong>construction-installation permit</strong> if it goes "
            "beyond that.",
        "sections": [
            ("Why this is the constraint that actually binds", [
                "People buy acreage imagining what they will add &mdash; the fourth bedroom, the "
                "shop with a bathroom, the ADU for a parent. Then they discover the drainfield was "
                "sized for three bedrooms in 1987 and the ground it sits on will not accept more.",
                "Zoning gets all the attention because it is easy to look up. Septic capacity is "
                "the quieter limit and it is more often the one that stops the project.",
            ]),
            ("How Oregon counts a bedroom", [
                "The system is sized on projected wastewater flow, and bedrooms are the proxy "
                "&mdash; the assumption being that bedrooms predict occupants and occupants "
                "predict gallons. Square footage is not the measure.",
                "This is why a \"bonus room\" or \"office\" with a closet and a window can quietly "
                "become a bedroom in the county's eyes, and why a listing that advertises more "
                "bedrooms than the septic record shows is a real problem rather than a marketing "
                "quibble. If you are selling, the septic record and the listing should agree.",
            ]),
            ("What it takes to add capacity", [
                "The rule is unambiguous: you may not alter or increase design capacity without "
                "the permit in hand first. Doing the work and sorting the paperwork afterward is "
                "not a route that exists here.",
                "An <strong>alteration permit</strong> covers the smaller case &mdash; changes "
                "within the original design flow, or an increase no greater than 300 gallons per "
                "day or 50% of existing capacity, whichever is greater. Even then the existing "
                "system has to be functioning properly, the setbacks have to be met, and the "
                "county has to find no public health hazard.",
                "Past that threshold you are into a <strong>construction-installation permit</strong>, "
                "which means a site evaluation and, in practice, the question of whether the "
                "parcel has anywhere left to put a system. On a small lot, or one with a high "
                "water table or a creek, the answer is sometimes no.",
            ]),
            ("How to check before you buy", [
                "Pull the septic record for the address through Lane County's Property Records "
                "Online portal, or through Oregon DEQ's statewide onsite records lookup. You are "
                "looking for the permit, the as-built drawing, and the stated design capacity.",
                "Then ask Lane County Land Management the specific question in writing &mdash; "
                "not \"is the septic okay\" but \"what bedroom count is this system approved for, "
                "and what would adding one require?\" Get the answer during your inspection "
                "period, from the county, in writing. Not from the listing, and not from the "
                "seller's recollection.",
                "If no permit exists at all, that is a different problem with its own answer.",
            ]),
        ],
        "sources": [
            ("OAR 340-071-0220 &mdash; Standard Subsurface Systems",
             "https://oregon.public.law/rules/oar_340-071-0220"),
            ("OAR 340-071-0210 &mdash; Alteration of Existing Onsite Wastewater Treatment Systems",
             "https://oregon.public.law/rules/oar_340-071-0210"),
            ("Oregon DEQ &mdash; Onsite Wastewater Treatment System Rules (OAR 340-071/073)",
             "https://www.oregon.gov/deq/Residential/Documents/OAR340-071-073.pdf"),
            ("Lane County &mdash; On-Site Wastewater",
             "https://www.lanecounty.org/government/county_departments/public_works/land_management_division/on-_site_wastewater"),
        ],
        "seo_desc":
            "Your septic permit's design capacity caps the bedroom count, not the zoning. Oregon's "
            "1,000 and 1,500 gallon tank thresholds, when an alteration permit is enough, and how "
            "to check a property's approved bedrooms before you buy.",
    },

    {
        "slug": "water-rights-transfer-with-land-oregon",
        "question": "Do water rights come with the land when I buy it?",
        "nav_label": "Do water rights transfer",
        "tag": "Water rights",
        "verified": "14 August 2026",
        "short_answer":
            "A <strong>certificated</strong> water right is appurtenant to the land under ORS "
            "540.510 &mdash; it attaches to the ground, and on a sale it is treated as included "
            "unless the seller expressly reserves it in the deed or sale contract. A water right "
            "<strong>permit</strong> is not yet vested and so is not legally appurtenant, though "
            "because it names a specific place of use it usually follows the land too. Two things "
            "matter more than the transfer question: the right runs with <em>that</em> land and "
            "cannot be moved to other property without a formal transfer application, and under "
            "ORS 540.610 five successive years of non-use raises a rebuttable presumption of "
            "forfeiture. A right nobody has exercised since 2015 may not be a right any more.",
        "sections": [
            ("Appurtenant is the word that does the work", [
                "ORS 540.510 puts it plainly: water used in this state remains appurtenant to the "
                "premises upon which it is used. It is attached to the dirt, not to the person.",
                "That is why a certificated right generally passes with the sale without anyone "
                "doing anything, and equally why a seller who wants to keep it has to say so "
                "explicitly in the deed or the contract. Silence transfers it.",
                "It is also why you cannot buy a neighbour's water right and bring it to your "
                "place. Moving the place of use, the point of diversion or the character of use "
                "requires a transfer application through the Water Resources Department under ORS "
                "540.520 and 540.530.",
            ]),
            ("Certificate versus permit", [
                "A <strong>certificate</strong> is a perfected, vested right &mdash; the water was "
                "put to beneficial use and the state confirmed it. This is the appurtenant case.",
                "A <strong>permit</strong> is a right in progress: authorised, not yet proven up. "
                "Because it is not vested it is not appurtenant in the strict sense, but each "
                "permit specifies a location of use, so in a real estate transaction it is "
                "generally taken to go with the land unless the parties clearly intend otherwise.",
                "Practical version: find out which one the property has, because they are not the "
                "same asset and they do not carry the same certainty.",
            ]),
            ("The forfeiture problem nobody checks", [
                "Under ORS 540.610, failing to use the water for five successive years establishes "
                "a <strong>rebuttable presumption of forfeiture</strong>. Rebuttable is the "
                "operative word &mdash; the state has to show the non-use, and the holder then "
                "gets to explain it.",
                "The statute lists a long set of circumstances that excuse non-use, and several "
                "are ordinary rather than exotic: water simply was not available though the holder "
                "was ready to use it, a declared drought year, land enrolled in the federal "
                "Conservation Reserve Program, economic hardship, a pending transfer application, "
                "or use that was prohibited by law.",
                "Still, a right that has sat unused through a decade of absentee ownership is not "
                "the clean asset a listing implies. If irrigation water is part of why you are "
                "buying the property, verify the right is live before you pay for it.",
            ]),
            ("What to check, and where", [
                "Get the certificate or permit number and look the right up directly with the "
                "Oregon Water Resources Department. You want the priority date, the authorised "
                "acreage, the place of use, the point of diversion and the character of use.",
                "Then ask the seller the question that actually matters: when was this water last "
                "used, and on what. Ask for something showing it &mdash; irrigation records, a "
                "district bill, photographs of a standing crop.",
                "A senior priority date on Oregon water is genuinely valuable in a dry year. That "
                "is exactly why it deserves verifying rather than assuming.",
            ]),
        ],
        "sources": [
            ("ORS 540.510 &mdash; Appurtenancy of water rights; changes in use",
             "https://oregon.public.law/statutes/ors_540.510"),
            ("ORS 540.610 &mdash; Presumption of forfeiture from nonuse; exceptions",
             "https://oregon.public.law/statutes/ors_540.610"),
            ("OAR 690-380-3000 &mdash; Application for Transfer",
             "https://oregon.public.law/rules/oar_690-380-3000"),
            ("OSU Extension EM 9521 &mdash; Water rights and water law: using your irrigation "
             "water legally",
             "https://extension.oregonstate.edu/catalog/em-9521-water-rights-water-law-using-your-irrigation-water-legally"),
        ],
        "seo_desc":
            "Certificated Oregon water rights are appurtenant and pass with the land unless "
            "expressly reserved. Certificate vs permit, why rights can't move to other property, "
            "and the five-year non-use forfeiture rule under ORS 540.610.",
    },

    {
        "slug": "lot-of-record-dwelling-efu-oregon",
        "question": "I own bare EFU land. Can I build a house on it?",
        "nav_label": "Building on EFU land",
        "tag": "Land use",
        "verified": "14 August 2026",
        "short_answer":
            "Not automatically, and owning the land is not the qualifying fact. Exclusive farm use "
            "zoning exists to keep farmland farmed, so a dwelling has to fit one of the narrow "
            "routes the statutes allow. The one that catches most bare parcels is the "
            "<strong>lot of record dwelling</strong> under ORS 215.705, and it turns on history "
            "rather than acreage: the lot must have been <strong>lawfully created</strong>, the "
            "tract must have <strong>no dwelling on it already</strong>, and the present owner "
            "must have acquired it <strong>before 1 January 1985</strong> &mdash; or received it "
            "by will or intestate succession from someone who did. If you bought it in 2019, that "
            "route is closed to you, no matter how the parcel is shaped or what the neighbours "
            "have.",
        "sections": [
            ("Why EFU works the way it does", [
                "Oregon's land use system deliberately makes rural houses hard. EFU is a "
                "protection designation, not a residential one, and the default answer to \"can I "
                "build here\" is no until a specific statutory route says yes.",
                "That surprises people who are used to other states, and it is the source of most "
                "of the disappointment I see on bare-land purchases. The listing says \"buildable\" "
                "or \"build your dream home\" and nobody has checked whether a dwelling is "
                "actually approvable.",
            ]),
            ("The 1985 test, in plain terms", [
                "The lot of record route asks who owned the parcel and when. The present owner "
                "must have acquired it before 1 January 1985, or inherited it &mdash; by devise or "
                "intestate succession &mdash; from a person who acquired it before that date.",
                "Inheritance carries the qualification. A purchase does not. This is why the right "
                "to build can evaporate at a sale: a parcel that qualified for decades in one "
                "family stops qualifying the moment it is sold to a stranger.",
                "It is also why you cannot buy the right. If a seller tells you the property \"has "
                "a lot of record dwelling approval,\" find out whether the approval has actually "
                "been granted and whether it survives the transfer, because the underlying "
                "qualification generally does not.",
            ]),
            ("The other conditions", [
                "<strong>Lawfully created.</strong> The parcel has to have been created in "
                "compliance with the law in force at the time. Ground split by handshake, or by a "
                "deed that never went through a partition process, may not be a legal lot at all "
                "&mdash; and an illegal lot is not buildable on any route.",
                "<strong>No existing dwelling on the tract.</strong> If the tract already includes "
                "a dwelling, this route is unavailable.",
                "<strong>Consolidation.</strong> Where the parcel is part of a larger tract, the "
                "remaining portions are consolidated into a single lot when the dwelling is "
                "allowed. You do not get a house and keep the pieces separately saleable.",
            ]),
            ("High-value farmland is harder again", [
                "If the ground is classified high-value farmland the bar rises. A county hearings "
                "officer has to find that the parcel cannot practicably be managed for farm use "
                "&mdash; alone or together with other land &mdash; because of extraordinary "
                "circumstances inherent in the land or its setting that do not apply generally to "
                "land nearby.",
                "The dwelling must also comply with ORS 215.296 and must not materially alter the "
                "stability of the overall land use pattern in the area, and the State Department "
                "of Agriculture gets notice at least 20 days before the hearing.",
                "\"Extraordinary\" is doing real work in that sentence. Steep, rocky, oddly shaped "
                "or landlocked might qualify. Merely small does not.",
            ]),
            ("What to do before you buy bare EFU ground", [
                "Ask Lane County Land Management one question in writing, before your inspection "
                "period closes: <em>is a dwelling approvable on this parcel, and under which "
                "route?</em> Not whether it is zoned EFU &mdash; whether a house can be approved.",
                "Ask for the parcel's creation history too. Legal lot verification is a real "
                "process and it is far cheaper to do before closing than to discover afterward "
                "that you own unbuildable ground.",
                "There are other routes &mdash; farm dwellings tied to genuine farm income, "
                "replacement dwellings, forest template dwellings on F1/F2 ground &mdash; each "
                "with its own tests. Which one applies is a question for the county planner "
                "handling your parcel, and it is worth the phone call before the money moves.",
            ]),
        ],
        "sources": [
            ("ORS 215.705 &mdash; Dwellings in farm or forest zone; criteria; transferability "
             "of application",
             "https://oregon.public.law/statutes/ors_215.705"),
            ("ORS 215.283 &mdash; Uses permitted in exclusive farm use zones in nonmarginal "
             "lands counties",
             "https://oregon.public.law/statutes/ors_215.283"),
            ("ORS 215.720 &mdash; Criteria for forestland dwelling under ORS 215.705",
             "https://oregon.public.law/statutes/ors_215.720"),
            ("Lane County &mdash; Land Management Division, Land Use Planning and Zoning",
             "https://www.lanecounty.org/government/county_departments/public_works/land_management_division"),
        ],
        "seo_desc":
            "Owning EFU land in Oregon does not mean you can build on it. The lot of record "
            "dwelling route under ORS 215.705 turns on the 1 January 1985 ownership test — what "
            "qualifies, what a sale destroys, and what to ask the county first.",
    },

    {
        "slug": "manufactured-home-real-or-personal-property-oregon",
        "question": "Is a manufactured home real property or personal property?",
        "title": "Oregon Manufactured Home Property Status",
        "nav_label": "Manufactured home status",
        "tag": "Manufactured",
        "verified": "14 August 2026",
        "short_answer":
            "It depends on whether it has been <strong>recorded in the county deed records</strong> "
            "under ORS 446.626. Until it is, a manufactured home is titled personal property "
            "&mdash; closer to a vehicle than a house &mdash; and it is financed, insured and "
            "conveyed differently. To record it, the owner must own the land beneath it, hold a "
            "recorded leasehold of <strong>20 years or more</strong> that expressly permits "
            "recording, or be a member of a qualifying nonprofit cooperative that owns the land. "
            "One nuance that trips people: recording is <em>independent of</em> how the assessor "
            "taxes it. Recording governs conveyance, mortgages and liens; the tax classification "
            "is a separate determination.",
        "sections": [
            ("Why this decides how you can buy it", [
                "The classification drives the financing, and the financing drives the price. A "
                "home still on an ownership document is chattel &mdash; conventional mortgage "
                "products largely do not apply, the loan terms are shorter, the rates are higher, "
                "and the buyer pool is smaller.",
                "Once recorded as part of the land it is treated like any other structure on that "
                "ground, which opens up ordinary real-estate lending. On the same physical home, "
                "that difference is worth real money to a seller.",
            ]),
            ("What it takes to record it", [
                "The owner has to hold the land under it in one of three ways: own it outright, "
                "hold a <strong>recorded leasehold estate of 20 years or more</strong> where the "
                "lease specifically permits recording under the statute, or be a member of a "
                "nonprofit cooperative formed under ORS 62.800 to 62.815 that owns the land.",
                "The application goes to the <strong>county assessor</strong> on a form approved "
                "by the Department of Consumer and Business Services, and it has to describe the "
                "real property the structure is or will be sited on. A dealer can file it for the "
                "owner within set timeframes.",
                "This is the reason a home in a rented space in a park generally cannot be "
                "recorded. A month-to-month space rental is not a 20-year recorded leasehold.",
            ]),
            ("Recording is not the same as the tax roll", [
                "This is the distinction almost everyone collapses, and the statute is explicit "
                "that recording is independent of assessment and taxation of the structure as real "
                "property.",
                "Recording is about <strong>conveyance</strong> &mdash; it makes the structure "
                "subject to the same law as any other building on the land, lets mortgages, trust "
                "deeds and liens attach as real property, and stops the home being sold separately "
                "from the land without first being de-recorded.",
                "How the assessor classifies it for taxes is decided under the Department of "
                "Revenue's rules. Do not assume that because the tax statement looks a certain way "
                "the deed records agree with it. Check both.",
            ]),
            ("It can be undone", [
                "De-recording is a real process: the owner applies to the county assessor to have "
                "the structure removed from the deed records and an ownership document issued, and "
                "the assessor terminates the recording.",
                "That matters when a home is being moved off the land, or sold separately from it. "
                "It also means \"recorded\" is a current state to verify rather than a permanent "
                "fact to assume.",
            ]),
            ("What to check before you write the offer", [
                "Ask which it is, and get proof &mdash; the recorded document if it is real "
                "property, the ownership document if it is not. \"The seller thinks it was done "
                "years ago\" is not proof, and it is discovered at the worst possible moment.",
                "If it has not been recorded and it could be, that is often worth sorting out "
                "before listing rather than after. It widens the buyer pool at very little cost.",
                "If it sits in a park on a rented space, expect personal property and plan the "
                "financing accordingly &mdash; along with the park's own approval process, which "
                "is a separate hurdle with its own timeline.",
            ]),
        ],
        "sources": [
            ("ORS 446.626 &mdash; Recording manufactured structures in county deed records; "
             "effect on security interest; recording as establishment of real property interest",
             "https://oregon.public.law/statutes/ors_446.626"),
            ("OAR 150-308-0760 &mdash; Manufactured Structure Classified as Real or Personal "
             "Property",
             "https://oregon.public.law/rules/oar_150-308-0760"),
            ("Oregon Building Codes Division &mdash; Manufactured home ownership documents",
             "https://www.oregon.gov/bcd/man-home-own/pages/man-home-owner.aspx"),
            ("Application for recording manufactured home as real property (Form 5176)",
             "https://www.oregon.gov/bcd/Formslibrary/5176.pdf"),
        ],
        "seo_desc":
            "An Oregon manufactured home is personal property until recorded in county deed "
            "records under ORS 446.626. What recording requires, why it changes the financing, "
            "and why it is not the same as the assessor's tax classification.",
    },

    {
        "slug": "septic-site-evaluation-bare-land-oregon",
        "question": "How do I find out if bare land will pass for a septic system?",
        "title": "Septic Site Evaluation on Bare Land",
        "nav_label": "Site evaluation on bare land",
        "tag": "Septic",
        "verified": "14 August 2026",
        "short_answer":
            "You apply for a <strong>site evaluation</strong>. Under OAR 340-071-0150 it is the "
            "required first step before anyone can issue a construction-installation permit for a "
            "new system &mdash; you cannot get the permit without a site evaluation report finding "
            "the site suitable. You dig test pits and the county reads the soil in them. The state "
            "rule calls for at least two pits roughly 75 feet apart within the proposed system "
            "area including the repair area; <strong>Lane County asks for at least two and "
            "prefers three, 50 to 100 feet apart</strong>, each two feet wide, four feet long and "
            "five feet deep, stepped or ramped at one end so an inspector can walk in safely. What "
            "decides the outcome is soil type, soil depth and depth to the water table.",
        "sections": [
            ("Why this is the whole ballgame on bare land", [
                "A parcel with no septic approval is not a homesite yet. It is a bet. Price, "
                "views, road frontage and zoning are all irrelevant if the ground will not accept "
                "a drainfield, and around Veneta, Elmira and the Fern Ridge flats the water table "
                "is the thing that most often says no.",
                "This is why \"buildable lot\" in a listing deserves a follow-up question rather "
                "than a nod. Ask whether there is an approved site evaluation on file, and ask to "
                "see it.",
            ]),
            ("What the county is actually looking at", [
                "<strong>Soil type and depth.</strong> How much usable soil sits above whatever "
                "stops water &mdash; bedrock, hardpan, heavy clay.",
                "<strong>Depth to the water table.</strong> The one that catches valley-floor "
                "parcels. A site that looks bone dry in August can have water eighteen inches down "
                "in February, and the winter condition is the one that governs.",
                "<strong>Everything around it.</strong> Slope, parcel size, and distance to wells, "
                "streams, cuts, fills and property lines. Lane County's setbacks run 100 to 150 "
                "feet from wells and surface water, 50 to 100 feet from intermittent streams, and "
                "20 to 30 feet from property lines and foundations. On a small or awkward parcel "
                "the setbacks alone can eliminate every candidate area.",
            ]),
            ("What you have to do", [
                "Submit the application with the fee and a plot plan showing your proposed test "
                "pit locations, the wells, the property lines and all existing and proposed "
                "development.",
                "Dig the pits where the system would actually go &mdash; including the repair "
                "area, which people forget. The county needs to approve a place for the "
                "replacement system too, not just the first one.",
                "Then tell the county the pits are ready, put the green card with your site "
                "inspection number somewhere visible from the road, keep open pits covered so "
                "nobody and nothing falls in, and backfill once the evaluation is done.",
                "One more: do not regrade, fill or drive over the drainfield area after approval. "
                "Compaction and fill can undo the approval you just paid for.",
            ]),
            ("Timing, and the mistake that costs a year", [
                "Soil evaluation depends on reading the water table, so the wet season is often "
                "the informative time to look. That is a scheduling problem, not a technicality "
                "&mdash; a buyer who waits until spring to start can lose the window and end up "
                "waiting.",
                "If you are buying bare land, make the site evaluation a condition of the sale "
                "with enough inspection period to actually complete it, or accept that you are "
                "buying the risk. Those are the two honest options. Closing first and evaluating "
                "afterward is how people end up owning ground they cannot build on.",
            ]),
        ],
        "sources": [
            ("OAR 340-071-0150 &mdash; Site Evaluation Procedures",
             "https://oregon.public.law/rules/oar_340-071-0150"),
            ("Lane County &mdash; Test Pit Information",
             "https://www.lanecounty.org/government/county_departments/public_works/land_management_division/on-_site_wastewater/test_pit_information"),
            ("OAR 340-071-0130 &mdash; General Standards, Prohibitions and Requirements",
             "https://oregon.public.law/rules/oar_340-071-0130"),
            ("Oregon DEQ &mdash; Onsite Wastewater Treatment System Rules (OAR 340-071/073)",
             "https://www.oregon.gov/deq/Residential/Documents/OAR340-071-073.pdf"),
        ],
        "seo_desc":
            "A septic site evaluation is the required first step before a permit on Oregon bare "
            "land. Lane County test pit requirements, the setbacks that eliminate small parcels, "
            "and why the water table decides it.",
    },

    {
        "slug": "farm-dwelling-income-test-oregon",
        "question": "How much farm income do I need to build a farm dwelling?",
        "title": "Oregon Farm Dwelling Income Test",
        "nav_label": "The farm income test",
        "tag": "Land use",
        "verified": "14 August 2026",
        "short_answer":
            "On <strong>high-value farmland</strong> the tract must have produced at least "
            "<strong>$80,000</strong> in gross annual income from the sale of farm products. On "
            "land <strong>not</strong> identified as high-value farmland the figure is "
            "<strong>$40,000</strong> &mdash; or the midpoint of the county's median income range "
            "from the 1992 Census of Agriculture, whichever applies. Either threshold has to be "
            "met in each of the last two years, or in three of the last five years, or as an "
            "average of three of the last five. The counting is strict: the cost of purchased "
            "livestock comes off the top, only income from land you <em>own</em> counts &mdash; "
            "not leased or rented ground &mdash; and income already used to qualify another "
            "dwelling cannot be used again.",
        "sections": [
            ("Note which number goes with which land", [
                "It reads backwards to most people, so it is worth stating twice: the "
                "<strong>higher</strong> bar, $80,000, applies to <strong>high-value</strong> "
                "farmland. The $40,000 figure is for ground that is not high-value.",
                "The logic follows from what the rules are protecting. The better the soil, the "
                "more the state wants proof that a house on it is genuinely serving a working farm "
                "rather than a rural homesite with a hobby attached.",
            ]),
            ("Gross, but not as gross as you would like", [
                "It is gross income from the sale of farm products, not net &mdash; you are not "
                "deducting your expenses. But three limits do real damage to the arithmetic:",
                "<strong>Purchased livestock comes off.</strong> Buy calves for $30,000 and sell "
                "them for $50,000 and you have contributed $20,000, not $50,000. This ends most "
                "quick paths to a qualifying number.",
                "<strong>Owned land only.</strong> Income earned off leased or rented ground does "
                "not count toward your tract. Farming 200 leased acres does not qualify your 40.",
                "<strong>No double-dipping.</strong> Gross farm income already used to qualify "
                "another parcel's dwelling cannot be reused for this one.",
            ]),
            ("The years matter as much as the money", [
                "One outstanding year does not do it. You need each of the last two years, or "
                "three of the last five, or an average across three of the last five.",
                "That means this is a multi-year project rather than a box to tick before an "
                "application. If building a farm dwelling is the plan, the income record has to be "
                "built first &mdash; deliberately, with documentation, in the name of the tract.",
                "Keep the paperwork as you go: Schedule F, sales receipts, settlement sheets. The "
                "county will want to see it, and reconstructing four-year-old cash sales at the "
                "hay barn is not a thing that can be done.",
            ]),
            ("If the income is not there", [
                "Then the farm dwelling route is not your route, and the honest move is to find "
                "out which one is &mdash; before you buy, not after. A lot of record dwelling "
                "turns on the 1 January 1985 ownership test. Forest ground has its own template "
                "dwelling test. Replacement dwellings have their own rules again.",
                "Ask the county planner assigned to your parcel which route, if any, is open. It "
                "is one phone call and it is the difference between land you can live on and land "
                "you can look at.",
            ]),
        ],
        "sources": [
            ("OAR 660-033-0135 &mdash; Dwellings in Conjunction with Farm Use",
             "https://oregon.public.law/rules/oar_660-033-0135"),
            ("ORS 215.213 &mdash; Uses permitted in exclusive farm use zones in counties that "
             "adopted marginal lands system prior to 1993",
             "https://oregon.public.law/statutes/ors_215.213"),
            ("ORS 215.283 &mdash; Uses permitted in exclusive farm use zones in nonmarginal "
             "lands counties",
             "https://oregon.public.law/statutes/ors_215.283"),
            ("Lane County &mdash; Farm Dwellings handout (Land Management Division)",
             "https://www.lanecounty.org/government/county_departments/public_works/land_management_division"),
        ],
        "seo_desc":
            "Oregon farm dwelling income test: $80,000 gross farm income on high-value farmland, "
            "$40,000 on land that is not. The year requirements, why purchased livestock is "
            "deducted, and why leased ground does not count.",
    },

    {
        "slug": "partition-acreage-oregon",
        "question": "Can I split my acreage and sell off a piece?",
        "title": "Partitioning Acreage in Oregon",
        "nav_label": "Splitting acreage",
        "tag": "Land use",
        "verified": "14 August 2026",
        "short_answer":
            "Maybe, and the first thing to get straight is which process you are in. Under ORS "
            "92.010 dividing a tract into <strong>two or three parcels within one calendar "
            "year</strong> is a <strong>partition</strong>; producing <strong>four or more</strong> "
            "units makes it a <strong>subdivision</strong>, with substantially heavier "
            "requirements. The count is by calendar year across all divisions of that tract, so "
            "you cannot take three this year and call next year's fourth a fresh partition of the "
            "same ground without consequence. On top of Chapter 92, resource zoning applies its "
            "own minimum parcel sizes &mdash; and on EFU or forest ground those minimums are "
            "usually what actually stops the split, not the partition process.",
        "sections": [
            ("Partition or subdivision", [
                "A partition creates parcels. A subdivision creates lots. The words are not "
                "decorative &mdash; they select which body of law and which county process you are "
                "subject to, and partitions are meaningfully less burdensome.",
                "The line is drawn by counting the units produced by one or more divisions of the "
                "same tract in a single calendar year: three or fewer are parcels, four or more "
                "are lots.",
            ]),
            ("Zoning is the harder gate", [
                "Chapter 92 tells you the procedure. Your zone tells you whether there is anything "
                "to procedure about. EFU and forest zones carry minimum parcel sizes that are "
                "large by design, and the entire point of resource zoning is to stop working "
                "ground being chipped into homesites.",
                "So the sequence is: find out your zone and its minimum parcel size first. If the "
                "split you have in mind would create a parcel under that minimum, the partition "
                "process is not the obstacle &mdash; the zone is, and no amount of surveying gets "
                "around it.",
            ]),
            ("What the county will want to see", [
                "Legal access to each new parcel. A parcel with no enforceable access to a public "
                "road is a problem you are creating for yourself and for whoever buys it.",
                "Septic feasibility for any parcel intended to be built on &mdash; which means a "
                "site evaluation, which means test pits.",
                "Water. Whether each parcel can actually be served, and on what.",
                "A survey and a recorded partition plat. This is a real project with real cost and "
                "a real timeline, not a paperwork afternoon.",
            ]),
            ("The consequences people miss", [
                "<strong>Special assessment.</strong> If the ground is in farm or forest deferral, "
                "understand what the split and the resulting use do to that status before you "
                "start. Recording a subdivision plat is itself a disqualifying event for farm use "
                "special assessment.",
                "<strong>Dwelling rights.</strong> Splitting can change what is approvable on what "
                "is left. Where a lot of record dwelling is allowed, the remainder of the tract "
                "gets consolidated &mdash; you do not get a house and keep the pieces separately "
                "saleable.",
                "<strong>The value question.</strong> Two parcels are not automatically worth more "
                "than one. Sometimes they are worth less, because the thing that made the property "
                "desirable was that it was whole.",
            ]),
            ("Start here", [
                "Call Lane County Land Management with your tax lot number and ask two questions: "
                "what is the minimum parcel size in this zone, and is a partition of this tract "
                "approvable at all. Free, and it saves surveyor money on parcels where the answer "
                "was always no.",
                "If the answer is yes, the next calls are a surveyor and a land use planner. If "
                "the ground is in deferral, add your CPA before anything is recorded.",
            ]),
        ],
        "sources": [
            ("ORS 92.010 &mdash; Definitions for ORS 92.010 to 92.192",
             "https://oregon.public.law/statutes/ors_92.010"),
            ("ORS 92.075 &mdash; Declaration required to subdivide or partition property; contents",
             "https://oregon.public.law/statutes/ors_92.075"),
            ("ORS Chapter 92 &mdash; Subdivisions and Partitions",
             "https://www.oregonlegislature.gov/bills_laws/ors/ors092.html"),
            ("ORS 308A.116 &mdash; Disqualification of nonexclusive farm use zone farmland",
             "https://oregon.public.law/statutes/ors_308a.116"),
        ],
        "seo_desc":
            "Splitting Oregon acreage: two or three parcels in a calendar year is a partition, "
            "four or more is a subdivision (ORS 92.010). Why zoning minimums — not the partition "
            "process — usually decide it, and what a split does to farm deferral.",
    },

    {
        "slug": "landlocked-property-legal-access-oregon",
        "question": "What happens if a property has no legal access?",
        "title": "Landlocked Property and Legal Access",
        "nav_label": "Landlocked and legal access",
        "tag": "Access",
        "verified": "14 August 2026",
        "short_answer":
            "A driveway is not legal access. What matters is whether there is a <strong>recorded, "
            "enforceable right</strong> to cross the ground between the parcel and a public road. "
            "An easement appurtenant attaches to the property and transfers automatically with it "
            "&mdash; it cannot be sold off separately from the land it serves. Where there is "
            "genuinely no access and no right to any, Oregon allows a landowner to petition for a "
            "<strong>statutory way of necessity</strong> under ORS 376.150 to 376.200. It is a "
            "real remedy but a slow, contested and expensive one, it requires proving you have no "
            "enforceable access at all, and a way of necessity created this way "
            "<strong>must be open to public use</strong>. If you already have enforceable access, "
            "you do not qualify &mdash; even if what you have is inconvenient.",
        "sections": [
            ("\"We've always driven in that way\" is not a right", [
                "Long use with a neighbour's blessing is a permission, and permissions end &mdash; "
                "when the neighbour sells, when the neighbour dies, when the neighbour's new "
                "spouse takes a different view.",
                "The question is not how people get to the property. It is what is recorded. Ask "
                "the title company to show you the access easement, and read it.",
            ]),
            ("What an easement appurtenant actually does", [
                "It attaches to the ownership interest and becomes part of it. Transfer the "
                "property and the easement goes with it automatically; it cannot be transferred "
                "independently of the land it benefits.",
                "That is the protection you want, and it is why the recorded document matters more "
                "than the gravel. Read it for what it actually grants: who may use it, for what, "
                "how wide it is, whether it permits utilities, and who maintains it.",
                "<strong>Maintenance is where the arguments live.</strong> A shared road with no "
                "maintenance agreement is a dispute with a delay on it. If the easement is silent, "
                "that silence is a term of your purchase.",
            ]),
            ("The way of necessity, honestly described", [
                "Where a parcel is landlocked with no other access easement, ORS 376.150 and "
                "following let the owner petition for a way of necessity across another's land to "
                "reach a public road. The petition has to name a specific proposed location and "
                "show that the petitioner has no existing easement, no right to one, and no "
                "enforceable access.",
                "Two conditions people do not expect. First, if you <em>do</em> have enforceable "
                "access, you are not entitled to a way of necessity &mdash; regardless of whether "
                "your access is reasonable or convenient. Second, a way of necessity created under "
                "these sections <strong>must be open to public use</strong>. You are not obtaining "
                "a private driveway.",
                "It is a proceeding against a neighbour who does not want it, with compensation, "
                "counsel and time attached. Treat it as the last resort it is, not as a reason to "
                "buy a landlocked parcel cheap.",
            ]),
            ("Before you buy", [
                "Get the title report and find the access. If your agent or the title officer "
                "cannot point to a recorded easement running from the parcel to a public road, "
                "assume there is not one until somebody proves otherwise.",
                "Check the road at the other end too. A recorded easement onto a road that is "
                "itself private, or a road nobody has accepted for maintenance, moves the problem "
                "rather than solving it.",
                "And ask the lender early. Access problems affect insurability and financing, and "
                "it is better to learn that in week one than in week five.",
            ]),
        ],
        "sources": [
            ("ORS 376.150 to 376.200 &mdash; Ways of necessity (ORS Chapter 376)",
             "https://www.oregonlegislature.gov/bills_laws/ors/ors376.html"),
            ("ORS 376.155 &mdash; Petition to establish way of necessity; contents; requirements",
             "https://oregon.public.law/statutes/ors_376.155"),
            ("ORS 376.180 &mdash; Conditions for way of necessity",
             "https://oregon.public.law/statutes/ors_376.180"),
        ],
        "seo_desc":
            "A driveway is not legal access. What a recorded easement appurtenant gives you, and "
            "how Oregon's statutory way of necessity under ORS 376.150 actually works — including "
            "why it must be open to public use.",
    },

    {
        "slug": "shared-well-agreement-oregon",
        "question": "The house shares a well with a neighbour. What should I check?",
        "title": "Shared Well Agreements in Oregon",
        "nav_label": "Shared wells",
        "tag": "Wells",
        "verified": "14 August 2026",
        "short_answer":
            "Whether there is a <strong>recorded shared well agreement</strong>, and what it says. "
            "A shared well without a recorded agreement is a financing problem and a future "
            "dispute at the same time &mdash; mortgage lenders generally require one before they "
            "will lend, and the government-backed programs are explicit about wanting it recorded "
            "so that it binds current <em>and future</em> owners rather than just the two "
            "neighbours who shook hands. The agreement should cover who owns the well, who may use "
            "how much, how maintenance and repair costs are split, who has physical access to the "
            "well head and equipment, and what happens when the pump fails at 11pm in January.",
        "sections": [
            ("Recorded is the word that matters", [
                "An unrecorded arrangement binds the people who signed it, not the person who buys "
                "next door in three years. Recording is what attaches the arrangement to both "
                "properties so it survives a sale.",
                "This is also what lenders look for. Expect a recorded agreement, along with a "
                "permanent easement covering physical access to the well and the water line, to be "
                "a condition rather than a nicety &mdash; particularly on FHA and VA financing, "
                "where the requirement is long-standing.",
                "Lender guidelines change and individual lenders add their own overlays, including "
                "on minimum yield and on how many homes may share one well. Confirm the current "
                "requirements with the actual lender early, because this is a condition that can "
                "surface late and stall a closing.",
            ]),
            ("What the agreement needs to say", [
                "<strong>Who owns the well</strong>, and whose land it sits on.",
                "<strong>Access.</strong> A permanent, recorded easement for getting to the well "
                "head, the pump and the line &mdash; including for a repair crew. Right to the "
                "water is worthless without the right to reach the equipment.",
                "<strong>Cost sharing.</strong> How routine maintenance, power, testing and "
                "capital repairs are split, and how a party who will not pay gets dealt with.",
                "<strong>Use limits.</strong> What each household may draw, and what happens in a "
                "dry summer when the well cannot serve both at full tilt.",
                "<strong>Failure and replacement.</strong> Who decides, who contracts, who fronts "
                "the money, and what happens if the well has to be redrilled somewhere else.",
                "<strong>Water testing.</strong> Who tests, how often, and who pays &mdash; "
                "separate from the seller's own testing obligation on a sale.",
            ]),
            ("Do the physical diligence too", [
                "Pull the well log through the Water Resources Department and look at the depth "
                "and the yield at completion. One well serving two households is doing twice the "
                "work, and a modest yield that is fine for one house can be marginal for two.",
                "Find out where the well, the pressure tank and the lines actually are, and whose "
                "power runs the pump. A pump on the neighbour's meter is an arrangement waiting to "
                "become an argument.",
                "Ask what has actually happened. Has it run dry in a hot August? Has the pump been "
                "replaced? Who paid, and did anybody argue about it?",
            ]),
            ("If there is no agreement", [
                "Getting one drafted and recorded before closing is usually the cleanest fix, and "
                "it is far easier while the seller still has a reason to cooperate. After closing "
                "you are asking a neighbour for a favour with nothing to trade.",
                "If the neighbour will not sign, that tells you something worth knowing about the "
                "next ten years, and it belongs in your decision rather than in your hopes.",
            ]),
        ],
        "sources": [
            ("Oregon Water Resources Department &mdash; Well Report Query",
             "https://apps.wrd.state.or.us/apps/gw/well_log/"),
            ("ORS 448.271 &mdash; Transfer of property that includes well; testing; effect",
             "https://oregon.public.law/statutes/ors_448.271"),
            ("Water Systems Council &mdash; Shared Well Agreements (wellcare information sheet)",
             "https://www.watersystemscouncil.org/download/wellcare_information_sheets/other_information_sheets/Shared_Well_Agreement.pdf"),
            ("Water Systems Council &mdash; Sharing a Well",
             "https://www.watersystemscouncil.org/download/wellcare_information_sheets/other_information_sheets/Sharing_a_Well.pdf"),
        ],
        "seo_desc":
            "Buying a house on a shared well in Oregon: why the agreement must be recorded to bind "
            "future owners, what it needs to cover, and the physical diligence to do on a well "
            "serving two households.",
    },

    {
        "slug": "floodplain-development-lane-county-oregon",
        "question": "The property is in a flood zone. What does that actually mean?",
        "title": "Flood Zones and Building in Lane County",
        "nav_label": "Flood zones",
        "tag": "Floodplain",
        "verified": "14 August 2026",
        "short_answer":
            "It means development there is regulated, and that the rules come from your "
            "<strong>city or county</strong> rather than from the state. Oregon's Department of "
            "Land Conservation and Development is explicit that cities and counties adopt the "
            "floodplain maps and regulations and issue floodplain development permits locally "
            "&mdash; there is no single statewide elevation standard to quote you. In a Special "
            "Flood Hazard Area you will generally need a <strong>floodplain development "
            "permit</strong> before building, and how far above the base flood elevation your "
            "lowest floor must sit is set by the local ordinance. For anything in Lane County, get "
            "that number from Land Management directly, in writing, before you design anything.",
        "sections": [
            ("Why I will not quote you an elevation figure", [
                "Local freeboard requirements are adopted locally and they change. Publishing a "
                "number that is out of date, on a page a buyer might rely on to size a foundation, "
                "would be worse than publishing nothing.",
                "So this page tells you what to ask and who to ask. The specific requirement for "
                "your parcel comes from Lane County Land Management Division, 3050 N. Delta "
                "Highway, Eugene &mdash; phone (541) 682-4651.",
            ]),
            ("The words on the map", [
                "<strong>Special Flood Hazard Area (SFHA).</strong> The area FEMA maps as having a "
                "1% annual chance of flooding &mdash; the \"100-year flood\", which is a "
                "probability, not a schedule. Two in ten years is entirely possible.",
                "<strong>Base flood elevation (BFE).</strong> How high the water is expected to "
                "reach in that event. Local rules are written in terms of height above it.",
                "<strong>Zone A versus Zone AE.</strong> Both are high-risk. The difference is "
                "study: AE zones have a determined base flood elevation, A zones do not &mdash; "
                "they were mapped without a detailed engineering study, so no BFE was established. "
                "An A zone is not lower risk than an AE zone; it is less measured. In practice "
                "that can mean you have to produce the elevation data yourself.",
                "<strong>Floodway.</strong> The channel and the adjoining land needed to carry the "
                "flood. This is the most restricted designation and the one most likely to make a "
                "building site unusable.",
            ]),
            ("What it does to the transaction", [
                "<strong>Insurance.</strong> A federally backed lender will require flood "
                "insurance on a structure in an SFHA. Get an actual quote during your inspection "
                "period &mdash; it is a permanent line in the monthly cost and it can be "
                "substantial.",
                "<strong>An elevation certificate</strong> documents where the building actually "
                "sits relative to the BFE, and it is what an insurer prices from. If the seller "
                "has one, get it. If not, factor in obtaining one.",
                "<strong>Permits and design.</strong> Elevation, flood-resistant construction, "
                "anchoring and where the mechanical equipment sits are all constrained. This is a "
                "cost and design conversation to have before you are committed, not after.",
            ]),
            ("Around Fern Ridge and the Long Tom", [
                "West Lane County has genuine flood geography &mdash; Fern Ridge Reservoir sits on "
                "the Long Tom River, and the low ground around it and its tributaries floods.",
                "It does not make property there a bad buy. Plenty of good land carries a flood "
                "designation on part of it, and where the mapped area falls on a parcel matters "
                "enormously &mdash; a floodway across the back pasture is a very different fact "
                "from an AE zone under the house site.",
                "Send me an address and I will pull what the county has mapped for it before you "
                "spend money on anything else.",
            ]),
        ],
        "sources": [
            ("Oregon DLCD &mdash; National Flood Insurance Program (NFIP) in Oregon",
             "https://www.oregon.gov/lcd/NH/Pages/NFIP.aspx"),
            ("FEMA &mdash; Permit for Floodplain Development",
             "https://www.fema.gov/about/glossary/permit-floodplain-development"),
            ("Lane County &mdash; Land Management Division",
             "https://www.lanecounty.org/government/county_departments/public_works/land_management_division"),
        ],
        "seo_desc":
            "What a flood zone means for an Oregon property: SFHA, base flood elevation, Zone A vs "
            "AE vs floodway, and why the elevation requirement comes from the county rather than "
            "the state. Fern Ridge and Long Tom context.",
    },

]
