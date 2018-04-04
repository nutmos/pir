from django.urls import path,include

from . import views

urlpatterns = [
    path('insert-data', views.insert_data),
    path(r'', views.calculate_pir),
]
