import datetime
from collections import defaultdict

try:
    from utils.mysql_connection import Connection, MySQLError
    from utils.logger import log_debug, log_error
except ImportError:
    from src.utils.mysql_connection import Connection, MySQLError
    from src.utils.logger import log_debug, log_error


def query_data(time_start, time_stop, reg):
    ttc_start = time_start.timestamp()
    ttc_stop = time_stop.timestamp()
    if len(reg.get('is_sport', '')) == 0:  # KHÔNG HỎI MÔN
        if len(reg.get('is_country', '')) == 0:  # ko quoc gia
            query = "SELECT * FROM schedule WHERE time>={} AND time<{} ".format(ttc_start, ttc_stop)
        elif len(reg.get('is_country', '')) == 1:  # HỎI 1 QUỐC GIA
            query = "SELECT * FROM schedule WHERE " \
                    "id_match in (SELECT id_match FROM schedule " \
                    "WHERE time>={} AND time<{} AND country = '{}') ". \
                format(ttc_start, ttc_stop, reg['is_country'][0])
        elif len(reg.get('is_country', '')) == 2:  # HỎI CẢ 2 QUỐC GIA
            query = "SELECT * FROM schedule " \
                    "WHERE id_match in ( SELECT s1.id_match " \
                    "FROM schedule s1 , schedule s2 " \
                    "WHERE s1.time>={} AND s1.time<{} AND s1.country = '{}' " \
                    "AND s2.country = '{}' AND s1.id_match = s2.id_match )". \
                format(ttc_start, ttc_stop, reg['is_country'][0], reg['is_country'][1])
    else:  # CÓ HỎI MÔN
        if len(reg.get('is_country', '')) == 0:
            query = "SELECT * FROM schedule WHERE time>={} AND time<{} AND sport = '{}' " \
                .format(ttc_start, ttc_stop, reg['is_sport'][0])
        elif len(reg.get('is_country', '')) == 1:  # hoi 1 quoc gia
            query = "SELECT * FROM schedule WHERE " \
                    "id_match in (SELECT id_match FROM schedule " \
                    "WHERE time>={} AND time<{} AND country = '{}' AND sport = '{}') ". \
                format(ttc_start, ttc_stop, reg['is_country'][0], reg['is_sport'][0])
        elif len(reg.get('is_country', '')) == 2:  # hoi 2 quoc gia
            query = "SELECT * FROM schedule " \
                    "WHERE sport ='{}' AND id_match in ( SELECT s1.id_match " \
                    "FROM schedule s1 , schedule s2 " \
                    "WHERE s1.time>={} AND s1.time<{} AND s1.country = '{}' " \
                    "AND s2.country = '{}' AND s1.id_match = s2.id_match )". \
                format(reg['is_sport'][0], ttc_start, ttc_stop, reg['is_country'][0],
                       reg['is_country'][1])
    connection = Connection().get_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    myresult = cursor.fetchall()
    return myresult


def cvt_1_to_2(so):
    if so < 10:
        return '0' + str(so)
    else:
        return str(so)


def gettime(time):
    month = cvt_1_to_2(time.month)
    day = cvt_1_to_2(time.day)
    hour = cvt_1_to_2(time.hour)
    minute = cvt_1_to_2(time.minute)
    return hour + ':' + minute + ' ' + day + '/' + month


def get_result(time_start, time_stop, reg):
    year = str(time_start.year)
    month = cvt_1_to_2(time_start.month)
    day = cvt_1_to_2(time_start.day)

    link = "https://interactive.guim.co.uk/2016/09/olympics-2016/ubuntu/schedule.html?#{}-{}-{}".format(
        year, month,
        day)
    myresult = query_data(time_start, time_stop, reg)
    dict_match = defaultdict(list)
    ## ➤  ➵ ☞
    if myresult:
        for x in myresult:
            dict_match[x.get("sport")].append(
                (x.get("id_match"), x.get("country"), x.get("result")))
        message = ''
        dem = 1
        for sport in dict_match:
            dict_match_sport = defaultdict(list)
            for i in dict_match[sport]:
                dict_match_sport[i[0]].append((i[1], i[2]))
            title = '➤ ' + sport.title() + ' :\n\n'
            c = 1
            c1 = ''
            for i in dict_match_sport:
                result = ''
                for j in dict_match_sport[i]:
                    result = result + '{}({}), '.format(j[0].title(), j[1])
                content = '  ➵ ' + result[:-2] + '\n'
                c += 1
                c1 = c1 + content
                if c == 5:
                    break
            ketqua = title + c1
            message = message + ketqua
            dem = dem + 1
            if dem == 4:
                break
        return message + '\nXem thêm : ☞  ' + link
    return "Không có trận đấu nào"


