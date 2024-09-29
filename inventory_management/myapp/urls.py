from django.urls import path
from . import views
from .views import protected_view

urlpatterns = [
    path('get_items/', views.get_items, name='get_items'),
    path('post_items/', views.post_items, name='post_items'),
    path('put_items/', views.put_items, name='put_items'),
    path('delete_items/', views.delete_items, name='delete_items'),
    path('', views.home_page, name='home_page'),
    path('api/protected/', protected_view, name='protected_view'),
    
]


