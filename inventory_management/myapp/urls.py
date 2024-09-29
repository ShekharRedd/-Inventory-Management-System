from django.urls import path
from .views import UserRegistrationView, UserLoginView, create_item, read_item, update_item, delete_item

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('items/', create_item, name='create_item'),
    path('items/<int:item_id>/', read_item, name='read_item'),
    path('items/<int:item_id>/update/', update_item, name='update_item'),
    path('items/<int:item_id>/delete/', delete_item, name='delete_item'),
]
