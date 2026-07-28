# Suggested Commands

- Sync environment: `uv sync`
- Run all tests: `uv run python -m unittest discover -s tests -v`
- Start Streamlit app: `uv run streamlit run app/streamlit_app.py`
- Start app on fixed local address: `uv run streamlit run app/streamlit_app.py --server.address 127.0.0.1 --server.port 8501`
- Start Jupyter Lab: `uv run jupyter lab`
- Execute K-phase notebook in place when intentionally refreshing it: `uv run jupyter nbconvert --to notebook --execute --inplace notebooks/005_K_Phase.ipynb`
- Safer notebook validation pattern for other phases: `uv run jupyter nbconvert --to notebook --execute notebooks/<phase>.ipynb --output <phase>.executed.ipynb --output-dir /tmp/<task-specific-dir> --ExecutePreprocessor.timeout=-1`
- If LFS data is missing/tiny: `git lfs pull` then `git lfs ls-files`.