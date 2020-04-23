# coding=utf-8
import re
import datetime

try:
    from utils.pattern.getdate import *
except ImportError:
    from src.utils.pattern.getdate import *

## ĐỊNH NGHĨA CÁC CHUỖI REGEX
# ĐỊNH DẠNG NGÀY THÁNG NĂM
date_now = 4
month_now = 8
year_now = 2016
datetime_dmy = [
    r'(?:[^0-9\w]|^)ngày(?:\s*)([1-2][0-9]|3[0-1]|0?[1-9])',
    r'(?:[^0-9\w]|^)ngày(?:\s*)([1-2][0-9]|3[0-1]|0?[1-9])'
    r'(?:\s*)tháng(?:\s*)(1[0-2]|0?[1-9])(?:\s*)năm(?:\s*)'
    r'(2[0-9]{3})',
    r'(?:[^0-9\w]|^)tháng(?:\s*)(1[0-2]|0?[1-9])(?:\s*)năm(?:\s*)(2[0-9]{3})',
    r'(?:[^0-9\w]|^)tháng(?:\s*)(1[0-2]|0?[1-9])',
    r'(?:[^0-9\w]|^)năm(?:\s*)(2[0-9]{3})',
    r'(?:[^0-9\w]|^)([1-2][0-9]|3[0-1]|0?[1-9])(?:\s*)'
    r'(?:[/-]|tháng)(?:\s*)(1[0-2]|0?[1-9])',
    r'(?:[^0-9\w]|^)([1-2][0-9]|3[0-1]|0?[1-9])(?:\s*)'
    r'(?:[/-]|tháng)(?:\s*)(1[0-2]|0?[1-9])(?:\s*)'
    r'(?:[/-]|năm)(?:\s*)(2[0-9]{3})',
    r'(?:[^0-9\w]|^)(1[0-2]|0?[1-9])(?:\s*)'
    r'(?:[/-]|năm)(?:\s*)(2[0-9]{3})',
]
# ĐỊnH DẠNG HÔM
datetime_hom = [
    r'(hôm nay|bây giờ|bây h|hiện tại|hiện nay|lúc này|nay)',
    r'(ngày mai|mai|hôm sau)',
    r'(ngày kia|ngày mốt)',
    r'(ngày kia nữa|hôm kia nữa)',
    r'(hôm qua)',
    r'(hôm kia)'
]
# ĐỊNH DẠNG TUẦN
datetime_week = [
    r'(tuần này|tuần hiện tại|tuần hiện giờ)',
    r'(tuần sau|tuần tới)',
    r'(tuần kia|tuần sau nữa)',
    r'(tuần trước|tuần vừa rồi)'
    r'(tuần trước nữa)'
]
# ĐỊNH DẠNG THỨ
datetime_day = [
    r'(thứ 2|thứ hai)',
    r'(thứ 3|thứ ba)',
    r'(thứ 4|thứ tư|thứ bốn)',
    r'(thứ 5|thứ năm)',
    r'(thứ 6|thứ sáu)',
    r'(thứ 7|thứ bảy|thứ bẩy)',
    r'(chủ nhật)'
]

datetime_buoi = [
    r'(sáng|buổi sáng)',
    r'(trưa|buổi trưa)',
    r'(tối|buổi tối)',
    r'(chiều|buổi chiều)'
]


