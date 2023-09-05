import requests
import xml.dom.minidom
from base64 import b64encode
import xmltodict
import datetime
import credentials as cred


# Authorization token: we need to base 64 encode it
# and then decode it to acsii as python 3 stores it as a byte string


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


basic_auth_token = basic_auth(cred.ed_client_username, cred.ed_client_password)


def dict_cities3_request(
        filename=(datetime.datetime.now()).strftime("%Y %m %d %H-%M-%S"),
        auth_token=basic_auth_token,
):
    url = "https://ed.major-express.ru/edclients2.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://ltl-ws.major-express.ru/edclients/dict_Cities3",
        "Authorization": f"{auth_token}",
        "Accept": "*/*",
        "Host": "ed.major-express.ru",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Content-Length": "1113",
    }
    body = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
    <dict_Cities3 xmlns="http://ltl-ws.major-express.ru/edclients/" />
    </soap:Body>
    </soap:Envelope>"""

    response = requests.post(url, data=body, headers=headers)
    # q = pprint.pformat(response.content.decode('utf-8'))
    q = xml.dom.minidom.parseString(response.content)
    pretty_xml_as_string = q.toprettyxml()
    # print(pretty_xml_as_string)
    with open(
            f"C:/tmp_garbage/soap_test/test_response_CL_ED {filename}.txt",
            "a",
            encoding="utf-8",
    ) as file:
        file.write(pretty_xml_as_string)

    # def handle(path, item):
    #     print('path:%s item:%s' % (path, item))
    #     return True
    doc = xmltodict.parse(pretty_xml_as_string)
    doc_list = doc["soap:Envelope"]["soap:Body"]["dict_Cities3Response"][
        "dict_Cities3Result"
    ]["CityInfo"]
    return pretty_xml_as_string, doc_list


def city_search(cityname, source=dict_cities3_request()[1]):
    """Поиск кода города по его названию с последовательным перебором общего
    списка городов (Линейный поиск)"""
    for i in range(len(source)):
        if source[i]["Name"]["NameRus"] == cityname:
            # print(source[i]["Code"], i)
            # print(source[i])
            return i, source[i]
        else:
            continue


def citycode_search_v2(citycode, source=dict_cities3_request()[1]):
    """Поиск информации о городе по его коду в отсортированному по возрастанию
    общем списке городов посредством бинарного поиска"""
    start = 0  # Переменная начала диапазона поиска
    stop = len(source) - 1  # Переменная конца диапазона поиска
    index = None  # Порядковый номер объекта в списке
    loop_count = 1
    while (start <= stop) and (index is None):
        half = (start + stop) // 2
        if int(source[half]['Code']) == citycode:
            index = half
        else:
            loop_count += 1
            if int(source[half]['Code']) > citycode:
                stop = half - 1
            else:
                start = half + 1
    if index is None:
        return loop_count, "Код города не найден"
    else:
        return loop_count, index, source[index]


# print(dict_cities3_request()[1][20])
# print(city_search('Новороссийск'))
# print(citycode_search_v2(72))
