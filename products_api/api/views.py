
import json

from api.models import Item
from api.serializers import ItemSerializer, LotSerializer
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ItemViewset(GenericViewSet, mixins.CreateModelMixin):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        file_obj = request.data['file']
        data = json.load(file_obj)
        serializer = LotSerializer(data=data['amounts'], many=True)
        print(serializer.is_valid())
        print(serializer.errors)
        serializer.save()
        return Response({'detail': 'recieved the file'})
