from django.urls import path
from .views import AdsDetail , AdsList ,MyAdList


app_name = 'ads_api'

urlpatterns = [
    path('<int:pk>', AdsDetail.as_view(), name='detailcreate'),
    path('', AdsList.as_view(), name='listcreate'),
    path('myads/',MyAdList.as_view(), name='listmyad' ),
]
