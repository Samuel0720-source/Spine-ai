import numpy as np
import SimpleITK as sitk 
"""
- SimpleITK 영상의 크기는 (i, j, k) 순서인데, 숫자 배열로 바꾸면 거꾸로 [k, j, i] 순서가 된다.
- 배열 번호만 봐서는 어느 쪽이 환자의 앞/뒤/위/아래인지 알 수 없다.
  그 정보는 영상 파일 안의 메모(direction, origin, spacing)에 있다.
- 그래서 모든 영상을 먼저 같은 방향(config.ORIENTATION = "PIL")으로 돌려 놓는다.
- "PIL" = i축은 Posterior(뒤), j축은 Inferior(아래), k축은 Left(왼쪽)로 갈수록 번호가 커진다.
  → 배열 [k, j, i] = [단면(오른→왼), 행(위→아래), 열(앞→뒤)]
"""
from scipy.ndimage import map_coordinates #의료 영상 도구
import config

class DataError(Exception):
    """
    - 오류를 나타내는 클래스, 데이터와 관련된 문제를 별도로 구분하고 싶어서 이걸 만듬; FileNotFoundError이런거 말고
    - DataError가 Exception의 기능을 물려받음
    - Exception = 프로그램 실햊중 발생하는 문제
    """
    pass # No additional code is needed because Exception already provides error functionality.

def read_image(path):# Define a function that reads an image from a given file path
    if not path.exists(): #not은 반대로 만듬
        raise DataError (f"File not found: {path}\n→ Please make sure you extracted the files into the data/raw directory following the folder structure in Step 1 of the guide.")
        # Raise an error instead of returning an invalid image
    image = sitk.ReadImage(str(path)) #전달받은 파일 경로를 문자열로 바꾸고, SimpleITK로 의료영상 파일을 읽은 다음, 결과를 image 변수에 저장한다
    return image

def geometry(img):
    """
    GetSize(), GetSpacing(), GetOrigin(), GetDirection() isnt a python tool
    & SimpleITK 라이브러리에서 제공하는 (Method)
    """
    info = {
        "size": img.GetSize(),
        "spacing": img.GetSpacing(),
        "origin": img.GetOrigin(),
        "direction": img.GetDirection(),
    }
    return info

def same_geometry(a,b, tol= 1e-3): #a = 첫번째 영상 b = 두번째 영상 tol(tolerance)= 숫자를 비교할때 허용하는 작은 차이
    """영상과 마스크가 같은 모눈종이(크기, 간격, 원점, 방향) 위에 있으면 True"""
    if a.GetSize() != b.GetSize(): #크기가 같아야 함
        return False
    #np.allclose()는 두 숫자 배열의 값들이 허용 범위 안에서 충분히 가까운지
    if not np.allclose(a.GetSpacing(), b.GetSpacing(), atol=tol):
        return False
    if not np.allclose(a.GetOrigin(), b.GetOrigin(), atol=tol):
        return False
    if not np.allclose(a.GetDirection(), b.GetDirection(), atol=tol):
        return False
    return True

def align_mask_to_image(image, mask): #image → 첫 번째로 전달받을 값, mask→ 두 번째로 전달받을 값
    """마스크가 영상과 다른 모눈종이 위에 있으면 영상 쪽으로 옮겨 그린다.
    nearest neighbor = 가장 가까운 칸의 번호를 그대로 쓴다 (201과 202가 섞여 201.5가 생기지 않게)."""
    if same_geometry(image, mask):
        return mask, False
    moved = sitk.Resample(mask, # resample mask if the values r diff
                          image, # Use the MRI image to define the output size, spacing, origin, and direction
                          sitk.Transform(), # Use an identity transform without changing physical coordinates
                          sitk.sitkNearestNeighbor, # 
                          0, # Fill locations outside the original mask with zero
                          mask.GetPixelID()# Preserve the original mask's pixel data typ
                          )
    return moved, True 

def orient(img):
    turned = sitk.DICOMOrient(img, config.ORIENTATION) #DICOMOrient = 이미지의 방향을 원하는 방향으로 변경, config.ORIENTATION = 어떻게 변경할지 지정하는 값
    return turned 

def to_arrays(image, mask):
    image = orient(image) #image를 새롭게 저장함 
    mask = orient(mask) #mask를 저장함
    sp = image.GetSpacing() #GetSpaing is method provided by SimpleTK --> 칸 간격을 알려줌

    col_sp = sp[0]
    row_sp = sp[1]
    slice_sp = sp[2]
    img = sitk.GetArrayFromImage(image). astype(np.float32)
    #GetArrayFromImage is part of simpletk = change imahe to numpy [slice, row, column]
    #astype = 모든 숫자를 종류(여기서는 비트)로 바꿔
    #np.float32 = 32비트를 씀

    msk = sitk.GetArrayFromImage(mask).astype(np.int32)
    spacing = (slice_sp, row_sp, col_sp)
    return img, msk, spacing 
