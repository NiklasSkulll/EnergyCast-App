# QUA³CK process model — overview

The PDF describes **QUA³CK** as a structured process model for **Data Science / Machine Learning projects**, from the initial question to deployment or knowledge transfer.

According to the PDF, QUA³CK was developed by **Stock et al. (2021)** at the **Institut für Technik der Informationsverarbeitung (ITIV)** at the **Karlsruher Institut für Technologie (KIT)**. The referenced publication is:

> Stock, S., Becker, J., Grimm, D., Hotfilter, T., Molinar, G., Stang, M., & Stork, W. (2021).
> **QUA³CK – A Machine Learning Development Process.** KIT.

The PDF describes the model as a **practice-oriented framework** for structuring Machine Learning projects. It is intended to bridge the gap between academic research and industrial practice and has a didactic focus so that students can remember and apply it systematically.

The model consists of five phases:

| Phase  | Meaning                                                           |
| ------ | ----------------------------------------------------------------- |
| **Q**  | Question                                                          |
| **U**  | Understanding the data                                            |
| **A³** | Algorithm selection, Adapting features, Adjusting hyperparameters |
| **C**  | Conclude and compare                                              |
| **K**  | Knowledge transfer                                                |

---

# Why the PDF says structured processes are important

The PDF argues that structured methods are important because many ML and Data Science projects fail without a clear methodology.

It gives the following figures:

| Statement in PDF                       |              Value |
| -------------------------------------- | -----------------: |
| Data Science projects fail             |         **85–87%** |
| ML projects reach production readiness |            **13%** |
| Cost reduction through MLOps practices |            **40%** |
| Forecasted MLOps market in 2034        | **39 billion USD** |

The PDF attributes these figures to **Gartner 2017–2019**, **Grand View Research 2024**, and **VentureBeat 2019**. It uses these numbers to justify why clear project structure, defined success metrics, stakeholder alignment, MLOps, and reproducibility are important.

---

# Phase Q — Question

## Meaning

The **Q phase** is about defining the project question clearly.

The PDF describes this as the **first and foundational step** of every Data Science project. It says that a project begins with a clear and precise question, and that an insufficient problem definition can lead to technically good results that do not meet the real requirements.

## Goals of the Q phase

According to the PDF, this phase should define:

| Element                    | Description from the PDF                     |
| -------------------------- | -------------------------------------------- |
| **Problem statement**      | What concrete problem should be solved?      |
| **Target group**           | For whom is the solution being developed?    |
| **Success metrics / KPIs** | How will success be measured quantitatively? |
| **Deployment goal**        | What are the final project artifacts?        |

## Example from the PDF

The PDF uses an **Iris classification project** as an example.

| Q element       | Iris example                                                                                 |
| --------------- | -------------------------------------------------------------------------------------------- |
| Problem         | Automatic classification of Iris species based on flower characteristics                     |
| Target group    | Botany students who want to identify Iris species in the field                               |
| Success metrics | Accuracy greater than **95%**, prediction time below **500 ms**                              |
| Deployment goal | Public **Streamlit app**                                                                     |
| Deliverables    | Jupyter Notebook, Streamlit web app, deployment in Streamlit Cloud, public GitHub repository |

## Important warning in the PDF

The PDF says that common reasons for Data Science project failure include:

* unclear problem definition
* missing success metrics
* insufficient stakeholder alignment

It emphasizes that translating a business problem into a precise Data Science question is especially important in professional contexts.

---

# Phase U — Understanding the Data

## Meaning

The **U phase** is about understanding the dataset before modeling.

The PDF describes this as **explorative data analysis**, or **EDA**, to gain insight into:

* data structure
* data quality
* distributions
* patterns
* anomalies
* correlations

## Goals of the U phase

The goal is to understand the data well enough to make informed decisions about:

* feature selection
* preprocessing
* model choice
* possible problems in the data

## Example from the PDF

The PDF again uses the Iris dataset.

The workflow shown is:

