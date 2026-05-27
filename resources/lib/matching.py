# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List

NOISE_TOKENS = {"sample", "trailer", "cam", "telesync", "ts", "hdcam", "subforced"}
QUALITY_ORDER = ["2160p", "1080p", "720p", "sd"]


def normalize_title(value: str) -> str:
    value = (value or "").lower()
    value = unicodedata.normalize("NFD", value)
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = re.sub(r"[._-]+", " ", value)
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    parts = [p for p in value.split() if p and p not in NOISE_TOKENS]
    return " ".join(parts)


def _as_int(value: Any) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0


def build_tmdbh_queries(params: Dict[str, Any]) -> List[str]:
    mediatype = (params.get("mediatype") or "").lower()
    queries: List[str] = []

    if mediatype == "episode":
        showname = (params.get("showname") or "").strip()
        show_originaltitle = (params.get("show_originaltitle") or "").strip()
        episode_title = (params.get("episode_title") or "").strip()
        season = _as_int(params.get("season"))
        episode = _as_int(params.get("episode"))
        if showname and season > 0 and episode > 0:
            queries.append(f"{showname} S{season:02d}E{episode:02d}")
            if show_originaltitle and normalize_title(show_originaltitle) != normalize_title(showname):
                queries.append(f"{show_originaltitle} S{season:02d}E{episode:02d}")
            queries.append(f"{showname} {season}x{episode:02d}")
            if show_originaltitle and normalize_title(show_originaltitle) != normalize_title(showname):
                queries.append(f"{show_originaltitle} {season}x{episode:02d}")
            if episode_title:
                queries.append(f"{showname} {episode_title}")
                if show_originaltitle and normalize_title(show_originaltitle) != normalize_title(showname):
                    queries.append(f"{show_originaltitle} {episode_title}")
    else:
        title = (params.get("title") or "").strip()
        originaltitle = (params.get("originaltitle") or "").strip()
        year = str(params.get("year") or "").strip()
        if title:
            if year:
                queries.append(f"{title} {year}")
            queries.append(title)
        if originaltitle and normalize_title(originaltitle) != normalize_title(title):
            if year:
                queries.append(f"{originaltitle} {year}")
            queries.append(originaltitle)

    dedup: List[str] = []
    seen = set()
    for q in queries:
        key = normalize_title(q)
        if key and key not in seen:
            seen.add(key)
            dedup.append(q)
    return dedup


def parse_quality(filename: str) -> Dict[str, Any]:
    text = normalize_title(filename)
    quality = "sd"
    score = 0
    if "2160p" in text:
        quality, score = "2160p", 30
    elif "1080p" in text:
        quality, score = "1080p", 20
    elif "720p" in text:
        quality, score = "720p", 10
    return {"quality": quality, "quality_score": score}


def parse_size(size_value: Any) -> int:
    try:
        return int(float(size_value))
    except (TypeError, ValueError):
        return 0


def _has_bad_tokens(text: str) -> bool:
    raw = re.sub(r"[._-]+", " ", (text or "").lower())
    words = set(raw.split())
    return any(token in words for token in ("sample", "trailer", "cam", "hdcam", "telesync", "ts"))


def _extract_years(text: str) -> List[int]:
    return [int(y) for y in re.findall(r"\b(19\d{2}|20\d{2})\b", text)]


def score_movie_result(file_info: Dict[str, Any], params: Dict[str, Any]) -> int:
    name = file_info.get("name", "")
    normalized = normalize_title(name)
    title = normalize_title(params.get("title", ""))
    original = normalize_title(params.get("originaltitle", ""))
    year = _as_int(params.get("year"))

    score = 0
    if title and title in normalized:
        score += 70
    if original and original in normalized and original != title:
        score += 20

    years = _extract_years(normalized)
    if year:
        if year in years:
            score += 15
        elif years:
            score -= 20

    if _has_bad_tokens(name):
        score -= 60

    score += parse_quality(name)["quality_score"] // 4
    return score


def score_episode_result(file_info: Dict[str, Any], params: Dict[str, Any]) -> int:
    name = file_info.get("name", "")
    normalized = normalize_title(name)
    show = normalize_title(params.get("showname", ""))
    show_orig = normalize_title(params.get("show_originaltitle", ""))
    ep_title = normalize_title(params.get("episode_title", ""))
    season = _as_int(params.get("season"))
    episode = _as_int(params.get("episode"))

    score = 0
    if show and show in normalized:
        score += 55
    if show_orig and show_orig != show and show_orig in normalized:
        score += 15

    sxe = f"s{season:02d}e{episode:02d}"
    xfmt = f"{season}x{episode:02d}"
    if season > 0 and episode > 0:
        if sxe in normalized.replace(" ", ""):
            score += 80
        elif xfmt in normalized.replace(" ", ""):
            score += 60

        other = re.findall(r"s(\d{2})e(\d{2})", normalized.replace(" ", ""))
        if other and (f"{season:02d}", f"{episode:02d}") not in other:
            score -= 50

    if ep_title and ep_title in normalized:
        score += 10

    if _has_bad_tokens(name):
        score -= 60

    score += parse_quality(name)["quality_score"] // 5
    return score
