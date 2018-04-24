from django.urls import path,include

from . import views

urlpatterns = [
    path('insert-data', views.insert_data),
    path('non-pir', views.non_pir),
    path(r'', views.calculate_pir),
]
