from django.core.management import BaseCommand
from rest_framework import serializers

from ekidata.management.commands.ekidata_api import EkidataAPI
from ekidata.models import Line


class LineSerializer(serializers.ModelSerializer):
    line_cd = serializers.IntegerField(source='id')
    line_name = serializers.CharField(source='name')
    line_lat = serializers.CharField(source='lat', allow_blank=True, required=False)
    line_lon = serializers.CharField(source='lon', allow_blank=True, required=False)
    line_zoom = serializers.CharField(source='zoom', allow_blank=True, required=False)

    class Meta:
        model = Line
        exclude = ['id', 'name']


class Command(BaseCommand):
    help = 'load ekidata'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        api = EkidataAPI()
        line = api.get_line(11302)
        # all_line = api.get_all_line_cd()
        all_line = [line['ekidata']['line']['line_cd']]
        for cd in all_line:
            res = api.get_line(cd)

            line = res['ekidata']['line']
            instance = Line.objects.filter(id=int(line['line_cd'])).first()
            if instance:
                serializer = LineSerializer(instance, data=line, partial=True)
            else:
                serializer = LineSerializer(data=line)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
            else:
                print('load error line_id:', line['line_cd'])
            break
