from django.urls import path

from .views import login, info, success

urlpatterns = [
    path('', login, name='login'),
    path('info/', info, name='info'),
    path('success/', success, name='success'),
]
