# RangeRx Beta 1 — local prototype

Run `pip install -r requirements.txt` then `streamlit run app.py`.

This is a local functional prototype, **not a public deployment**. It has registration, the 54 proposed universal statements, response capture, progress, editing previous responses, and completion validation.

Important before any real participant pilot:
- Replace the basic data-use acknowledgement with approved privacy information and retention arrangements.
- Add secure participant resume (current session-only resume is not durable across browsers).
- Add authenticated admin export; there is no participant-data export UI yet.
- Confirm response labels and coding against the authoritative PT instrument.
- Reintegrate/verify the original swipe component; this prototype intentionally uses accessible tap controls.
- Verify mapping to canonical Nudge IDs and Engine V2 before scoring.
- Use managed secure storage for deployment rather than local SQLite on ephemeral hosting.
- Do not treat the statements as psychometrically validated yet.
