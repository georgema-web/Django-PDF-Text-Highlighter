
from django.conf.urls import url
from django.urls import path, include 
from . import views 


#app_name = 'segment_tool' 

urlpatterns = [
    url(r'api/image/(?P<query_pk>\d+)/$', views.ImageListCreate.as_view()),
    path('api/image/', views.ImageListCreate.as_view()),
#    path('api/image/<int:query_pk>', views.ImageListCreate.as_view()),
#    path('api/image/<pk>', views.ImageDetail.as_view()),
]



'''
urlpatterns = [
	path('upload', views.upload, name='upload'),
	path('segment', views.segment, name='segment'), 
	path('increase_kernel', views.increase_kernel, name='increase_kernel'),
	path('decrease_kernel', views.decrease_kernel, name='decrease_kernel'),
]
'''

