"""Gradio chat UI with a 3D embedding tab."""

import os

import gradio as gr

from tintinallis.rag import answer, log_chat
from tintinallis.viz import embedding_figure


def build_app(store, llm=None):
    """Build the Gradio Blocks app for the given store."""

    def respond(message, history):
        text, docs = answer(message, store, llm=llm, history=history)
        sections = sorted({d.metadata.get("section", "unknown") for d in docs})
        if sections:
            text = f"{text}\n\nSources: {', '.join(sections)}"
        log_chat(message, text)
        return text

    with gr.Blocks(title="Tintinallis EM Assistant") as demo:
        with gr.Tab("Chat"):
            gr.ChatInterface(fn=respond)
        with gr.Tab("3D Embeddings"):
            plot = gr.Plot()
            button = gr.Button("Show graph")
            button.click(lambda: embedding_figure(store), outputs=plot)
    return demo


def main():
    """Load the index and launch the app."""
    from tintinallis.index import load_index

    demo = build_app(load_index())
    demo.launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "127.0.0.1"),
        server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
        share=False,
    )


if __name__ == "__main__":
    main()
