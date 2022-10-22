from http import client
import os, io
from google.cloud import vision
import cv2
from enum import Enum
import re
import numpy as np
from scipy import ndimage
import math
from typing import Tuple, Union
from deskew import determine_skew
# import matplotlib.pyplot as plt
from PIL import Image

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
client = vision.ImageAnnotatorClient()


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def Detect_Text(image_file):
    def rotate(
            image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
    ) -> np.ndarray:
        old_width, old_height = image.shape[:2]
        angle_radian = math.radians(angle)
        width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
        height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        rot_mat[1, 2] += (width - old_width) / 2
        rot_mat[0, 2] += (height - old_height) / 2
        return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)
    
    pillowImage = Image.open(image_file).convert('RGBA')
    img = np.array(pillowImage)
    red = img[:, :, 0].copy()
    img[:, :, 0] = img[:, :, 2].copy()
    img[:, :, 2] = red
    opencvImage = img
    grayscale = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2GRAY)
    
    # resize = cv2.resize(grayscale, None, fx=0.8, fy=0.8)
    resize = cv2.resize(grayscale, (1400, 1960), interpolation=cv2.INTER_LINEAR)
    angle = determine_skew(resize)
    rotated = ndimage.rotate(resize, angle, reshape=True)
    rotated2 = ndimage.rotate(rotated, -0.5, reshape=True)
    success, encoded_image = cv2.imencode('.jpg', rotated2)
    # cv2.imshow("", rotated2)
    # cv2.waitKey(0)
    content = encoded_image.tobytes()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    document = response.full_text_annotation

    bounds = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        x = symbol.bounding_box.vertices[0].x
                        y = symbol.bounding_box.vertices[0].y
                        text = symbol.text
                        bounds.append([x, y, text, symbol.bounding_box])

    bounds.sort(key=lambda x: x[1])
    old_y = -1
    line = []
    lines = []
    if angle >= 3.0 or angle <= -3.0:
        threshold = 10
    elif angle >= 1.5 or angle <= - 1.5:
        threshold = 5
    else:
        threshold = 3
    for bound in bounds:
        x = bound[0]
        y = bound[1]
        if old_y == -1:
            old_y = y
        elif old_y - threshold <= y <= old_y + threshold:
            old_y = y
        else:
            old_y = -1
            line.sort(key=lambda x: x[0])
            lines.append(line)
            line = []
        line.append(bound)
    line.sort(key=lambda x: x[0])
    lines.append(line)
    return lines


def all_text(lines):
    raw_text = ""
    for line in lines:
        texts = [i[2] for i in line]
        texts = ''.join(texts)
        bounds = [i[3] for i in line]
        x = f"{texts} "
        # print(texts, end=' ')
        raw_text = raw_text + x
        raw_text = raw_text.lower()
    return raw_text

