"""product URL Configuration

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

from django.conf.urls import include, url
from . import views
# path('snippets/', views.SnippetList.as_view()),
# urlpattern = patterns('',
#     url(r'^$',views.index,name='index')
# )
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^new_post/$', views.new_post, name='new_post'),
    url(r'^sign-up/$', views.RegisterUsers.as_view(), name='sign-up'),
    url(r'^login/$', csrf_exempt(views.LoginView.as_view())),
    url(r'^products/$', views.ProductList.as_view()),
    url(r'^ratings/$', views.UserRatingView.as_view()),
    ]

