"""product_review URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from sentimental_analysis.views import *
# from sentimental_analysis.models import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/',home,name='home_url'),
    url(r'^hashtag-tweets/',search,name='search'),
    url(r'^login/',log_in,name='login_url'),
    url(r'^signup/',sign_up,name='signup_url'),
    url(r'^logout/', signout, name='logout_url'),
    url(r'^product/', product, name='product_url'),
    url(r'^single/(?P<id>\d+)/$', single, name='single_url'),

    url(r'^analysis-tweets/',senti,name='Analyser_url'),

]
urlpatterns += url(r'^$', home),
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
