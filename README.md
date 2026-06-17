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

Navigate the Roman telescope through space as it travels to L2. Dodge obstacles and navigate through
precarious structures and tunnels to get Roman to its destination. Click or tap the
screen (or press the **Space** bar) to fire the thrusters and keep the telescope flying straight. 
See how far you can fly before a collision ends the run.

### How it works

- **One-button flight** — click, tap the screen (on mobile), or press Spacebar to fly.
- **Score** — +1 for every gap or obstacle cleared. A single collision (with debris, the ceiling, walls, etc) ends the run.
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

The full game UI — an HTML canvas running the Flappy bird-style physics, obstacle scrolling,
collision detection, and rendering — inside an iframe. Communicates the completed run's
score back to Python through the Streamlit component `postMessage` protocol.

---

## Installation & Running (locally)

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

4. Launch the app:

   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`.

---
