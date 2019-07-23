"""scrumlab URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from jedzonko.views import *

urlpatterns = [
    url(r'^$', landing_page),
    url(r'^recipe/(?P<id>\d+)/$', RecipeDetails.as_view()),
    url(r'^recipe/modify/(?P<id>\d+)/$',EditRecipe.as_view()),
    url(r'^plan/add/$', RenderPlanAdd.as_view()),
    url(r'^plan/(?P<id>\d+)/$', plan_details),
    url(r'^plan/list/$', plan_list),
    url(r'^plan/list/$', plan_list),
    url(r'^plan/add/details/$', RenderPlanAddDetails.as_view()),
    # path('index/', IndexView.as_view()),
    url(r'^about/$', render_about),
    url(r'^contact/$', render_contact),
    url(r'^recipe/list/$', render_recipe_list),
    url(r'^recipe/add/$', NewRecipe.as_view()),
]
