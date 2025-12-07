# Essential Gene Classification from DNA Sequences

This project implements a baseline machine learning pipeline to classify bacterial genes as essential or non-essential using DNA sequence information from the **macwiatrak/bacbench-essential-genes-dna** dataset (Hugging Face Datasets).

## Project Overview

The notebook:
- Loads the BacBench essential genes dataset (train/validation/test splits).
- Cleans and simplifies the dataset by removing unused metadata columns.
- Encodes DNA sequences into integer representations using a custom nucleotide mapping.
- Extracts non-overlapping 4-mer (length-4 subsequence) count features.
- Trains a Logistic Regression classifier on the resulting feature vectors.
- Evaluates model performance using accuracy and F1 score on validation and test splits.

This serves as a simple, fast baseline for essential-gene prediction from raw DNA sequences.

## Dataset

The project uses the `macwiatrak/bacbench-essential-genes-dna` dataset loaded via `datasets.load_dataset`.  
Each split (train, validation, test) originally contains, among others, the following fields:
- `dna_seq`: DNA sequence of the gene.
- `essential`: Label indicating whether a gene is essential (`"Yes"` or `"No"`).
- Several metadata columns (e.g., `genome_name`, `start`, `end`, `protein_id`, `strand`, `product`, `__index_level_0__`).

In this notebook, the unnecessary metadata columns are dropped, and only `dna_seq` and `essential` are retained for modeling.

## Preprocessing

Key preprocessing steps:

- **Label encoding**  
  The `essential` field is converted from string to integer:
  - `"Yes"` → `1`  
  - `"No"` → `0`  

- **DNA character mapping**  
  Each base in `dna_seq` is mapped to an integer to prioritize efficiency:
  - `A → 0`, `T → 1`, `C → 2`, `G → 3`  
  - Ambiguous bases: `N → 4`, `K → 5`, `R → 6`, `S → 7`, `Y → 8`, `M → 9`, `W → 10`  

- **Sequence encoding**  
  A helper function converts each DNA string into a list of integers using the mapping above, discarding characters not present in the map.

## Feature Extraction

The feature representation is based on **non-overlapping 4-mers**:

- The number of possible symbols is `NUM_BASES = 11`.
- The total number of distinct 4-mers is `NUM_4MERS = 11^4 = 14641`.
- For each encoded sequence, the notebook:
  - Iterates with step size `STEP = 4` to form non-overlapping 4-mers.
  - Maps each 4-mer to a unique integer index using positional encoding:
    \[
    \text{kmer\_int} = b_0 \cdot 11^3 + b_1 \cdot 11^2 + b_2 \cdot 11 + b_3
    \]
  - Increments the corresponding position in a length-14641 count vector.

The resulting dense feature matrix is then converted to a SciPy CSR sparse matrix for memory efficiency.

## Model

The classification model is a **Logistic Regression** from `sklearn.linear_model` with:

- `solver='saga'`
- `max_iter=2000`
- `n_jobs=-1` (parallel training where possible)

Training is performed on the 4-mer count features of the train split.

## Evaluation

Model performance is evaluated on both validation and test splits using:

- **Accuracy** (`sklearn.metrics.accuracy_score`)
- **F1 Score** (`sklearn.metrics.f1_score`)

The notebook prints:

- Validation Accuracy  
- Validation F1 Score  
- Test Accuracy  
- Test F1 Score  

These metrics provide an initial benchmark for this simple 4-mer + Logistic Regression approach.

## Requirements

Main Python dependencies:

- `pandas`
- `numpy`
- `scipy`
- `datasets` (Hugging Face Datasets)
- `scikit-learn`

Example installation (if running locally):
`pip install pandas numpy scipy datasets scikit-learn`

## How to Run

1. Open the notebook in Google Colab or your preferred environment.
2. Ensure all required packages are installed.
3. Run the cells in order:
   - Dataset loading and column filtering
   - Label encoding
   - DNA mapping and sequence encoding
   - 4-mer feature extraction
   - Model training
   - Evaluation on validation and test splits

## Possible Extensions

- Use overlapping k-mers or different k-mer sizes to capture more sequence context.
- Try more expressive models (e.g., tree-based methods, neural networks).
- Explore alternative encodings (e.g., one-hot, embeddings, or biologically informed encodings).
- Add cross-validation and hyperparameter tuning for more robust performance estimates.
# Issues with Current Gene Classifier

1. **Class Imbalance**
   - Essential genes (`1`) are much rarer than non-essential genes (`0`).
   - Logistic Regression tends to predict the majority class, lowering F1 score on validation.

2. **Simple Features**
   - Using **non-overlapping 4-mer counts** loses many sequence patterns.
   - Linear combinations of k-mer counts may not capture complex dependencies between nucleotides.

3. **Non-Overlapping k-mers**
   - Step size of 4 skips many overlapping patterns in the DNA sequence.
   - Important motifs or codon patterns might be missed.

4. **Normalization**
   - Raw 4-mer counts vary with sequence length.
   - Longer sequences dominate the feature vectors, potentially biasing the classifier.

5. **Linear Model Limitations**
   - Logistic Regression is a linear classifier.
   - Cannot capture non-linear interactions between k-mers that may be biologically relevant.

6. **Potential Data Leakage**
   - Some sequences in train/test splits may be very similar or overlapping.
   - This can inflate test accuracy artificially, as seen in the high test F1 compared to validation.

7. **Limited Biological Context**
   - Only nucleotide sequences are considered.
   - Other biological features (gene location, GC content, protein info) are ignored, which may be predictive of essentiality.

8. **Sparse Signal**
   - Many 4-mer combinations may never appear, making feature vectors sparse.
   - Sparse linear models may struggle to generalize with limited data for certain patterns.
9. **Mapping**
   - I did not take into account whether W which is mapped to 10 will be treated as 10 or 1 and 0 which would essentialy derail the classification
## Model Evaluation

The baseline Logistic Regression classifier was evaluated on the validation and test splits using **accuracy** and **F1 score**:

| Split       | Accuracy | F1 Score |
|------------|---------|----------|
| Validation | 0.45    | 0.25     |
| Test       | 0.90    | 0.80     |

> ⚠️ Note:  
> - Validation F1 is low due to class imbalance and simple linear model.  
> - The high test metrics may be artificially inflated if some sequences are very similar across splits.  
> - This baseline serves as a starting point for further improvements.


## Credits

- **Dataset:** [BacBench Essential Genes DNA Dataset](https://huggingface.co/macwiatrak/bacbench-essential-genes-dna) by Mac Wiatrak et al., hosted on HuggingFace.  
- **Libraries & Tools:**  
  - [HuggingFace `datasets`](https://huggingface.co/docs/datasets) for data loading and preprocessing  
  - [NumPy](https://numpy.org/) for numerical operations  
  - [SciPy](https://www.scipy.org/) for scientific computing  
  - [scikit-learn](https://scikit-learn.org/) for machine learning models and evaluation metrics  
- **Inspired by:** Standard bioinformatics workflows for DNA k-mer feature extraction and baseline classification.  
-**Workflow & Model Implementation:** Done by Sharat Doddihal
### Note 
This was my first attempt at creating a Ml model by myself without too much use from AI.AI has been used here but only for helping with the debugging process.
Overall I am happy with how this turned as this was a great learning experience.There are many fundamental errors that mess with the accuracy.