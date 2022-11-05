
import json

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.models import Item
from api.serializers import (AcceptCodeSerializer, AcceptFileSerializer,
                             ItemListSerializer, LotCreateSerializer)

from api.tasks import save_session_data
from api.utils import remove_leading_zeros


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
        """ This action is use to handle session data if it's sent as json str"""
        # We save the data in a background task to handle the case when the payload is large and takes time
        save_session_data.delay(request.data)

        return Response({'detail': 'Session data is being saved'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def create_from_feed_file(self, request, *args, **kwargs):
        """ This action is use to handle session data if it's sent as json file"""

        file_obj = request.data['file']

        # We save the data in a background task to handle the case when the payload is large and takes time
        save_session_data.delay(json.load(file_obj))

        return Response({'detail': 'Session data is being saved'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def list_products(self, request, *args, **kwargs):
        if request.data.get('code', None):
            code = remove_leading_zeros(request.data['code'])
            serializer = ItemListSerializer(Item.objects.filter(code=code).first())
            return Response(serializer.data)
        else:
            serializer = ItemListSerializer(Item.objects.all(), many=True)
            return Response(serializer.data)
