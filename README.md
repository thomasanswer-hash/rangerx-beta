# RangeRx Beta 2 — shareable preview

A shareable **demo-only** RangeRx assessment based on the existing Beta 1 Streamlit project. Uses the original 54 RangeRx statements **unchanged**, not the Nudge statement bank.

## Included
- Three fixed stages: Starting Off / Finding Out / Meeting Needs, with introductory cards.
- 18 independently shuffled statements within each stage, fixed for the duration of each session.
- Existing swipe component and accessible tap buttons; four score directions.
- Review/change answers and strict 54-response validation.
- Download a CSV with exact statement identity and metadata.
- No collection of personal details and no server-side storage of answers.

## Run locally
```sh
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to existing Render service
1. Back up your current GitHub `rangerx-beta` repository first (download ZIP or create a branch).
2. Replace the repository's app files with the files in this ZIP (retain `.git` if working locally), then commit to `main`.
3. In Render, verify the service uses Python and has:
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`
4. Deploy and test on a phone and desktop. Keep link to project collaborators.

**Important**: This is a usability preview for Mike, not a participant-ready pilot. Session state can be lost on refresh, restarts or browser closure. No participant responses are centrally retained. CSV is a provisional export; confirm exact Nudge Engine import schema and scoring mappings before using it for analysis. Intro video is a placeholder. Privacy/security review, durable storage, authenticated export, and a resume mechanism are required before a live participant pilot.


Beta 2.8: Back/Next now render inside the swipe component. The current logo asset has not been altered; replace assets/rangerx_official.png with the exact approved logo image when supplied.
