# AI Prompt for Phase K

## Initial prompt for creating the K Phase

**GPT-5.2-Codex [AI_TOOL_DISCLOSURE.md](AI_TOOL_DISCLOSURE.md):**
```markdown
You have full access to my codebase. Your task is to complete **Phase K of the QUACK workflow** and implement the corresponding **Streamlit application**.

## Project status

The following phases are already complete:

* Phase Q
* Phase U
* Phase A
* Phase C

Their executed notebooks are:

* `notebooks/001_Q_Phase.ipynb`
* `notebooks/002_U_Phase.ipynb`
* `notebooks/003_A_Phase.ipynb`
* `notebooks/004_C_Phase.ipynb`

All cells have already been run, and their outputs are stored in the notebooks. Read these notebooks carefully to understand the project, with particular attention to `notebooks/001_Q_Phase.ipynb`, which contains essential project context, objectives, stakeholders, and requirements.

## Supporting material

Use the following sources as context:

1. `docs/course-material`

   * Read the documentation about the QUACK methodology.
   * Focus especially on the requirements, goals, and expected outputs of Phase K.

2. `reference-repo/Degrees-of-No-Return-App`

   * This is a separate completed project provided only as a reference.
   * Inspect its Phase K notebook and finished Streamlit implementation.
   * Use it to understand the expected depth, structure, analytical reasoning, visualisation approach, and implementation quality.
   * Adapt relevant ideas to my project rather than copying them blindly.

The reference repository is temporary and will be deleted after this project is finished.

## Critical constraint

Do **not** integrate, import, depend on, or reference files from `reference-repo/Degrees-of-No-Return-App` in the final implementation.

The completed project must work independently after the entire `reference-repo` directory has been deleted.

Do not copy project-specific assumptions, labels, variables, datasets, text, or visualisations from the reference project unless they are genuinely appropriate for my project.

## Part 1: Understand the project

Before modifying files:

1. Inspect the repository structure.
2. Read the course documentation relevant to Phase K.
3. Read all completed QUAC notebooks and their stored outputs.
4. Identify:

   * the project objective;
   * the target users and stakeholders;
   * the main analytical findings;
   * the available processed data and models;
   * the decisions the final application should support;
   * any requirements or commitments established in earlier phases.
5. Inspect the reference project’s Phase K notebook and Streamlit application.
6. Determine which aspects of the reference implementation are reusable as patterns and which must be redesigned for this project.

Do not begin by copying the reference app.

## Part 2: Design the Streamlit application

Before implementing the app, perform a project-specific design analysis.

Determine:

* the app’s primary user journey;
* the most important questions the app should answer;
* which findings should be visible immediately;
* which visualisations best communicate the project’s results;
* how information should be grouped across pages, tabs, sections, or sidebars;
* which controls provide real analytical value;
* which controls would create unnecessary complexity;
* whether users should be able to change filters, ranges, thresholds, categories, scenarios, model parameters, or other relevant settings;
* how outputs should update when users change those settings;
* how uncertainty, limitations, assumptions, and interpretation guidance should be communicated;
* what explanatory text, labels, tooltips, captions, or annotations are needed;
* how to make the application understandable to its intended audience without requiring them to read the notebooks.

Base these decisions on my project’s data, findings, and stakeholder needs—not merely on the structure of the reference project.

Document this design reasoning in the Phase K notebook before implementing the app.

## Part 3: Complete the Phase K notebook

Write the finished Phase K work into:

`notebooks/005_K_Phase.ipynb`

The notebook is currently empty.

It should be a polished, self-contained continuation of the previous notebooks and should include, where appropriate:

1. Phase K objective and connection to the earlier QUAC phases.
2. Summary of the relevant project context and key findings.
3. Intended audience and decision-making use case.
4. Requirements for the final application.
5. Analysis of suitable visualisations and interaction patterns.
6. Comparison of alternative app designs.
7. Justification for the selected design.
8. Planned application structure and user flow.
9. Description of filters, controls, ranges, thresholds, or settings.
10. Explanation of the implemented visualisations and metrics.
11. Data flow and implementation approach.
12. Validation of the app’s outputs against the notebook results.
13. Limitations, assumptions, and responsible-use considerations.
14. Final conclusions and recommendations.

Use clear Markdown, well-structured sections, concise explanations, and executable code cells where relevant.

Reuse existing project utilities and data-processing logic whenever possible instead of duplicating code unnecessarily.

Ensure the notebook contains no broken paths, missing variables, placeholder text, unfinished sections, or references that require the temporary reference repository.

## Part 4: Implement the Streamlit application

Implement the final Streamlit app in the location and structure most consistent with the existing repository.

Before creating new files, inspect whether the project already contains:

* a Streamlit entry point;
* an `app`, `src`, or `pages` directory;
* shared utility modules;
* configuration files;
* data-loading functions;
* plotting functions;
* modelling or inference code.

Prefer extending the existing architecture over creating a competing structure.

The app should:

* reflect the project goals established in Phase Q;
* present the most important findings clearly;
* use appropriate interactive visualisations;
* provide only meaningful user controls;
* explain metrics and outputs in plain language;
* handle missing, empty, or invalid inputs gracefully;
* use cached data or resource loading where beneficial;
* avoid recomputing expensive operations unnecessarily;
* use paths that work from the repository root;
* avoid hard-coded machine-specific paths;
* avoid dependencies on notebook-only state;
* avoid dependencies on the reference repository;
* follow the project’s existing visual and coding conventions;
* remain maintainable and reasonably modular.

Where useful, separate data loading, transformation, visualisation, and user-interface logic into reusable functions or modules.

Do not invent functionality that is unsupported by the available data or previous analysis.

## Part 5: Verification

After implementation:

1. Run or validate the Phase K notebook.
2. Check that all notebook cells execute in order from a clean kernel.
3. Start the Streamlit application.
4. Test the main user flow and all interactive controls.
5. Verify that visualisations and metrics agree with the notebook outputs.
6. Check for broken imports, file paths, missing assets, undefined variables, and dependency issues.
7. Confirm that the app still works without accessing `reference-repo`.
8. Remove temporary debugging code and unnecessary generated files.
9. Do not modify unrelated parts of the repository.

If execution is blocked by a missing dependency, unavailable dataset, or environment limitation, still complete as much as possible and clearly document:

* what is blocked;
* the exact reason;
* the affected file or feature;
* the command or action needed to finish verification.

## Expected deliverables

Complete all of the following:

* `notebooks/005_K_Phase.ipynb`
* the finished Streamlit application;
* any necessary supporting modules or configuration changes;
* dependency updates only where required.

At the end, provide a concise implementation report containing:

1. Files created or modified.
2. App structure and main user flow.
3. Visualisations and interactions implemented.
4. Important design decisions and their rationale.
5. Validation performed.
6. Remaining limitations or unresolved issues.
7. The exact command for launching the Streamlit app.

Work autonomously and make reasonable project-specific decisions based on the repository evidence. Do not stop at an analysis or implementation plan—the required output is a completed Phase K notebook and a working Streamlit implementation.
```

