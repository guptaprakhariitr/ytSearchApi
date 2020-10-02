
from django.urls import path
from . import views
urlpatterns = [
    path('', views.YTListView.as_view(),name='home'),    
    path('getVideo/', views.VidAPIView.as_view(),name='getVid'),    
]
