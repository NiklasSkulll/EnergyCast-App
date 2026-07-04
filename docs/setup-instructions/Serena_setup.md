## Overview: What Serena is

**Serena** is an MCP-based coding assistant toolkit described as an “IDE for your coding agent.” It gives AI coding agents IDE-like abilities such as semantic code retrieval, symbol-level navigation, editing, refactoring, and project memory. Instead of only searching text or editing by line numbers, Serena works with code structure such as symbols, references, declarations, and file outlines. It integrates with AI clients through the **Model Context Protocol**, or **MCP**. ([oraios.github.io][1])

For your project, Serena would be useful because your repo will likely contain multiple notebooks, Python helper modules, data-processing scripts, model-training code, and possibly a Streamlit app. Serena can help an AI coding agent understand the repo structure and make safer code changes across files.

Serena can use two language-intelligence backends:

| Backend                                | Meaning                                                                                               |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **SolidLSP / language server backend** | Default backend. Serena starts language servers for the selected programming languages automatically. |
| **JetBrains backend**                  | Uses the Serena JetBrains plugin and the code intelligence of a JetBrains IDE.                        |

For your Python/Jupyter project, the default language server backend is probably enough unless you specifically want JetBrains integration. ([oraios.github.io][1])

---

## 1. Install Serena

Serena is installed with **uv**. The documentation says `uv` is the required package manager. After installing `uv`, install Serena with:

```bash
uv tool install -p 3.13 serena-agent@latest --prerelease=allow
```

After this, the command `serena` should be available in your terminal. ([oraios.github.io][2])

Then initialize Serena globally:

```bash
serena init
```

This initializes Serena with the default language-server backend. For JetBrains backend, the documentation gives:

```bash
serena init -b JetBrains
```

For your project, I would use:

```bash
serena init
```

---

## 2. Add Serena to your repo

Serena works project-based. A Serena project is simply a directory on your filesystem that contains the code and files Serena should work with. The normal project workflow is: create/configure the project, activate it, let Serena onboard itself, then work on coding tasks. ([oraios.github.io][3])

Go into your repository folder:

```bash
cd smart-grid-load-forecasting
```

Then create the Serena project:

```bash
serena project create --language python --name smart-grid-load-forecasting
```

For your repo, I would explicitly specify Python because your project uses Python notebooks, scripts, data processing, and ML models.

This should create a Serena project configuration folder:

```text
.serena/
└── project.yml
```

The docs say the generated `.serena/project.yml` can be adjusted after creation. It can configure things like programming languages, language backend, encoding, ignore rules, write access, initial prompts, project name, tools, and default modes. ([oraios.github.io][3])

---

## 3. Recommended setup for your project

For your repository, I would create Serena like this:

```bash
cd smart-grid-load-forecasting
serena project create --language python --name smart-grid-load-forecasting --index
```

This does two things:

1. creates the Serena project configuration
2. immediately indexes the project

The documentation says `--index` can be used during project creation if you want Serena to index the project right away. ([oraios.github.io][3])

Your repo would then look roughly like this:

```text
smart-grid-load-forecasting/
│
├── .serena/
│   └── project.yml
│
├── README.md
├── requirements.txt
├── notebooks/
├── src/
├── data/
├── models/
├── reports/
└── app/
```

Whether you commit `.serena/project.yml` to Git depends on how you want to use it. The Serena docs say `project.yml` is intended to be versioned together with the project, while local overrides can be placed in `project.local.yml`, which is ignored by Git by default. ([oraios.github.io][3])

So a reasonable Git setup is:

```text
Commit:
.serena/project.yml

Do not commit:
.serena/project.local.yml
.serena/cache files, if generated
large data files
model binaries
```

---

## 4. Activate the project

Serena needs to know which project you want to work with. The documentation calls this **project activation**. You can activate a project either inside an AI conversation or when starting the MCP server. ([oraios.github.io][3])

### Option A: Activate through the AI agent

You can tell your AI coding agent:

```text
Activate the project /path/to/smart-grid-load-forecasting
```

or, if you created it with a name:

```text
Activate the project smart-grid-load-forecasting
```

The docs also mention phrasing like:

```text
Activate the current dir as project using serena
```

This is especially relevant when using a global MCP configuration. ([oraios.github.io][4])

### Option B: Start Serena with a project path

You can also start Serena’s MCP server with a specific project:

```bash
serena start-mcp-server --project /path/to/smart-grid-load-forecasting
```

Some client contexts use a more specific startup command, for example with `--context` and `--project`. The docs explain that per-workspace clients such as VSCode or Claude Code often use a project path at startup, while global MCP configurations often require manually activating the project in chat. ([oraios.github.io][4])

---

## 5. How to connect Serena to an AI client

Serena works by running an MCP server and connecting it to an MCP-compatible client. The documentation says you either provide the client with a command that starts the Serena MCP server, or you start Serena yourself in HTTP mode and give the client the URL. ([oraios.github.io][1])

### Generic MCP configuration

A typical MCP-style config looks like this:

