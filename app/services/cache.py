import time
import hashlib

_cache: dict[str, tuple[str, float]] = {}  # key -> (reply, expires_at)
TTL_SECONDS = 60 * 60  # 1 hour


def _normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())


def _make_key(text: str) -> str:
    return hashlib.sha256(_normalize(text).encode()).hexdigest()


def get_cached_reply(text: str) -> str | None:
    key = _make_key(text)
    entry = _cache.get(key)
    if entry is None:
        return None
    reply, expires_at = entry
    if time.time() > expires_at:
        del _cache[key]
        return None
    return reply


def set_cached_reply(text: str, reply: str) -> None:
    key = _make_key(text)
    _cache[key] = (reply, time.time() + TTL_SECONDS)