
# Analytics Module — Titanic Dataset

## 1. Overview

This module implements an analyst-to-data-scientist workflow using the Titanic dataset.

The workflow covers:
- Data loading and profiling
- Missing-value handling
- Exploratory data analysis
- Outlier analysis
- Correlation analysis
- Data visualization
- Classification modeling
- Class imbalance comparison
- Hyperparameter tuning
- Fare regression
- Model persistence

## 2. Dataset

The Titanic dataset was loaded using Seaborn's built-in loader during the EDA stage.

An offline fallback file named `titanic.csv` was created using:

`df.to_csv("titanic.csv", index=False)`

The modeling notebook reads this committed CSV instead of independently loading the dataset again.

## 3. Missing-Value Handling

Missing-value percentages were calculated immediately after loading the dataset.

The following threshold rule was used:

- Less than 5% missing: affected rows were dropped.
- 5% to 30% missing: values were imputed.
- More than 30% missing: the column was dropped when imputation was considered unreliable.

The exact measured percentages and the corresponding decisions are documented in the EDA notebook.

## 4. Exploratory Data Analysis

Age and fare were analyzed using histograms and box plots.

The IQR rule was used to identify outliers:

Lower bound = Q1 - 1.5 × IQR

Upper bound = Q3 + 1.5 × IQR

Fare mean, median, and mode were calculated to assess its skewness.

Survival rates were analyzed by:
- Sex
- Passenger class
- Sex and passenger class together

A correlation matrix was created using exactly:
- survived
- pclass
- age
- sibsp
- parch
- fare

The boolean-derived columns `adult_male` and `alone` were excluded.

## 5. Standardization

Age and fare were standardized using z-score standardization.

The transformed variables were verified to have approximately:
- Mean = 0
- Standard deviation = 1

This was an EDA sanity check only and was not used as the modeling pipeline's preprocessing.

## 6. Classification

A stratified 80/20 train-test split was used.

Features included:
- age
- sibsp
- parch
- fare
- sex
- embarked

Preprocessing was implemented using a scikit-learn Pipeline and ColumnTransformer.

Numeric features used median imputation and StandardScaler.

Categorical features used most-frequent imputation and OneHotEncoder.

Three classifiers were trained:
1. Logistic Regression
2. Decision Tree
3. Random Forest

## 7. Classification Results

| Model | Accuracy | Precision | Recall | F1 | AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.799 | 0.780 | 0.667 | 0.719 | 0.819 |
| Decision Tree | 0.810 | 0.797 | 0.681 | 0.734 | 0.831 |
| Random Forest | 0.788 | 0.746 | 0.681 | 0.712 | 0.820 |

The Decision Tree achieved the strongest overall classification performance.

## 8. Class Imbalance

| Strategy | Precision | Recall | F1 |
|---|---:|---:|---:|
| Baseline | 0.746 | 0.681 | 0.712 |
| Class Weight Balanced | 0.742 | 0.667 | 0.702 |
| SMOTE | 0.690 | 0.710 | 0.700 |

The baseline achieved the highest F1 score and precision. SMOTE achieved the highest recall, but its precision and F1 were lower than the baseline.

## 9. Hyperparameter Tuning

Random Forest hyperparameters were tuned using GridSearchCV for:
- n_estimators
- max_depth
- max_features

The Random Forest estimator was configured with `oob_score=True` so that an out-of-bag score could be reported.

The exact best parameters and OOB score are recorded in the modeling notebook output.

## 10. Regression

A multivariate Linear Regression model was used to predict fare.

Results:

| Metric | Value |
|---|---:|
| MAE | 17.261 |
| RMSE | 28.999 |
| R² | 0.457 |
| Adjusted R² | 0.359 |

The residual plot showed a funnel-like increase in residual spread at higher predicted fare values, providing evidence of heteroscedasticity.

## 11. Final Recommendation

The Decision Tree is the recommended classifier because it achieved the highest accuracy (0.810), precision (0.797), F1 score (0.734), and AUC (0.831). Its recall of 0.681 was equal to the Random Forest and higher than Logistic Regression at 0.667. Therefore, based on the evaluated metrics, the Decision Tree provided the strongest overall classification performance on the test split.

## 12. Saved Model

The complete fitted Decision Tree pipeline was saved using `joblib.dump()`.

The saved artifact contains both preprocessing steps and the final estimator, allowing raw input data to be passed directly to the pipeline.

The saved pipeline was reloaded using `joblib.load()` and successfully produced predictions on raw test input.

## 13. Run Instructions

1. Open `01_eda.ipynb`.
2. Load and profile the Titanic dataset.
3. Save the offline fallback `titanic.csv`.
4. Complete cleaning and EDA.
5. Open `02_Modeling.ipynb`.
6. Read `titanic.csv`.
7. Run the preprocessing, classification, imbalance, tuning, and regression sections.
8. Generate and save the final pipeline artifact.

## 14. Files

- `01_eda.ipynb` — profiling, cleaning and EDA
- `02_Modeling.ipynb` — predictive modeling and regression
- `titanic.csv` — offline dataset fallback
- `best_titanic_pipeline.joblib` — complete fitted Decision Tree pipeline
