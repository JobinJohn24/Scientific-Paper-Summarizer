from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
EXAMPLES_DIR = BASE_DIR / "examples"


@dataclass(frozen=True)
class AppConfig:
    app_title: str = "Scientific Paper Abstract Summarizer"
    app_description: str = (
        "Paste a scientific abstract and get a plain-English summary with "
        "student-friendly sections."
    )
    model_name: str = "google/flan-t5-base"
    max_input_chars: int = 6000
    max_input_tokens: int = 1024
    max_new_tokens: int = 256
    min_new_tokens: int = 96
    num_beams: int = 4
    temperature: float = 0.3
    repetition_penalty: float = 1.1
    no_repeat_ngram_size: int = 3
    device: str = "cpu"


CONFIG = AppConfig()


EXAMPLE_FILES = {
    "Biology / Genomics": EXAMPLES_DIR / "biology_genomics_abstract.txt",
    "Public Health": EXAMPLES_DIR / "public_health_abstract.txt",
    "Machine Learning": EXAMPLES_DIR / "machine_learning_abstract.txt",
}
