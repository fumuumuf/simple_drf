from django.core.management import BaseCommand
from rest_framework import serializers

from ekidata.management.commands.ekidata_api import EkidataAPI
from ekidata.models import Line, Station


class LineSerializer(serializers.ModelSerializer):
    line_cd = serializers.IntegerField(source='id')
    line_name = serializers.CharField(source='name')
    line_lat = serializers.CharField(source='lat', allow_blank=True, required=False)
    line_lon = serializers.CharField(source='lon', allow_blank=True, required=False)
    line_zoom = serializers.CharField(source='zoom', allow_blank=True, required=False)

    class Meta:
        model = Line
        exclude = ['id', 'name']


class StationSerializer(serializers.ModelSerializer):
    station_cd = serializers.IntegerField(source='id')
    station_name = serializers.CharField(source='name')
    station_g_cd = serializers.CharField(source='g_cd', required=False, allow_blank=True)
    pref_cd = serializers.IntegerField(source='prefecture')
    line_cd = serializers.PrimaryKeyRelatedField(source='line', required=False,
                                                 queryset=Line.objects.all())

    class Meta:
        model = Station
        exclude = ['id', 'name', 'prefecture']

class Command(BaseCommand):
    help = 'load line data'
    station_cds = set()

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def _add_stations(self, stations):
        if isinstance(stations, dict):
            stations = [stations]
        for s in stations:
            self.station_cds.add(s['station_cd'])

    def load_lines(self):
        all_line = self.api.get_all_line_cd()
        for cd in all_line:
            line_data = self.api.get_line(cd)
            line = line_data['line']

            print('load', cd, line['line_name'])
            instance = Line.objects.filter(id=int(line['line_cd'])).first()
            if instance:
                serializer = LineSerializer(instance, data=line, partial=True)
            else:
                serializer = LineSerializer(data=line)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
            else:
                print('load line error', cd, line['line_name'])
                continue

            if 'station' in line_data:
                self._add_stations(line_data['station'])

    def load_stations(self):
        for cd in self.station_cds:

            instance = Station.objects.filter(id=int(cd)).first()
            if instance:
                # すでに登録済の場合は pass
                # serializer = StationSerializer(instance, data=station, partial=True)
                continue

            station = self.api.get_station(cd)
            print('load station', cd, station['station_name'])
            serializer = StationSerializer(data=station)

            if serializer.is_valid(raise_exception=False):
                serializer.save()
            else:
                print('load station error', cd, station['station_name'])
                print(serializers.errors)



    def handle(self, *args, **options):
        self.api = EkidataAPI()
        print('--- load lines ---')
        self.load_lines()
        print('--- load stations ---')
        self.load_stations()
