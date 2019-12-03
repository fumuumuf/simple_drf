import time
import urllib

import requests
import xmltodict


class EkidataAPI:
    BASE_URL = 'http://www.ekidata.jp/api/'
    SLEEP_TIME = 0.5

    def _get(self, path=None, data={}):
        headers = {
            'Accept': 'application/xml',
            'accept-encoding': 'gzip, deflate, br',
        }
        time.sleep(self.SLEEP_TIME)

        url = self.BASE_URL
        if path:
            url = urllib.parse.urljoin(url, path)

        response = requests.get(url, data, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            raise Exception(str(response.text))

        return response.text
        # return response.json()

    def get_prefecture(self, i):
        data = self._get(f'p/{i}.xml')
        return xmltodict.parse(data)

    def get_line(self, line_cd):
        data = self._get(f'l/{line_cd}.xml')
        return xmltodict.parse(data)

    def get_all_line_cd(self):
        line_cds = set()
        for i in range(1, 48):
            data = self.get_prefecture(i)
            lines = xmltodict.parse(data)['ekidata']['line']
            if isinstance(lines, list):
                for line in lines:
                    line_cds.add(line['line_cd'])
            elif isinstance(lines, dict):
                line_cds.add(lines['line_cd'])

        return line_cds
