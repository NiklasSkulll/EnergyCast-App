# Git LFS setup

Git LFS (Large File Storage) stores big files outside normal git history and keeps a tiny pointer file in the repo. This keeps clones fast and avoids bloating the git history.

**One‑time setup (WSL):**
```shell
sudo apt install git-lfs
git lfs install
```

**Per‑repo setup:**
```shell
git lfs track "*.csv"             # track large CSVs
git lfs track "*.ipynb"           # optional: large notebooks
git add .gitattributes            # commit tracking rules
```

**Then just use git normally:**
```shell
git add data/raw/*.csv
git commit -m "data: add raw datasets"
git push
```

**Useful commands:**
```shell
git lfs ls-files
git lfs status
git lfs pull
```

> **Key note for collaborators:** install git‑lfs before cloning, otherwise they get pointer files instead of the real datasets.