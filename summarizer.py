import re
from functools import lru_cache

from config import CONFIG


SECTION_HEADERS = [
    "Title",
    "Plain-English Summary",
    "Main Topic",
    "Research Question",
    "Methods",
    "Key Findings",
    "Why It Matters",
    "Important Terms Explained",
]


def clean_text(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def split_sentences(text: str) -> list[str]:
    cleaned = clean_text(text)
    if not cleaned:
        return []
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", cleaned) if part.strip()]


def extract_sentence_by_keywords(text: str, keywords: list[str]) -> str:
    for sentence in split_sentences(text):
        lowered = sentence.lower()
        if any(keyword in lowered for keyword in keywords):
            return sentence
    return ""


def extract_important_terms(text: str, max_terms: int = 4) -> list[str]:
    terms: list[str] = []
    seen: set[str] = set()

    acronym_matches = re.findall(r"\b([A-Z][A-Z0-9-]{1,})\b", text)
    long_form_matches = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b", text)

    for match in acronym_matches + long_form_matches:
        term = match.strip()
        normalized = term.lower()
        if normalized in seen:
            continue
        if len(term) < 3:
            continue
        seen.add(normalized)
        terms.append(term)
        if len(terms) >= max_terms:
            break

    return terms


def build_prompt(title: str, abstract: str) -> str:
    prompt_title = clean_text(title) or "Untitled Scientific Abstract"
    prompt_abstract = clean_text(abstract)
    return f"""
You are helping a student understand a scientific abstract.
Read the abstract and explain it in simple, plain English.
Avoid jargon when possible. If a technical term is important, explain it briefly.
Keep each section concise and accurate.

Return the answer using exactly these headings:
Title:
Plain-English Summary:
Main Topic:
Research Question:
Methods:
Key Findings:
Why It Matters:
Important Terms Explained:

Title: {prompt_title}
Abstract: {prompt_abstract}
""".strip()


def fallback_structure(title: str, abstract: str, generated_summary: str) -> str:
    sentences = split_sentences(abstract)
    topic = sentences[0] if sentences else "The abstract describes a scientific research study."
    question = extract_sentence_by_keywords(
        abstract,
        [
            "aim",
            "objective",
            "we asked",
            "we investigate",
            "we investigated",
            "this study examines",
            "this study explored",
            "whether",
        ],
    ) or "The study asks what the researchers wanted to understand or test."
    methods = extract_sentence_by_keywords(
        abstract,
        [
            "method",
            "using",
            "we used",
            "we analyzed",
            "we measured",
            "participants",
            "dataset",
            "experiment",
            "trial",
            "sequencing",
            "survey",
        ],
    ) or "The researchers used a scientific method described in the abstract."
    findings = extract_sentence_by_keywords(
        abstract,
        [
            "found",
            "results",
            "show",
            "showed",
            "observed",
            "improved",
            "increased",
            "decreased",
            "associated",
        ],
    ) or (sentences[-1] if sentences else "The study reports its main result in the abstract.")
    why_it_matters = extract_sentence_by_keywords(
        abstract,
        [
            "suggest",
            "implication",
            "important",
            "may help",
            "supports",
            "could improve",
            "provides",
            "highlights",
        ],
    ) or "The findings matter because they add evidence that could help future research or real-world decisions."

    terms = extract_important_terms(abstract)
    term_lines = "\n".join(
        f"- {term}: Important scientific term mentioned in the abstract."
        for term in terms
    ) or "- No major technical terms needed extra explanation."

    return "\n".join(
        [
            f"Title: {clean_text(title) or 'Untitled Scientific Abstract'}",
            "",
            f"Plain-English Summary: {generated_summary or 'A simpler summary could not be generated, so the system returned a fallback explanation.'}",
            "",
            f"Main Topic: {topic}",
            "",
            f"Research Question: {question}",
            "",
            f"Methods: {methods}",
            "",
            f"Key Findings: {findings}",
            "",
            f"Why It Matters: {why_it_matters}",
            "",
            "Important Terms Explained:",
            term_lines,
        ]
    )


def ensure_all_sections(text: str, title: str, abstract: str, generated_summary: str) -> str:
    if all(header + ":" in text for header in SECTION_HEADERS):
        return text
    return fallback_structure(title=title, abstract=abstract, generated_summary=generated_summary)


@lru_cache(maxsize=1)
def load_model():
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(CONFIG.model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(CONFIG.model_name)
    model.to(CONFIG.device)
    model.eval()
    return tokenizer, model


class ScientificAbstractSummarizer:
    def __init__(self) -> None:
        self.model_name = CONFIG.model_name

    def summarize(self, abstract: str, title: str = "") -> str:
        cleaned_abstract = clean_text(abstract)
        cleaned_title = clean_text(title)

        if not cleaned_abstract:
            raise ValueError("Please paste a scientific abstract before generating a summary.")

        prompt = build_prompt(cleaned_title, cleaned_abstract)
        tokenizer, model = load_model()

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=CONFIG.max_input_tokens,
        )
        inputs = {key: value.to(CONFIG.device) for key, value in inputs.items()}

        import torch

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=CONFIG.max_new_tokens,
                min_new_tokens=CONFIG.min_new_tokens,
                num_beams=CONFIG.num_beams,
                temperature=CONFIG.temperature,
                repetition_penalty=CONFIG.repetition_penalty,
                no_repeat_ngram_size=CONFIG.no_repeat_ngram_size,
                early_stopping=True,
            )

        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        structured = ensure_all_sections(
            text=decoded,
            title=cleaned_title,
            abstract=cleaned_abstract,
            generated_summary=decoded,
        )
        return structured
