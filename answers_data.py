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

]
