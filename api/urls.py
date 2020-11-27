from django.urls import path
from .views import InformationViewSet, UserCreate, LanguageViewSet, LocationViewSet

urlpatterns = [
    path('account/register/', UserCreate.as_view()),
    path('info/', InformationViewSet.as_view()),
    path('info/<int:inf_id>/', InformationViewSet.as_view()),
    path('language/', LanguageViewSet.as_view()),
    path('language/<str:lang_id>/', LanguageViewSet.as_view()),
    path('location/', LocationViewSet.as_view()),
    path('loctaion/<int:loc_id>/', LocationViewSet.as_view()),
]
