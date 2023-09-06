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


class Methods(object):
    items = []

    def __init__(self, soap_action, depth):
        self.soap_action = soap_action
        self.depth = depth
        Methods.items.append(self)

    def dict_request(self, print_state=False,
                     filename=(datetime.datetime.now()).strftime(
                         "%Y %m %d %H-%M-%S"),
                     auth_token=basic_auth_token,
                     ):
        url = f"{cred.base_url}/edclients2.asmx"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": f"{cred.methods_url}/{self.soap_action}",
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
        <{self.soap_action} xmlns="{cred.methods_url}" />
        </soap:Body>
        </soap:Envelope>"""

        response = requests.post(url, data=body, headers=headers)
        # q = pprint.pformat(response.content.decode('utf-8'))
        q = xml.dom.minidom.parseString(response.content)
        pretty_xml_as_string = q.toprettyxml()
        # print(pretty_xml_as_string)
        if print_state is True:
            with open(
                    f"C:/tmp_garbage/soap_test/{self.soap_action}{filename}.txt",
                    "a",
                    encoding="utf-8",
            ) as file:
                file.write(pretty_xml_as_string)
        item_list = []

        def handle(path, item):
            # print(item)
            item_list.append(item)
            return True
        xmltodict.parse(pretty_xml_as_string, item_depth=self.depth,
                        item_callback=handle)
        return item_list


dict_methods = ['Version', 'dict_Consignees', 'dict_Shippers',
                'dict_CostCenters', 'dict_Cities', 'dict_Cities2',
                'dict_Cities3', 'dict_ErrorCodes', 'dict_PaidServices',
                'dict_Countries', 'dict_Events', 'dict_DistrictsRFs',
                'dict_Regions']
for i in range(len(dict_methods)):
    dict_methods[i] = Methods(dict_methods[i], 5)
print(Methods.items[4].soap_action)

dict_Cities = Methods('dict_Cities', 5)
print(Methods.items[-1].soap_action)
print(dict_Cities.dict_request(True)[0])
