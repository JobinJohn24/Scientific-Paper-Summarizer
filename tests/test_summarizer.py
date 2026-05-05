import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from summarizer import clean_text, ensure_all_sections


def test_clean_text_removes_extra_whitespace():
    assert clean_text("  A   short \n abstract.  ") == "A short abstract."


def test_ensure_all_sections_adds_fallback_structure():
    output = ensure_all_sections(
        text="This is not in the required format.",
        title="Example Title",
        abstract="We investigated whether reminders improved follow-up visits. We used a randomized trial. Results showed higher completion rates.",
        generated_summary="This study tested whether reminders help and found they improved completion.",
    )
    assert "Title:" in output
    assert "Plain-English Summary:" in output
    assert "Methods:" in output
    assert "Key Findings:" in output
