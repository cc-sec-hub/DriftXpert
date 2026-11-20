# DriftXpert

**DriftXpert** is a drift-adaptive network intrusion detection system
(NIDS) framework designed to maintain detection performance in evolving
network environments. It addresses **concept drift** by integrating
unsupervised drift detection with drift-driven model adaptation, while
balancing the acquisition of emerging traffic patterns and the
preservation of previously learned knowledge.

> **Published at ACM CCS 2026**
>
> *Navigating the Latent Manifold: Proactive Concept Drift Adaptation
> for Resilient NIDS*

## Framework Overview

DriftXpert consists of three major components: an online
intrusion-detection task and two offline adaptation phases. The online
task performs real-time traffic detection with a lightweight
encoder-classifier model. Phase 1 proactively monitors traffic windows
and identifies distribution shifts in the latent space. Once drift is
detected, Phase 2 adapts the model through representation alignment and
parameter-level knowledge preservation.

![Overall architecture of DriftXpert](Framework.png)

*Figure: Overall architecture of DriftXpert (Figure 3 in the CCS 2026
paper).*

### Main Components

-   **Online Task --- Intrusion Detection.** A lightweight, fully
    connected encoder and classifier perform real-time binary traffic
    classification (Benign or Attack).
-   **Phase 1 --- Proactive Sensing.** The historical encoder is reused
    to map recent traffic into the latent space. K-Means clustering and
    outlier analysis are used to detect concept drift without requiring
    manual labels for drift detection. Two indicators are introduced:
    the **Confidence Interval (CI)**, which defines a reliable
    latent-distance range, and the **Outlier Ratio (OR)**, which
    compares outlier proportions in recent and historical traffic
    windows.
-   **Phase 2 --- Evolutionary Alignment.** After drift is identified,
    the model is updated using a contrastive objective to align current
    latent representations with historical representations while
    distinguishing them from the previous epoch. Cross-entropy supports
    learning from drifted data. Historical/current model weight
    aggregation and selective freezing of early encoder parameters help
    mitigate catastrophic forgetting.

The framework is designed for adaptation without storing or replaying
historical raw traffic during the update process.

## Key Features

-   **Unsupervised concept-drift detection:** identifies changes in
    network traffic through latent-manifold deviation.
-   **Drift-triggered adaptation:** uses detected drift to trigger model
    updates instead of continuously retraining the detector.
-   **Representation consistency alignment:** encourages the updated
    model to retain useful historical representations while learning
    emerging patterns.
-   **Knowledge preservation:** combines cross-epoch weight aggregation
    with selective freezing to balance model plasticity and stability.
-   **Evaluation on public and real-world traffic:** evaluated on
    CICIDS-2017, CICIDS-2018, and enterprise network traffic in the
    paper.

## Installation

### Requirements

The reference environment uses:

-   Python 3.8.12
-   PyTorch 2.0.1 with CUDA 11.7 support
-   scikit-learn for the Phase 1 clustering component

We recommend using Conda to manage the environment.

``` bash
# Clone the repository
git clone https://github.com/cc-sec-hub/DriftXpert.git
cd DriftXpert

# Create and activate the environment
conda create -n drift_xpert python=3.8.12
conda activate drift_xpert

# Install dependencies
pip install -r requirements.txt
```

The PyTorch CUDA 11.7 wheel index and pinned package versions can be
specified in `requirements.txt`, for example:

``` text
--extra-index-url https://download.pytorch.org/whl/cu117

torch==2.0.1+cu117
numpy==1.24.1
pandas==1.3.2
matplotlib==3.7.1
seaborn==0.12.2
scikit-learn==1.2.2
```

## Repository Usage

The repository is the implementation accompanying the paper:

-   GitHub: https://github.com/cc-sec-hub/DriftXpert
-   Full paper: https://arxiv.org/abs/2609.08623

The exact training and evaluation entry points depend on the scripts and
configuration files in the repository. Please refer to the source code
and its accompanying configuration for dataset paths, model checkpoints,
and experiment commands.

## Publication

**Navigating the Latent Manifold: Proactive Concept Drift Adaptation for
Resilient NIDS**

Chao Zha, Zifeng Kang, Tian Liu, Dakun Shen, and Ruyun Zhang.

In *Proceedings of the 2026 ACM SIGSAC Conference on Computer and
Communications Security (CCS '26)*, November 15--19, 2026, The Hague,
Netherlands. ACM, New York, NY, USA, 15 pages.

**DOI:**
[10.1145/3830454.3846612](https://doi.org/10.1145/3830454.3846612)

## Citation

If you use DriftXpert in your research, please cite:

``` bibtex
@inproceedings{zha2026navigating,
  author    = {Zha, Chao and Kang, Zifeng and Liu, Tian and
               Shen, Dakun and Zhang, Ruyun},
  title     = {Navigating the Latent Manifold: Proactive Concept Drift
               Adaptation for Resilient NIDS},
  booktitle = {Proceedings of the 2026 ACM SIGSAC Conference on
               Computer and Communications Security},
  series    = {CCS '26},
  year      = {2026},
  publisher = {Association for Computing Machinery},
  address   = {New York, NY, USA},
  location  = {The Hague, Netherlands},
  pages     = {1--15},
  doi       = {10.1145/3830454.3846612}
}
```

## License

Please refer to the repository's `LICENSE` file for the software
license. The paper states that its full version is available under the
[Creative Commons Attribution 4.0 International
License](https://creativecommons.org/licenses/by/4.0/).
