# Roman Telescope: Journey to L2!

<p>
  Hosted on Streamlit
  <a href="https://streamlit.io/" target="_blank">
    <img src="icon/streamlit_icon.png" alt="Streamlit" height="22" align="top"/>
  </a>
</p>

<a href="https://romanjourney.streamlit.app/" target="_blank">
  <img src="https://img.shields.io/badge/Play%20Now-brightgreen?style=for-the-badge" alt="Play Now!"/>
</a>

A Flappy-Bird-style arcade game themed around the [Nancy Grace Roman Space Telescope](https://roman.gsfc.nasa.gov/).

---

## About the Game

Pilot the Roman Space Telescope through a field of drifting space debris. Click the
screen (or press the **Space** bar) to fire the thrusters and keep the telescope aloft —
gravity is always pulling it back down. Thread the gap in each obstacle to score, and
see how far you can fly before a collision ends the run.

### How it works

- **One-button flight** — click or press Space to flap; the telescope rises, then falls under gravity.
- **Endless side-scroller** — space-debris columns scroll in from the right with a gap to fly through.
- **Score** — +1 for every gap cleared. A single collision (with debris, the ceiling, or the lunar surface) ends the run.
- **All-time leaderboard** — after a run, enter your nickname and submit your best score to the global rankings.

---

## Project Structure

```
roman_journey/
├── app.py              # Streamlit app: renders the game, logs scores, shows the leaderboard
├── frontend/
│   └── index.html      # Self-contained canvas game (physics, rendering, score submit)
├── icon/
│   └── RST_icon.png    # Page icon
├── requirements.txt
└── README.md
```

### `app.py`

Renders the game via a bidirectional custom Streamlit component, receives the finished-run
result (player name + score) back from the frontend, logs it to Google Sheets, and displays
the all-time high-score leaderboard.

### `frontend/index.html`

The full game UI — an HTML canvas running the Flappy-style physics, obstacle scrolling,
collision detection, and rendering — inside an iframe. Communicates the completed run's
score back to Python through the Streamlit component `postMessage` protocol.

---

## Installation & Running

**Requirements:** Python 3.9+

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/roman_journey.git
   cd roman_journey
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add a `.streamlit/secrets.toml` with your Google service account credentials
   (a `[gcp_service_account]` table including `spreadsheet_id`).

4. Launch the app:

   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`.

---
