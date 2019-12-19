import urllib.parse

from allauth.account.models import EmailConfirmationHMAC
from allauth.account.views import ConfirmEmailView
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from rest_auth.registration.serializers import VerifyEmailSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class CustomConfirmEmailView(APIView, ConfirmEmailView):
    """
    ユーザー登録の email verification.

    email 認証後, Front サーバーにリダイレクトします.
    このとき認証結果をクエリパラメータにセットします.

    `<リダイレクト先URL>?detail=<認証結果詳細>&status=<ステータスコード>`

    ### ステータスコード
    + 200: 認証成功
    + 400: 認証用データの不備
    + その他: その他のエラー

    """
    permission_classes = (AllowAny,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def get_optional_params(self, confirmation: EmailConfirmationHMAC):
        return {}

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        try:
            serializer.is_valid(raise_exception=True)
            self.kwargs['key'] = serializer.validated_data['key']
            confirmation = self.get_object()
            confirmation.confirm(self.request)
            params = {'detail': _('ok'), 'status': status.HTTP_200_OK}
            params.update(self.get_optional_params(confirmation))

        except ValidationError as e:
            params = {'detail': _('Invalid input.'), 'status': e.status_code}
        except Http404:
            params = {'detail': _('Invalid input.'), 'status': status.HTTP_404_NOT_FOUND}

        # Front サーバーへリダイレクト.
        url = 'http://localhost:3000/complete_sign_up'
        # クエリパラメータに認証結果を付与
        url = '{}?{}'.format(url, urllib.parse.urlencode(params))
        return HttpResponseRedirect(redirect_to=url)
