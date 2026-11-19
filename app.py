
import csv
import base64
import io
import random
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent
STAGES = ["Starting Off", "Finding Out", "Meeting Needs"]
STAGE_INFO = {
    "Starting Off": ("rocket", "Every client relationship begins somewhere. Think about how you open conversations, make contact and get things moving."),
    "Finding Out": ("search", "Good coaching starts with understanding. Think about how you listen, explore and discover what matters to someone."),
    "Meeting Needs": ("handshake", "Understanding is only the beginning. Think about how you respond, offer direction and help someone move forward."),
}
LABELS = {1: "Never", 2: "Sometimes", 3: "Often", 4: "Always"}
STAGE_SVG = {
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.08 2.08 0 0 0-2.91-.09Z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6.05 11A22 22 0 0 1 12 15Z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5-1 5-1M12 15v5s3.03-.55 4-2c1.08-1.62 1-5 1-5"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>',
    "handshake": '<svg x="0" y="1" width="24" height="22" viewBox="0 0 576 512" fill="#5ED8CE" stroke="none"><path d="M323.4 85.2l-96.8 78.4c-16.1 13-19.2 36.4-7 53.1c12.9 17.8 38 21.3 55.3 7.8l99.3-77.2c7-5.4 17-4.2 22.5 2.8s4.2 17-2.8 22.5l-20.9 16.2L512 316.8 512 128l-.7 0-3.9-2.5L434.8 79c-15.3-9.8-33.2-15-51.4-15c-21.8 0-43 7.5-60 21.2zm22.8 124.4l-51.7 40.2C263 274.4 217.3 268 193.7 235.6c-22.2-30.5-16.6-73.1 12.7-96.8l83.2-67.3c-11.6-4.9-24.1-7.4-36.8-7.4C234 64 215.7 69.6 200 80l-72 48 0 224 28.2 0 91.4 83.4c19.6 17.9 49.9 16.5 67.8-3.1c5.5-6.1 9.2-13.2 11.1-20.6l17 15.6c19.5 17.9 49.9 16.6 67.8-2.9c4.5-4.9 7.8-10.6 9.9-16.5c19.4 13 45.8 10.3 62.1-7.5c17.9-19.5 16.6-49.9-2.9-67.8l-134.2-123zM16 128c-8.8 0-16 7.2-16 16L0 352c0 17.7 14.3 32 32 32l32 0c17.7 0 32-14.3 32-32l0-224-80 0zM48 320a16 16 0 1 1 0 32 16 16 0 1 1 0-32zM544 128l0 224c0 17.7 14.3 32 32 32l32 0c17.7 0 32-14.3 32-32l0-208c0-8.8-7.2-16-16-16l-80 0zm32 208a16 16 0 1 1 32 0 16 16 0 1 1 -32 0z"/></svg>',
}
def stage_icon(name):
    return f'<svg width="76" height="76" viewBox="0 0 24 24" fill="none" stroke="#5ED8CE" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{STAGE_SVG[name]}</svg>'


