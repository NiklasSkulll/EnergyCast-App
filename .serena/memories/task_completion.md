# Task Completion

- Always run from repo root.
- Baseline completion check for code/app changes: `uv run python -m unittest discover -s tests -v`.
- For Streamlit app changes, the unittest suite includes `streamlit.testing.v1.AppTest`; also run the app manually with `uv run streamlit run app/streamlit_app.py` when behavior/layout needs visual confirmation.
- For notebook changes, execute the changed notebook with `uv run jupyter nbconvert --to notebook --execute notebooks/<phase>.ipynb --output <phase>.executed.ipynb --output-dir /tmp/<task-specific-dir> --ExecutePreprocessor.timeout=-1` unless the user explicitly wants in-place output refresh.
- No dedicated lint/format/type-check command is configured at onboarding time; do not claim those passed unless added or run explicitly.
- Before final handoff, report any verification command that could not be run and why.