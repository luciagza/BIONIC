# BIONIC: Bayesian Integration of Nonlinear Incomplete Clinical data

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-TBD-lightgrey)](#license)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)](#)

Official repository for the paper:

**Bayesian Integration of Nonlinear Incomplete Clinical Data**
*Submitted to IEEE Journal of Biomedical and Health Informatics (under review)*

---

## Table of Contents

- [Overview](#overview)
- [Model Architecture](#model-architecture)
- [Getting Started](#getting-started)
- [Datasets](#datasets)
- [Output](#output)
- [Citation](#citation)
- [License](#license)

---

## Overview

**BIONIC** (Bayesian Integration of Nonlinear Incomplete Clinical data) is a unified probabilistic framework for multimodal clinical learning under structured missingness. It combines a generative and a discriminative latent space to integrate heterogeneous data sources — such as pretrained embeddings from medical images or clinical text, together with structured clinical variables — within a single Bayesian architecture.

It is designed to:

- Integrate heterogeneous multimodal data (structured variables + pretrained embeddings from imaging, text, transcriptomics, etc.) within a joint generative-discriminative latent architecture.
- Explicitly model missingness at the variable, modality, and label level, enabling principled probabilistic imputation and semi-supervised learning.
- Automatically adapt representation complexity per modality via Bayesian sparsity (ARD priors), improving robustness in limited-cohort settings.
- Provide intrinsic interpretability by propagating discriminative relevance from the latent space back to the embedding and, when possible, the original input domain.

---

## Model Architecture

![BIONIC architecture](assets/graphicalModel.png)

Structured clinical variables and pretrained embeddings are projected into a dual latent space: the **generative pathway (G)** models multimodal structure and missing data, while the **discriminative pathway (Z)** aggregates predictive information for the classification task.

---

## Getting Started

### Requirements

- Python 3.8+
- See `requirements.txt` for dependencies.

### Usage

To train the model on a specific dataset, run:

```
python Models/main_github.py --fold {test fold} --seed {random seed}
```

If you wish to reproduce the paper results, the arguments can take the following values:

- `fold`: from 0 to 9 (10-fold cross-validation).
- `seed`: from 0 to 9 (10 random seeds).

This will:

- Train the indicated model using the specified parameters and dataset.
- Internally create train/validation/test splits used in the original experiments.
- Save soft predictions and true labels of the test set to the `./Results/{dataset}/` directory.

---

## Datasets

BIONIC was evaluated on three publicly available multimodal clinical datasets:

| Dataset | Patients | Modalities | Task |
|---------|----------|------------|------|
| [MMIST-ccRCC](https://arxiv.org/abs/2405.01658) | 618 | CT, MRI, WSI, genomic, clinical | 12-month survival classification |
| [MOTUM](https://www.nature.com/articles/s41597-024-03634-0) | 67 | 4 MRI sequences (FLAIR, T1, T1ce, T2), clinical | Glioma vs. metastasis (binary) |
| [TCGA-BRCA](https://www.nature.com/articles/nature11412) | 867 | WSI, diagnostic Q&A text, transcriptomics | Basal/triple-negative vs. other subtypes |

> **Note:** Datasets are **not included** in this repository due to licensing / data-sharing restrictions. All datasets used are publicly available — see the links above for access instructions. For TCGA-BRCA, WSI and transcriptomic embeddings were processed following [Ren et al. (OTSurv, MICCAI 2025)](https://arxiv.org/abs/2506.20741), and the diagnostic question-answer pairs come from the [WSI-VQA dataset](https://arxiv.org/abs/2407.05603) (Chen et al., ECCV 2024). Refer to the paper for full preprocessing and embedding-extraction details (Table II).

---

## Output

After training, the following outputs will be available:

- **Test metrics**: AUC and Balanced Accuracy (BACC) printed to console for each fold, plus the mean and standard deviation across folds.
- **Saved labels**: The train/test label splits for each fold are stored in `./Results/{dataset}_weights/Y_{dataset}_tr.npy` and `Y_{dataset}_tst.npy`.

> Note: the current script prints predictions and metrics to console but does not yet save the model's soft predictions to disk. If you need to persist predictions (e.g., for later analysis or the interpretability pipeline described in the paper), you'll need to add that saving step yourself.

---

## Citation

Please cite the paper using the placeholder below. This will be updated upon publication:

```
@article{bionic2026,
  title={Bayesian Integration of Nonlinear Incomplete Clinical Data},
  author={Gonz\'{a}lez-Zamorano, Luc\'{i}a and Balb\'{a}s-Esteban, Nuria and G\'{o}mez-Verdejo, Vanessa and Belenguer-Llorens, Albert and Sevilla-Salcedo, Carlos},
  journal={IEEE Journal of Biomedical and Health Informatics},
  year={2026},
  note={Under review}
}
```

---

## License

This project is licensed under an open-source license (TBD upon publication).