## --------------------------------------NHẬN DIỆN THỰC THỂ-----------------------------------------
# class NER_DATETIME():
#     def __init__(self):
#         return sel
def ner_datetime_dmy(str):
    date = []
    lenght = 0
    time = []
    ner_date = 0
    ner_month = 0
    ner_year = 0
    for i in range(len(datetime_dmy)):
        match = re.findall(datetime_dmy[i], str.lower())
        if match:
            if len(match[0]) >= lenght:
                date.append(match[0])
                lenght = len(match[0])

    print(date)
    if len(date) > 0:
        is_tupple = 0
        for i in date:
            if isinstance(i, tuple):
                is_tupple = 1
                break
        if is_tupple == 1:
            max_len = 0
            for i in date:
                if isinstance(i, tuple) and len(i) >= max_len:
                    max_len = len(i)
                    date_full = i
            if len(date_full) == 2:
                if len(date_full[1]) == 4:
                    ner_date = 0
                    ner_month = date_full[0]
                    ner_year = date_full[1]
                else:
                    ner_date = date_full[0]
                    ner_month = date_full[1]
                    ner_year = year_now
            elif len(date_full) == 3:
                ner_date = date_full[0]
                ner_month = date_full[1]
                ner_year = date_full[2]
        else:
            if 'ngày' in str:
                ner_date = date[0]
                ner_month = month_now
                ner_year = year_now
            else:
                ner_date = 0
                ner_month = date[0]
                ner_year = year_now
        return int(ner_date), int(ner_month), int(ner_year)

    else:
        return 0, 0, 0


def ner_datetime_hom(str):
    for i in range(len(datetime_hom)):
        match = re.findall(datetime_hom[i], str.lower())
        if match:
            return match[0].strip()


def ner_datetime_day(str):
    for i in range(len(datetime_day)):
        match = re.findall(datetime_day[i], str.lower())
        if match:
            return match[0].strip()


def ner_datetime_week(str):
    for i in range(len(datetime_week)):
        match = re.findall(datetime_week[i], str.lower())
        if match:
            return match[0].strip()


def ner_datetime_buoi(str):
    for i in range(len(datetime_buoi)):
        match = re.findall(datetime_buoi[i], str.lower())
        if match:
            return match[0].strip()


def regex(str):
    ngay, thang, nam = ner_datetime_dmy(str)
    hom = ner_datetime_hom(str)
    tuan = ner_datetime_week(str)
    thu = ner_datetime_day(str)
    buoi = ner_datetime_buoi(str)
    return ngay, thang, nam, hom, thu, tuan, buoi


##---------------------------------ĐƯA VỀ DATETIME------------------------------------------------------

