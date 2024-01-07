from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    
    # simple jwt
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('user_registration_api/', views.user_registration_api, name='user_registration_api'),
    path('user_login/', views.user_login, name='user_login'),
    path('view_all_contents/', views.view_all_contents, name='view_all_contents'),
    path('edit_content/', views.edit_content, name='edit_content'),
    path('delete_content/', views.delete_content, name='delete_content'),
    path('create_content/', views.create_content, name='create_content'),
    path('view_author_contents/', views.view_author_contents, name='view_author_contents'),
    path('edit_author_content/', views.edit_author_content, name='edit_author_content'),
    path('delete_author_content/', views.delete_author_content, name='delete_author_content'),
    path('search_contents/', views.search_contents, name='search_contents'),
]