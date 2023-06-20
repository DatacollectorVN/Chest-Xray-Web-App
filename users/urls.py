from django.urls import path
from .views import HomeView, ProfileView, RegisterView, ImagePredictionView, ImagePredictionCreate, ImagePredictionUpdate, ImagePredictionDelete, ImagePredictionSubmitSuccess, test, news_1, news_2, news_3

urlpatterns = [
    path('', HomeView.as_view(), name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', ProfileView.as_view(), name='users-profile'),
    path('prediction/', ImagePredictionView.as_view(), name='image_prediction_all'),
    path('prediction/create/', ImagePredictionCreate.as_view(), name='image_prediction_create'),
    path('prediction/<int:pk>/update/', ImagePredictionUpdate.as_view(), name='image_prediction_update'),
    path('prediction/<int:pk>/delete/', ImagePredictionDelete.as_view(), name='image_prediction_delete'),
    path('prediction/submit_success/', ImagePredictionSubmitSuccess.as_view() , name='image_prediction_submit_success'),
    path('test/', test, name='test'),
    path('news_1/', news_1, name='news_1'),
    path('news_2/', news_2, name='news_2'),
    path('news_3/', news_3, name='news_3'),
]
