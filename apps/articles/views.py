from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from articles.serializers import TagSerializer, CategorySerializer, ArticleSerializer
from articles.models import Tag, Category, Article


class TagAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Tag.objects.get(pk=id)
            serializer = TagSerializer(item)
            return Response(serializer.data)
        except Tag.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Tag.objects.get(pk=id)
        except Tag.DoesNotExist:
            return Response(status=404)
        serializer = TagSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Tag.objects.get(pk=id)
        except Tag.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class TagAPIListView(APIView):

    def get(self, request, format=None):
        items = Tag.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = TagSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CategoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Category.objects.get(pk=id)
            serializer = CategorySerializer(item)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return Response(status=404)
        serializer = CategorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class CategoryAPIListView(APIView):

    def get(self, request, format=None):
        items = Category.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CategorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ArticleAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Article.objects.get(pk=id)
            serializer = ArticleSerializer(item)
            return Response(serializer.data)
        except Article.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return Response(status=404)
        serializer = ArticleSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ArticleAPIListView(APIView):

    def get(self, request, format=None):
        items = Article.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = ArticleSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
