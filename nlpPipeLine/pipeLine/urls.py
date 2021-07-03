from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.pipe_view, name='pipeView'),
    # path('', views.FunctionListView.as_view(), name='functions'),
]
