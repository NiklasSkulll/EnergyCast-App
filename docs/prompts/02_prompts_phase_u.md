# AI Prompt for Phase U

**GPT-5.2-Codex [AI_TOOL_DISCLOSURE.md](AI_TOOL_DISCLOSURE.md):**
```markdown
You are an expert data analytics and machine learning project assistant with full access to my repository.

**Context:**
I am working on a data analytics project that follows the QUACK process model. Phase Q has already been completed and documented in:
- `notebooks/01_Q_Phase.ipynb`

I am now working on Phase U. Your task is to create and complete the Phase U notebook using the DIG framework step by step.

**Main objective:**
Analyze the raw datasets located in `data/raw` and produce a complete, well-structured Jupyter notebook for Phase U at:
- `notebooks/02_U_Phase.ipynb`

The notebook must follow the DIG framework carefully and should prepare the project for the next QUACK phase.

Before starting the notebook:
1. Inspect the repository structure.
2. Review `notebooks/01_Q_Phase.ipynb` to understand the project context, research goal, datasets purpose, and any decisions already made in Phase Q.
3. Inspect the files in `data/raw`.
4. Set up the project environment because it does not exist yet.

Environment setup requirements:
- Use `uv` for environment and dependency management.
- Create a `pyproject.toml` file if it does not exist.
- Add all necessary dependencies for:
  - data loading
  - data inspection
  - exploratory data analysis
  - missing-value analysis
  - statistical summaries
  - visualization
  - Jupyter notebook support
  - Plotly-based charts
- Use clear, reproducible setup instructions.
- Do not install unnecessary packages.

**Notebook requirements:**
- Use `notebooks/02_U_Phase.ipynb` as a professional, readable Jupyter notebook.

**The notebook should include:**
1. A clear title and short explanation of Phase U.
2. A summary of what was learned from Phase Q.
3. datasets loading from `data/raw`.
4. Step-by-step data understanding using the DIG framework.
5. Clear markdown explanations before and after each analysis step.
6. Python code cells that are clean, modular, and reproducible.
7. Plotly visualizations wherever diagrams or charts are useful.
8. A final Phase U summary with key findings, risks, limitations, and recommendations for the next phase.

**Analysis requirements:** Perform a complete data understanding analysis, including but not limited to:
- Identify all raw data files.
- Load the datasets correctly.
- Inspect datasets shape, columns, data types, and basic structure.
- Explain the meaning of each feature where possible.
- Identify target variable candidates if relevant.
- Check missing values.
- Check duplicates.
- Check inconsistent values.
- Check invalid or suspicious values.
- Analyze numerical variables using descriptive statistics.
- Analyze categorical variables using frequency distributions.
- Detect potential outliers.
- Explore relationships between important variables.
- Create meaningful Plotly visualizations.
- Document data quality issues.
- Document assumptions.
- Document limitations.
- Explain whether the datasets is suitable for the next machine learning phase.

**Visualization requirements:** Use Plotly for necessary diagrams and charts, such as:
- missing value charts
- distributions of numerical features
- categorical frequency charts
- correlation heatmaps where appropriate
- boxplots for outlier detection
- relationship plots for important variables

**Coding standards:**
- Use robust file paths, preferably with `pathlib`.
- Make the notebook reusable from the repository root.
- Add comments where useful, but avoid over-commenting obvious code.
- Use functions for repeated logic.
- Do not hard-code fragile assumptions unless clearly explained.
- Handle multiple files in `data/raw` if present.
- If there are multiple possible interpretations, make a reasonable choice and document it.

**Deliverables:**
1. A valid `pyproject.toml` configured for the project.
2. A complete `notebooks/02_U_Phase.ipynb`.
3. Any necessary supporting files only if they are truly needed.
4. A short final summary explaining:
   - what was created,
   - which dependencies were added,
   - what the main Phase U findings were,
   - and what should happen next.

**Important:**
Do not skip directly to modeling. This task is only for Phase U: understanding and analyzing the datasets.
Follow the DIG framework step by step and keep the notebook aligned with the QUACK process model.

- DIG Framework: `docs/DIG_framework.md`
- Project informations: `docs/Project_plan_and_structure.md` and `docs/QUACK_process_model.md`
```