def specific_text(raw_text):
    raw_text = raw_text.replace("total", "", raw_text.count("total"))
    raw_text = raw_text.replace("count", "", raw_text.count("count"))
    raw_text = raw_text.replace(",", "", raw_text.count(","))
    raw_text = raw_text.replace("µ", "u", raw_text.count("µ"))
    raw_text = raw_text.replace("μ", "u", raw_text.count("μ"))
    raw_text = raw_text.upper()
    text_list = raw_text.split(" ")
    # print(text_list)

    # Removing everything before "result"
    for i in text_list[:]:
        if "RESULT" in i:
            r_pos = text_list.index(i)
            del text_list[:r_pos]
    # print(text_list)
    parameter = dict()

    # initially all parameters are empty
    hbg_found = False
    rbc_found = False
    wbc_found = False
    plt_found = False
    neutrophil_found = False
    lymphocyte_found = False
    monocyte_found = False
    eosinophil_found = False
    basophil_found = False
    abs_neutrophil_found = False
    abs_lymphocyte_found = False
    abs_monocyte_found = False
    abs_eosinophil_found = False
    abs_basophil_found = False
    pcv_found = False
    rdw_found = False
    mchc_found = False
    mcv_found = False
    mch_found = False
    mpv_found = False
    pct_found = False
    pdw_found = False
    esr_found = False
    hba1c_found = False
    ferritin_found = False
    iron_found = False
    tibc_found = False

    # Searching values for each parameter
    for i in text_list[:]:

        # PDW START (for some reason not working when placed serialize)
        if not pdw_found:
            if "PDW" in i or "P.D.W" in i:
                pdw_pos = text_list.index(i)
                pdw_string_list = text_list[pdw_pos:pdw_pos + 3]
                pdw_string = " ".join(pdw_string_list)
                if "%" in pdw_string:
                    pdw_prob_val = re.findall('[-+]?\d*\.\d+|\d+', pdw_string)
                    if len(pdw_prob_val) > 0:
                        pdw_val = float(pdw_prob_val[0])
                        pdw_found = True
                        pdw_si_val = pdw_val
                        parameter["pdw"] = pdw_si_val
        # PDW END

        # WBC START
        if not wbc_found:
            if "WHITEBLOODCELL" in i or "WBC" in i or "W.B.C" in i:
                wbc_pos = text_list.index(i)
                wbc_string_list = text_list[wbc_pos:wbc_pos+3]
                wbc_string = " ".join(wbc_string_list)
                wbc_prob_val = re.findall('[-+]?\d*\.\d+|\d+', wbc_string)

                if len(wbc_prob_val) > 0:
                    wbc_val = float(wbc_prob_val[0])
                    # print("WBC          =", wbc_val)
                    wbc_found = True
                    wbc_prob_unit = re.sub("\s", "", wbc_string)

                    if "K/UL" in wbc_prob_unit or "10^3/UL" in wbc_prob_unit or "/L" in wbc_prob_unit \
                            or "10^3/MM^3" in wbc_prob_unit or "K/MM^3" in wbc_prob_unit:
                        wbc_si_val = wbc_val
                    elif "CELLS/UL" in wbc_prob_unit or "CELLS/MM^3" in wbc_prob_unit \
                            or "/CMM" in wbc_prob_unit or "CUMM" in wbc_prob_unit:
                        wbc_si_val = wbc_val / 1000
                    else:
                        if wbc_val < 300:
                            wbc_si_val = wbc_val
                        else:
                            wbc_si_val = wbc_val / 1000
                    parameter["wbc"] = wbc_si_val
        # WBC END

        # RBC START
        if not rbc_found:
            if "REDBLOODCELL" in i or "RBC" in i or "R.B.C" in i:
                rbc_pos = text_list.index(i)
                rbc_string_list = text_list[rbc_pos:rbc_pos + 3]
                rbc_string = " ".join(rbc_string_list)
                rbc_prob_val = re.findall('[-+]?\d*\.\d+|\d+', rbc_string)

                if len(rbc_prob_val) > 0:
                    rbc_val = float(rbc_prob_val[0])
                    rbc_found = True
                    rbc_prob_unit = re.sub("\s", "", rbc_string)

                    if "M/UL" in rbc_prob_unit or "10^6/UL" in rbc_prob_unit or "/L" in rbc_prob_unit \
                            or "10^6/MM^3" in rbc_prob_unit or "M/MM^3" in rbc_prob_unit:
                        rbc_si_val = rbc_val
                    elif "CELLS/UL" in rbc_prob_unit or "CELLS/MM^3" in rbc_prob_unit:
                        rbc_si_val = rbc_val / 1000000
                    else:
                        if rbc_val < 50000:
                            rbc_si_val = rbc_val
                        else:
                            rbc_si_val = rbc_val / 1000000
                    parameter["rbc"] = rbc_si_val
        # RBC END


        # PLT START
        if not plt_found:
            if "PLATELET" in i or "PLT" in i:
                plt_pos = text_list.index(i)
                plt_string_list = text_list[plt_pos:plt_pos+3]
                plt_string= " ".join(plt_string_list)
                plt_prob_val = re.findall('[-+]?\d*\.\d+|\d+', plt_string)
                if len(plt_prob_val) > 0:
                    plt_val = float(plt_prob_val[0])
                    plt_found = True
                    plt_prob_unit = re.sub("\s", "", plt_string)

                    if "K/UL" in plt_prob_unit or "10^3/UL" in plt_prob_unit or "/L" in plt_prob_unit \
                            or "10^3/MM^3" in plt_prob_unit or "K/MM^3" in plt_prob_unit:
                        plt_si_val = plt_val
                    elif "CELLS/UL" in plt_prob_unit or "CELLS/MM^3" in plt_prob_unit \
                            or "/CMM" in plt_prob_unit or "CUMM" in plt_prob_unit:
                        plt_si_val = plt_val / 1000
                    else:
                        if plt_val < 9999:
                            plt_si_val = plt_val
                        else:
                            plt_si_val = plt_val / 1000
                    parameter["plt"] = plt_si_val
        # PLT END

        # HGB START
        if not hbg_found:
            if "MOGLOBIN" in i or ("HB" in i and "A1C" not in i):
                hgb_pos = text_list.index(i)
                hgb_string_list = text_list[hgb_pos:hgb_pos+3]
                hgb_string= " ".join(hgb_string_list)
                hgb_prob_val = re.findall('[-+]?\d*\.\d+|\d+', hgb_string)
                if len(hgb_prob_val) > 0:
                    hgb_val = float(hgb_prob_val[0])
                    hbg_found = True
                    hgb_prob_unit = re.sub("\s", "", hgb_string)

                    if "/L" in hgb_prob_unit or "/ML" in hgb_prob_unit:
                        hgb_si_val = hgb_val
                    elif "/DL" in hgb_prob_unit or "/100ML" in hgb_prob_unit or "g%" in hgb_prob_unit:
                        hgb_si_val = hgb_val * 10
                    else:
                        if hgb_val < 100:
                            hgb_si_val = hgb_val * 10
                        else:
                            hgb_si_val = hgb_val
                    parameter["hbg"] = hgb_si_val
        # HGB END
        
        # NEUTROPHIL START
        if not neutrophil_found:
            if "NEUTROPHIL" in i:
                ntph_pos = text_list.index(i)
                ntph_string_list = text_list[ntph_pos:ntph_pos+3]
                ntph_string = " ".join(ntph_string_list)
                if "%" in ntph_string:
                    ntph_prob_val = re.findall('[-+]?\d*\.\d+|\d+', ntph_string)
                    if len(ntph_prob_val) > 0:
                        ntph_val = float(ntph_prob_val[0])
                        neutrophil_found = True
                        ntph_si_val = ntph_val
                        parameter["neutrophil%"] = ntph_si_val
        # NEUTROPHIL END

        # ABSOLUTE NEUTROPHIL START
        if not abs_neutrophil_found:
            if "NEUTROPHIL" in i:
                abs_ntph_pos = text_list.index(i)
                abs_ntph_string_list = text_list[abs_ntph_pos:abs_ntph_pos+3]
                abs_ntph_string = " ".join(abs_ntph_string_list)
                if "%" not in abs_ntph_string:
                    abs_ntph_prob_val = re.findall('[-+]?\d*\.\d+|\d+', abs_ntph_string)
                    if len(abs_ntph_prob_val) > 0:
                        abs_ntph_val = float(abs_ntph_prob_val[0])
                        abs_neutrophil_found = True
                        abs_ntph_prob_unit = re.sub("\s", "", abs_ntph_string)
                        if "K/UL" in abs_ntph_prob_unit or "10^3/UL" in abs_ntph_prob_unit or "/L" in abs_ntph_prob_unit \
                                or "10^3/MM^3" in abs_ntph_prob_unit or "K/MM^3" in abs_ntph_prob_unit:
                            abs_ntph_si_val = abs_ntph_val
                        elif "CELLS/UL" in abs_ntph_prob_unit or "CELLS/MM^3" in abs_ntph_prob_unit \
                                or "/CMM" in abs_ntph_prob_unit or "CUMM" in abs_ntph_prob_unit:
                            abs_ntph_si_val = abs_ntph_val / 1000
                        else:
                            if abs_ntph_val < 300:
                                abs_ntph_si_val = abs_ntph_val
                            else:
                                abs_ntph_si_val = abs_ntph_val / 1000
                        parameter["neutrophil"] = abs_ntph_si_val
        # ABSOLUTE NEUTROPHIL END

        # LYMPHOCYTE START
        if not lymphocyte_found:
            if "LYMPHOCYTE" in i:
                lmph_pos = text_list.index(i)
                lmph_string_list = text_list[lmph_pos:lmph_pos+3]
                lmph_string = " ".join(lmph_string_list)
                if "%" in lmph_string:
                    lmph_prob_val = re.findall('[-+]?\d*\.\d+|\d+', lmph_string)
                    if len(lmph_prob_val) > 0:
                        lmph_val = float(lmph_prob_val[0])
                        lymphocyte_found = True
                        lmph_si_val = lmph_val
                        parameter["lymphocyte%"] = lmph_si_val
        # LYMPHOCYTE END

        # ABSOLUTE LYMPHOCYTE START
        if not abs_lymphocyte_found:
            if "LYMPHOCYTE" in i:
                abs_lmph_pos = text_list.index(i)
                abs_lmph_string_list = text_list[abs_lmph_pos:abs_lmph_pos+3]
                abs_lmph_string = " ".join(abs_lmph_string_list)
                if "%" not in abs_lmph_string:
                    abs_lmph_prob_val = re.findall('[-+]?\d*\.\d+|\d+', abs_lmph_string)
                    if len(abs_lmph_prob_val) > 0:
                        abs_lmph_val = float(abs_lmph_prob_val[0])
                        abs_lymphocyte_found = True
                        abs_lmph_prob_unit = re.sub("\s", "", abs_lmph_string)
                        if "K/UL" in abs_lmph_prob_unit or "10^3/UL" in abs_lmph_prob_unit or "/L" in abs_lmph_prob_unit \
                                or "10^3/MM^3" in abs_lmph_prob_unit or "K/MM^3" in abs_lmph_prob_unit:
                            abs_lmph_si_val = abs_lmph_val
                        elif "CELLS/UL" in abs_lmph_prob_unit or "CELLS/MM^3" in abs_lmph_prob_unit \
                                or "/CMM" in abs_lmph_prob_unit or "CUMM" in abs_lmph_prob_unit:
                            abs_lmph_si_val = abs_lmph_val / 1000
                        else:
                            if abs_lmph_val < 300:
                                abs_lmph_si_val = abs_lmph_val
                            else:
                                abs_lmph_si_val = abs_lmph_val / 1000
                        parameter["lymphocyte"] = abs_lmph_si_val
        # ABSOLUTE LYMPHOCYTE END

        # MONOCYTE START
        if not monocyte_found:
            if "MONOCYTE" in i:
                mnct_pos = text_list.index(i)
                mnct_string_list = text_list[mnct_pos:mnct_pos+3]
                mnct_string = " ".join(mnct_string_list)
                if "%" in mnct_string:
                    mnct_prob_val = re.findall('[-+]?\d*\.\d+|\d+', mnct_string)
                    if len(mnct_prob_val) > 0:
                        mnct_val = float(mnct_prob_val[0])
                        monocyte_found = True
                        mnct_si_val = mnct_val
                        parameter["monocyte%"] = mnct_si_val
        # MONOCYTE END

        # ABSOLUTE MONOCYTE START
        if not abs_monocyte_found:
            if "MONOCYTE" in i:
                abs_mnct_pos = text_list.index(i)
                abs_mnct_string_list = text_list[abs_mnct_pos:abs_mnct_pos+3]
                abs_mnct_string = " ".join(abs_mnct_string_list)
                if "%" not in abs_mnct_string:
                    abs_mnct_prob_val = re.findall('[-+]?\d*\.\d+|\d+', abs_mnct_string)
                    if len(abs_mnct_prob_val) > 0:
                        abs_mnct_val = float(abs_mnct_prob_val[0])
                        abs_monocyte_found = True
                        abs_mnct_prob_unit = re.sub("\s", "", abs_mnct_string)
                        if "K/UL" in abs_mnct_prob_unit or "10^3/UL" in abs_mnct_prob_unit or "/L" in abs_mnct_prob_unit \
                                or "10^3/MM^3" in abs_mnct_prob_unit or "K/MM^3" in abs_mnct_prob_unit:
                            abs_mnct_si_val = abs_mnct_val
                        elif "CELLS/UL" in abs_mnct_prob_unit or "CELLS/MM^3" in abs_mnct_prob_unit \
                                or "/CMM" in abs_mnct_prob_unit or "CUMM" in abs_mnct_prob_unit:
                            abs_mnct_si_val = abs_mnct_val / 1000
                        else:
                            if abs_mnct_val < 300:
                                abs_mnct_si_val = abs_mnct_val
                            else:
                                abs_mnct_si_val = abs_mnct_val / 1000
                        parameter["monocyte"] = abs_mnct_si_val
        # ABSOLUTE MONOCYTE END
        
        # EOSINOPHIL START
        if not eosinophil_found:
            if "EOSINOPHIL" in i:
                esnp_pos = text_list.index(i)
                esnp_string_list = text_list[esnp_pos:esnp_pos+3]
                esnp_string = " ".join(esnp_string_list)
                if "%" in esnp_string:
                    esnp_prob_val = re.findall('[-+]?\d*\.\d+|\d+', esnp_string)
                    if len(esnp_prob_val) > 0:
                        esnp_val = float(esnp_prob_val[0])
                        eosinophil_found = True
                        esnp_si_val = esnp_val
                        parameter["eosinophil%"] = esnp_si_val
        # EOSINOPHIL END

        # ABSOLUTE EOSINOPHIL START
        if not abs_eosinophil_found:
            if "EOSINOPHIL" in i:
                abs_esnp_pos = text_list.index(i)
                abs_esnp_string_list = text_list[abs_esnp_pos:abs_esnp_pos+3]
                abs_esnp_string = " ".join(abs_esnp_string_list)
                if "%" not in abs_esnp_string:
                    abs_esnp_prob_val = re.findall('[-+]?\d*\.\d+|\d+', abs_esnp_string)
                    if len(abs_esnp_prob_val) > 0:
                        abs_esnp_val = float(abs_esnp_prob_val[0])
                        abs_eosinophil_found = True
                        abs_esnp_prob_unit = re.sub("\s", "", abs_esnp_string)
                        if "K/UL" in abs_esnp_prob_unit or "10^3/UL" in abs_esnp_prob_unit or "/L" in abs_esnp_prob_unit \
                                or "10^3/MM^3" in abs_esnp_prob_unit or "K/MM^3" in abs_esnp_prob_unit:
                            abs_esnp_si_val = abs_esnp_val
                        elif "CELLS/UL" in abs_esnp_prob_unit or "CELLS/MM^3" in abs_esnp_prob_unit \
                                or "/CMM" in abs_esnp_prob_unit or "CUMM" in abs_esnp_prob_unit:
                            abs_esnp_si_val = abs_esnp_val / 1000
                        else:
                            if abs_esnp_val < 300:
                                abs_esnp_si_val = abs_esnp_val
                            else:
                                abs_esnp_si_val = abs_esnp_val / 1000
                        parameter["eosinophil"] = abs_esnp_si_val
        # ABSOLUTE EOSINOPHIL END

        # BASOPHIL START
        if not basophil_found:
            if "BASOPHIL" in i:
                bsph_pos = text_list.index(i)
                bsph_string_list = text_list[bsph_pos:bsph_pos+3]
                bsph_string = " ".join(bsph_string_list)
                if "%" in bsph_string:
                    bsph_prob_val = re.findall('[-+]?\d*\.\d+|\d+', bsph_string)
                    if len(bsph_prob_val) > 0:
                        bsph_val = float(bsph_prob_val[0])
                        basophil_found = True
                        bsph_si_val = bsph_val
                        parameter["basophil%"] = bsph_si_val
        # BASOPHIL END

        # ABSOLUTE BASOPHIL START
        if not abs_basophil_found:
            if "BASOPHIL" in i:
                abs_bsph_pos = text_list.index(i)
                abs_bsph_string_list = text_list[abs_bsph_pos:abs_bsph_pos+3]
                abs_bsph_string = " ".join(abs_bsph_string_list)
                if "%" not in abs_bsph_string:
                    abs_bsph_prob_val = re.findall('[-+]?\d*\.\d+|\d+', abs_bsph_string)
                    if len(abs_bsph_prob_val) > 0:
                        abs_bsph_val = float(abs_bsph_prob_val[0])
                        abs_basophil_found = True
                        abs_bsph_prob_unit = re.sub("\s", "", abs_bsph_string)
                        if "K/UL" in abs_bsph_prob_unit or "10^3/UL" in abs_bsph_prob_unit or "/L" in abs_bsph_prob_unit \
                                or "10^3/MM^3" in abs_bsph_prob_unit or "K/MM^3" in abs_bsph_prob_unit:
                            abs_bsph_si_val = abs_bsph_val
                        elif "CELLS/UL" in abs_bsph_prob_unit or "CELLS/MM^3" in abs_bsph_prob_unit \
                                or "/CMM" in abs_bsph_prob_unit or "CUMM" in abs_bsph_prob_unit:
                            abs_bsph_si_val = abs_bsph_val / 1000
                        else:
                            if abs_bsph_val < 300:
                                abs_bsph_si_val = abs_bsph_val
                            else:
                                abs_bsph_si_val = abs_bsph_val / 1000
                        parameter["basophil"] = abs_bsph_si_val
        # ABSOLUTE BASOPHIL END
    
        # PCV START
        if not pcv_found:
            if "PCV" in i or "HCT" in i or "P.C.V" in i:
                pcv_pos = text_list.index(i)
                pcv_string_list = text_list[pcv_pos:pcv_pos + 3]
                pcv_string = " ".join(pcv_string_list)
                if "%" in pcv_string:
                    pcv_prob_val = re.findall('[-+]?\d*\.\d+|\d+', pcv_string)
                    if len(pcv_prob_val) > 0:
                        pcv_val = float(pcv_prob_val[0])
                        pcv_found = True
                        pcv_si_val = pcv_val
                        parameter["pcv"] = pcv_si_val
        # PCV END

        # RDW START
        if not rdw_found:
            if "RDW" in i or "R.D.W" in i:
                rdw_pos = text_list.index(i)
                rdw_string_list = text_list[rdw_pos:rdw_pos + 3]
                rdw_string = " ".join(rdw_string_list)
                if "%" in rdw_string:
                    rdw_prob_val = re.findall('[-+]?\d*\.\d+|\d+', rdw_string)
                    if len(rdw_prob_val) > 0:
                        rdw_val = float(rdw_prob_val[0])
                        rdw_found = True
                        rdw_si_val = rdw_val
                        parameter["rdw"] = rdw_si_val
        # RDW END

        # MCHC start
        if not mchc_found:
            if "MCHC" in i or "M.C.H.C" in i:
                mchc_pos = text_list.index(i)
                mchc_string_list = text_list[mchc_pos:mchc_pos+3]
                mchc_string= " ".join(mchc_string_list)
                mchc_prob_val = re.findall('[-+]?\d*\.\d+|\d+', mchc_string)
                if len(mchc_prob_val) > 0:
                    mchc_val = float(mchc_prob_val[0])
                    mchc_found = True
                    mchc_prob_unit = re.sub("\s", "", mchc_string)
                    if "G/L" in mchc_prob_unit or "MG/ML" in mchc_prob_unit:
                        mchc_si_val = mchc_val * 0.0621
                    elif "G/DL" in mchc_prob_unit or "G/100ML" in mchc_prob_unit or "G%" in mchc_prob_unit or "%" in mchc_prob_unit:
                        mchc_si_val = mchc_val * 0.6206
                    elif "UMOL/L" in mchc_prob_unit:
                        mchc_si_val = mchc_val * 0.001
                    elif "MMOL/L" in mchc_prob_unit:
                        mchc_si_val = mchc_val
                    else:
                        mchc_si_val = mchc_val * 0.6206

                    parameter["mchc"] = mchc_si_val
        # MCHC END

        # MCV START
            if not mcv_found:
                if "MCV" in i or "M.C.V" in i:
                    mcv_pos = text_list.index(i)
                    mcv_string_list = text_list[mcv_pos:mcv_pos + 3]
                    mcv_string = " ".join(mcv_string_list)
                    mcv_prob_val = re.findall('[-+]?\d*\.\d+|\d+', mcv_string)
                    if len(mcv_prob_val) > 0:
                        mcv_val = float(mcv_prob_val[0])
                        mcv_found = True
                        mcv_si_val = mcv_val
                        parameter["mcv"] = mcv_si_val
        # MCV END

        # MCH START
        if not mch_found:
            if ("MCH" in i and "MCHC" not in i) or ("M.C.H" in i and "M.C.H.C" not in i):
                mch_pos = text_list.index(i)
                mch_string_list = text_list[mch_pos:mch_pos+3]
                mch_string= " ".join(mch_string_list)
                mch_prob_val = re.findall('[-+]?\d*\.\d+|\d+', mch_string)
                if len(mch_prob_val) > 0:
                    mch_val = float(mch_prob_val[0])
                    mch_found = True
                    mch_prob_unit = re.sub("\s", "", mch_string)

                    if "PG" in mch_prob_unit:
                        mch_si_val = mch_val * 0.0621
                    elif "FMOL" in mch_prob_unit or "MOL" in mch_prob_unit:
                        mch_si_val = mch_val
                    else:
                        mch_si_val = mch_val * 0.0621
                    parameter["mch"] = mch_si_val
        # MCH END

        # PCT START
        if not pct_found:
            if "PCT" in i or "P.C.T" in i:
                pct_pos = text_list.index(i)
                pct_string_list = text_list[pct_pos:pct_pos + 3]
                pct_string = " ".join(pct_string_list)
                if "%" in pct_string:
                    pct_prob_val = re.findall('[-+]?\d*\.\d+|\d+', pct_string)
                    if len(pct_prob_val) > 0:
                        pct_val = float(pct_prob_val[0])
                        pct_found = True
                        pct_si_val = pct_val
                        parameter["pct"] = pct_si_val
        # PCT END

        # MPV START
        if not mpv_found:
            if "MPV" in i or "M.P.V" in i:
                mpv_pos = text_list.index(i)
                mpv_string_list = text_list[mpv_pos:mpv_pos + 3]
                mpv_string = " ".join(mpv_string_list)
                mpv_prob_unit = re.sub("\s", "", mpv_string)
                if "FL" in mpv_prob_unit:
                    mpv_prob_val = re.findall('[-+]?\d*\.\d+|\d+', mpv_string)
                    if len(mpv_prob_val) > 0:
                        mpv_val = float(mpv_prob_val[0])
                        mpv_found = True
                        mpv_si_val = mpv_val
                        parameter["mpv"] = mpv_si_val
        # MPV END

        # ESR START
        if not esr_found:
            if "ESR" in i or "WESTERGREN" in i or "CAPILLARY" in i or "ALIFAX" in i:
                esr_pos = text_list.index(i)
                esr_string_list = text_list[esr_pos:esr_pos + 3]
                esr_string = " ".join(esr_string_list)
                esr_prob_val = re.findall('[-+]?\d*\.\d+|\d+', esr_string)
                if len(esr_prob_val) > 0:
                    esr_val = float(esr_prob_val[0])
                    esr_found = True
                    esr_si_val = esr_val
                    parameter["esr"] = esr_si_val
        # ESR END

        # HBA1C START
        if not hba1c_found:
            if "HBA1C" in i or "A1C" in i:
                hba1c_pos = text_list.index(i)
                hba1c_string_list = text_list[hba1c_pos:hba1c_pos + 3]
                hba1c_string = " ".join(hba1c_string_list)
                if "%" in hba1c_string:
                    hba1c_prob_val = re.findall('[-+]?\d*\.\d+|\d+', hba1c_string)
                    if len(hba1c_prob_val) > 0:
                        hba1c_val = float(hba1c_prob_val[1])
                        hba1c_found = True
                        hba1c_si_val = hba1c_val
                        parameter["hba1c"] = hba1c_si_val
        # HBA1C END

    return parameter