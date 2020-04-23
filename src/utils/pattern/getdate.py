import datetime


# HÔM

def hom1(date_now, month_now, year_now, hom_):
    if hom_ == 'homnay':
        result_start = datetime.datetime(year_now, month_now, date_now)
    elif hom_ == 'ngaymai':
        result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(1)
    elif hom_ == 'ngaykia':
        result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(2)
    elif hom_ == 'homqua':
        result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(1)
    elif hom_ == 'homkia':
        result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(2)
    result_stop = datetime.datetime(result_start.year, result_start.month,
                                    result_start.day) + datetime.timedelta(1)
    return result_start, result_stop


# Tuần
def week(date_now, month_now, year_now, week):
    datetime_now = datetime.datetime(year_now, month_now, date_now)
    day = datetime_now.strftime("%A").lower()
    if week == 'tuannay':
        if day == 'monday':
            result_start = datetime.datetime(year_now, month_now, date_now)
        elif day == 'tuesday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(1)
        elif day == 'wednesday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(2)
        elif day == 'thursday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(3)
        elif day == 'friday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(4)
        elif day == 'saturday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(5)
        elif day == 'sunday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(6)
    elif week == 'tuansau':
        if day == 'monday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(7)
        elif day == 'tuesday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(6)
        elif day == 'wednesday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(4)
        elif day == 'thursday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(4)
        elif day == 'friday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(3)
        elif day == 'saturday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(2)
        elif day == 'sunday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(1)
    elif week == 'tuansaunua':
        if day == 'monday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(14)
        elif day == 'tuesday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(13)
        elif day == 'wednesday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(12)
        elif day == 'thursday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(11)
        elif day == 'friday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(10)
        elif day == 'saturday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(9)
        elif day == 'sunday':
            result_start = datetime.datetime(year_now, month_now, date_now) + datetime.timedelta(8)
    elif week == 'tuantruoc':
        if day == 'monday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(7)
        elif day == 'tuesday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(8)
        elif day == 'wednesday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(9)
        elif day == 'thursday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(10)
        elif day == 'friday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(11)
        elif day == 'saturday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(12)
        elif day == 'sunday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(13)
    elif week == 'tuantruocnua':
        if day == 'monday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(14)
        elif day == 'tuesday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(15)
        elif day == 'wednesday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(16)
        elif day == 'thursday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(17)
        elif day == 'friday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(18)
        elif day == 'saturday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(19)
        elif day == 'sunday':
            result_start = datetime.datetime(year_now, month_now, date_now) - datetime.timedelta(20)
    result_stop = result_stop = datetime.datetime(result_start.year, result_start.month,
                                                  result_start.day) + datetime.timedelta(7)
    return result_start, result_stop


##Thứ + tuần
def day_week(date_now, month_now, year_now, day, tuan):
    monday = week(date_now, month_now, year_now, tuan)[0]
    if day == 'monday':
        result_start = monday
        result_stop = monday + datetime.timedelta(1)
    elif day == 'tuesday':
        result_start = monday + datetime.timedelta(1)
        result_stop = monday + datetime.timedelta(2)
    elif day == 'wednesday':
        result_start = monday + datetime.timedelta(2)
        result_stop = monday + datetime.timedelta(3)
    elif day == 'thursday':
        result_start = monday + datetime.timedelta(3)
        result_stop = monday + datetime.timedelta(4)
    elif day == 'friday':
        result_start = monday + datetime.timedelta(4)
        result_stop = monday + datetime.timedelta(5)
    elif day == 'saturday':
        result_start = monday + datetime.timedelta(5)
        result_stop = monday + datetime.timedelta(6)
    elif day == 'sunday':
        result_start = monday + datetime.timedelta(6)
        result_stop = monday + datetime.timedelta(7)
    return result_start, result_stop


# Buổi + ngày
def buoi_ngay(date_now, month_now, year_now, buoi, hom_):
    a = hom1(date_now, month_now, year_now, hom_)[0]
    if buoi.strip() == 'sang':
        result_start = datetime.datetime(a.year, a.month, a.day, 0, 0, 0)
        result_stop = datetime.datetime(a.year, a.month, a.day, 11, 0, 0)
    elif buoi.strip() == 'trua':
        result_start = datetime.datetime(a.year, a.month, a.day, 11, 0, 0)
        result_stop = datetime.datetime(a.year, a.month, a.day, 13, 0, 0)
    elif buoi.strip() == 'chieu':
        result_start = datetime.datetime(a.year, a.month, a.day, 13, 0, 0)
        result_stop = datetime.datetime(a.year, a.month, a.day, 18, 0, 0)
    elif buoi.strip() == 'toi':
        result_start = datetime.datetime(a.year, a.month, a.day, 18, 0, 0)
        result_stop = datetime.datetime(a.year, a.month, a.day, 0, 0, 0) + datetime.timedelta(1)

    return result_start, result_stop


def buoi1(ngay, buoi):
    a = ngay
    if buoi.strip() == 'sang':
        result_start = datetime.datetime(a.year, a.month, a.day, 0, 0, 0)
        result_stop = datetime.datetime(a.year, a.month, a.day, 11, 0, 0)
    elif buoi.strip() == 'trua':
        result_start = datetime.datetime(a.year, a.month, a.day, 11, 0, 0)
        result_stop = datetime.datetime(a.year, a.month, a.day, 13, 0, 0)
    elif buoi.strip() == 'chieu':
        result_start = datetime.datetime(a.year, a.month, a.day, 13, 0, 0)
        result_stop = datetime.datetime(a.year, a.month, a.day, 16, 0, 0)
    elif buoi.strip() == 'toi':
        result_start = datetime.datetime(a.year, a.month, a.day, 18, 0, 0)
        result_stop = datetime.datetime(a.year, a.month, a.day, 0, 0, 0) + datetime.timedelta(1)
    return result_start, result_stop
# print(buoi_ngay(date_now,month_now,year_now,'toi','ngaymai')[1])
# # print(hom1(date_now,month_now,year_now,'ngaymai')[1])
# # print(hom(date_now,month_now,year_now,'ngaymai'))
# # print(hom(date_now,month_now,year_now,'ngaykia'))
# # print(hom(date_now,month_now,year_now,'homqua'))
# # print(hom(date_now,month_now,year_now,'homkia'))
# # print(week(date_now,month_now,year_now,'tuannay')[1])
# # print(week(date_now,month_now,year_now,'tuansau'))
# # print(week(date_now,month_now,year_now,'tuansaunua'))
# # print(week(date_now,month_now,year_now,'tuantruoc'))
# print(day_week(date_now,month_now,year_now,'tuesday','tuantruoc')[1])
