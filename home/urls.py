from .views import *

from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('webhook/',whatsapp_hook_receiver_view,name='whatsapp_webhook'),
    path('templates/', templatelist, name='templatelist'),
    path('templates/<int:pk>/', templatelist, name='templatelist'),
    path('sendtemplate/', sendtemplate, name='sendtemplate'),

]
