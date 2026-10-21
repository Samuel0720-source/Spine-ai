# Lumbar MRI disc herniation finding classifier (education / research)

> **What it is:** A model that classifies whether the SPIDER dataset records a *disc herniation finding* for a
> lumbar disc on T2 sagittal MRI, using the expert-provided segmentation mask to locate and crop each disc.
> **What it is not:** It does not locate discs automatically, cannot be applied to new scans without masks,
> does not diagnose the cause of a patient's symptoms, and is not a medical device.
> "No herniation finding" does not mean "normal spine".

Demo: [링크 입력] · Video: [링크 입력]

## Data
- SPIDER (van der Graaf et al., *Sci Data* 2024), https://zenodo.org/records/10159290, CC BY 4.0
- Used: T2 sagittal series only. Included after checks: **[N] patients, [N] discs ([N] positive / [N] negative)**
  (from `prep_summary.json`). Excluded: [N] discs — reasons in `exclusions.csv`.
- Evaluation unit: disc. Split unit: patient (train/val/test = [N]/[N]/[N] patients, `split_summary.csv`).

## Method
1. Reorient every series to a common anatomical orientation (SimpleITK `DICOMOrient`, PIL).
2. Representative slice = sagittal slice with the largest disc-mask area (a fixed rule, not "the slice where herniation is most visible").
3. Physical crop: [80] mm square centred on the disc centroid → 224×224 (aspect ratio preserved, out-of-image padded with 0).
4. Percentile (1–99) intensity normalisation from the representative slice, applied identically in training, evaluation and the demo.
5. ImageNet-pretrained ResNet18, class-weighted cross-entropy, model selection by validation average precision.
6. Threshold chosen on validation (Youden's J), then applied unchanged to the test set.

## Results (test set, evaluated once on [날짜])
| Model | ROC-AUC (95% CI) | Average precision (95% CI) | Sensitivity | Specificity | Precision |
|---|---|---|---|---|---|
| Majority class | [ ] | [ ] | [ ] | [ ] | [ ] |
| Single slice | [ ] | [ ] | [ ] | [ ] | [ ] |
| Three adjacent slices | [ ] | [ ] | [ ] | [ ] | [ ] |

CIs: patient-level bootstrap (2,000 resamples). Seed variation (3 seeds): [ ]. Paired difference three − single: [ ].

## Error review
Grad-CAM (target: herniation class, per-image min-max scaled) was used as a visual check on validation cases
selected by a fixed rule (TP/TN/FP/FN). Observations: [ ]. Hypotheses (not verified): [ ].

## Limitations
- Small number of positive discs ([N] in test); wide confidence intervals.
- Four Dutch hospitals; sagittal only (no axial); vertebra numbering in SPIDER is not anatomical.
- Uses ground-truth masks at inference.

## Reproduce
```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
python -m pytest -q
python src/validate_data.py --n-patients 5
python src/prepare_data.py && python src/make_split.py
python src/train.py --mode single --seed 0
python src/train.py --mode three --seed 0
python src/final_test.py --runs runs/<single> runs/<three> --confirm-final
python src/export_examples.py --run runs/<chosen> && python app.py
```
Tested library versions: `requirements-tested.txt`.
