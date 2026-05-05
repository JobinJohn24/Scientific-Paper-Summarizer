from fastapi import FastAPI

import gradio as gr

from app import demo


web_app = FastAPI(title="Scientific Paper Abstract Summarizer")
app = gr.mount_gradio_app(web_app, demo, path="/")
