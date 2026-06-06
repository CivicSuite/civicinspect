"""Static public UI shells for CivicInspect v0.2.2."""

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
  :root { --ink:#17202a; --muted:#526170; --paper:#fffaf2; --blue:#174f68; --green:#27604b; --gold:#d8ad48; --line:#d8c7a5; --warn:#8f4a2b; }
  * { box-sizing: border-box; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:linear-gradient(135deg,#fff6e8,#e8f3f4); }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:8px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1120px, calc(100% - 32px)); margin:0 auto; }
  header { padding:48px 0 24px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; font-weight:800; font-size:.78rem; }
  h1 { max-width:980px; margin:0; font-family:Georgia,"Times New Roman",serif; font-size:4.8rem; line-height:1; }
  .lede { max-width:820px; font-size:1.25rem; line-height:1.55; color:#31404a; }
  .badge { display:inline-flex; width:fit-content; padding:.45rem .75rem; border-radius:8px; background:var(--green); color:white; font-weight:900; }
  .grid { display:grid; grid-template-columns:repeat(12,1fr); gap:18px; }
  .panel { grid-column:span 6; min-width:0; padding:24px; border:1px solid var(--line); border-radius:8px; background:rgba(255,250,242,.92); box-shadow:0 18px 40px rgba(35,43,50,.10); }
  .panel.large { grid-column:span 12; }
  h2,h3 { font-family:Georgia,"Times New Roman",serif; }
  h2 { margin:0 0 14px; font-size:2.2rem; }
  p, li { line-height:1.65; }
  label { display:block; margin:.9rem 0 .35rem; font-weight:800; }
  input, textarea, select, button { width:100%; border:1px solid #b9c6cc; border-radius:8px; padding:.85rem 1rem; font:inherit; }
  input, textarea, select { background:#f5f8f8; color:var(--ink); }
  button { width:fit-content; min-width:190px; margin-top:1rem; border:0; background:var(--blue); color:white; font-weight:900; cursor:pointer; }
  button:disabled { opacity:.65; cursor:wait; }
  .result { margin-top:18px; padding:18px; border-left:6px solid var(--green); border-radius:8px; background:white; }
  .result.warning { border-left-color:var(--warn); background:#fff8f4; }
  .result.error { border-left-color:#a4262c; background:#fff2f2; }
  .kicker { color:var(--muted); font-size:.86rem; font-weight:900; text-transform:uppercase; }
  footer { padding:38px 0 56px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:760px) {
    header, main, footer { margin:0; max-width:430px; width:100%; padding-left:24px; padding-right:24px; }
    header { padding-top:34px; }
    h1 { font-size:2.7rem; }
    h2 { font-size:1.8rem; }
    .panel { grid-column:span 12; padding:20px; }
    button { width:100%; }
  }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicInspect public sample</p>
  <h1>Turn field notes into review-ready inspection drafts.</h1>
  <p class="lede">CivicInspect demonstrates inspection support: sample repeat-case lookup, inspector-owned report drafting, notice draft support, staff review queues, CivicCode context packets, and records-ready exports without issuing findings or replacing the system of record.</p>
  <p><span class="badge">v0.2.2 inspection support + staff review queues</span></p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-labelledby="lookup-title">
    <article class="panel large">
      <p class="kicker">Sample repeat-case lookup</p>
      <h2 id="lookup-title">Draft inspection support</h2>
      <label for="property">Property reference</label>
      <input id="property" value="100 Main Street">
      <label for="violation">Inspection type</label>
      <select id="violation">
        <option value="nuisance">Nuisance</option>
        <option value="building">Building condition</option>
        <option value="fire">Fire prevention</option>
      </select>
      <label for="notes">Inspector notes</label>
      <textarea id="notes" rows="4">Inspector observed overgrown vegetation near the alley and two prior related cases for the same property.</textarea>
      <button id="draft-button" type="button">Draft sample report</button>
      <div id="result" class="result" role="status" aria-live="polite">
        <h3>Ready for sample input</h3>
        <p>Enter property notes and create a review-required draft. Use "100 Main Street" or "42 Oak Avenue" to show sample repeat-case context.</p>
      </div>
    </article>
    <article class="panel"><p class="kicker">Inspector-owned</p><h2>Humans decide</h2><div class="result"><p>Every draft is explicitly marked for inspector review; CivicInspect does not make findings, issue citations, or assess fines.</p></div></article>
    <article class="panel"><p class="kicker">Notice support</p><h2>Draft, not issuance</h2><div class="result"><p>Notice drafts list required staff actions: confirm code section, ownership, address, and repeat-case context.</p></div></article>
    <article class="panel"><p class="kicker">Staff queue</p><h2>Route review work</h2><div class="result"><p>Persisted draft reports can be routed to staff-only review queues with status, assignment, and resolution records.</p></div></article>
    <article class="panel"><p class="kicker">Records-ready export</p><h2>Keep provenance</h2><div class="result"><p>Exports preserve notes, draft text, reviewer, queue status, review date, and system-of-record links.</p></div></article>
    <article class="panel large"><p class="kicker">Boundary</p><h2>No official inspection action</h2><div class="result warning"><p>CivicInspect does not issue official findings, citations, fines, notices, inspection schedules, or system-of-record updates.</p></div></article>
  </section>
</main>
<footer><p>CivicInspect is part of the Apache 2.0 CivicSuite open-source municipal AI project.</p></footer>
<script>
  const result = document.querySelector("#result");
  const button = document.querySelector("#draft-button");
  const property = document.querySelector("#property");
  const notes = document.querySelector("#notes");

  function clearResult(kind) {
    result.className = `result ${kind}`;
    result.replaceChildren();
  }

  function appendText(tagName, text) {
    const node = document.createElement(tagName);
    node.textContent = text;
    result.appendChild(node);
    return node;
  }

  function setResult(kind, title, body) {
    clearResult(kind);
    appendText("h3", title);
    appendText("p", body);
  }

  function renderDraft(payload) {
    clearResult("");
    appendText("h3", "Draft ready for staff review");
    appendText("p", payload.summary || "Draft created for inspector review.");
    const list = document.createElement("ul");
    const observations = Array.isArray(payload.observation_bullets) ? payload.observation_bullets : [];
    for (const observation of observations) {
      const item = document.createElement("li");
      item.textContent = observation;
      list.appendChild(item);
    }
    if (observations.length) {
      result.appendChild(list);
    }
    appendText("p", payload.disclaimer || "Inspectors own every decision before any official action.");
  }

  button.addEventListener("click", async () => {
    button.disabled = true;
    setResult("", "Drafting report", "Sending inspector-entered notes to the local CivicInspect API.");
    try {
      const propertyText = property.value.trim();
      const noteText = notes.value.trim();
      if (!propertyText || !noteText) {
        setResult("error", "More detail is needed", "Add a property reference and inspector notes, then draft again. CivicInspect cannot create useful review text from blank inputs.");
        return;
      }
      const response = await fetch("/api/v1/civicinspect/reports/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          inspection_id: "public-sample",
          property_reference: propertyText,
          inspector_notes: noteText,
          photo_observations: [],
          voice_notes: ""
        })
      });
      const payload = await response.json();
      if (!response.ok) {
        const detail = payload.detail || {};
        setResult("error", "Draft failed", detail.fix || detail.message || "Review the input and try again.");
        return;
      }
      renderDraft(payload);
    } catch {
      setResult("error", "Draft failed", "The local CivicInspect API did not respond. Check the runtime logs and try again.");
    } finally {
      button.disabled = false;
    }
  });
</script>
</body>
</html>
"""


def render_staff_page() -> str:
    """Render the staff inspection review workspace."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicInspect Staff Workspace</title>
<style>
  :root { --ink:#18212a; --muted:#526170; --paper:#fbfbf8; --blue:#24566b; --green:#2f684f; --gold:#d7aa3f; --line:#d8d1bf; --warn:#8a4b2f; }
  * { box-sizing:border-box; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:#f5f7f4; }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:8px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1180px, calc(100% - 32px)); margin:0 auto; }
  header { padding:38px 0 20px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; font-weight:900; font-size:.78rem; }
  h1 { margin:0; font-family:Georgia,"Times New Roman",serif; font-size:3.6rem; line-height:1.02; max-width:940px; }
  .lede { max-width:840px; font-size:1.12rem; line-height:1.55; color:#344552; }
  .grid { display:grid; grid-template-columns:repeat(12,1fr); gap:16px; align-items:start; }
  .panel { grid-column:span 6; min-width:0; padding:22px; border:1px solid var(--line); border-radius:8px; background:var(--paper); }
  .panel.large { grid-column:span 12; }
  h2,h3 { margin-top:0; font-family:Georgia,"Times New Roman",serif; }
  label { display:block; margin:.8rem 0 .3rem; font-weight:800; }
  input, textarea, select, button { width:100%; border:1px solid #bac4c8; border-radius:8px; padding:.75rem .9rem; font:inherit; }
  input, textarea, select { background:white; color:var(--ink); }
  button { width:fit-content; min-width:180px; margin-top:1rem; border:0; background:var(--blue); color:white; font-weight:900; cursor:pointer; }
  button:disabled { opacity:.65; cursor:wait; }
  .row { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
  .result { margin-top:16px; padding:16px; border-left:6px solid var(--green); border-radius:8px; background:white; line-height:1.55; }
  .result.warning { border-left-color:var(--warn); }
  .result.error { border-left-color:#a4262c; background:#fff4f4; }
  .list { display:grid; gap:10px; }
  .item { padding:12px; border:1px solid var(--line); border-radius:8px; background:white; }
  .kicker { color:var(--muted); font-size:.82rem; font-weight:900; text-transform:uppercase; }
  footer { padding:34px 0 50px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:760px) {
    header, main, footer { margin:0; max-width:430px; width:100%; padding-left:22px; padding-right:22px; }
    h1 { font-size:2.45rem; }
    .panel { grid-column:span 12; }
    .row { grid-template-columns:1fr; }
    button { width:100%; }
  }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicInspect staff</p>
  <h1>Inspection drafts, review queue, and records export prep.</h1>
  <p class="lede">Create an inspector-owned draft from field notes, route it to staff review, resolve queue items, and prepare records-ready inspection export checklists. CivicInspect does not issue findings, notices, citations, fines, schedules, or system-of-record updates.</p>
</header>
<main id="main" tabindex="-1">
  <section class="grid">
    <article class="panel">
      <p class="kicker">Create draft</p>
      <h2>Field notes</h2>
      <label for="staff-key">Staff API key</label>
      <input id="staff-key" type="password" autocomplete="off" placeholder="Local staff key">
      <div class="row">
        <div>
          <label for="inspection-id">Inspection ID</label>
          <input id="inspection-id" value="insp-100">
        </div>
        <div>
          <label for="property">Property reference</label>
          <input id="property" value="100 Main Street">
        </div>
      </div>
      <label for="notes">Inspector notes</label>
      <textarea id="notes" rows="5">Overgrown vegetation observed near the alley. Prior case history should be reviewed before any notice is drafted.</textarea>
      <button id="create-draft" type="button">Create review draft</button>
      <div id="draft-result" class="result" role="status" aria-live="polite">Ready to create a review-required draft.</div>
    </article>
    <article class="panel">
      <p class="kicker">Queue</p>
      <h2>Staff review items</h2>
      <button id="load-queue" type="button">Load queue</button>
      <div id="queue-result" class="result" role="status" aria-live="polite">Queue has not been loaded.</div>
    </article>
    <article class="panel large">
      <p class="kicker">Boundary</p>
      <h2>Review support only</h2>
      <div class="result warning">Every result remains a staff-review draft. Preserve the draft, reviewer, queue disposition, and final system-of-record links with the inspection case file.</div>
    </article>
  </section>
</main>
<footer><p>CivicInspect is part of the Apache 2.0 CivicSuite open-source municipal AI project.</p></footer>
<script>
  const key = document.querySelector("#staff-key");
  const inspectionId = document.querySelector("#inspection-id");
  const property = document.querySelector("#property");
  const notes = document.querySelector("#notes");
  const draftResult = document.querySelector("#draft-result");
  const queueResult = document.querySelector("#queue-result");
  const createDraft = document.querySelector("#create-draft");
  const loadQueue = document.querySelector("#load-queue");

  function headers() {
    return {
      "Content-Type": "application/json",
      "X-CivicInspect-Role": "staff",
      "X-CivicInspect-Staff-Key": key.value
    };
  }

  function setBox(target, kind, lines) {
    target.className = `result ${kind}`;
    target.replaceChildren();
    for (const line of lines) {
      const p = document.createElement("p");
      p.textContent = line;
      target.appendChild(p);
    }
  }

  async function loadReviewQueue() {
    loadQueue.disabled = true;
    try {
      const response = await fetch("/api/v1/civicinspect/staff/reviews", { headers: headers() });
      const payload = await response.json();
      if (!response.ok) {
        const detail = payload.detail || {};
        setBox(queueResult, "error", [detail.fix || detail.message || "Unable to load staff queue."]);
        return;
      }
      queueResult.className = "result";
      queueResult.replaceChildren();
      const items = document.createElement("div");
      items.className = "list";
      for (const item of payload.items || []) {
        const card = document.createElement("div");
        card.className = "item";
        card.textContent = `${item.status}: ${item.inspection_id} at ${item.property_reference} - ${item.reason}`;
        items.appendChild(card);
      }
      if (!items.children.length) {
        setBox(queueResult, "", ["No staff review items are queued."]);
      } else {
        queueResult.appendChild(items);
      }
    } catch {
      setBox(queueResult, "error", ["The local CivicInspect API did not respond."]);
    } finally {
      loadQueue.disabled = false;
    }
  }

  createDraft.addEventListener("click", async () => {
    createDraft.disabled = true;
    try {
      const response = await fetch("/api/v1/civicinspect/reports/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          inspection_id: inspectionId.value,
          property_reference: property.value,
          inspector_notes: notes.value,
          photo_observations: [],
          voice_notes: ""
        })
      });
      const payload = await response.json();
      if (!response.ok) {
        const detail = payload.detail || {};
        setBox(draftResult, "error", [detail.fix || detail.message || "Unable to create draft."]);
        return;
      }
      setBox(draftResult, "", [
        `Draft ${payload.report_id || "created"} requires inspector review.`,
        payload.summary || "Draft created.",
        `Staff review item: ${payload.staff_review_id || "not persisted"}`
      ]);
      await loadReviewQueue();
    } catch {
      setBox(draftResult, "error", ["The local CivicInspect API did not respond."]);
    } finally {
      createDraft.disabled = false;
    }
  });
  loadQueue.addEventListener("click", loadReviewQueue);
</script>
</body>
</html>
"""
