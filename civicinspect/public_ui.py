"""Static public UI shell for CivicInspect v0.1.0."""

from __future__ import annotations


def render_public_lookup_page() -> str:
    """Render the public-facing CivicInspect sample page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicInspect Inspection Support</title>
<style>
  :root { --ink:#18212a; --muted:#526170; --paper:#fffaf2; --blue:#174f68; --green:#27604b; --gold:#d8ad48; --line:#d8c7a5; }
  * { box-sizing: border-box; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:linear-gradient(135deg,#fff6e8,#e8f3f4); }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:999px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1120px, calc(100% - 32px)); margin:0 auto; }
  header { padding:48px 0 24px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:.18em; font-weight:800; font-size:.78rem; }
  h1 { max-width:980px; margin:0; font-family:Georgia,"Times New Roman",serif; font-size:clamp(2.7rem,7vw,5.7rem); line-height:.95; letter-spacing:-.05em; }
  .lede { max-width:820px; font-size:clamp(1.1rem,2.4vw,1.45rem); line-height:1.55; color:#31404a; }
  .badge { display:inline-flex; width:fit-content; padding:.45rem .75rem; border-radius:999px; background:var(--green); color:white; font-weight:900; }
  .grid { display:grid; grid-template-columns:repeat(12,1fr); gap:18px; }
  .card { grid-column:span 6; min-width:0; padding:24px; border:1px solid var(--line); border-radius:28px; background:rgba(255,250,242,.92); box-shadow:0 18px 40px rgba(35,43,50,.10); }
  .card.large { grid-column:span 12; }
  h2,h3 { font-family:Georgia,"Times New Roman",serif; letter-spacing:-.03em; }
  h2 { margin:0 0 14px; font-size:clamp(1.8rem,4vw,3rem); }
  p, li { line-height:1.65; }
  textarea, button { width:100%; border:1px solid #b9c6cc; border-radius:16px; padding:.85rem 1rem; font:inherit; }
  textarea { background:#f5f8f8; color:var(--ink); }
  button { width:fit-content; min-width:190px; border:0; background:var(--blue); color:white; font-weight:900; cursor:default; }
  .result { margin-top:18px; padding:18px; border-left:6px solid var(--green); border-radius:18px; background:white; }
  .warning { border-left-color:#b2603f; background:#fff8f4; }
  .kicker { color:var(--muted); font-size:.86rem; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
  footer { padding:38px 0 56px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:760px) { header{padding-top:34px}.card{grid-column:span 12;padding:20px;border-radius:22px}button{width:100%} }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicInspect public sample</p>
  <h1>Turn field notes into review-ready inspection drafts.</h1>
  <p class="lede">CivicInspect demonstrates inspection support: sample repeat-case lookup, inspector-owned report drafting, notice draft support, and records-ready exports without issuing findings or replacing the system of record.</p>
  <p><span class="badge">v0.1.0 inspection support foundation</span></p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-labelledby="lookup-title">
    <article class="card large">
      <p class="kicker">Sample repeat-case lookup</p>
      <h2 id="lookup-title">100 Main Street nuisance inspection</h2>
      <textarea aria-label="Sample inspection notes" rows="4">Inspector observed overgrown vegetation near the alley and two prior related cases for the same property.</textarea>
      <button type="button">Draft sample report</button>
      <div class="result" role="status" aria-live="polite">
        <h3>Draft report support</h3>
        <ul><li>Preserve inspector-entered observations.</li><li>Show related sample case identifiers.</li><li>Require staff review before any notice is issued.</li></ul>
      </div>
    </article>
    <article class="card"><p class="kicker">Inspector-owned</p><h2>Humans decide</h2><div class="result"><p>Every draft is explicitly marked for inspector review; CivicInspect does not make findings, issue citations, or assess fines.</p></div></article>
    <article class="card"><p class="kicker">Notice support</p><h2>Draft, not issuance</h2><div class="result"><p>Notice drafts list required staff actions: confirm code section, ownership, address, and repeat-case context.</p></div></article>
    <article class="card"><p class="kicker">Records-ready export</p><h2>Keep provenance</h2><div class="result"><p>Exports preserve notes, draft text, reviewer, review date, and system-of-record links.</p></div></article>
    <article class="card large"><p class="kicker">Boundary</p><h2>No official inspection action</h2><div class="result warning"><p>CivicInspect does not issue official findings, citations, fines, notices, inspection schedules, or system-of-record updates.</p></div></article>
  </section>
</main>
<footer><p>CivicInspect is part of the Apache 2.0 CivicSuite open-source municipal AI project.</p></footer>
</body>
</html>
"""
