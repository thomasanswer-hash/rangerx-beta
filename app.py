
import csv
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent
DB = ROOT / "rang erx.sqlite3".replace(" ", "")
INSTRUMENT = "range-universal-v0.1"
STAGES = ["Starting Off", "Finding Out", "Meeting Needs"]

st.set_page_config(page_title="RangeRx | Your human edge", page_icon="⚡", layout="centered")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');
.stApp {background:#0b0e10;color:#f6f8f8}
html,body,p,h1,h2,h3,label {font-family:Montserrat,sans-serif!important}
h1,h2,h3 {color:#fff!important;letter-spacing:-.04em}
p, label, .stMarkdown {color:#e5e9e9!important}
[data-testid="stHeader"]{background:#0b0e10}
[data-testid="stTextInput"] input {background:#1c2325;color:white;border:1px solid #455052}
.stButton button[kind="primary"],[data-testid="stFormSubmitButton"] button {background:#16b9aa;color:#071010;border:0;font-weight:800}
.stButton button {border-radius:12px;min-height:3rem}
[data-testid="stProgressBar"] div[role="progressbar"] {background:#16b9aa}
hr{border-color:#273133}
</style>
""", unsafe_allow_html=True)

def now():
    return datetime.now(timezone.utc).isoformat()

def connect():
    con=sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    return con

def init():
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS participants(
          id TEXT PRIMARY KEY, first_name TEXT NOT NULL,
          last_name TEXT NOT NULL, email TEXT NOT NULL,
          created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS assessments(
          id TEXT PRIMARY KEY, participant_id TEXT NOT NULL,
          instrument_version TEXT NOT NULL,
          status TEXT NOT NULL CHECK(status IN ('in_progress','complete')),
          created_at TEXT NOT NULL, completed_at TEXT,
          FOREIGN KEY(participant_id) REFERENCES participants(id));
        CREATE TABLE IF NOT EXISTS responses(
          assessment_id TEXT NOT NULL, statement_id TEXT NOT NULL,
          stage TEXT NOT NULL, score INTEGER NOT NULL CHECK(score BETWEEN 1 AND 4),
          updated_at TEXT NOT NULL,
          PRIMARY KEY(assessment_id,statement_id),
          FOREIGN KEY(assessment_id) REFERENCES assessments(id));
        """)

def load_items():
    with (ROOT/"data"/"rangerx_instrument_v0_1.csv").open(encoding="utf-8",newline="") as f:
        items=list(csv.DictReader(f))
    assert len(items)==54 and len({x["statement_id"] for x in items})==54
    assert all(sum(x["stage"]==stage for x in items)==18 for stage in STAGES)
    assert all(x["instrument_version"]==INSTRUMENT for x in items)
    return items

init()
items=load_items()
if "assessment" not in st.session_state: st.session_state.assessment=None
if "position" not in st.session_state: st.session_state.position=0

st.image(str(ROOT/"assets"/"rangerx.png"),width=230)

if st.session_state.assessment is None:
    st.caption("DEVELOP YOUR HUMAN EDGE")
    st.title("Better conversations. More PT clients.")
    st.write("How do you start conversations, discover what matters and help people take the next step? Find out how you tend to approach those moments.")
    st.markdown("#### Welcome to RangeRx")
    st.info("Welcome video coming soon. For now, the assessment takes you through 54 short statements in three parts.")
    st.markdown("### First, a little about you")
    with st.form("register"):
        first=st.text_input("First name")
        last=st.text_input("Last name")
        email=st.text_input("Email")
        acknowledged=st.checkbox("I understand that my responses and contact details will be stored for this beta assessment and reviewed by the authorised RangeRx project team.")
        go=st.form_submit_button("Start my assessment",type="primary")
    if go:
        if not first.strip() or not last.strip() or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+",email.strip()):
            st.error("Please enter your name and a valid email.")
        elif not acknowledged:
            st.error("Please confirm the data-use acknowledgement.")
        else:
            pid=str(uuid.uuid4());aid=str(uuid.uuid4())
            with connect() as con:
                con.execute("INSERT INTO participants VALUES (?,?,?,?,?)",(pid,first.strip(),last.strip(),email.strip().lower(),now()))
                con.execute("INSERT INTO assessments VALUES (?,?,?,?,?,?)",(aid,pid,INSTRUMENT,"in_progress",now(),None))
            st.session_state.assessment=aid
            st.session_state.position=0
            st.rerun()
else:
    aid=st.session_state.assessment
    with connect() as con:
        assessment=con.execute("SELECT status FROM assessments WHERE id=?",(aid,)).fetchone()
        answered={r[0]:r[1] for r in con.execute("SELECT statement_id,score FROM responses WHERE assessment_id=?",(aid,))}
    if assessment is None:
        st.error("Assessment unavailable.")
        st.stop()
    if assessment[0]=="complete":
        st.title("That's a wrap.")
        st.success("All 54 responses have been saved. Thank you for taking part.")
        st.write("Your responses will help us understand how PTs experience the assessment.")
    else:
        pos=st.session_state.position
        item=items[pos]
        st.caption(f"{item['stage'].upper()} · {pos+1} OF 54")
        st.progress(len(answered)/54)
        st.title(item["statement"])
        st.write("How often does this sound like you?")
        options=[("Never",1),("Sometimes",2),("Often",3),("Always",4)]
        for label,value in options:
            if st.button(f"{label}  {'✓' if answered.get(item['statement_id'])==value else ''}",key=f"answer_{pos}_{value}",use_container_width=True,type="primary" if answered.get(item["statement_id"])==value else "secondary"):
                with connect() as con:
                    con.execute("""INSERT INTO responses(assessment_id,statement_id,stage,score,updated_at)
                        VALUES(?,?,?,?,?) ON CONFLICT(assessment_id,statement_id)
                        DO UPDATE SET score=excluded.score,updated_at=excluded.updated_at""",
                        (aid,item["statement_id"],item["stage"],value,now()))
                st.session_state.position=min(pos+1,53)
                st.rerun()
        a,b=st.columns(2)
        with a:
            if st.button("← Previous",disabled=pos==0,use_container_width=True):
                st.session_state.position-=1;st.rerun()
        with b:
            if st.button("Next →",disabled=pos==53,use_container_width=True):
                st.session_state.position+=1;st.rerun()
        if len(answered)==54:
            if st.button("Submit all 54 responses",type="primary",use_container_width=True):
                with connect() as con:
                    count=con.execute("SELECT COUNT(*) FROM responses WHERE assessment_id=?",(aid,)).fetchone()[0]
                    if count==54:
                        con.execute("UPDATE assessments SET status='complete',completed_at=? WHERE id=? AND status='in_progress'",(now(),aid))
                st.rerun()
