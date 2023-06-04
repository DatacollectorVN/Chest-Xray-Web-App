from django.urls import path
from .views import home, profile, RegisterView, ConditionPredictionView, ConditionPredictionCreate, ConditionPredictionUpdate, ConditionPredictionDelete

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('prediction/', ConditionPredictionView.as_view(), name='condition_prediction_all'),
    path('prediction/create/', ConditionPredictionCreate.as_view(), name='condition_prediction_create'),
    path('prediction/<int:pk>/update/', ConditionPredictionUpdate.as_view(), name='condition_prediction_update'),
    path('prediction/<int:pk>/delete/', ConditionPredictionDelete.as_view(), name='condition_prediction_delete'),
]
