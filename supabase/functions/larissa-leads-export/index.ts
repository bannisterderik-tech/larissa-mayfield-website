// larissa-leads-export: the website's leads, read back out of Follow Up Boss,
// for the spreadsheet her box keeps (vault/leads/website-leads.xlsx).
//
// FUB is the record; this only reads. It walks FUB's events newest first,
// keeps the ones the site sent (by source: FUB does not return the system
// name on a read), and returns
// each with the person's name, email and phone. Called by her box only.
//
// The caller proves itself with X-Export-Key. Only the key's SHA-256 lives
// here; the key itself is in her box's env, nowhere else. The FUB key is the
// FUB_API_KEY secret, shared with larissa-fub-lead, and never leaves.

const KEY_SHA256 = 'bcea15c53694e4993dc37955962666f24301881a98c744dbc9c9a07f4100d278'
const SYSTEM = 'LarissaMayfieldWebsite'
// What larissa-fub-lead writes as the source. The first, mistyped domain is
// kept so the few leads sent under it on 9 Oct 2026 still count.
const SOURCES = new Set(['larissamayfieldre.com', 'larissamayfield.com'])

async function sha256(s: string) {
  const d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s))
  return Array.from(new Uint8Array(d)).map((b) => b.toString(16).padStart(2, '0')).join('')
}

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } })

Deno.serve(async (req) => {
  if (req.method !== 'GET') return json({ ok: false, error: 'GET only' }, 405)
  const given = req.headers.get('X-Export-Key') || ''
  if (!given || (await sha256(given)) !== KEY_SHA256) return json({ ok: false, error: 'not allowed' }, 401)
  const key = Deno.env.get('FUB_API_KEY')
  if (!key) return json({ ok: false, error: 'FUB_API_KEY is not set' }, 500)

  const url = new URL(req.url)
  // Only events newer than this are needed; the box keeps the rest.
  const since = url.searchParams.get('since') || '1970-01-01T00:00:00Z'
  const auth = { 'Authorization': 'Basic ' + btoa(key + ':'), 'X-System': SYSTEM }
  // FUB throttles reads hard. On a 429, wait what it asks (or a few seconds)
  // and try again, up to four times, before giving up for this run.
  const fub = async (path: string) => {
    for (let tryN = 0; ; tryN++) {
      const r = await fetch('https://api.followupboss.com/v1' + path, { headers: auth })
      if (r.status === 429 && tryN < 4) {
        const wait = Math.min(15, Number(r.headers.get('Retry-After')) || 3 + tryN * 3)
        await new Promise((ok) => setTimeout(ok, wait * 1000))
        continue
      }
      if (!r.ok) throw new Error(`FUB ${path.split('?')[0]} ${r.status}`)
      return r.json()
    }
  }

  try {
    // ?debug=1: how FUB labels its newest events, with no names or contacts,
    // for when the filter below stops matching.
    if (url.searchParams.get('debug') === '1') {
      const r = await fub('/events?sort=-created&limit=25')
      const ev = (r.events ?? []) as Record<string, any>[]
      return json({ ok: true, keys: ev[0] ? Object.keys(ev[0]) : [], events: ev.map((e) => ({ created: e.created, system: e.system, source: e.source, type: e.type, hasPerson: Boolean(e.personId) })) })
    }
    const out: Record<string, unknown>[] = []
    const people = new Map<number, Record<string, any>>()
    // Newest first, 100 at a time, stopping at the first event older than
    // `since`. Twenty pages is two thousand events of every kind, far more
    // than a run between two box syncs.
    for (let page = 0, done = false; page < 20 && !done; page++) {
      const r = await fub(`/events?sort=-created&limit=100&offset=${page * 100}`)
      const events = (r.events ?? []) as Record<string, any>[]
      if (!events.length) break
      for (const e of events) {
        if (String(e.created) <= since) { done = true; break }
        if (!SOURCES.has(String(e.source))) continue
        const pid = Number(e.personId)
        if (pid && !people.has(pid)) people.set(pid, await fub(`/people/${pid}`).catch(() => ({})))
        const p = people.get(pid) ?? {}
        const first = (v: unknown) => (Array.isArray(v) && v[0] && typeof v[0].value === 'string' ? v[0].value : '')
        out.push({
          id: e.id, created: e.created, type: e.type, page: e.description ?? '', notes: e.message ?? '',
          personId: pid || null, name: p.name ?? [p.firstName, p.lastName].filter(Boolean).join(' '),
          email: first(p.emails), phone: first(p.phones),
          tags: Array.isArray(p.tags) ? p.tags : [], stage: p.stage ?? '',
          fubUrl: pid ? `https://app.followupboss.com/2/people/view/${pid}` : '',
        })
      }
      if (events.length < 100) break
    }
    return json({ ok: true, since, leads: out })
  } catch (e) {
    console.error('[larissa-leads-export]', (e as Error).message)
    return json({ ok: false, error: (e as Error).message }, 502)
  }
})
