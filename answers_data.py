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

]