| Step                 | Description                                                                |
| -------------------- | -------------------------------------------------------------------------- |
| Load data            | Load the standard Iris dataset from `sklearn.datasets`                     |
| Inspect data         | Check shape, features, and target classes                                  |
| Statistical analysis | Calculate mean, standard deviation, minimum, maximum per feature and class |
| Visualization        | Create scatter plots and box plots                                         |

The PDF lists the Iris dataset properties as:

| Property       | Value                                                |
| -------------- | ---------------------------------------------------- |
| Rows           | **150**                                              |
| Columns        | **5**                                                |
| Features       | sepal length, sepal width, petal length, petal width |
| Target classes | setosa, versicolor, virginica                        |

## Visual findings from the Iris example

The PDF reports the following findings:

| Visualization                              | Finding                                                                                                                                  |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Scatter plot: petal length vs. petal width | Clear separation of the three species; Setosa is linearly separable and clearly isolated; Versicolor and Virginica overlap only slightly |
| Scatter plot: sepal length vs. sepal width | Stronger overlap between classes, especially Versicolor and Virginica                                                                    |
| Box plots                                  | Petal features show less overlap between classes than sepal features                                                                     |

## Conclusion from the U phase in the example

The PDF concludes that the **petal features are the strongest predictive features** and should be weighted highly in the model. It also says this insight is especially useful for interpretable models such as decision trees.

---

# Phase A³ — Algorithm selection, Adapting features, Adjusting hyperparameters

## Meaning

The **A³ phase** is the iterative model-development phase.

The PDF calls this the **heart** of the machine learning process. In this phase, different models are trained and systematically evaluated.

A³ stands for:

| A³ component                  | Meaning                                                                  |
| ----------------------------- | ------------------------------------------------------------------------ |
| **Algorithm selection**       | Choose suitable algorithms based on the problem and data characteristics |
| **Adapting features**         | Adapt and transform features to improve model performance                |
| **Adjusting hyperparameters** | Fine-tune model parameters to optimize performance                       |

## Iterative nature

The PDF states that these three steps are usually repeated multiple times. Each iteration contributes to continuous improvement.

In an MLOps context, the PDF says that experiments should be systematically logged to ensure:

* reproducibility
* comparability
* structured experiment management

## Example from the PDF: “AMALEA Big 3”

The PDF uses three algorithms in the Iris example:

| Algorithm           | Type according to PDF         |
| ------------------- | ----------------------------- |
| Decision Tree       | Tree-based model              |
| K-Nearest Neighbors | Instance-based model          |
| K-Means             | Unsupervised clustering model |

## Data split in the example

The PDF shows a stratified train/test split:

| Split         | Value                          |
| ------------- | ------------------------------ |
| Training data | **70%**                        |
| Test data     | **30%**                        |
| Method        | Stratified split to avoid bias |

The shown code uses `train_test_split` with:

```python
test_size=0.3
random_state=42
stratify=y
```

## MLFlow integration

The PDF mentions **MLFlow Experiment Tracking** in this phase.

It says MLFlow is used for:

* logging experiments
* logging parameters
* logging metrics
* improving reproducibility
* enabling systematic model comparison

The example shows logging a parameter such as `max_depth` and a metric such as `accuracy`.

---

# Phase C — Conclude and Compare

## Meaning

The **C phase** is about comparing experimental results and selecting the best model.

The PDF says this phase is important because it connects experimental research with practical application.

## Goal

The goal is not only to find the most accurate model, but to find a balanced compromise between:

* quantitative criteria
* qualitative criteria

## Quantitative metrics mentioned in the PDF

The PDF lists the following quantitative metrics:

| Metric         | Meaning in PDF                                             |
| -------------- | ---------------------------------------------------------- |
| Accuracy       | Percentage of correctly classified instances               |
| Precision      | Ratio of true positives to all positive predictions        |
| Recall         | Ratio of true positives to all actually positive instances |
| F1-score       | Harmonic mean of precision and recall                      |
| Inference time | Time needed for a single prediction                        |

