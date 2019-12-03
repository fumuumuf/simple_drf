import time
import urllib

import requests
import xmltodict


class EkidataAPI:
    BASE_URL = 'http://www.ekidata.jp/api/'
    SLEEP_TIME = 0.5

    def _get(self, path, data=None):
        headers = {
            'Accept': 'application/xml',
            'accept-encoding': 'gzip, deflate, br',
        }
        time.sleep(self.SLEEP_TIME)

        url = self.BASE_URL
        url = urllib.parse.urljoin(url, path + '.xml')

        if not data: data = {}
        response = requests.get(url, data, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            raise Exception(f'status:{response.status_code}, {str(response.text)}')

        data = xmltodict.parse(response.text)
        return data['ekidata']

    def get_prefecture(self, i):
        return self._get(f'p/{i}')

    def get_line(self, line_cd):
        return self._get(f'l/{line_cd}')

    def get_station(self, station_cd):
        return self._get(f's/{station_cd}')['station']

    def get_all_line_cd(self):
        line_cds = set()
        for i in range(1, 48):
            data = self.get_prefecture(i)
            lines = data['line']
            if isinstance(lines, list):
                for line in lines:
                    line_cds.add(line['line_cd'])
            elif isinstance(lines, dict):
                line_cds.add(lines['line_cd'])

        return line_cds
