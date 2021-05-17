
from django.urls import path
# from django.urls.conf import include

from django.views.generic import TemplateView
from . import views 
app_name= 'ads'

urlpatterns = [
    path('', TemplateView.as_view(template_name="ads/index.html")),
    path('secret/', views.index, name='sec' )

]