## Prompt for updating the README.md

**GPT-5.2-Codex [AI_TOOL_DISCLOSURE.md](AI_TOOL_DISCLOSURE.md):**
```markdown
Look at my README.md. It got longer not updated. ANalyze my whole project and update my README.md file. Additionally: add explanaitions for using the project:
- setup uv: from download to sync/run etc.
- setup git lfs and pull the objects by first clone
- start the app and stop the run
```

## Prompt for creating a summary

**GPT-5.2-Codex [AI_TOOL_DISCLOSURE.md](AI_TOOL_DISCLOSURE.md):**
```markdown
You have access to the complete project repository. Analyze the project and create a clear, accurate, and reader-friendly project summary based on the repository’s actual contents.

## Objective

Write the finished summary directly to:

```text
docs/overview_summary.md
```

The file is currently empty and should be replaced with the completed Markdown document.

## Analysis Scope

Review the entire repository, including:

* the repository structure
* `README` and other documentation files
* configuration and dependency files
* source code
* the Streamlit application
* data-related files and scripts
* all notebooks inside `notebooks/`

The notebooks have already been executed and contain saved outputs. Use both their Markdown explanations and their visible outputs, including:

* tables
* metrics
* charts
* model results
* comparisons
* observations
* conclusions

Do not rerun the notebooks unless this is necessary to understand the project. Treat the saved notebook outputs as the primary source for reported results.

## Methodology

Organize the project summary according to the **QUA³CK process model**:

* **Q — Question:** problem, research question, target audience, success criteria, and intended product
* **U — Understanding the Data:** dataset, variables, data quality, preparation, exploratory analysis, patterns, and important findings
* **A³ — Algorithm Selection, Adapting Features, and Adjusting Hyperparameters:** feature preparation, models tested, training approach, experiments, optimization, and iteration
* **C — Conclude & Compare:** evaluation metrics, model comparison, selected solution, strengths, weaknesses, and reasons for the final choice
* **K — Knowledge Transfer:** deployment, Streamlit application, documentation, reproducibility, practical use, and possible next steps

Base every section on evidence found in the repository. Do not invent missing project details, results, metrics, or decisions. When something is unclear or undocumented, state that explicitly.

## Required Document Structure

Use the following structure:

```markdown
# Project Summary

