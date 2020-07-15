from django.urls import path 
from . import views 


urlpatterns = [
    path('(?P<query_pk>\d+)/$', views.index), 
    path('', views.index), 
]

#   url(r'api/image/(?P<query_pk>\d+)/$', views.ImageListCreate.as_view()),
