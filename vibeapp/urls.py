from django.urls import path
from . import views

urlpatterns = [
    path('vibe/', views.peru_vibe, name='peru_vibe'),
]
