from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('realtime/', views.realtime_view, name='realtime'),
    path('history/', views.history_view, name='history'),
    path('settings/', views.settings_view, name='settings'),
    path('api/detection-stats/', views.get_detection_stats, name='detection_stats'),
]