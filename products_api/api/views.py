
import json

from api.models import Item
from api.serializers import (AcceptCodeSerializer, AcceptFileSerializer,
                             ItemListSerializer, LotCreateSerializer,
                             SessionCreateSerializer)
from api.utils import remove_leading_zeros
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ItemViewset(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = AcceptFileSerializer
    parser_classes = [MultiPartParser, JSONParser]

    serializer_action_classes = {
        'create': LotCreateSerializer,
        'list_products': AcceptCodeSerializer,
        'create_from_feed_file': AcceptFileSerializer
    }

    def get_serializer_class(self):
        """ To retrun a specific serializer based on the action"""
        try:
            return self.serializer_action_classes[self.action]
        except Exception:
            return super().get_serializer_class()

    def get_queryset(self):
        Item.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = LotCreateSerializer(data=request.data['amounts'], many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'detail': 'recieved the file'})

    # @action(detail=False, methods=['post'])
    # def create_from_feed_file(self, request, *args, **kwargs):
    #     file_obj = request.data['file']
    #     data = json.load(file_obj)
    #     serializer = LotCreateSerializer(data=data['amounts'], many=True)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #     return Response({'detail': 'recieved the file'})

    @action(detail=False, methods=['post'])
    def create_from_feed_file(self, request, *args, **kwargs):
        file_obj = request.data['file']
        data = json.load(file_obj)
        serializer = SessionCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'detail': 'recieved the file'})

    @action(detail=False, methods=['post'])
    def list_products(self, request, *args, **kwargs):
        if request.data.get('code', None):
            code = remove_leading_zeros(request.data['code'])
            serializer = ItemListSerializer(Item.objects.filter(code=code).first())
            return Response(serializer.data)
        else:
            serializer = ItemListSerializer(Item.objects.all(), many=True)
            return Response(serializer.data)