st.set_page_config(page_title="RangeRx | Beta preview", page_icon="⚡", layout="centered")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');
.stApp {background:#0b0e10;color:#f6f8f8}
html,body,p,h1,h2,h3,label {font-family:Montserrat,sans-serif!important}
h1,h2,h3 {color:#fff!important;letter-spacing:-.035em}
p,label,.stMarkdown {color:#e5e9e9!important}
[data-testid="stHeader"]{background:#0b0e10}
.stButton button[kind="primary"],[data-testid="stFormSubmitButton"] button {background:#16b9aa;color:#071010;border:0;font-weight:800}
.stButton button {border-radius:12px;min-height:2.3rem}
[data-testid="stProgressBar"] div[role="progressbar"] {background:#16b9aa}
.stButton button[kind="secondary"]{background:#22292b!important;color:#fff!important;border:1px solid #465154!important}
.stButton button[kind="secondary"] p{color:#fff!important}
.stButton button[kind="primary"] p{color:#061512!important}
[data-testid="stHeading"] h1{font-size:clamp(1.7rem,5vw,2.5rem)!important}

 /* Centre Streamlit's main column on desktop, including the embedded swipe UI. */
 [data-testid="stAppViewContainer"] .block-container {
   width: min(100% - 48px, 760px) !important;
   max-width: 760px !important;
   margin-left: auto !important;
   margin-right: auto !important;
   padding-top: 4.8rem !important;
   padding-bottom: 1rem !important;
 }
 [data-testid="stImage"] img { object-fit:contain; display:block; }
  /* Navigation labels stay on one line, regardless of button width. */
  div[data-testid="stButton"] button { white-space:nowrap !important; }
  div[data-testid="stButton"] button p { white-space:nowrap !important; }
  div[data-testid="stButton"] button p span { white-space:nowrap !important; }
 [data-testid="stMain"] > div { width: 100%; }
 [data-testid="stVerticalBlock"] { width: 100%; }
 [data-testid="stIFrame"] { display:block; width:100% !important; margin:0 auto; }
 @media (min-width: 1200px) {
   [data-testid="stAppViewContainer"] .block-container {
     width: min(100% - 80px, 760px) !important;
   }
 }
 @media (max-width: 700px) {
   [data-testid="stAppViewContainer"] .block-container {
     width: calc(100% - 24px) !important;
     padding-left: 0 !important;
     padding-right: 0 !important;
     padding-top: 4.2rem !important;
   }
 }
</style>
""", unsafe_allow_html=True)

def load_items():
    with (ROOT / "data" / "rangerx_instrument_v0_1.csv").open(encoding="utf-8-sig", newline="") as f:
        items = list(csv.DictReader(f))
    ids = [r["statement_id"] for r in items]
    assert len(items) == 54 and len(set(ids)) == 54, "Statement bank must contain 54 unique IDs"
    assert len({r["statement"] for r in items}) == 54, "Statement text must be unique"
    assert all(sum(r["stage"] == stage for r in items) == 18 for stage in STAGES)
    assert all(r["abc"] in ("Attentive", "Balanced", "Connected") for r in items)
    assert all(r["flexibility"] in ("Flexible", "Inflexible") for r in items)
    return items

def start():
    items = load_items()
    ordered = []
    for stage in STAGES:
        stage_items = [x for x in items if x["stage"] == stage]
        random.SystemRandom().shuffle(stage_items)
        ordered.extend(stage_items)
    st.session_state.order = ordered
    st.session_state.responses = {}
    st.session_state.position = 0
    st.session_state.view = "stage"
    st.session_state.swipe_nonce = 0

def answer(score):
    if type(score) is not int or score not in LABELS:
        st.error("Invalid response. Choose Never, Sometimes, Often or Always.")
        return
    pos = st.session_state.position
    item = st.session_state.order[pos]
    st.session_state.responses[item["statement_id"]] = score
    if pos == 53:
        st.session_state.view = "review"
    else:
        st.session_state.position = pos + 1
        if (pos + 1) % 18 == 0:
            st.session_state.view = "stage"
    st.session_state.swipe_nonce += 1
    st.rerun()

def csv_bytes():
    rows = st.session_state.order
    answers = st.session_state.responses
    expected = {r["statement_id"] for r in rows}
    if len(answers) != 54 or set(answers) != expected or any(type(v) is not int or v not in LABELS for v in answers.values()):
        raise ValueError("All 54 valid responses are required.")
    output = io.StringIO()
    fields = ["statement_id", "statement", "stage", "abc", "level", "flexibility", "instrument_version", "score"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for item in rows:
        writer.writerow({**{k: item[k] for k in fields if k != "score"}, "score": answers[item["statement_id"]]})
    return output.getvalue().encode("utf-8-sig")

swipe_card = components.declare_component("rangerx_swipe", path=str(ROOT / "swipe_component"))
items = load_items()
# Show the original, unmodified PNG as a native Streamlit image.
# A three-column row centres the logo without HTML clipping.
import base64
logo_data = base64.b64encode((ROOT / "assets" / "rangerx_official.png").read_bytes()).decode("ascii")
st.markdown(
    f'<div style="display:flex;justify-content:center;align-items:center;overflow:visible;padding:8px 0 12px;">'
    f'<img src="data:image/png;base64,{logo_data}" '
    f'style="display:block;width:230px;max-width:100%;height:auto;border:0;border-radius:0;object-fit:contain;">'
    f'</div>',
    unsafe_allow_html=True
)


if "view" not in st.session_state:
    st.session_state.view = "welcome"

view = st.session_state.view
if view == "welcome":
    st.title("Better conversations. More PT clients.")
    st.write("Discover how you tend to start conversations, find out what matters and respond to people's needs.")
    st.info("🎬 Introduction video coming soon. You can continue without watching.")
    st.markdown("""
**Make your choice with a swipe.**

For each statement, swipe towards the answer that feels most true for you.

**← Never · ↑ Sometimes · ↓ Often · Always →**

You can also tap a direction instead of swiping.

There are no right or wrong answers. Just go with what feels most like you.
""")

    st.caption("54 short statements · 3 stages · Around 10–15 minutes")
    st.warning("Demo mode: no name, email or answers are saved to the server. Keep this preview link within the project team. Closing or refreshing the browser session may lose your progress.")
    if st.button("Start the assessment →", type="primary", use_container_width=True):
        start()
        st.rerun()

elif view == "stage":
    pos = st.session_state.position
    stage_index = pos // 18
    stage = STAGES[stage_index]
    icon, description = STAGE_INFO[stage]
    st.markdown(f"<div style='display:flex;justify-content:center;padding:28px 0 8px'>{stage_icon(icon)}</div>", unsafe_allow_html=True)
    st.caption(f"STAGE {stage_index+1} OF 3")
    st.title(stage)
    st.write(description)
    st.write("You'll see 18 statements, one at a time. Respond to each as it feels true for you. There's no ideal answer.")
    if st.button("Let's go →", type="primary", use_container_width=True):
        st.session_state.view = "question"
        st.rerun()

elif view == "question":
    pos = st.session_state.position
    item = st.session_state.order[pos]
    responses = st.session_state.responses
    st.caption(f"{item['stage'].upper()} · {pos % 18 + 1} OF 18")
    st.progress(len(responses) / 54)
    st.caption(f"{len(responses)} of 54 answered")
    st.caption("")
    result = swipe_card(
        statement=item["statement"], stage=item["stage"],
        position=pos+1, selected=responses.get(item["statement_id"], 0),
        answered=item["statement_id"] in responses,
        key=f"swipe_{pos}_{st.session_state.swipe_nonce}", default=None
    )
    if type(result) is int and result in LABELS:
        answer(result)
    elif result == "back" and pos > 0:
        st.session_state.position = pos - 1
        st.session_state.view = "question"
        st.session_state.swipe_nonce += 1
        st.rerun()
    elif result == "next" and item["statement_id"] in responses:
        if pos == 53:
            st.session_state.view = "review"
        else:
            st.session_state.position = pos + 1
            st.session_state.view = "stage" if (pos + 1) % 18 == 0 else "question"
        st.session_state.swipe_nonce += 1
        st.rerun()
    # Navigation remains outside the iframe.
    if len(responses) == 54:
        if st.button("Review all responses", type="primary", use_container_width=True):
            st.session_state.view = "review"
            st.rerun()

elif view == "review":
    answers = st.session_state.responses
    st.title("That's all 54.")
    st.write("Thanks for exploring your conversational range.")
    st.progress(len(answers) / 54)
    if len(answers) != 54:
        st.error(f"{54-len(answers)} statements still need an answer.")
        if st.button("Return to assessment"):
            missing = next(i for i,r in enumerate(st.session_state.order) if r["statement_id"] not in answers)
            st.session_state.position = missing
            st.session_state.view = "question"
            st.rerun()
    else:
        st.success("All 54 responses are complete and valid.")
        st.caption("Preview CSV includes exact RangeRx statement text and metadata. Nudge Engine import compatibility must still be verified before production use.")
        st.download_button("Download my responses (CSV)", data=csv_bytes(),
                           file_name="RangeRx_beta_responses.csv", mime="text/csv",
                           type="primary", use_container_width=True)
        if st.button("Review / change an answer", use_container_width=True):
            st.session_state.position = 0
            st.session_state.view = "question"
            st.session_state.swipe_nonce += 1
            st.rerun()
    if st.button("Start a new demo", use_container_width=True):
        start()
        st.rerun()
