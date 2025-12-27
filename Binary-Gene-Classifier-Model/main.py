import pandas as pd
import numpy as np
from scipy import stats
from datasets import load_dataset
from scipy.sparse import csr_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
# Load datasets
ds = load_dataset("macwiatrak/bacbench-essential-genes-dna", split="validation")
ds = ds.remove_columns(['genome_name', 'start', 'end', 'protein_id',
                        'strand', 'product', '__index_level_0__'])
ds1 = load_dataset("macwiatrak/bacbench-essential-genes-dna", split="train")
ds1 = ds1.remove_columns(['genome_name', 'start', 'end', 'protein_id',
                          'strand', 'product', '__index_level_0__'])
ds2 = load_dataset("macwiatrak/bacbench-essential-genes-dna", split="test")
ds2 = ds2.remove_columns(['genome_name', 'start', 'end', 'protein_id',
                          'strand', 'product', '__index_level_0__'])
# Convert Yes/No to 1/0
def convert(example):
    example["essential"] = [1 if x == "Yes" else 0 for x in example["essential"]]
    return example
ds = ds.map(convert)
ds1 = ds1.map(convert)
ds2 = ds2.map(convert)
# DNA base mapping
dna_map = {
    "A": 0, "T": 1, "C": 2, "G": 3,
    "N": 4, "K": 5, "R": 6, "S": 7,
    "Y": 8, "M": 9, "W": 10
}
# encode sequences in each split
for i in range(len(ds1)):
    ds1[i]["dna_seq"] = [dna_map[base] for base in ds1[i]["dna_seq"]]
for i in range(len(ds)):
    ds[i]["dna_seq"] = [dna_map[base] for base in ds[i]["dna_seq"]]
for i in range(len(ds2)):
    ds2[i]["dna_seq"] = [dna_map[base] for base in ds2[i]["dna_seq"]]
# 4-mer encoding utilities
NUM_BASES = len(dna_map)
NUM_4MERS = NUM_BASES ** 4
STEP = 4
def encode_sequence(seq, mapping=dna_map):
    return [mapping[base] for base in seq if base in mapping]
def sequence_to_4mer_counts(seq, step=STEP):
    counts = np.zeros(NUM_4MERS, dtype=int)
    for i in range(0, len(seq) - (step - 1), step):
        kmer = seq[i:i + step]
        if len(kmer) < step:
            continue
        kmer_int = (
            kmer[0] * NUM_BASES ** 3 +
            kmer[1] * NUM_BASES ** 2 +
            kmer[2] * NUM_BASES +
            kmer[3]
        )
        counts[kmer_int] += 1
    return counts
# Prepare dataset for ML
def prepare_dataset(ds_split):
    def _map_dna_sequence_to_integers(batch):
        return {"dna_seq": [encode_sequence(seq_str) for seq_str in batch["dna_seq"]]}
    ds_processed = ds_split.map(_map_dna_sequence_to_integers, batched=True)
    X_dense = np.array([sequence_to_4mer_counts(item["dna_seq"]) for item in ds_processed])
    y = np.array([item["essential"][0] for item in ds_processed])
    return X_dense, y
X_train_dense, y_train = prepare_dataset(ds1)
X_val_dense, y_val = prepare_dataset(ds)
X_test_dense, y_test = prepare_dataset(ds2)
# sparse conversion
X_train = csr_matrix(X_train_dense)
X_val = csr_matrix(X_val_dense)
X_test = csr_matrix(X_test_dense)
# Train classifier
clf = LogisticRegression(max_iter=2000, solver='saga', n_jobs=-1)
clf.fit(X_train, y_train)
# Evaluation
y_pred_val = clf.predict(X_val)
print("Validation Accuracy:", accuracy_score(y_val, y_pred_val))
print("Validation F1 Score:", f1_score(y_val, y_pred_val))
y_pred_test = clf.predict(X_test)
print("Test Accuracy:", accuracy_score(y_test, y_pred_test))
print("Test F1 Score:", f1_score(y_test, y_pred_test))