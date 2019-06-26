import uuid

import inflection
from django.db import models

from accounts.models import User
import mimetypes
from os.path import splitext

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class FileValidator(object):
    """
    ModelのFileField, ImageField用のvalidator. これらのコンストラクタの ``validator`` 引数に指定してください.

    Examples:
        usage::

            MyModel(models.Model):
                myfile = FileField(validators=FileValidator(max_bytes=24*1024*1024), ...)
    """

    _extension_message = _("Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'")
    _mime_message = _("MIME type '%(mimetype)s' is not valid. Allowed types are: %(allowed_mimetypes)s.")
    _min_bytes_message = _('The current file %(size)s, which is too small. The minumum file size is %(allowed_size)s.')
    _max_bytes_message = _('The current file %(size)s, which is too large. The maximum file size is %(allowed_size)s.')

    def __init__(self,
                 max_bytes=None,
                 min_bytes=0,
                 allowed_mimetypes=None,
                 allowed_extensions=None, *args, **kwargs):
        """

        Args:
            max_bytes: 最小ファイルサイズ(bytes)
            min_bytes: 最大ファイルサイズ(bytes)
            allowed_mimetypes: 許可するmimetypeリスト ie. ('txt', 'doc')
            allowed_extensions: 許可する拡張子リスト ie. ('image/png', )
            *args:
            **kwargs:
        """
        self.allowed_extensions = allowed_extensions
        self.allowed_mimetypes = allowed_mimetypes
        self.min_bytes = min_bytes
        self.max_bytes = max_bytes

    def __call__(self, value):
        """
        Check the extension, content type and file size.
        """

        # Check the extension
        ext = splitext(value.name)[1][1:].lower()
        if self.allowed_extensions and ext not in self.allowed_extensions:
            message = self._extension_message % {
                'extension': ext,
                'allowed_extensions': ', '.join(self.allowed_extensions)
            }

            raise ValidationError(message)

        # Check the content type
        mimetype = mimetypes.guess_type(value.name)[0]
        if self.allowed_mimetypes and mimetype not in self.allowed_mimetypes:
            message = self._mime_message % {
                'mimetype': mimetype,
                'allowed_mimetypes': ', '.join(self.allowed_mimetypes)
            }

            raise ValidationError(message)

        # Check the file size
        filesize = len(value)
        if self.max_bytes and filesize > self.max_bytes:
            message = self._max_bytes_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.max_bytes)
            }

            raise ValidationError(message)

        elif filesize < self.min_bytes:
            message = self._min_bytes_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.min_bytes)
            }

            raise ValidationError(message)

    def __eq__(self, other):
        """
        validation内容を比較

        Args:
            other: FileValidator

        Returns:
            bool: 比較結果
        """

        def compare_list(self_list, other_list):
            _self = set(self_list) if self_list else set()
            _other = set(other_list) if other_list else set()
            return _self == _other

        return (compare_list(self.allowed_extensions, other.allowed_extensions) and
                compare_list(self.allowed_mimetypes, other.allowed_mimetypes) and
                self.min_bytes == other.min_bytes and
                self.max_bytes == other.max_bytes)


@deconstructible
class MyCharValidator(object):
    def __call__(self, value):
        """
        Check the extension, content type and file size.
        """

        # Check the extension
        if not value:
            return
        if len(value) > 0:
            raise ValidationError('spam')

    def __eq__(self, other):
        """
        validation内容を比較

        Args:
            other: FileValidator

        Returns:
            bool: 比較結果
        """

        def compare_list(self_list, other_list):
            _self = set(self_list) if self_list else set()
            _other = set(other_list) if other_list else set()
            return _self == _other

        return (compare_list(self.allowed_extensions, other.allowed_extensions) and
                compare_list(self.allowed_mimetypes, other.allowed_mimetypes) and
                self.min_bytes == other.min_bytes and
                self.max_bytes == other.max_bytes)


def upload_to_uuid4_name(instance, filename):
    """
    uuid4をファイル名としたアップロード先を取得する関数

    モデルの FileFieldやImageFieldのupload_toに指定してください.

    Examples:
        usages::

            class LiquorImage(BaseModel):
                # ImageField の upload_to に指定する


    """
    extension = filename.split('.')[-1]

    _uuid = str(uuid.uuid4()).replace('-', '_')
    return '{}/{}/{}.{}'.format(instance._meta.app_label,
                                inflection.underscore(instance.__class__.__name__),
                                _uuid,
                                extension)


class Tag(models.Model):
    name = models.CharField('タグ名', max_length=120)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Article(models.Model):
    '''
    記事
    '''

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='記事の作者')
    title = models.CharField('タイトル', max_length=120, validators=[MyCharValidator()],
                             default='no title')
    body = models.TextField('本文')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name='タグ', help_text='記事につけるタグ')

    file = models.FileField('file', null=True, blank=True, upload_to=upload_to_uuid4_name,
                            validators=[
                                FileValidator(max_bytes=3, allowed_extensions=('pdf', 'jpeg', 'jpg', 'png'))],
                            help_text='アップロード可能な最大ファイルサイズは3Bです. '
                                      '拡張子は次のいずれかが使用できます {"pdf", "jpeg", "jpg", "png"}.',
                            )

    def __str__(self):
        return f'{self.id} - {self.title}'


class Meta:
    ordering = ['-created_at']
