from resources.lib.source_ui import (
    detect_audio_format,
    detect_codec,
    detect_languages,
    detect_quality,
    detect_source_type,
    format_size,
    normalize_source,
    source_heading,
)


def test_format_size_mb_and_gb():
    assert format_size(700 * 1024 * 1024) == "700 MB"
    assert format_size(int(1.6 * 1024 * 1024 * 1024)) == "1.6 GB"


def test_detect_release_metadata():
    text = "Obsession 2026 S02E02 1080p NF WEB-DL DDP5.1 Atmos H.264 EN CZ titulky.mkv"
    assert detect_quality(text) == ("FHD", "1080p")
    assert detect_source_type(text) == "WEB-DL"
    assert detect_codec(text) == "H.264"
    assert detect_audio_format(text) == "DDP5.1"
    audio, subs = detect_languages(text)
    assert audio == ["EN"]
    assert subs == ["CZ"]


def test_detect_4k_h265_and_embedded_subtitles():
    text = "Film.2160p.UHD.BluRay.x265.CZ.vlozene.titulky.mkv"
    assert detect_quality(text) == ("4K", "2160p")
    assert detect_source_type(text) == "BluRay"
    assert detect_codec(text) == "H.265"
    audio, subs = detect_languages(text)
    assert audio == []
    assert subs == ["CZ"]


def test_normalize_source_handles_missing_metadata():
    source = normalize_source({"name": "Episode.720p.WEBRip.audio.Japanese.subs.en.mkv", "size": "734003200", "score": "72"})
    assert source["title"] == "Episode.720p.WEBRip.audio.Japanese.subs.en"
    assert source["quality_label"] == "HD"
    assert source["resolution_label"] == "720p"
    assert source["size_text"] == "700 MB"
    assert source["audio_langs"] == ["JA"]
    assert source["subtitle_langs"] == ["EN"]
    assert source["score"] == 72


def test_source_heading_keeps_modal_rows_short():
    source = normalize_source({
        "name": "Deadpool.2016.UHD.BluRay.2160p.TrueHD.Atmos.x265.CZ.SK.EN.mkv",
        "size": str(14 * 1024 * 1024 * 1024),
        "score": 92,
    })
    label = source_heading(source, max_title=28)
    assert label.startswith("[4K 2160p] Deadpool.2016.UHD.BluRay.21…")
    assert label.endswith("[92]")
    assert "Size" not in label
    assert "Audio" not in label
