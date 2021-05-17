from django.urls import path
from .views import CustomUserCreate, MeUserDetails

app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('me/', MeUserDetails.as_view(), name='me_user'),
]