# Lumbar MRI disc herniation finding classifier (education / research)

> **What it is:** A model that classifies whether the SPIDER dataset records a *disc herniation finding* for a
> lumbar disc on T2 sagittal MRI, using the expert-provided segmentation mask to locate and crop each disc.
> **What it is not:** It does not locate discs automatically, cannot be applied to new scans without masks,
> does not diagnose the cause of a patient's symptoms, and is not a medical device.
> "No herniation finding" does not mean "normal spine".

**Status: work in progress.** The data pipeline is being built first; training and evaluation come next, and the results table will be filled only after a single, final test-set run.

| Step | State |
|---|---|
| Project config: paths, labels, crop size, split and training settings (`src/config.py`) | done |
| MRI loading, geometry checks, mask-to-image alignment, common orientation, NumPy conversion (`src/preprocess.py`) | done |
| Representative slice, 80 mm physical crop, intensity normalisation | next |
| Patient-level split, ResNet18 training (single vs. three adjacent slices) | planned |
| One final test run with bootstrap confidence intervals, Grad-CAM error review, demo | planned |

## Data
- SPIDER (van der Graaf et al., *Sci Data* 2024), https://zenodo.org/records/10159290, CC BY 4.0. Not included in this repository; place it under `data/raw` (or set `SPINE_DATA_DIR`).
- Plan: T2 sagittal series only; evaluation unit = disc; split unit = patient, so no patient appears in both training and test.

## Method (planned)
1. Reorient every series to one anatomical orientation (`DICOMOrient` to PIL) so array axes always mean the same direction. *(done)*
2. Resample a mask onto its image grid with nearest-neighbour when their geometry differs, so label values never blend. *(done)*
3. Representative slice = sagittal slice with the largest disc-mask area (a fixed rule, not "the slice where herniation looks clearest").
4. Physical crop: 80 mm square centred on the disc → 224×224, aspect ratio kept, outside padded with 0.
5. 1st–99th percentile intensity normalisation, identical in training, evaluation and demo.
6. ImageNet-pretrained ResNet18, class-weighted cross-entropy, model selection by validation average precision; threshold chosen on validation and applied unchanged to test.

## Why it is built this way
- Splitting by **patient**, not by disc, prevents the same person's other discs leaking into the test set.
- The test set is evaluated **once**; choosing anything on it would make the reported numbers optimistic.
- Cropping in **millimetres** rather than pixels keeps the anatomy the same size across scanners with different resolutions.

## Limitations (known in advance)
- Four Dutch hospitals; sagittal only (no axial); few positive discs, so confidence intervals will be wide.
- Uses expert masks to find discs, so it cannot run on a new scan without them.

## Run what exists today
```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
cd src && python -c "import preprocess; print('preprocessing module loads')"
```
Tested library versions: `requirements-tested.txt`.
