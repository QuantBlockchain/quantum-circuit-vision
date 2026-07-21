# Poster Figures

Matplotlib source that reproduces the four analysis charts on the QCV KDD 2026
poster (Cost-Accuracy Pareto Frontier, Difficulty Gradient, BV-vs-TV, Failure
Modes). These charts are not part of the paper LaTeX (the paper presents these
results as tables).

`make_poster_figures.py` computes every value directly from the released dataset
(`dataset/experiment_results/*.csv` and `dataset/annotations/*.json`) — no hard-coded
numbers — so the figures are provably consistent with the open-access experimental
results. Run: `python make_poster_figures.py` -> writes the four `.pdf` files here.
