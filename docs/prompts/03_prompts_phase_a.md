You are an expert Python data science assistant working in a structured machine learning course project.

Your task is to write and complete the **A phase** in:

`notebooks/003_A_Phase.ipynb`

The A phase should build directly on the previous U phase and follow the course requirements.

## Files to read and analyze first

Read these files carefully before editing or generating the notebook content:

1. `docs/course-material/004_The_machine_learning_environment.md`

   * Use this to understand the expected machine learning environment, workflow, and project structure.

2. `docs/course-material/005_Classification.md`

   * Use this to understand the classification concepts, methods, and expectations relevant to the A phase.

3. `docs/course-material/006_Training_models.md`

   * Use this to understand how models should be trained, validated, evaluated, and compared.

4. `notebooks/002_U_Phase.ipynb`

   * Use this as the foundation for the A phase.
   * Reuse the analysis results, selected variables, insights, preprocessing decisions, and assumptions from the U phase.
   * Do not repeat unnecessary exploratory analysis unless it is needed to justify modeling decisions.

5. `data/raw`

   * Inspect the raw datasets needed for the modeling task.
   * Load the relevant datasets and verify that the data used in the A phase matches the findings from the U phase.

6. `docs/data-set-information`

   * Read this only when necessary to clarify field meanings, target variables, feature definitions, units, or data constraints.

## Main objective

Create a complete, well-structured A phase notebook that prepares the data for machine learning, trains appropriate classification models, evaluates them, and explains the results clearly.

## Expected notebook content

The notebook should include:

1. **Introduction to the A phase**

   * Explain the goal of the A phase.
   * Briefly summarize the most important findings from the U phase.
   * Define the classification problem clearly.
   * Identify the target variable and relevant feature variables.

2. **Data loading and preparation**

   * Load the required raw data.
   * Apply all necessary preprocessing steps based on the U phase findings.
   * Handle missing values, categorical variables, outliers, duplicates, and irrelevant columns where appropriate.
   * Explain each preprocessing decision briefly.

3. **Feature and target selection**

   * Define `X` and `y`.
   * Justify why the selected features are relevant.
   * Avoid data leakage.
   * Ensure the target variable is suitable for classification.

4. **Train/test split**

   * Split the data into training and test sets.
   * Use a suitable split ratio.
   * Use stratification if the class distribution requires it.
   * Set a random seed for reproducibility.

5. **Model training**

   * Train multiple relevant classification models, such as:

     * Logistic Regression
     * Decision Tree
     * Random Forest
     * k-Nearest Neighbors
     * Support Vector Machine, if appropriate
   * Use pipelines where helpful, especially when scaling or encoding is required.
   * Keep the implementation clean, reproducible, and easy to understand.

6. **Model evaluation**

   * Evaluate models using suitable classification metrics, such as:

     * Accuracy
     * Precision
     * Recall
     * F1-score
     * Confusion matrix
     * ROC-AUC, if appropriate for the target
   * Compare model performance in a clear table.
   * Explain which metrics matter most for this specific classification problem.

7. **Model comparison and interpretation**

   * Identify the best-performing model.
   * Explain why it performs best.
   * Discuss overfitting, underfitting, class imbalance, and limitations.
   * Include feature importance or coefficient interpretation where possible.

8. **Conclusion**

   * Summarize the results of the A phase.
   * State the recommended model.
   * Explain what could be improved in a future phase or iteration.

## Style and quality requirements

* Write clear markdown explanations before and after important code cells.
* Use clean, readable Python code.
* Avoid unnecessary complexity.
* Follow the terminology and expectations from the course material.
* Do not invent conclusions that are not supported by the data.
* Make sure the notebook can run from top to bottom without errors.
* Use reproducible settings such as `random_state`.
* Keep all file paths relative to the project root.
* Add comments only where they improve understanding.

## Output format

Return the completed content for `notebooks/003_A_Phase.ipynb`.

The notebook should contain both markdown and code cells, organized in a logical order, and should be ready to run in Jupyter.
