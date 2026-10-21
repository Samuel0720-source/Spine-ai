
import os
from pathlib import Path

#DIR = dictionary
# Define variables and default settings for file paths, data processing, and AI model training before running the project

ROOT = Path(__file__).resolve().parents[1] # 현재 Python 파일에서 두 단계 위에 있는 프로젝트 최상위 폴더의 경로를 ROOT에 저장
# SPIDER 원본 위치. 연습용 합성 데이터를 쓸 때는 환경변수로 바꾼다:
RAW_DIR = (ROOT / os.environ.get("SPINE_DATA_DIR", "data/raw")).resolve() # SPINE_DATA_DIR에서 데이터 폴더 경로를 가져오고, 없으면 data/raw를 사용해 전체 경로를 RAW_DIR에 저장
IMAGES_DIR = RAW_DIR / "images"
MASKS_DIR = RAW_DIR / "masks"
GRADINGS_CSV = RAW_DIR / "radiological_gradings.csv"
OVERVIEW_CSV = RAW_DIR / "overview.csv"

PROCESSED_DIR = ROOT / "data" / "processed" / RAW_DIR.name
CROPS_DIR = PROCESSED_DIR/ "crops" #spine-ai
PREVIEW_DIR = PROCESSED_DIR / "previews" 
LABELS_CSV = PROCESSED_DIR / "labels.csv"
EXCLUSIONS_CSV = PROCESSED_DIR / "exclusions.csv"
PREP_SUMMARY_JSON = PROCESSED_DIR / "prep_summary.json"
SPLIT_CSV = PROCESSED_DIR / "split.csv"
SPLIT_SUMMARY_CSV = PROCESSED_DIR / "split_summary.csv"

# ROOT(spine-ai) → data → processed → raw → crops, previews, labels.csv, split.csv 폴더의 경로를 저장
# ROOT(spine-ai) → data → raw → images or masks 

REPORTS_DIR = ROOT / "reports"
RUNS_DIR = ROOT / "runs"       # 실행마다 새 폴더가 생긴다
APP_ASSETS_DIR = ROOT / "app_assets"
TEST_LOG_CSV = REPORTS_DIR / f"test_log_{RAW_DIR.name}.csv"     # raw / synthetic 따로 기록

SEQUENCE = "t2"
SPINAL_CANAL_VALUE = 100
IVD_MASK_OFFSET = 200
COL_PATIENT = "Patient"
COL_IVD = "IVD label"
COL_HERNIATION = "Disc herniation"
VALID_LABELS = {0,1}
CENTER_COLUMN = None

ORIENTATION = "PIL"
CROP_MM = 80.0 #디스크 중심에서 가로세로 80mm 정사각형을 자른다.
IMAGE_SIZE = 224
PERCENTILES = (1,99)

SPLIT_SEED = 42
N_FOLDS = 7
DEFAULT_EPOCHS = 15
DEFAULT_BATCH_SIZE = 32
DEFAULT_LR = 1e-4 #1 × 10⁻⁴ 
MODES = ("single", "three")
