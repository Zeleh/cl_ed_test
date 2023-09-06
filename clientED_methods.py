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
    url = f"{cred.base_url}/edclients2.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f"{cred.methods_url}/dict_Cities3",
        "Authorization": f"{auth_token}",
        "Accept": "*/*",
        "Host": "ed.major-express.ru",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    body = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
    <dict_Cities3 xmlns="{cred.methods_url}" />
    </soap:Body>
    </soap:Envelope>"""

    response = requests.post(url, data=body, headers=headers)
    # q = pprint.pformat(response.content.decode('utf-8'))
    q = xml.dom.minidom.parseString(response.content)
    pretty_xml_as_string = q.toprettyxml()
    # print(pretty_xml_as_string)
    with open(
            f"C:/tmp_garbage/soap_test/test_Cities3{filename}.txt",
            "a",
            encoding="utf-8",
    ) as file:
        file.write(pretty_xml_as_string)
    item_list = []

    def handle(path, item):
        # print(item)
        item_list.append(item)
        return True

    # def postprocessor(path, key, value):
    #     try:
    #         return key + ':int', int(value)
    #     except (ValueError, TypeError):
    #         return key, value
    xmltodict.parse(pretty_xml_as_string,item_depth=5, item_callback=handle)
    return item_list


class TeSt:
    def city_search(self, cityname, source=None):
        """Поиск кода города по его названию с последовательным перебором общего
        списка городов (Линейный поиск)"""
        if source is None:
            source = dict_cities3_request()
        for i in range(len(source)):
            if source[i]["Name"]["NameRus"] == cityname:
                # print(source[i]["Code"], i)
                # print(source[i])
                return i, source[i]
            else:
                continue

    def citycode_search_v2(self, citycode, source=None):
        """Поиск информации о городе по его коду в отсортированному по возрастанию
        общем списке городов посредством бинарного поиска"""
        if source is None:
            source = dict_cities3_request()
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


def dict_consignees(
        filename=(datetime.datetime.now()).strftime("%Y %m %d %H-%M-%S"),
        auth_token=basic_auth_token,
                        ):
    url = f"{cred.base_url}/edclients2.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f"{cred.methods_url}/dict_Consignees",
        "Authorization": f"{auth_token}",
        "Accept": "*/*",
        "Host": "ed.major-express.ru",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    body = f'''<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
        <dict_Consignees xmlns="{cred.methods_url}"/>
        </soap:Body>
        </soap:Envelope>'''

    response = requests.post(url, data=body, headers=headers)
    q = xml.dom.minidom.parseString(response.content)
    pretty_xml_as_string = q.toprettyxml()
    with open(
            f"C:/tmp_garbage/soap_test/test_Consignee{filename}.txt",
            "a",
            encoding="utf-8",
    ) as file:
        file.write(pretty_xml_as_string)
    item_list = []

    def handle(path, item):
        # print(item)
        item_list.append(item)
        return True
    xmltodict.parse(pretty_xml_as_string, item_depth=5, item_callback=handle)
    return item_list

def dict_shippers(
        filename=(datetime.datetime.now()).strftime("%Y %m %d %H-%M-%S"),
        auth_token=basic_auth_token,
                        ):
    url = f"{cred.base_url}/edclients2.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f"{cred.methods_url}/dict_Shippers",
        "Authorization": f"{auth_token}",
        "Accept": "*/*",
        "Host": "ed.major-express.ru",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    body = f'''<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
        <dict_Shippers xmlns="{cred.methods_url}"/>
        </soap:Body>
        </soap:Envelope>'''
    response = requests.post(url, data=body, headers=headers)
    q = xml.dom.minidom.parseString(response.content)
    pretty_xml_as_string = q.toprettyxml()
    with open(
            f"C:/tmp_garbage/soap_test/test_Shipper{filename}.txt",
            "a",
            encoding="utf-8",
    ) as file:
        file.write(pretty_xml_as_string)
    item_list = []

    def handle(path, item):
        # print(item)
        item_list.append(item)
        return True

    xmltodict.parse(pretty_xml_as_string, item_depth=5, item_callback=handle)
    return item_list


var = dict_cities3_request()
print(var[0])
var = TeSt()
print('-'*10 + '\n' + str(var.city_search('Москва')))
print('-'*10 + '\n' + str(var.citycode_search_v2(129)))
print(dict_consignees()[0])
print(dict_shippers()[0])
