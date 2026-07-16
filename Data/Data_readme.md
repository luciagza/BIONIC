# Data

Datasets are **not included** in this repository due to licensing / data-sharing restrictions.

The datasets used in the paper (MMIST-ccRCC, MOTUM, TCGA-BRCA) are publicly available — see the links in the main [README](../README.md#datasets) for access instructions.

## Expected structure for MMIST

Once you have downloaded and preprocessed MMIST-ccRCC, `Models/main_github.py` expects the following files, placed under `Data/`:

```
Data/
├── MMIST/
│   └── 10folds_MMIST.p        # pickled [fold_tst, dict_fold_val] train/test index splits, 10-fold CV
└── MMIST_new/
    ├── view_Clinical_semi.npy
    ├── view_CT_semi.npy       # raw CT embeddings (used as input to the SVD step)
    ├── view_Genomic_semi.npy
    ├── view_MRI_semi.npy      # raw MRI embeddings (used as input to the SVD step)
    ├── view_WSI_semi.npy      # raw WSI embeddings (used as input to the SVD step)
    └── Y_semi.npy              # labels
```

Each `view_*.npy` file should be a NumPy array of shape `(n_samples, n_features)` for that modality, in the same patient order as `Y_semi.npy`.

> Note: the raw (pre-dimensionality-reduction) embedding filenames above are the ones expected by the current script. If your preprocessing pipeline produces different filenames, update the `np.load(...)` paths in `Models/main_github.py` accordingly.

Once all the required files are in place, run the training script from the repository root (see [Usage](../README.md#usage) in the main README).