## Overview

Provide a concise explanation of:

- what the project does
- which problem it addresses
- which data and methods it uses
- what the final result or product is

## Phase Q — Question

Explain the original problem, project objective, target audience, success criteria, and intended outcome.

## Phase U — Understanding the Data

Explain the dataset, relevant variables, data quality, preparation steps, exploratory analysis, visual findings, and the most important insights.

## Phase A³ — Algorithm Development and Optimization

### Algorithm Selection

Explain which algorithms or approaches were evaluated and why they were appropriate.

### Adapting Features

Explain feature selection, transformations, preprocessing, encoding, scaling, or feature engineering performed in the project.

### Adjusting Hyperparameters

Explain tuning, experimentation, validation, iteration, and any changes made to improve the models.

## Phase C — Conclude & Compare

Summarize the results of each evaluated approach.

Include a compact Markdown comparison table when the repository contains enough information, for example:

| Model or Approach | Main Metrics | Strengths | Limitations |
|---|---:|---|---|

Explain:

- which approach performed best
- which evaluation criteria were used
- whether the project met its success criteria
- why the final solution was selected
- any important limitations or uncertainties

## Phase K — Knowledge Transfer

Explain how the results were turned into a usable product or communicated to others.

Cover relevant elements such as:

- the Streamlit application
- model integration
- user workflow
- documentation
- reproducibility
- deployment
- practical value
- recommended next steps

# Finished Product

[Open the Streamlit application](STREAMLIT_APP_LINK)
```

Keep `STREAMLIT_APP_LINK` as a placeholder unless an actual deployment URL exists in the repository.

## Writing Requirements

* Write for readers who understand basic data science but may not know this project.
* Use simple, professional language.
* Explain technical decisions rather than merely listing them.
* Focus on the project-specific process and findings.
* Clearly connect notebook outputs to the corresponding QUA³CK phase.
* Report exact metrics when they are available.
* Avoid unsupported claims and generic textbook explanations.
* Do not copy notebook content verbatim; synthesize it into a coherent narrative.
* Use concise paragraphs, meaningful headings, and Markdown tables where useful.
* Preserve important model names, dataset names, feature names, and metric values exactly as shown in the project.
* Do not include code unless a very short excerpt is essential for understanding the project.
* Do not describe files one by one. Present the repository as one coherent project.

## Final Verification

Before finishing:

1. Confirm that all relevant notebooks were reviewed.
2. Verify every numerical result against the saved notebook outputs.
3. Confirm that all five QUA³CK phases are covered.
4. Check that no unsupported information was added.
5. Ensure the Markdown is readable and correctly formatted.
6. Save the completed document to `docs/overview_summary.md`.

At the end of your response, briefly report:

* that `docs/overview_summary.md` was updated
* which repository materials were used
* any important information that could not be determined from the repository
```