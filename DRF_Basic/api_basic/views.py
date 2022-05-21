from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class GenericAPIView(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'
    authentication_classes = [SessionAuthentication, BaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, pk):
        return self.destroy(request, id)


class ArticleAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        artice_serilizers = ArticleSerializer(articles, many=True)  # many=True used for query sets
        return Response(artice_serilizers.data)

    def post(self, request):
        artice_serilizers = ArticleSerializer(data=request.data)
        if artice_serilizers.is_valid():
            artice_serilizers.save()
            return Response(artice_serilizers.data, status=status.HTTP_201_CREATED)
        return Response(artice_serilizers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# @api_view(['GET', 'POST']) #function based
# def aritcle_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         artice_serilizers = ArticleSerializer(articles, many=True)  # many=True used for query sets
#         return Response(artice_serilizers.data)  # if safe = false any object can be passed for serialization; otherwise only dict instances are allowed.
#
#     elif request.method == 'POST':
#         artice_serilizers = ArticleSerializer(data=request.data)
#
#         if artice_serilizers.is_valid():
#             artice_serilizers.save()
#             return Response(artice_serilizers.data, status=status.HTTP_201_CREATED)
#
#         else:
#             return Response(artice_serilizers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class ArticleDetails(APIView):
    def get_object(self, pk):
        try:
            article = Article.objects.get(pk=pk)
            return article
        except Article.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        article = self.get_object(pk)
        article_serializers = ArticleSerializer(article)
        return Response(article_serializers.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        article_serializers = ArticleSerializer(article, data=request.data, partial=True)

        if article_serializers.is_valid():
            article_serializers.save()
        else:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PUT', 'DELETE'])
# def article_details(request, pk):
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'GET':
#         article_serilizers = ArticleSerializer(article)
#         return Response(article_serilizers.data)
#
#     elif request.method == 'PUT':
#         artice_serilizers = ArticleSerializer(article, data=request.data, partial=True)
#         if artice_serilizers.is_valid():
#             artice_serilizers.save()
#             return Response(artice_serilizers.data)
#
#         else:
#             return Response(artice_serilizers.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         article.delete()
#         # print(f"Instances with {pk} Deleted")
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
