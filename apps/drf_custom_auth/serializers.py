from rest_auth.serializers import PasswordResetSerializer


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        email_context = {
            'front_password_reset_url': 'http://localhost:3000/rest_password/'
        }
        # 本文のテンプレートパスと email の追加コンテキストを返す
        return {
            'email_template_name': 'drf_custom_auth/password_reset_body.txt',
            'extra_email_context': email_context,
        }
