import base64
import binascii
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.fields import FileField
from rest_framework.utils.field_mapping import get_field_kwargs

from articles.models import Article
from django.db import models

from accounts.models import User
import mimetypes
from os.path import splitext

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


class Base64FileField(serializers.FileField):
    """
    base64でエンコードされたファイルを扱うField
    base64 エンコードされたファイルをアップロードする場合はこの Field を使用する.

    References:
        https://stackoverflow.com/questions/28036404/django-rest-framework-upload-image-the-submitted-data-was-not-a-file
    Notes:
        Heavily based on
        https://github.com/tomchristie/django-rest-framework/pull/1268

        Updated for Django REST framework 3.

        and based on
        https://github.com/tsh/django-rest-framework-base64-fields
    """

    _ERROR_MESSAGE = 'Base64データが不正です.'

    _MIME_MAPPING = {
        'image/jpeg': '.jpg',
        'application/pdf': '.pdf',
        'image/png': '.png'
    }

    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise serializers.ValidationError(self._ERROR_MESSAGE)

        split_data = data.replace('data:', '', 1).split(';base64,')
        if len(split_data) != 2:
            raise serializers.ValidationError(self._ERROR_message + ' データの中に MIME Type が含まれているか確認してください.')

        mime, encoded_data = split_data
        try:
            extension = self._MIME_MAPPING[mime] if mime in self._MIME_MAPPING.keys() else mimetypes.guess_extension(
                mime)

            data = ContentFile(base64.b64decode(encoded_data),
                               name='{name}{extension}'.format(name=str(uuid.uuid4()), extension=extension))
            return super(Base64FileField, self).to_internal_value(data)

        except (ValueError, binascii.Error):
            raise serializers.ValidationError(self._ERROR_MESSAGE)

def get_field_kwargs_from_model(model, field_name):
    '''
    モデルの指定フィールドの定義をコピーする
    :param model:
    :param field_name:
    :return:
    '''

    model_field = next(filter(lambda x: x.name == field_name, model._meta.fields), None)
    if not model_field: return {}
    kwargs = get_field_kwargs(field_name, model_field)
    kwargs.pop('model_field', None)
    return kwargs

class ArticleSerializer(serializers.ModelSerializer):

    file = Base64FileField(**get_field_kwargs_from_model(Article,'file'))

    class Meta:
        model = Article
        fields = '__all__'