def ner(ngay, thang, nam, hom, tuan, thu, buoi):
    if ngay == 0 and thang == 0 and nam == 0 and hom == None and tuan == None and thu == None and buoi == None:
        return 0, 0
    ## CÓ NGÀY THÁNG NĂM
    if ngay > 0 or thang > 0 or nam > 0:
        if buoi == None:
            datetime_to_second_start = datetime.datetime(nam, thang, ngay, 0, 0, 0)
            if ngay != 0:
                datetime_to_second_stop = datetime_to_second_start + datetime.timedelta(1)
            else:
                datetime_to_second_stop = datetime_to_second_start + datetime.timedelta(30)
            # print(datetime_to_second)
            return datetime_to_second_start, datetime_to_second_stop
        else:
            if buoi == 'sáng' or buoi == 'buổi sáng':
                buoi_result = 'sang'
            elif buoi == 'trưa' or buoi == 'trưa':
                buoi_result = 'trua'
            elif buoi == 'tối' or buoi == 'buổi tối':
                buoi_result = 'toi'
            elif buoi == 'chiều' or buoi == 'buổi chiều':
                buoi_result = 'chieu'
            datetime_to_second = datetime.datetime(nam, thang, ngay)
            datetime_to_second_start, datetime_to_second_stop = buoi1(datetime_to_second,
                                                                      buoi_result)
            # print(datetime_to_second)
            return datetime_to_second_start, datetime_to_second_stop
    elif ngay > 0 and thang > 0 and nam == 0:
        if buoi == None:
            datetime_to_second_start = datetime.datetime(year_now, thang, ngay, 0, 0, 0)
            datetime_to_second_stop = datetime_to_second_start + datetime.timedelta(1)
            return datetime_to_second_start, datetime_to_second_stop
        else:
            if buoi == 'sáng' or buoi == 'buổi sáng':
                buoi_result = 'sang'
            elif buoi == 'trưa' or buoi == 'trưa':
                buoi_result = 'trua'
            elif buoi == 'tối' or buoi == 'buổi tối':
                buoi_result = 'toi'
            elif buoi == 'chiều' or buoi == 'buổi chiều':
                buoi_result = 'chieu'
            datetime_to_second = datetime.datetime(year_now, thang, ngay)
            datetime_to_second_start, datetime_to_second_stop = buoi1(datetime_to_second,
                                                                      buoi_result)
            # print(datetime_to_second)
            return datetime_to_second_start, datetime_to_second_stop

    else:  ## KHÔNG CÓ NGÀY THÁNG NĂM
        ## Ko có buổi
        if buoi == None:
            # THỨ 6 TUẦN SAU
            if tuan != None and thu != None:
                if tuan == 'tuần này' or tuan == 'tuần hiện tại' or tuan == 'tuần hiện giờ':
                    tuan_result = 'tuannay'
                elif tuan == 'tuần sau' or tuan == 'tuần tới':
                    tuan_result = 'tuansau'
                elif tuan == 'tuần kia' or tuan == 'tuần sau nữa':
                    tuan_result = 'tuansaunua'
                elif tuan == 'tuần trước' or tuan == 'tuần vừa rồi':
                    tuan_result = 'tuantruoc'
                elif tuan == 'tuần trước nữa':
                    tuan_result = 'tuantruocnua'
                if thu == 'thứ 2' or thu == 'thứ hai':
                    thu_result = 'monday'
                elif thu == 'thứ 3' or thu == 'thứ ba':
                    thu_result = 'tuesday'
                elif thu == 'thứ 4' or thu == 'thứ tư' or thu == 'thứ bốn':
                    thu_result = 'wednesday'
                elif thu == 'thứ 5' or thu == 'thứ năm':
                    thu_result = 'thursday'
                elif thu == 'thứ 6' or thu == 'thứ sáu':
                    thu_result = 'friday'
                elif thu == 'thứ 7' or thu == 'thứ bảy':
                    thu_result = 'saturday'
                elif thu == 'chủ nhật':
                    thu_result = 'sunday'
                # print(thu_result,tuan_result)
                datetime_to_second_start, datetime_to_second_stop = day_week(date_now, month_now,
                                                                             year_now, thu_result,
                                                                             tuan_result)
                # print(datetime_to_second)
                return datetime_to_second_start, datetime_to_second_stop

            # THỨ 6
            elif tuan == None and thu != None:
                tuan_result = 'tuannay'
                if thu == 'thứ 2' or thu == 'thứ hai':
                    thu_result = 'monday'
                elif thu == 'thứ 3' or thu == 'thứ ba':
                    thu_result = 'tuesday'
                elif thu == 'thứ 4' or thu == 'thứ tư' or thu == 'thứ bốn':
                    thu_result = 'wednesday'
                elif thu == 'thứ 5' or thu == 'thứ năm':
                    thu_result = 'thursday'
                elif thu == 'thứ 6' or thu == 'thứ sáu':
                    thu_result = 'friday'
                elif thu == 'thứ 7' or thu == 'thứ bảy':
                    thu_result = 'saturday'
                elif thu == 'chủ nhật':
                    thu_result = 'sunday'
                # print(thu_result,tuan_result)
                datetime_to_second_start, datetime_to_second_stop = day_week(date_now, month_now,
                                                                             year_now, thu_result,
                                                                             tuan_result)
                # print(datetime_to_second)
                return datetime_to_second_start, datetime_to_second_stop

            ## TUẦN SAU
            elif tuan != None and thu == None:
                thu_result = 'monday'
                if tuan == 'tuần này' or tuan == 'tuần hiện tại' or tuan == 'tuần hiện giờ':
                    tuan_result = 'tuannay'
                elif tuan == 'tuần sau' or tuan == 'tuần tới':
                    tuan_result = 'tuansau'
                elif tuan == 'tuần kia' or tuan == 'tuần sau nữa':
                    tuan_result = 'tuansaunua'
                elif tuan == 'tuần trước' or tuan == 'tuần vừa rồi':
                    tuan_result = 'tuantruoc'
                elif tuan == 'tuần trước nữa':
                    tuan_result = 'tuantruocnua'
                # print(thu_result,tuan_result)
                datetime_to_second_start, datetime_to_second_stop = week(date_now, month_now,
                                                                         year_now, 'tuannay')
                # print(datetime_to_second)
                return datetime_to_second_start, datetime_to_second_stop
            ## HÔM
            elif thu == None and tuan == None:
                if hom == 'hôm nay' or hom == 'bây giờ' or hom == 'bây h' or hom == 'hiện tại' or hom == 'hiện nay' or hom == 'lúc này' or hom == 'nay':
                    hom_result = 'homnay'
                elif hom == 'ngày mai' or hom == 'mai' or hom == 'hôm sau':
                    hom_result = 'ngaymai'
                elif hom == 'ngày kia' or hom == 'ngày mốt':
                    hom_result = 'ngaykia'
                elif hom == 'hôm qua':
                    hom_result = 'homqua'
                elif hom == 'hôm kia':
                    hom_result = 'homkia'
                # print(hom_result)
                datetime_to_second_start, datetime_to_second_stop = hom1(date_now, month_now,
                                                                         year_now, hom_result)
                # print(datetime_to_second)
                return datetime_to_second_start, datetime_to_second_stop
                # print(hom_result)

                ## Có BUổi
        else:
            if buoi == 'sáng' or buoi == 'buổi sáng':
                buoi_result = 'sang'
            elif buoi == 'trưa' or buoi == 'trưa':
                buoi_result = 'trua'
            elif buoi == 'tối' or buoi == 'buổi tối':
                buoi_result = 'toi'
            elif buoi == 'chiều' or buoi == 'buổi chiều':
                buoi_result = 'chieu'
            if tuan != None and thu != None:
                if tuan == 'tuần này' or tuan == 'tuần hiện tại' or tuan == 'tuần hiện giờ':
                    tuan_result = 'tuannay'
                elif tuan == 'tuần sau' or tuan == 'tuần tới':
                    tuan_result = 'tuansau'
                elif tuan == 'tuần kia' or tuan == 'tuần sau nữa':
                    tuan_result = 'tuansaunua'
                elif tuan == 'tuần trước' or tuan == 'tuần vừa rồi':
                    tuan_result = 'tuantruoc'
                elif tuan == 'tuần trước nữa':
                    tuan_result = 'tuantruocnua'
                if thu == 'thứ 2' or thu == 'thứ hai':
                    thu_result = 'monday'
                elif thu == 'thứ 3' or thu == 'thứ ba':
                    thu_result = 'tuesday'
                elif thu == 'thứ 4' or thu == 'thứ tư' or thu == 'thứ bốn':
                    thu_result = 'wednesday'
                elif thu == 'thứ 5' or thu == 'thứ năm':
                    thu_result = 'thursday'
                elif thu == 'thứ 6' or thu == 'thứ sáu':
                    thu_result = 'friday'
                elif thu == 'thứ 7' or thu == 'thứ bảy':
                    thu_result = 'saturday'
                elif thu == 'chủ nhật':
                    thu_result = 'sunday'
                # print(buoi_result,thu_result, tuan_result)
                datetime_to_second = \
                    day_week(date_now, month_now, year_now, thu_result, tuan_result)[0]
                datetime_to_second_start, datetime_to_second_stop = buoi1(datetime_to_second,
                                                                          buoi_result)
                # print(datetime_to_second)
                return datetime_to_second_start, datetime_to_second_stop
            # THỨ 6
            elif tuan == None and thu != None:
                tuan_result = 'tuannay'
                if thu == 'thứ 2' or thu == 'thứ hai':
                    thu_result = 'monday'
                elif thu == 'thứ 3' or thu == 'thứ ba':
                    thu_result = 'tuesday'
                elif thu == 'thứ 4' or thu == 'thứ tư' or thu == 'thứ bốn':
                    thu_result = 'wednesday'
                elif thu == 'thứ 5' or thu == 'thứ năm':
                    thu_result = 'thursday'
                elif thu == 'thứ 6' or thu == 'thứ sáu':
                    thu_result = 'friday'
                elif thu == 'thứ 7' or thu == 'thứ bảy':
                    thu_result = 'saturday'
                elif thu == 'chủ nhật':
                    thu_result = 'sunday'
                # print(buoi_result,thu_result, tuan_result)
                datetime_to_second = \
                    day_week(date_now, month_now, year_now, thu_result, tuan_result)[0]
                datetime_to_second_start, datetime_to_second_stop = buoi1(datetime_to_second,
                                                                          buoi_result)
                # print(datetime_to_second)
                return datetime_to_second_start, datetime_to_second_stop

            ## TUẦN SAU
            elif tuan != None and thu == None:
                thu_result = 'monday'
                if tuan == 'tuần này' or tuan == 'tuần hiện tại' or tuan == 'tuần hiện giờ':
                    tuan_result = 'tuannay'
                elif tuan == 'tuần sau' or tuan == 'tuần tới':
                    tuan_result = 'tuansau'
                elif tuan == 'tuần kia' or tuan == 'tuần sau nữa':
                    tuan_result = 'tuansaunua'
                elif tuan == 'tuần trước' or tuan == 'tuần vừa rồi':
                    tuan_result = 'tuantruoc'
                elif tuan == 'tuần trước nữa':
                    tuan_result = 'tuantruocnua'
                # print(buoi_result,thu_result, tuan_result)
                datetime_to_second = \
                    day_week(date_now, month_now, year_now, thu_result, tuan_result)[0]
                datetime_to_second_start, datetime_to_second_stop = buoi1(datetime_to_second,
                                                                          buoi_result)
                # print(datetime_to_second)
                return datetime_to_second_start, datetime_to_second_stop
            ## HÔM
            elif thu == None and tuan == None:
                if hom == 'hôm nay' or hom == 'bây giờ' or hom == 'bây h' or hom == 'hiện tại' or hom == 'hiện nay' or hom == 'lúc này' or hom == 'nay':
                    hom_result = 'homnay'
                elif hom == 'ngày mai' or hom == 'mai' or hom == 'hôm sau':
                    hom_result = 'ngaymai'
                elif hom == 'ngày kia' or hom == 'ngày mốt':
                    hom_result = 'ngaykia'
                elif hom == 'hôm qua':
                    hom_result = 'homqua'
                elif hom == 'hôm kia':
                    hom_result = 'homkia'
                # print(buoi_result,hom_result)
                datetime_to_second = hom1(date_now, month_now, year_now, hom_result)[0]
                datetime_to_second_start, datetime_to_second_stop = buoi1(datetime_to_second,
                                                                          buoi_result)
                # print(datetime_to_second)
                return datetime_to_second_start, datetime_to_second_stop

##-----------------------------------CHẠy------------------------

# str1='kết quả việt nam và mỹ'
# str2='ngày 30-4 có trận đấu nào không'
# str3='tối thứ 3 tuần sau có trận nào'
# str4='aa ngày mai có những trận đấu nào'
# str5='sáng mai có có trận đấu nào'
# ngay, thang, nam, hom, thu, tuan, buoi = regex('lịch thi đấu hôm nay ?')
# date_start,date_stop = ner(ngay, thang, nam, hom, tuan, thu, buoi)
# print('- ner_datetime : start - stop')
# print(date_start.timestamp())
# print(date_stop.timestamp())
