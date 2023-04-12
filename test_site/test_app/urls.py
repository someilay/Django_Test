from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),
    path('menu/<int:menu_id>/', views.menu_view),
    path('menu/<int:menu_id>/<int:entry_id>', views.entry_view),
]
