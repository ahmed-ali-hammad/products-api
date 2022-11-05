
import json

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.models import Item
from api.serializers import (AcceptCodeSerializer, AcceptFileSerializer,
                             ItemListSerializer, LotCreateSerializer)
from api.utils import remove_leading_zeros


class ItemViewset(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = AcceptFileSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def get_queryset(self):
        Item.objects.all()

    def create(self, request, *args, **kwargs):
        file_obj = request.data['file']
        data = json.load(file_obj)
        serializer = LotCreateSerializer(data=data['amounts'], many=True)
        print(serializer.is_valid())
        print(serializer.errors)
        serializer.save()
        return Response({'detail': 'recieved the file'})

    @action(detail=False, methods=['post'], serializer_class=AcceptCodeSerializer)
    def list_products(self, request, *args, **kwargs):
        if request.data.get('code', None):
            code = remove_leading_zeros(request.data['code'])
            serializer = ItemListSerializer(Item.objects.filter(code=code).first())
            return Response(serializer.data)
        else:
            serializer = ItemListSerializer(Item.objects.all(), many=True)
            return Response(serializer.data)
