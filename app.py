import datetime
import html as _html
import os

import gspread
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# ── page config ──
_icon_path = os.path.join(os.path.dirname(__file__), "icon", "RST_icon.png")
st.set_page_config(
    page_title="Roman Telescope: Journey to L2!",
    layout="centered",
    page_icon=Image.open(_icon_path),
)
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer     {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Google Sheets ──
@st.cache_resource
def _gs_client():
    info = {k: v for k, v in st.secrets["gcp_service_account"].items() if k != "spreadsheet_id"}
    return gspread.service_account_from_dict(info)

def _sheet():
    return _gs_client().open_by_key(st.secrets["gcp_service_account"]["spreadsheet_id"]).sheet1

def log_score(player: str, score: int) -> None:
    try:
        _sheet().append_row([
            datetime.datetime.now(datetime.timezone.utc).isoformat(),
            player,
            score,
        ])
    except Exception:
        pass  # don't crash the game if Sheets is unavailable

@st.cache_data(ttl=60)
def get_leaderboard() -> list[dict]:
    """All-time high scores — one row per player, their best run, score desc."""
    try:
        records = _sheet().get_all_records()
        best: dict[str, dict] = {}
        for r in records:
            name = str(r.get("Player", "")).strip()
            if not name:
                continue
            try:
                score = int(r.get("Score", 0))
            except (TypeError, ValueError):
                continue
            if name not in best or score > int(best[name].get("Score", 0)):
                best[name] = {"Player": name, "Score": score}
        return sorted(
            best.values(),
            key=lambda r: (-r["Score"], r["Player"].lower()),
        )
    except Exception:
        return []


# ── bidirectional game component ──
# A static (no-build) custom component: the game's index.html pushes its
# {player, score, …} result back to Python via the Streamlit component
# postMessage protocol — the only iframe→Python channel the sandbox allows.
_FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
_game_component = components.declare_component("roman_rush", path=_FRONTEND_DIR)


# ── render the game; receive the finished-game result back from the iframe ──
_result = _game_component(
    default=None,
    key="roman_rush_game",
)

# When the player taps "Submit Score" inside the game, _result becomes the
# game payload. gameId dedupes so each finished game is logged exactly once
# (the value persists across reruns until a new game is submitted).
_highlight = st.session_state.get("last_player", "")
if isinstance(_result, dict) and _result.get("gameId"):
    _gid = _result["gameId"]
    if st.session_state.get("last_logged_game_id") != _gid:
        _name = str(_result.get("player", "Anonymous")).strip() or "Anonymous"
        log_score(_name, int(_result.get("score", 0)))
        st.session_state.last_logged_game_id = _gid
        st.session_state.last_player = _name
        get_leaderboard.clear()
        _highlight = _name
        st.success(f"Score submitted! Great flying, **{_html.escape(_name)}**!")
    else:
        _highlight = str(_result.get("player", "")).strip()

st.divider()

st.markdown(
    """
    <div style="text-align:center;padding:2px 0 12px;">
      <span style="font-size:1.1rem;font-weight:900;letter-spacing:3px;color:#0b3d91;">
        LEADERBOARD
      </span><br>
      <span style="font-size:0.82rem;color:#666;">
        Finish a run and tap <strong>Submit Score</strong> to join the rankings.
      </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── leaderboard table ──
_rows = get_leaderboard()
if _rows:
    _table_rows = ""
    _rank = 0
    _prev_score = None
    for _i, _r in enumerate(_rows):
        _score = _r.get("Score", 0)
        if _score != _prev_score:
            _rank = _i + 1
            _prev_score = _score
        _is_me = bool(_highlight) and (_r.get("Player") == _highlight)
        _bg    = "#e8f0fc" if _is_me else ("transparent" if _i % 2 == 0 else "#f8f9ff")
        _name  = _html.escape(str(_r.get("Player", "")))
        _table_rows += (
            f'<tr style="background:{_bg};">'
            f'<td style="padding:8px 12px;text-align:center;font-weight:700;color:#aaa;">{_rank}</td>'
            f'<td style="padding:8px 12px;font-weight:{"800" if _is_me else "600"};'
            f'color:{"#0b3d91" if _is_me else "#1a1a2e"};">{_name}</td>'
            f'<td style="padding:8px 12px;text-align:center;font-weight:700;color:#0b3d91;">'
            f'{_r.get("Score", "")}</td>'
            f'</tr>'
        )
    st.markdown(
        f"""
        <div style="background:#fff;border:1.5px solid #d0d8ef;border-radius:10px;
                    padding:14px 16px;margin-bottom:10px;">
          <div style="margin-bottom:10px;">
            <span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;
                         letter-spacing:1.5px;color:#999;">All-Time</span>
            <span style="font-size:1rem;font-weight:800;color:#c0392b;
                         letter-spacing:0.5px;"> High Scores</span>
          </div>
          <div style="max-height:320px;overflow-y:auto;">
          <table style="width:100%;border-collapse:collapse;">
            <thead>
              <tr style="border-bottom:2px solid #eef2fb;">
                <th style="padding:6px 12px;text-align:center;font-size:0.72rem;color:#aaa;">#</th>
                <th style="padding:6px 12px;text-align:left;font-size:0.72rem;color:#aaa;">Player</th>
                <th style="padding:6px 12px;text-align:center;font-size:0.72rem;color:#aaa;">Score</th>
              </tr>
            </thead>
            <tbody>{_table_rows}</tbody>
          </table>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div style="text-align:center;color:#aaa;padding:8px 0 4px;font-size:0.9rem;">
          No scores submitted yet — be the first!
        </div>
        """,
        unsafe_allow_html=True,
    )