## Qualitative metrics mentioned in the PDF

The PDF lists the following qualitative criteria:

| Criterion          | Meaning                                            |
| ------------------ | -------------------------------------------------- |
| Model complexity   | Number of parameters, tree depth, etc.             |
| Interpretability   | Understandability of model decisions               |
| Training time      | Time required for model training                   |
| Maintenance effort | Resources needed for model maintenance and updates |

## Model comparison from the Iris example

The PDF gives the following model results:

| Algorithm           | Metric              |    Result |
| ------------------- | ------------------- | --------: |
| Decision Tree       | Accuracy            | **0.978** |
| K-Nearest Neighbors | Accuracy            | **0.978** |
| K-Means             | Adjusted Rand Score | **0.669** |

The PDF identifies the **Decision Tree** as the best model because it achieves the same accuracy as K-Nearest Neighbors but is potentially more interpretable and efficient.

It also notes that the target KPI of **accuracy > 95%** was exceeded, because the best supervised models reached **97.8% accuracy**.

## MLOps connection

The PDF says that in the MLOps context, dashboards such as the **MLFlow UI** can provide an overview of all experiments and support decision-making by visualizing metrics.

---

# Phase K — Knowledge Transfer

## Meaning

The **K phase** is the final phase. It focuses on transferring the results into a usable form.

The PDF describes this phase as ensuring that analysis results are made available to stakeholders or transferred into productive systems.

## Goals

The PDF mentions three main aspects:

| Aspect                      | Description                                                                                            |
| --------------------------- | ------------------------------------------------------------------------------------------------------ |
| Documentation for portfolio | Create a concise project summary showing methodology, results, and technologies                        |
| Preparation for deployment  | Structure the code so the trained model can be integrated into applications such as Streamlit web apps |
| Communication of results    | Clearly communicate key findings and business impact for the target audience                           |

## Academic vs. practical context

The PDF distinguishes between two contexts:

| Context           | Focus                                          |
| ----------------- | ---------------------------------------------- |
| Academic context  | Documentation of method and results            |
| Practical context | Transfer of the model into a production system |

## Portfolio outputs mentioned in the PDF

The PDF says the project summary can be presented as:

| Output            | Description                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------- |
| GitHub README     | Structured description of project, method, results, installation, and usage                 |
| Streamlit web app | Interactive app where users can input data and generate predictions                         |
| Blog post         | Detailed documentation of the project process, e.g. on Medium, LinkedIn, or a personal blog |

## AMALEA Iris portfolio summary example

The PDF gives the following portfolio summary:

| Aspect         | Description                               |
| -------------- | ----------------------------------------- |
| Project        | AMALEA QUA³CK Demo – Iris Classification  |
| Methodology    | QUA³CK process model + Big 3 algorithms   |
| Best algorithm | Decision Tree                             |
| Performance    | 97.8%                                     |
| Technologies   | Python, Pandas, Scikit-learn, Matplotlib  |
| Next steps     | MLFlow integration + Streamlit deployment |

---

# MLOps integration in QUA³CK

The PDF extends QUA³CK with a modern MLOps-oriented approach in the AMALEA 2025 course.

It gives this mapping:

| QUA³CK phase | Traditional approach       | AMALEA 2025 / MLOps approach         | Tools                   |
| ------------ | -------------------------- | ------------------------------------ | ----------------------- |
| Q + U        | Static Jupyter notebooks   | Interactive analysis apps            | Streamlit, Docker       |
| A³           | Local, manual experiments  | MLFlow experiment tracking           | MLFlow, GitHub          |
| C            | Manual reports, e.g. Excel | Automated model comparison           | MLFlow UI, dashboards   |
| K            | Local model deployment     | Cloud deployment and model portfolio | Streamlit Cloud, GitHub |

The PDF says this integration is intended to connect experimental research and production applications. It emphasizes:

* reproducibility
* efficiency
* quality assurance
* experiment tracking
* model comparison
* cloud deployment

