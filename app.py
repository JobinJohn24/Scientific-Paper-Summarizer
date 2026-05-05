from pathlib import Path

import gradio as gr

from config import CONFIG, EXAMPLE_FILES
from summarizer import ScientificAbstractSummarizer


summarizer = ScientificAbstractSummarizer()


def read_example(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


EXAMPLES = [
    [
        "Single-cell RNA sequencing reveals stress-response pathways in drought-treated maize roots",
        read_example(EXAMPLE_FILES["Biology / Genomics"]),
    ],
    [
        "Mobile reminder messages and vaccination completion in urban primary-care clinics",
        read_example(EXAMPLE_FILES["Public Health"]),
    ],
    [
        "A lightweight transformer for identifying misinformation in scientific claim verification",
        read_example(EXAMPLE_FILES["Machine Learning"]),
    ],
]


def summarize_abstract(title: str, abstract: str) -> str:
    return summarizer.summarize(title=title, abstract=abstract)


with gr.Blocks(title=CONFIG.app_title) as demo:
    gr.Markdown(
        f"""
        # {CONFIG.app_title}

        {CONFIG.app_description}

        This prototype is designed for students, researchers, and non-technical readers
        who want a faster way to understand research abstracts.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            title_input = gr.Textbox(
                label="Paper Title (Optional)",
                placeholder="Paste the paper title here",
            )
            abstract_input = gr.Textbox(
                label="Scientific Abstract",
                placeholder="Paste a scientific abstract here",
                lines=14,
                max_lines=20,
            )

            with gr.Row():
                summarize_button = gr.Button("Generate Summary", variant="primary")
                clear_button = gr.Button("Clear")

        with gr.Column(scale=1):
            output = gr.Markdown(label="Summary Output")

    gr.Examples(
        examples=EXAMPLES,
        inputs=[title_input, abstract_input],
        label="Example Abstracts",
    )

    summarize_button.click(
        fn=summarize_abstract,
        inputs=[title_input, abstract_input],
        outputs=output,
    )
    clear_button.click(
        fn=lambda: ("", "", ""),
        inputs=None,
        outputs=[title_input, abstract_input, output],
    )


if __name__ == "__main__":
    demo.launch()
