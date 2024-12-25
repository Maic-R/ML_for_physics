# Jet Classification with LHCb Simulated Data

## Overview

This repository contains code and resources for jet classification using simulated proton-proton collision data from the LHCb experiment. The goal is to classify jets into three categories based on their flavour:

1. **Light jets** (`mc_flavour = 0`)
2. **Charm jets (c-jets)** (`mc_flavour = 4`)
3. **Bottom jets (b-jets)** (`mc_flavour = 5`)

Jet flavour tagging plays a crucial role in understanding the properties of jets, enabling better discrimination of heavy and light flavour quarks in high-energy physics experiments.

---

## Dataset

The dataset consists of four CSV files: 

- `ljet_training.csv` (light jets)
- `cjet_training.csv` (c-jets)
- `bjet_training.csv` (b-jets)
- `competitionData.csv` (unlabeled, for model testing)

Each file contains 15 features describing the properties of jets and their associated secondary vertices. A description of the features is given in `notes.md` file.

---

## Methodology

The classification leverages the following insights:

- **Heavy flavour jets** (b-jets and c-jets) are characterized by:
  - Displaced secondary vertices with significant lifetime (`tau`)
  - High values of transverse momentum (`PT`) and secondary vertex corrected mass (`mCor`)
  - Large number of tracks associated with the jet (`nTrk`)

- **Light jets** lack distinct secondary vertex signatures or exhibit minimal displacement from the primary vertex.

A machine learning model will be trained on the labeled datasets (`ljet_training.csv`, `cjet_training.csv`, `bjet_training.csv`) to distinguish the three classes based on the feature set. The `competitionData.csv` will serve as the test set for validation.
