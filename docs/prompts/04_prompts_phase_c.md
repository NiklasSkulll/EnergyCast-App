

```markdown
You are working directly inside my existing data science repository. Your task is to complete the **C phase ("Conclude & Compare")** of my QUA³CK project by analyzing the preceding work and writing a complete, reproducible notebook.

## Primary deliverable

**Complete the currently empty notebook:**
- `notebooks/004_C_Phase.ipynb`

Do not merely provide suggestions or example code. Inspect the repository, perform the required analysis and write the finished C-phase content into that notebook.

## Required source material

Before editing the C-phase notebook, inspect and understand:

### Previous project phases

- `notebooks/001_Q_Phase.ipynb`
- `notebooks/002_U_Phase.ipynb`
- `notebooks/003_A_Phase.ipynb`

**Use these notebooks as the authoritative source for:**
- the research question and project objectives
- stakeholders and intended use
- success criteria
- target variable
- dataset and feature definitions
- preprocessing decisions
- train, validation, and test strategy
- models and baselines
- feature sets
- hyperparameter experiments
- metrics
- saved artifacts and intermediate results
- conclusions already established

Verify the actual notebook names and paths in the repository before proceeding. If the repository uses slightly different numbering or naming, use the real paths rather than failing.

### Course documentation

**Read the documents in:**
- `docs/course-material/`

**Pay particular attention to:**
- `docs/course-material/001_Overview_Data_Analytics_and_Big_Data.md`
- `docs/course-material/002_QUACK_prozess_model_for_Data_Science_Projects.md`

Apply the course's definition of the C phase. The notebook must compare the candidate approaches using both:
1. **Quantitative criteria**, such as predictive performance, generalization, robustness and inference cost.
2. **Qualitative criteria**, such as interpretability, complexity, maintainability, reproducibility and deployment suitability.

Use regression and time-series forecasting metrics appropriate to this project. Do not copy classification-specific examples from the course material when they do not apply.

### Reference repository

Inspect the cloned reference project:
- `reference-repo/Degrees-of-No-Return-App`

**Study its C-phase notebook and any supporting files to understand:**
- notebook structure
- narrative flow
- comparison methodology
- tables and visualizations
- model-selection reasoning
- documentation style
- how conclusions and limitations are presented

Use the reference repository only as structural and methodological inspiration. Do not copy its project-specific conclusions, metrics, code or wording.

## Analysis requirements

Look at the output of the Q, U, and A notebooks. Then determine which models, baselines, feature variants and hyperparameter configurations are valid candidates for the final comparison (view `models` folder aswell).

For a forecasting project, preserve temporal ordering and avoid data leakage.

## Required notebook structure

Create a polished notebook with clear Markdown explanations and executable Python cells. Use a structure similar to the following, adapting it to the project where necessary.

## Final response

After editing the notebook, provide a concise summary containing:

- the file completed
- the models compared
- the selected model
- the main reason for selecting it
- whether the notebook executed successfully
- any unresolved blockers or assumptions
- any additional files changed

Do not replace the requested implementation with a tutorial or a proposed outline. Do not change the existing notebooks (Q, U and A)
```