---

# Additional ML concepts explained in the PDF

## X/y split vs. train/test split

The PDF explains that these are two different concepts.

### X/y split

This separates the dataset into:

| Symbol | Meaning                    |
| ------ | -------------------------- |
| **X**  | Features / input variables |
| **y**  | Labels / target variable   |

The PDF explains that **X** is capitalized because it represents a matrix, while **y** is lowercase because it represents a vector.

### Train/test split

This separates the rows of the dataset into:

| Subset        | Meaning                                        |
| ------------- | ---------------------------------------------- |
| Training data | Used by the model to learn                     |
| Test data     | Used for independent evaluation on unseen data |

The PDF gives an approximate split example:

| Subset        | Approximate share |
| ------------- | ----------------: |
| Training data |          **~80%** |
| Test data     |          **~20%** |

---

# Glossary information from the PDF

## QUA³CK glossary

| Term                       | PDF explanation                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------------- |
| Q — Question               | First phase where problem, target group, and KPIs are defined                                            |
| U — Understanding the data | Thorough EDA of large external data sources; visualization and documentation are important               |
| A³ — Algorithms            | Algorithm selection, feature adaptation, and hyperparameter adjustment; often with MLFlow                |
| C — Conclude and compare   | Model comparison and evaluation using quantitative and qualitative criteria                              |
| K — Knowledge transfer     | Communication of results and transfer into portfolio elements such as Streamlit app or GitHub repository |

## Machine Learning terms mentioned

The PDF also defines these terms:

| Term                                  | Meaning according to the PDF                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------------------- |
| EDA                                   | Process for examining datasets and summarizing their main characteristics, often visually   |
| Feature Engineering                   | Creating new features from raw data to improve model performance                            |
| Hyperparameter                        | Parameter that controls the learning process or model structure and is set before training  |
| Overfitting                           | Model learns training data too closely, including noise or irrelevant patterns              |
| Underfitting                          | Model is too simple to capture the underlying data structure                                |
| Train-test split                      | Dividing data into training and test sets                                                   |
| Cross-validation                      | Evaluating model performance by splitting data into several folds                           |
| Confusion matrix                      | Table summarizing classification performance by correct and incorrect predictions per class |
| Accuracy, Precision, Recall, F1-score | Common classification metrics derived from the confusion matrix                             |
| Decision Tree                         | Classification or regression algorithm using a tree-like decision structure                 |
| Random Forest                         | Ensemble method combining several decision trees                                            |
| Logistic Regression                   | Statistical model for predicting the probability of a binary outcome                        |
| Classification                        | Supervised learning task where data points are assigned to predefined classes               |
| Supervised Learning                   | Learning from labeled data with known outputs                                               |

## MLOps terms mentioned

| Term                | Meaning according to the PDF                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ |
| MLOps               | Practices for standardizing and streamlining development, deployment, and maintenance of ML models in production   |
| MLFlow              | Open-source platform for managing the ML lifecycle, including experiment tracking, reproducibility, and deployment |
| Experiment Tracking | Logging and organizing experiment information such as parameters, metrics, code versions, and artifacts            |
| Model Registry      | Central repository for managing ML model lifecycle, including versioning, staging, and archiving                   |
| Deployment          | Moving a trained ML model into a production environment                                                            |
| CI/CD               | Automation practices for fast and reliable model delivery                                                          |
| Reproducibility     | Ability to replicate results using the same data, code, and configuration                                          |
| Model Drift         | Decline in model accuracy over time due to changes in data distributions or relationships                          |

## Tools and technologies mentioned

| Tool             | PDF description                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------ |
| Streamlit        | Python library for creating interactive web apps for data analysis and model demonstrations            |
| Jupyter Notebook | Interactive environment combining code, text, equations, and visualizations                            |
| Python           | Widely used programming language in Data Science and Machine Learning                                  |
| Scikit-learn     | Python ML library for classification, regression, clustering, dimensionality reduction, and evaluation |
| Pandas           | Python library for data manipulation and analysis using DataFrames                                     |

