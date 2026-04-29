from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('api/log/', views.api_log_workout, name='api_log_workout'),
    path('api/history/', views.api_get_history, name='api_history'),
    path('api/edit_log/', views.api_edit_log, name='api_edit_log'),
    path('api/finish_day/', views.api_finish_day, name='api_finish_day'),
    path('api/update_schedule/', views.api_update_schedule, name='api_update_schedule'),
    path('api/upload_audio/', views.api_upload_audio, name='api_upload_audio'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)