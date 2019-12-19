"""simple_drf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authentication import SessionAuthentication
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

import articles.urls
import drf_custom_auth.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^silk/', include('silk.urls', namespace='silk')),
    path('articles/', include(articles.urls)),
]

urlpatterns.append(
    url(r'^docs/', include_docs_urls(title='API Docs',
                                     permission_classes=(AllowAny,),
                                     authentication_classes=(SessionAuthentication,)))
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# rest_auth urls
urlpatterns += [
    url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
    url(r'^rest-auth/registration/', include(drf_custom_auth.urls))
]