---

# Data sources mentioned in the PDF

The PDF lists the following sources for freely available datasets:

| Source                          | URL shown in PDF                       |
| ------------------------------- | -------------------------------------- |
| UCI Machine Learning Repository | `archive.ics.uci.edu/ml/index.php`     |
| Iris dataset                    | `archive.ics.uci.edu/ml/datasets/iris` |
| Kaggle Datasets                 | `kaggle.com/datasets`                  |
| Google Dataset Search           | `datasetsearch.research.google.com`    |
| AWS Open Data Registry          | `registry.opendata.aws`                |
| Data.gov                        | `data.gov`                             |
| European Data Portal            | `data.europa.eu`                       |
| OpenML                          | `openml.org`                           |

---

# Official documentation links mentioned in the PDF

The PDF lists documentation for these tools:

| Tool         | URL shown in PDF                    |
| ------------ | ----------------------------------- |
| MLFlow       | `mlflow.org/docs/latest/index.html` |
| Streamlit    | `docs.streamlit.io`                 |
| Scikit-learn | `scikit-learn.org/stable/`          |
| Pandas       | `pandas.pydata.org/docs/`           |

---

# Further resources mentioned in the PDF

The PDF names these related process or research resources:

| Resource             | Description in PDF                                                  |
| -------------------- | ------------------------------------------------------------------- |
| CRISP-DM Methodology | Classical reference model for data mining processes                 |
| KDD Process          | Knowledge Discovery in Databases, another established process model |
| Papers with Code     | Current ML research with code and benchmarks                        |

---

# Information gaps: what the PDF does **not** provide

The PDF gives a good overview of the QUA³CK process, but it does **not** provide detailed information for everything.

## Missing or limited information

| Topic                                                                  | Is detailed information provided?                                                              |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Exact formal definition of QUA³CK from the original Stock et al. paper | Only summarized, not deeply formalized                                                         |
| Full original QUA³CK paper content                                     | Not included; only citation and summary                                                        |
| Detailed mathematical formulation                                      | Not provided                                                                                   |
| Detailed deployment architecture                                       | Not provided                                                                                   |
| Detailed Docker setup                                                  | Mentioned as a tool, but no concrete setup                                                     |
| Detailed MLFlow implementation                                         | Only short example snippets and explanation                                                    |
| Detailed Streamlit implementation                                      | Mentioned as deployment goal, but not implemented in this PDF                                  |
| Detailed risk management process                                       | Not explicitly described                                                                       |
| Detailed data governance or privacy process                            | Not described                                                                                  |
| Detailed hyperparameter tuning strategy                                | Mentioned, but no full tuning workflow                                                         |
| Regression or time-series example                                      | Not included; the practical example is Iris classification                                     |
| Big Data system architecture                                           | Not provided                                                                                   |
| Cloud infrastructure details                                           | Streamlit Cloud and GitHub are mentioned, but no full architecture                             |
| Evaluation for non-classification tasks                                | K-Means uses Adjusted Rand Score, but no detailed regression/time-series metrics are discussed |

---

# Compact interpretation for your own project

Based only on the PDF, your university project should probably map your work like this:

| QUA³CK phase | What you should produce                                                                       |
| ------------ | --------------------------------------------------------------------------------------------- |
| **Q**        | Research question, target group, KPIs, deployment/deliverables                                |
| **U**        | Data loading, structure analysis, missing values, distributions, correlations, visualizations |
| **A³**       | Train multiple models, adapt features, tune hyperparameters, track experiments if possible    |
| **C**        | Compare models quantitatively and qualitatively, justify best model                           |
| **K**        | GitHub repository, README, documentation, possibly Streamlit app or portfolio summary         |

For your energy/smart-grid project, this means the PDF supports your idea of building **notebooks for each phase**, comparing models, documenting results in GitHub, and optionally building a Streamlit app.
