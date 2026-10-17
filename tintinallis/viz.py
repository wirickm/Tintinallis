"""3D t-SNE plot of the vector store embeddings."""

import numpy as np
import plotly.graph_objects as go
from sklearn.manifold import TSNE


def embedding_figure(store):
    """Return a 3D t-SNE scatter of all chunks colored by section."""
    result = store._collection.get(include=["embeddings", "documents", "metadatas"])
    vectors = np.array(result["embeddings"]) if result["embeddings"] is not None else np.empty((0, 0))
    n = len(vectors)
    if n < 4:
        fig = go.Figure()
        fig.update_layout(title="Not enough chunks to plot embeddings")
        return fig
    reduced = TSNE(n_components=3, perplexity=min(30, n - 1), random_state=42).fit_transform(vectors)
    sections = [(m or {}).get("section", "unknown") for m in result["metadatas"]]
    fig = go.Figure()
    for section in sorted(set(sections)):
        idx = [i for i, s in enumerate(sections) if s == section]
        fig.add_trace(go.Scatter3d(
            x=reduced[idx, 0], y=reduced[idx, 1], z=reduced[idx, 2],
            mode="markers", name=section, marker=dict(size=5, opacity=0.8),
            text=[result["documents"][i][:100] + "..." for i in idx], hoverinfo="text",
        ))
    fig.update_layout(title="3D Chroma Vector Store Visualization",
                      scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z"),
                      margin=dict(r=20, b=10, l=10, t=40))
    return fig
