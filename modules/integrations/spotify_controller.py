import os
import logging

log = logging.getLogger("FRIDAY")
TOKEN_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "spotify_token.json"
)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:8888/callback"


def _get_spotify():
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth
    except ImportError:
        return None

    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=REDIRECT_URI,
                scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing",
                cache_path=TOKEN_FILE,
                open_browser=False,
            )
        )
        return sp
    except Exception as e:
        log.error("Spotify auth error: %s", e)
        return None


def current_playing() -> str:
    sp = _get_spotify()
    if not sp:
        return "Spotify not configured or not running."
    try:
        track = sp.current_playback()
        if track and track.get("item"):
            name = track["item"]["name"]
            artist = track["item"]["artists"][0]["name"]
            return f"Now playing: {name} by {artist}"
        return "Nothing is playing on Spotify."
    except Exception as e:
        return f"Spotify error: {e}"


def play() -> str:
    sp = _get_spotify()
    if not sp:
        return "Spotify not configured."
    try:
        sp.start_playback()
        return "Playback started."
    except Exception:
        return "Could not start playback. Open Spotify first."


def pause() -> str:
    sp = _get_spotify()
    if not sp:
        return "Spotify not configured."
    try:
        sp.pause_playback()
        return "Playback paused."
    except Exception:
        return "Could not pause."


def next_track() -> str:
    sp = _get_spotify()
    if not sp:
        return "Spotify not configured."
    try:
        sp.next_track()
        return "Skipped to next track."
    except Exception:
        return "Could not skip."


def previous_track() -> str:
    sp = _get_spotify()
    if not sp:
        return "Spotify not configured."
    try:
        sp.previous_track()
        return "Went to previous track."
    except Exception:
        return "Could not go back."


def search_and_play(query: str) -> str:
    sp = _get_spotify()
    if not sp:
        return "Spotify not configured."
    try:
        results = sp.search(q=query, type="track", limit=1)
        items = results.get("tracks", {}).get("items", [])
        if not items:
            return f"No results for {query}."
        track = items[0]
        sp.start_playback(uris=[track["uri"]])
        return f"Playing {track['name']} by {track['artists'][0]['name']}."
    except Exception as e:
        return f"Spotify search error: {e}"
