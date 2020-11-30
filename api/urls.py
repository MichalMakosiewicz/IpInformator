from django.urls import path
from .views import InformationViewSet, UserCreate

urlpatterns = [
    path('account/register/', UserCreate.as_view()),
    path('info/', InformationViewSet.as_view()),
    path('info/<int:inf_id>/', InformationViewSet.as_view()),

]
