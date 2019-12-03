import json
import urllib

import requests
import xmltodict


class EkidataAPI:
    BASE_URL = 'http://www.ekidata.jp/api/'

    def _get(self, path=None, data={}):
        headers = {
            'Accept': 'application/xml',
            'accept-encoding': 'gzip, deflate, br',
        }

        url = self.BASE_URL
        if path:
            url = urllib.parse.urljoin(url, path)

        response = requests.get(url, data, headers=headers)
        response.encoding = 'utf-8'
        print(response.encoding)
        if response.status_code != 200:
            raise Exception(str(response.text))

        return response.text
        # return response.json()

    def get_line_data(self, line_id):
        data = self._get(f'l/{line_id}.xml')
        return data


if __name__ == '__main__':
    data = EkidataAPI().get_line_data(11302)

    res = xmltodict.parse(data)
    res = json.dumps(res, indent=4)
    print(res)
