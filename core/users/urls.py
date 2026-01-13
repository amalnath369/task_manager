from django.urls import path
from .views import (
    CustomLoginView, LogoutView, 
    UserListCreateView, UserDetailView, AdminUserListView,
    login_view, logout_view
)

urlpatterns = [
    # Web interface URLs
    path('login/', login_view, name='user-login'),
    path('logout/', logout_view, name='user-logout'),

        # API URLs
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('admins/', AdminUserListView.as_view(), name='admin-list'),
    path('api-login/', CustomLoginView.as_view(), name='api-login'),
    path('api-logout/', LogoutView.as_view(), name='api-logout'),

]