def get_schedule(time_start, time_stop, reg):
    year = str(time_start.year)
    if time_start.month >= 10:
        month = str(time_start.month)
    else:
        month = '0' + str(time_start.month)
    if time_start.day >= 10:
        day = str(time_start.day)
    else:
        day = '0' + str(time_start.day)
    link = "https://interactive.guim.co.uk/2016/09/olympics-2016/ubuntu/schedule.html?#{}-{}-{}".format(
        year, month,
        day)
    myresult = query_data(time_start, time_stop, reg)
    dict_match = defaultdict(list)
    ## ➤  ➵ ☞
    if myresult:
        for x in myresult:
            dict_match[x.get("sport")].append((x.get("id_match"), x.get("country"), x.get("result"),
                                               x.get("time")))
        message = ''
        dem = 1
        for sport in dict_match:
            dict_match_sport = defaultdict(list)
            for i in dict_match[sport]:
                dict_match_sport[i[0]].append((i[1], i[2], i[3]))
            title = '\n➤ ' + sport.title() + ' :\n'
            c = 1
            c1 = ''
            for i in dict_match_sport:
                result = ''
                time = datetime.datetime.fromtimestamp(float(dict_match_sport[i][0][2]))
                for j in dict_match_sport[i]:
                    result = result + '{}({}), '.format(j[0].title(), j[1])
                content = '  ➵ ' + gettime(time) + ' ' + result[:-2] + '\n'
                c += 1
                c1 = c1 + content
                if c == 5:
                    break
            ketqua = title + c1
            message = message + ketqua
            dem = dem + 1
            if dem == 4:
                break
        return message + '\n Xem thêm : ☞  ' + link
    return "Không có trận đấu nào"


def answer_athele(name_athele, data):
    result = ''
    for x in data:
        if name_athele == x.get("name").lower():
            result = result + '\
Tên vận động viên : {}\n\
Số  áo: {}\n\
Ngày sinh: {}\n\
Vị trí thi đấu: {}\n\
Quốc tịch:{} \n\
Bộ môn thi đấu:{} \n\
CLB: {}\n\
Chiều cao:  {}cm\n\
Cân nặng: {}kg\n'.format(x.get("name").title(), x.get("number"), x.get("dob"), x.get("position"),
                         x.get("country").title(), x.get("sport"), x.get("club").title(),
                         x.get("height"), x.get("weight"))

            if result:
                return result
    return 'Không có vận động viên nào'


def get_athlete(name_athlete):
    """
    Get info of athlete
    :param name_athlete: str
    :return:
    """
    if not name_athlete:
        return 'nhập tên vận động viên'
    connection = Connection().get_connection()
    try:
        cursor = connection.cursor()  # prepare an object cursor

        query = """
                    SELECT * FROM athlete WHERE name='{}';
                """.format(name_athlete.strip().lower())
        log_debug(query)
        cursor.execute(query)
        result = cursor.fetchall()
        result = answer_athele(name_athlete, result)
        # cursor.close()
        # del cursor
        # connection.close()
        return result
    except MySQLError as ex:
        connection.close()
        log_error("Can't get if of athlete with name - {}: {}".format(name_athlete, ex))
        return []


# BẢNG XẾP HẠNG
def answer_ranking(result):
    """
    Answer ranking
    :param result:
    :return:
    """
    ranking = ["Vị trí\t  HCV\t  HCB\t  HCĐ\t  Quốc gia"]
    for item in result:
        country = str(item[6]).title() + "\t"
        position = str(item[5]) + ".\t"
        gold_medal = str(item[2]) + "\t"
        sliver_medal = str(item[3]) + "\t"
        bronze_medal = str(item[3]) + "\t"
        value = position + '\t ' + gold_medal + '\t  ' + sliver_medal + '\t  ' + \
                bronze_medal + '\t  ' + country
        ranking.append(value)

    return "\n".join(ranking)


def get_ranking():
    """
    Get ranking
    :return:
    """
    connection = Connection().get_connection()
    try:
        cursor = connection.cursor()  # prepare an object cursor

        query = """
                SELECT * FROM ranking ORDER BY position ASC;
                """
        log_debug(query)
        cursor.execute(query)
        result = cursor.fetchall()
        result = answer_ranking(result)
        # cursor.close()
        # del cursor
        # connection.close()
        return result
    except MySQLError as ex:
        connection.close()
        log_error("Can't get ranking: {}".format(ex))
        return []
