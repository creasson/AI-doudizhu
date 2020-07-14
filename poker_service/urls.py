"""poker_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import os, sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

from django.conf.urls import url
import view_card_predict
from django.shortcuts import render

def example(request):
    return render(request, 'example.html', None)

urlpatterns = [
    url(r'^example$', example),
    url(r'^out_card_predict$', view_card_predict.out_card_predict),
]