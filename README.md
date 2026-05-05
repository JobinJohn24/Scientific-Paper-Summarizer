# Scientific Paper Abstract Summarizer

Portfolio-ready NLP project that turns scientific abstracts into clear, plain-English summaries using Hugging Face models and a Gradio interface.

## Project Overview

This project helps students, researchers, and non-technical readers understand scientific papers faster. A user pastes a research abstract into the app, and the system generates a simpler explanation with structured sections:

- what the paper is about
- what question the researchers asked
- how they studied it
- what they found
- why the result matters

This is useful because scientific writing is often dense, technical, and full of field-specific language. The app makes research more accessible while still keeping the main ideas intact.

## Why This Project Works Well in a Portfolio

- It shows practical NLP application design.
- It uses real Hugging Face tooling.
- It includes an interactive UI, not just a notebook.
- It is small enough for a beginner to finish.
- It leaves room for later upgrades like fine-tuning, evaluation, and deployment.

## Recommended Model Choices

These recommendations were checked against current Hugging Face model pages and Transformers summarization docs.

### 1. `google/flan-t5-base`
Link: [google/flan-t5-base](https://hf.co/google/flan-t5-base)

What it is good at:
- Instruction-following text generation
- Flexible prompting
- Producing structured outputs

Why it may work for scientific text:
- You can directly prompt it to explain an abstract in plain English.
- It is useful when you want more than a short summary, such as sectioned outputs.

Possible limitations:
- It is not specialized for scientific literature.
- It may simplify too aggressively or miss domain nuance.

Beginner-friendly:
- Yes. Good default choice for a first working prototype.

### 2. `facebook/bart-large-cnn`
Link: [facebook/bart-large-cnn](https://hf.co/facebook/bart-large-cnn)

What it is good at:
- Strong baseline abstractive summarization
- Easy to use through the Transformers summarization pipeline

Why it may work for scientific text:
- It is a reliable starting point for summarization even outside news.
- Good for comparing a generic summarizer against more specialized models.

Possible limitations:
- It was trained on news summarization, not scientific abstracts.
- It may miss methods or technical nuance.

Beginner-friendly:
- Yes. Very common and well-documented.

### 3. `allenai/led-base-16384`
Link: [allenai/led-base-16384](https://hf.co/allenai/led-base-16384)

What it is good at:
- Long-document summarization
- Handling much longer inputs than standard encoder-decoder models

Why it may work for scientific text:
- Useful if you later expand from abstracts to full papers or long sections.

Possible limitations:
- Heavier than a small starter model.
- More setup decisions are needed for longer documents.

Beginner-friendly:
- Medium. Better as a phase-two or future-upgrade model.

### 4. `UNIST-Eunchan/Research-Paper-Summarization-Pegasus-x-ArXiv`
Link: [UNIST-Eunchan/Research-Paper-Summarization-Pegasus-x-ArXiv](https://hf.co/UNIST-Eunchan/Research-Paper-Summarization-Pegasus-x-ArXiv)

What it is good at:
- Research-paper-focused summarization
- Based on PEGASUS-X and fine-tuned on arXiv summarization data

Why it may work for scientific text:
- It is closer to the target domain than general news models.
- Useful for model comparison once the basic app works.

Possible limitations:
- Lower community usage than broad baseline models.
- Less beginner-friendly documentation than BART or T5 baselines.

Beginner-friendly:
- Medium. Good comparison model after the baseline is stable.

### 5. `allenai/scibert_scivocab_uncased`
Link: [allenai/scibert_scivocab_uncased](https://hf.co/allenai/scibert_scivocab_uncased)

What it is good at:
- Understanding scientific language
- Classification, tagging, retrieval, and downstream scientific NLP tasks

Why it may work for scientific text:
- Useful later for jargon detection, entity extraction, or term explanation.
- Helpful as a companion model in an upgraded version of the project.

Possible limitations:
- It is not a drop-in summarization model.
- You would not use it as the main summarizer in this first version.

Beginner-friendly:
- Medium. Best treated as an advanced extension.

## Suggested Starting Model

Use `google/flan-t5-base` for version 1.

Reason:
- It handles instruction prompts well.
- It can generate the exact section format you want.
- It keeps the code simple for a beginner-friendly portfolio project.

If your machine is slower, switch to `google/flan-t5-small`.

## Project Architecture

```text
scientific-paper-summarizer/
│
├── app.py
├── summarizer.py
├── config.py
├── requirements.txt
├── README.md
├── examples/
├── data/
└── tests/
```

### File Purposes

- `app.py`: Gradio user interface. Handles text input, buttons, examples, and output display.
- `summarizer.py`: Core NLP logic. Loads the Hugging Face model, builds prompts, cleans text, and generates structured summaries.
- `config.py`: Central place for model name, generation settings, and example file paths.
- `requirements.txt`: Python packages needed to run the project locally.
- `README.md`: Project documentation for GitHub and portfolio presentation.
- `examples/`: Sample abstracts for testing the app.
- `data/`: Placeholder for future evaluation data, saved summaries, or fine-tuning datasets.
- `tests/`: Simple tests for helper functions and formatting logic.

## Full Workflow

### Step 1: User pastes abstract
The user enters a paper title and abstract into the Gradio app.

### Step 2: Text is cleaned
The system removes extra whitespace and normalizes the input.

### Step 3: Hugging Face model processes text
The app sends a prompt to a Hugging Face encoder-decoder model.

### Step 4: Summary is generated
The model creates a simplified, structured explanation.

### Step 5: Summary is simplified into plain English
The prompt asks for short, accessible explanations and reduced jargon.

### Step 6: Results are displayed in the app
The final answer appears in the interface using the required section headings.

## Implementation Plan

### Phase 1: Basic summarizer
- Load one Hugging Face model
- Accept pasted abstract text
- Return a plain-English output

### Phase 2: Clean UI
- Build a Gradio interface
- Add title field, abstract box, and sample examples
- Improve layout and readability

### Phase 3: Structured summary sections
- Return the summary using fixed headings
- Add fallback logic if the model misses a section

### Phase 4: Model comparison
- Compare `flan-t5-base`, `bart-large-cnn`, and a scientific-domain model
- Check which model is easiest to understand and most accurate

### Phase 5: Deployment to Hugging Face Spaces
- Push the project to GitHub
- Create a Space
- Upload the files and launch the app

### Phase 6: GitHub README and portfolio polish
- Add screenshots
- Add example input and output
- Explain what you learned and how you would improve it

## Plain-English Summary Format

The app outputs this structure:

```text
Title:
Plain-English Summary:
Main Topic:
Research Question:
Methods:
Key Findings:
Why It Matters:
Important Terms Explained:
```

## Example Abstracts

Three sample abstracts are included in the `examples/` folder:

- `biology_genomics_abstract.txt`
- `public_health_abstract.txt`
- `machine_learning_abstract.txt`

## Evaluation Strategy

Use both human judgment and later automatic metrics.

### Human evaluation first

- Readability: Is the explanation understandable to a student outside the field?
- Accuracy: Does the summary match the original abstract?
- Coverage: Are the question, methods, findings, and importance all included?
- Hallucination check: Did the model invent details that were not in the abstract?
- Terminology handling: Are difficult terms explained simply instead of removed incorrectly?

### Simple manual evaluation workflow

1. Read the original abstract.
2. Read the generated summary.
3. Highlight any missing key idea.
4. Highlight any invented claim.
5. Decide whether the output is useful for a beginner.

### Later automatic evaluation

- ROUGE for overlap-based comparison
- BERTScore for semantic similarity
- Custom rubric scoring for plain-English readability

## How To Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/scientific-paper-summarizer.git
cd scientific-paper-summarizer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Then open the local Gradio URL shown in the terminal.

## Example Input / Output

### Example Input

Title:
`Mobile reminder messages and vaccination completion in urban primary-care clinics`

Abstract:
`We conducted a randomized trial across six urban primary-care clinics to test whether SMS reminders improved completion of a two-dose adult vaccination schedule...`

### Example Output

```text
Title: Mobile reminder messages and vaccination completion in urban primary-care clinics

Plain-English Summary: This study tested whether text-message reminders help adults finish a vaccine series. Patients who received reminders were more likely to complete both doses, especially in younger groups. The findings suggest that low-cost messaging can improve follow-up care in busy clinics.

Main Topic: Vaccination adherence and digital health reminders.

Research Question: Can SMS reminders improve completion of a two-dose vaccine schedule?

Methods: The researchers ran a randomized trial in six clinics and compared reminder and no-reminder groups.

Key Findings: Patients who received reminder messages completed the vaccine schedule more often.

Why It Matters: A simple digital intervention may improve public-health outcomes without large costs.

Important Terms Explained:
- SMS: Standard text message sent to a mobile phone.
- Randomized trial: A study where participants are assigned to groups by chance.
```

## Deployment Plan: Hugging Face Spaces

### Recommended choice

Use Gradio Spaces because this app is already written with Gradio.

### Deployment steps

1. Create a new GitHub repository and push this project.
2. Log in to Hugging Face.
3. Create a new Space.
4. Choose `Gradio` as the Space SDK.
5. Connect the GitHub repository or upload the project files directly.
6. Make sure `requirements.txt` is included.
7. Set `app.py` as the main app file.
8. Wait for the Space to build.
9. Test the live app with the included examples.

### Helpful deployment note

If the default model feels slow, switch to a smaller checkpoint before deploying.

## Vercel Deployment Note

This repository also includes [index.py](/Users/jobinjohn/Desktop/projects/scientific-paper-summarizer/index.py), which mounts the Gradio interface on a FastAPI app so the project can be deployed on Vercel's Python runtime.

Why this is needed:

- Gradio is easiest to run locally as a Python web app.
- Vercel deploys Python applications as functions and ASGI apps.
- The FastAPI wrapper provides a Vercel-compatible entrypoint without changing the local developer experience.

## Future Improvements

- PDF upload for abstract extraction
- Full paper summarization
- Citation extraction
- Keyword extraction
- Jargon simplification dictionary
- Side-by-side model comparison dashboard
- Biomedical named entity recognition
- Save summary as PDF
- Paper Q&A chatbot
- Fine-tuning on PubMed or arXiv summarization datasets

## What I Learned

Use this section in your portfolio write-up:

- How to build an end-to-end NLP app with Hugging Face
- How prompting changes summarization quality
- Why domain-specific text is harder than general text
- How to balance readability and accuracy
- How to turn an ML idea into a usable product

## Notes For Version 1

Keep the first release simple:

- one model
- one input box
- one output format
- one clean interface

Once that works reliably, add comparison models and advanced scientific NLP features.
