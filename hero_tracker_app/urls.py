from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('my_heroes',views.my_heroes),
    path('new_database',views.new_database),
    path('log_in_page',views.log_in_page),
    path('registration_page',views.registration_page),
    path('log_in',views.log_in),
    path('register',views.register),
    path('log_out',views.log_out),
    path('stats_page',views.view_stats),
    path('all_heroes',views.all_heroes),
    # path('main/blog', views.blog),
    # path('main/<int:var1>/<str:title_name>', views.example1),	   
]