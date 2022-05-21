from django.urls import path
from .views import ArticleAPIView, ArticleDetails, GenericAPIView


urlpatterns = [
    # path('article/', aritcle_list),
    path('article/', ArticleAPIView.as_view()),
    path('article_generic/<int:id>/', GenericAPIView.as_view()),
    path('article/<int:pk>/', ArticleDetails.as_view()),
    # path('article/<int:pk>/', article_details),
]
