# AGENTS.md — Project Rules & Guidelines

## Figure Mapping Rules for Manuscript (`paper/manuscript/src/sections/methodology.tex`)

To prevent regressions in LaTeX compilation and figure-to-caption alignment, always maintain the following strict mapping:

1. **Figure 1 (`\label{fig:strata-map}`):**
   - **Position:** Inside Section 3.1 (`\subsection{Study area}`).
   - **Caption:** `\caption{\.{I}zmir functional urban region study area map...}`
   - **Image:** `\includegraphics[width=\textwidth]{fig1}` (`outputs/figures/fig1.png`).

2. **Figure 2 (`\label{fig:flowchart}`):**
   - **Position:** At the end of Section 3.7 (`Spatial prioritization` / end of `methodology.tex`).
   - **Caption:** `\caption{Methodological flowchart of the two-stage explain-then-optimize...}`
   - **Image:** `\includegraphics[width=\textwidth]{fig2}` (`outputs/figures/fig2.png`).

3. **Explicit Manuscript Figures from `outputs/figures`:**
   - Figure 1: `fig1` (`fig1.png`)
   - Figure 2: `fig2` (`fig2.png`)
   - Figure 3: `fig3` (`fig3.png`)
   - Figure 5: `fig5` (`fig5.png`)
   - Figure 9: `fig9` (`fig9.png`)

Do not swap the caption positions or image inclusions.