```json
{
  "mcpServers": {
    "serena": {
      "command": "serena",
      "args": [
        "start-mcp-server",
        "--context=agent",
        "--project",
        "/absolute/path/to/smart-grid-load-forecasting"
      ]
    }
  }
}
```

The exact config depends on your client.

### VSCode-style setup

The docs say that in VSCode you can add Serena through **MCP: Add Server** and choose **Command (stdio)**. For a workspace-specific setup, the documented pattern is:

```bash
serena start-mcp-server --context=vscode --project ${workspaceFolder}
```

For a global VSCode setup, the docs mention:

```bash
serena start-mcp-server --context=vscode
```

With the global setup, you may need to ask the agent to activate the current project manually at the start of a session. ([oraios.github.io][4])

---

## 6. Onboarding: what happens after activation

After a project is activated for the first time, Serena may run an **onboarding** process. The documentation says onboarding happens when Serena encounters a project for the first time and no project memories exist yet. Its goal is to understand the project structure, build system, testing setup, and other important project information, then store this as project-specific memories. ([oraios.github.io][5])

For your project, onboarding would likely make Serena learn things like:

```text
project topic: smart grid load forecasting
main language: Python
notebook workflow: QUA³CK process notebooks
data folders: raw, interim, processed
source code folder: src/
app folder: Streamlit dashboard
evaluation metrics: MAE, RMSE, sMAPE, R²
```

After onboarding, the docs recommend reviewing the generated memories and editing or adding to them if needed. They also note that onboarding can use a lot of context, so it can be useful to start a new conversation after onboarding is complete. ([oraios.github.io][5])

---

## 7. How to do indexing

Indexing means Serena pre-caches symbol information from the language server. The docs say this can be useful for larger projects because it avoids delays during the first tool call that needs symbol information. Indexing is not relevant when using the JetBrains plugin because indexing is handled by the IDE. ([oraios.github.io][3])

### Index during project creation

Recommended for your repo:

```bash
cd smart-grid-load-forecasting
serena project create --language python --name smart-grid-load-forecasting --index
```

### Index after project creation

If the project already exists:

```bash
cd smart-grid-load-forecasting
serena project index
```

The docs say indexing only needs to be called once. During normal use, Serena automatically updates the index when files change. ([oraios.github.io][3])

### For your project specifically

Run indexing after you have created the basic repo structure and added your first files:

```bash
smart-grid-load-forecasting/
├── README.md
├── requirements.txt
├── notebooks/
├── src/
│   ├── data_loading.py
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── modeling.py
│   └── evaluation.py
└── app/
    └── streamlit_app.py
```

Then run:

```bash
serena project index
```

This gives Serena useful symbol information for your Python files. For notebooks, Serena may still help with file-level operations, but its strongest semantic abilities are usually most useful in `.py` source files.

---

## 8. Practical setup checklist for your repo

Use this as your setup sequence:

```bash
# 1. Go to your repository
cd smart-grid-load-forecasting

# 2. Make sure Serena is installed globally
serena --help

# 3. Initialize Serena globally, if not already done
serena init

# 4. Create Serena project config for this repo and index it
serena project create --language python --name smart-grid-load-forecasting --index

# 5. Optional: inspect the generated project config
cat .serena/project.yml

# 6. Later, re-index manually if needed
serena project index
```

Then in your AI coding client, start with something like:

```text
Activate the project smart-grid-load-forecasting using Serena.
Please onboard the project and summarize the repository structure.
```

---

## 9. How Serena fits your Smart Grid project

For your specific **Smart Grid Load Forecasting** repo, Serena can help with:

| Area                  | How Serena helps                                                                                |
| --------------------- | ----------------------------------------------------------------------------------------------- |
| Repository navigation | Understands where notebooks, Python scripts, and app files are located                          |
| Refactoring           | Helps rename or move functions across `src/` modules                                            |
| Feature engineering   | Helps locate and edit functions for lag features, rolling averages, calendar features           |
| Model code            | Helps manage training, evaluation, and comparison functions                                     |
| Streamlit app         | Helps connect trained models and visualizations to the app                                      |
| Documentation         | Can use memories to remember the project goal, research question, metrics, and QUA³CK structure |

A good project-specific Serena memory would be:

```markdown
# Project Memory: Smart Grid Load Forecasting

This repository contains a university Data Analytics / Big Data project following the QUA³CK process model.

The goal is to predict hourly electricity load in Germany using weather data, renewable generation, calendar effects, and historical load values.

Main target variable:
- hourly electricity load in Germany

Main features:
- temperature
- solar radiation
- wind generation
- solar generation
- electricity price
- hour of day
- weekday/weekend
- month/season
- lagged load values
- rolling demand averages

Main evaluation metrics:
- MAE
- RMSE
- sMAPE
- R²

Repository structure:
- notebooks/: QUA³CK phase notebooks
- src/: reusable Python modules
- data/: raw, interim, and processed data
- models/: trained models
- reports/: figures and final report
- app/: optional Streamlit dashboard
```
