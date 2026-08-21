"""
Unit tests for YouTube Media Production Agents (Shorts, Longform & Bilingual Voiceovers)
"""

import pytest
from visionloop_sdk.swarm import (
    YouTubeShortsProducerAgent,
    YouTubeLongformDirectorAgent,
    ChiefAuditorVerificationAgent,
    VideoFormat,
    AudioLanguage
)

@pytest.mark.asyncio
async def test_youtube_shorts_production_and_cross_examination():
    shorts_agent = YouTubeShortsProducerAgent()
    auditor = ChiefAuditorVerificationAgent()

    # Step 1: Generate Shorts Production Blueprint
    proposal = await shorts_agent.process_task(
        task_instruction="Create viral YouTube Short on 15% Sinking Fund",
        context={"duration_sec": 45, "primary_language": AudioLanguage.HINDI}
    )

    pkg = proposal.data_payload
    assert pkg["format_type"] == VideoFormat.SHORTS_VERTICAL.value
    assert pkg["visual_spec"]["aspect_ratio"] == "9:16"
    assert pkg["visual_spec"]["resolution_width"] == 1080
    assert pkg["visual_spec"]["resolution_height"] == 1920
    assert pkg["target_duration_seconds"] == 45
    assert pkg["voiceover_spec"]["target_loudness_lufs"] == -14.0
    assert len(pkg["scenes"]) == 4

    # Check Bilingual Localization
    for scene in pkg["scenes"]:
        assert len(scene["voiceover_script_english"]) > 0
        assert len(scene["voiceover_script_hindi"]) > 0

    # Step 2: Auditor Cross-Examination
    audit_result = await auditor.cross_examine_and_verify(shorts_agent, proposal)
    assert audit_result.verified is True
    assert any("YouTube Shorts Formatting" in inv for inv in audit_result.invariants_checked)
    assert any("Bilingual Audio" in inv for inv in audit_result.invariants_checked)


@pytest.mark.asyncio
async def test_youtube_longform_production_and_cross_examination():
    longform_agent = YouTubeLongformDirectorAgent()
    auditor = ChiefAuditorVerificationAgent()

    # Step 1: Generate Long-form 4K Production Blueprint
    proposal = await longform_agent.process_task(
        task_instruction="Produce 10-minute master deep-dive on EV Leasing and GST 997311 in India",
        context={"duration_sec": 600, "primary_language": AudioLanguage.ENGLISH_INDIAN}
    )

    pkg = proposal.data_payload
    assert pkg["format_type"] == VideoFormat.LONGFORM_HORIZONTAL.value
    assert pkg["visual_spec"]["aspect_ratio"] == "16:9"
    assert pkg["visual_spec"]["resolution_width"] == 3840
    assert pkg["visual_spec"]["resolution_height"] == 2160
    assert pkg["target_duration_seconds"] == 600
    assert pkg["voiceover_spec"]["target_loudness_lufs"] == -14.0
    assert len(pkg["scenes"]) == 4
    assert "CHAPTERS:" in pkg["description_english"]

    # Step 2: Auditor Cross-Examination
    audit_result = await auditor.cross_examine_and_verify(longform_agent, proposal)
    assert audit_result.verified is True
    assert any("YouTube Long-Form Invariant" in inv for inv in audit_result.invariants_checked)
    assert any("Bilingual Audio" in inv for inv in audit_result.invariants_checked)
