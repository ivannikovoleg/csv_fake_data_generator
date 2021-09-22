from django.urls import path
from . import views

app_name = 'generator'
urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate, name='generate'),
    path('schemas/', views.schemas, name='schemas'),
    path('schema/<int:pk>/', views.schema_view, name='schema_view'),
    path('create/<int:pk>/', views.create_file, name='create_file'),
    path('delete/<int:pk>/', views.delete_schema, name='delete_schema'),
    path('data_set_list/<int:pk>', views.data_set_list, name='data_set_list'),
]
