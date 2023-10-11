from django.urls import path

from .views import *

urlpatterns = [
  path('startpage/', StartPage.as_view(), name='start_page'),
  path('advert/<int:pk>/', AdvertDetail.as_view(), name='advert_detail'),
  path('advert/create/', AdvertCreate.as_view(), name='advert_create'),
  path('advert/<int:pk>/update/', AdvertUpdate.as_view(), name='advert_update'),
  path('advert/<int:pk>/delete/', AdvertDelete.as_view(), name='advert_delete'),
  path('responses/', Responses.as_view(), name='responses'),
  path('responses/<int:pk>', Responses.as_view(), name='responses'),
  path('respond/<int:pk>', Respond.as_view(), name='respond'),
  path('response/accept/<int:pk>', response_accept),
  path('response/delete/<int:pk>', response_delete),
  path('', lambda request: redirect('startpage/', permanent=False)),
    ]
