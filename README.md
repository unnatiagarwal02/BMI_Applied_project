# Applied_Project

## Research question
Who in the U.S. has diabetes based on lab data but does not report having diabetes, and what characterizes them?

**Explanation**: Among U.S. adults, what proportion have laboratory-defined diabetes (HbA1c \(\ge 6.5\%\)) but do not report a prior diabetes diagnosis, and how do their demographic and clinical characteristics differ from diagnosed and non-diabetic individuals?

## Dataset / variables (NHANES-style)
This project uses NHANES 2021–2023 style variables merged across multiple components (DEMO/DIQ/GHB/GLU/HIQ/HUQ/INQ/UCPREG).

- **`LBXGH`**: HbA1c (glycated hemoglobin) lab value (main outcome/biomarker)
- **`LBXGLU`, `LBDGLUSI`**: glucose (different units)
- **`DIQ010`**: self-reported diabetes status (doctor told diabetes / borderline / no, depending on coding)

## Files in this repo
- **`Cleaning_data.csv`**: working dataset (raw / pre-cleaning)
- **`Cleaning_data_cleaned.csv`**: cleaned dataset output (created by cleaning steps)
- **`Data_cleaning.ipynb`**: standalone cleaning notebook for `Cleaning_data.csv`
- **`Data_understanding.ipynb`**: main workflow notebook (merging, filters, cleaning recodes, LBXGH analysis + visualizations)
- **`Sid_WIP.ipynb`**: work-in-progress notebook

## What we have done so far (end-to-end workflow)

### 1) Build the merged analysis dataset (`Data_understanding.ipynb`)
In `Data_understanding.ipynb` we:
- Load NHANES component files from local `.xpt` files (DEMO/DIQ/GHB/GLU/HIQ/HUQ/INQ/UCPREG)
- Merge them on **`SEQN`**
- Keep/inspect the merged columns (60 columns originally)

### 2) Apply analysis filters (adults, non-pregnant, valid diabetes-response)
In `Data_understanding.ipynb` we filter the dataset to match the research question:
- **Remove** participants with **`RIDAGEYR < 18`**
- **Remove** pregnancy cases (exclude **`URXPREG == 1`**)
- **Keep** only rows with **non-missing `LBXGH`**
- **Keep** only rows where **`DIQ010`** is within expected coded values (e.g. `[1, 2, 3, 7]` as used in the notebook)
- Drop NHANES **weight/design variables** for modeling convenience:
  - `SDDSRVYR`, `WTINT2YR`, `WTMEC2YR`, `WTSAF2YR`, `WTPH2YR`, `SDMVSTRA`, `SDMVPSU`

### 3) Handle missingness: summarize and optionally drop high-missing columns
In `Data_understanding.ipynb` we:
- Compute missing counts and missing %
- Optionally drop columns with **> 50% missingness** (threshold is adjustable)

### 4) Recode NHANES special/refusal values to NaN (targeted)
In `Data_understanding.ipynb` we recode common NHANES “Refused/Don’t know” codes to missing:
- For questionnaire-style variables only (prefixes **DIQ/HIQ/HUQ/INQ**):
  - Replace **7** and **9** with `NaN`
- For survey/demographic prefixes (**DIQ/HIQ/HUQ/INQ/DMD/DMQ**):
  - Replace **99** and **999** with `NaN`
- For lab variables (prefix **LBX/LBD**):
  - Replace **near-zero / underflow** values (e.g. `5.4e-79`) with `NaN` using a threshold (in notebook: \(0 < x < 1e{-10}\))

### 5) Create a separate cleaning pipeline for `Cleaning_data.csv` (`Data_cleaning.ipynb`)
We added `Data_cleaning.ipynb` to clean **`Cleaning_data.csv`** and save **`Cleaning_data_cleaned.csv`**.
This notebook:
- Loads `Cleaning_data.csv`
- Summarizes missingness
- Replaces common special codes **(7, 77, 99, 999)** with `NaN` in numeric columns (with a skip-list for ID/design/household-size style fields)
- Replaces extreme near-zero numeric artifacts with `NaN` (default threshold: \(|x| < 1e{-50}\))
- Optionally drops columns that are entirely missing
- Saves the output as **`Cleaning_data_cleaned.csv`**

### 6) Find “most related” columns w.r.t. `LBXGH` + visualize (heatmap)
In `Data_understanding.ipynb` we added an analysis section that:
- Computes **Pearson** (linear) and **Spearman** (monotonic) correlation between **`LBXGH`** and every other numeric column (pairwise complete rows)
- Ranks columns by **\(|Pearson|\)** and shows the top results
- Plots:
  - A **heatmap** (Pearson + Spearman shown as two rows for the top variables)
  - Optional **bar charts** for Pearson and Spearman (top variables)

## How to run

### Option A: Run the main workflow notebook
Open `Data_understanding.ipynb` and run all cells in order.

### Option B: Clean the CSV first, then analyze
Open `Data_cleaning.ipynb` and run all cells:
- Input: `Cleaning_data.csv`
- Output: `Cleaning_data_cleaned.csv`

## Notes / caveats
- NHANES special codes differ by variable; the current recoding focuses on common patterns (7/9, 99/999) and prefixes.
- Correlation is a quick “relatedness” screen. For categorical predictors, consider group comparisons (e.g., ANOVA) or modeling (e.g., regression/classification) for more reliable inference.


Pearson vs Spearman: which to use?
Given your NHANES diabetes/HbA1c data, Spearman is the safer default. Reasons:
1. Your data are mostly non-normal and mixed
Lab variables (LBXGH, LBXGLU, LBDGLUSI): Typically right-skewed; outliers and non-linearity are common.
Survey variables (DIQ, HIQ, HUQ, INQ): Often ordinal or categorical with Likert-like scales, not truly continuous.
Demographics (RIDAGEYR, DMDEDUC2, etc.): Mix of continuous and ordinal.
Pearson assumes linearity and roughly normal distributions; your data do not clearly meet those assumptions.
2. What your correlation table suggests
Variable	Pearson	Spearman	Interpretation
LBXGLU	0.81	0.58	Strong linear component (glucose ↔ HbA1c). Pearson higher.
RIDAGEYR	0.26	0.44	Stronger monotonic than linear relationship. Spearman more informative.
DMDHHSIZ	-0.04	-0.10	Linear correlation near zero; monotonic effect more noticeable. Spearman better.
HUQ042	0.05	-0.01	Weak overall; Pearson/Spearman differ, emphasizing non-linearity.
So:
For glucose ↔ HbA1c: both are strong; Pearson is fine for modeling if the relationship is linear.
For many other variables (age, household size, survey items): Spearman better reflects monotonic association and is less sensitive to non-normality.
3. Practical recommendation
Use Spearman as your main correlation metric for:
Variable ranking
Feature selection
Interpretation of associations with LBXGH
Mention Pearson for glucose/HbA1c as a secondary check, since that relationship is plausibly linear.
For modeling, consider both; if Pearson and Spearman differ a lot for a variable, interpret it as non-linear association.
Is your data normalized?
No. The notebook does not show any normalization or scaling. Values are used as in the original NHANES files:
LBXGH: HbA1c (%)
LBXGLU: fasting glucose (mg/dL)
RIDAGEYR: age in years
INDFMPIR: income-to-poverty ratio
Survey codes (e.g., 1–5 Likert)
For correlation coefficients, normalization is not needed; Pearson and Spearman are invariant to linear scaling. You would only need scaling if you plan to use methods sensitive to units (e.g., linear regression with regularization, k-means, some distance-based models).