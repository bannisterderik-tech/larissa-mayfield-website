// larissa-fub-lead: hands a lead from larissamayfield.com to Follow Up Boss.
//
// Deployed to Supabase project ayskxkjorhoaknkqtyvm. The site's forms post
// here and to RealtyGrind's webhook-receive at the same time; this one is
// only for FUB. Self-contained on purpose: nothing from the shared
// RealtyGrind code, so neither side can break the other.
//
// The key lives in the FUB_API_KEY secret on that project and never leaves
// this function. Leads go through /v1/events, not /v1/people, because that
// is what fires FUB's lead routing and action plans.

const ALLOWED_ORIGINS = [
  'https://larissamayfield.com',
  'https://www.larissamayfield.com',
  'https://bannisterderik-tech.github.io',
]
const isAllowed = (o: string) =>
  ALLOWED_ORIGINS.includes(o) || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(o)

function cors(origin: string): Record<string, string> {
  return {
    'Access-Control-Allow-Origin': isAllowed(origin) ? origin : ALLOWED_ORIGINS[0],
    'Access-Control-Allow-Headers': 'content-type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Vary': 'Origin',
  }
}

function json(body: unknown, origin: string, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors(origin), 'Content-Type': 'application/json' },
  })
}

// Per-IP cap. In-memory, so it resets on cold start; it only has to stop a
// burst, the form's own honeypot and time trap stop the rest.
const hits = new Map<string, { n: number; until: number }>()
function limited(ip: string) {
  const now = Date.now()
  const h = hits.get(ip)
  if (!h || h.until < now) { hits.set(ip, { n: 1, until: now + 3600_000 }); return false }
  return ++h.n > 20
}

const str = (v: unknown) => (typeof v === 'string' ? v.trim() : '')

function eventType(leadType: string, source: string) {
  if (leadType === 'seller') return 'Seller Inquiry'
  if (source.includes('(showing)')) return 'Property Inquiry'
  if (source.includes('(guide)')) return 'Registration'
  return 'General Inquiry'
}

Deno.serve(async (req) => {
  const origin = req.headers.get('Origin') || ''
  if (req.method === 'OPTIONS') return new Response(null, { headers: cors(origin) })
  if (req.method !== 'POST') return json({ ok: false, error: 'POST only' }, origin, 405)
  if (origin && !isAllowed(origin)) return json({ ok: false, error: 'Origin not allowed' }, origin, 403)

  const ip = (req.headers.get('x-forwarded-for') || '').split(',')[0].trim() || 'unknown'
  if (limited(ip)) return json({ ok: false, error: 'Too many requests' }, origin, 429)

  const key = Deno.env.get('FUB_API_KEY')
  if (!key) {
    console.error('[larissa-fub-lead] FUB_API_KEY is not set')
    return json({ ok: false }, origin, 500)
  }

  const b = await req.json().catch(() => ({})) as Record<string, unknown>
  const name = str(b.name)
  const email = str(b.email)
  const phone = str(b.phone)
  if (!name || (!email && !phone)) {
    return json({ ok: false, error: 'name and an email or phone are required' }, origin, 400)
  }
  const [firstName, ...rest] = name.split(/\s+/)
  const leadType = str(b.lead_type)
  const source = str(b.source)
  const tags = Array.isArray(b.tags) ? b.tags.filter((t) => typeof t === 'string') : []
  let message = str(b.notes)
  if (leadType === 'privacy_request' && !message.startsWith('⚠')) {
    message = '⚠ CCPA / DO-NOT-SELL REQUEST — DO NOT MARKET TO THIS PERSON' + (message ? ' | ' + message : '')
  }

  const event: Record<string, unknown> = {
    source: 'larissamayfield.com',
    system: 'LarissaMayfieldWebsite',
    type: eventType(leadType, source),
    message: message || undefined,
    description: source || undefined,
    person: {
      firstName,
      lastName: rest.join(' ') || undefined,
      emails: email ? [{ value: email }] : undefined,
      phones: phone ? [{ value: phone }] : undefined,
      tags,
    },
  }
  const street = str(b.seller_listing_address)
  const mls = str(b.seller_listing_mls)
  if (street || mls) event.property = { street: street || undefined, mlsNumber: mls || undefined }

  const r = await fetch('https://api.followupboss.com/v1/events', {
    method: 'POST',
    headers: {
      'Authorization': 'Basic ' + btoa(key + ':'),
      'Content-Type': 'application/json',
      'X-System': 'LarissaMayfieldWebsite',
    },
    body: JSON.stringify(event),
  })
  if (r.status === 200 || r.status === 201 || r.status === 204) return json({ ok: true }, origin)

  console.error('[larissa-fub-lead] FUB rejected the event:', r.status, (await r.text()).slice(0, 500))
  return json({ ok: false }, origin, 502)
})
