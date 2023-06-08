from django.urls import path
from .views import home, profile, RegisterView, ImagePredictionView, ImagePredictionCreate, ImagePredictionUpdate, ImagePredictionDelete

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('prediction/', ImagePredictionView.as_view(), name='image_prediction_all'),
    path('prediction/create/', ImagePredictionCreate.as_view(), name='image_prediction_create'),
    path('prediction/<int:pk>/update/', ImagePredictionUpdate.as_view(), name='image_prediction_update'),
    path('prediction/<int:pk>/delete/', ImagePredictionDelete.as_view(), name='image_prediction_delete'),
]
