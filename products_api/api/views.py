
import json

from api.models import Item
from api.serializers import (AcceptCodeSerializer, AcceptFileSerializer,
                             ItemListSerializer, SessionCreateSerializer)
from api.tasks import save_session_data
from api.utils import remove_leading_zeros
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ItemViewset(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = ItemListSerializer
    parser_classes = [MultiPartParser, JSONParser]  # MultiPartParser is used to handle the file upload

    serializer_action_classes = {
        'list_products': AcceptCodeSerializer,
        'create': SessionCreateSerializer,
        'create_from_feed_file': AcceptFileSerializer
    }

    def get_serializer_class(self):
        """ To retrun a specific serializer based on the action"""
        try:
            return self.serializer_action_classes[self.action]
        except Exception:
            return super().get_serializer_class()

    def get_queryset(self):
        return Item.objects.prefetch_related('lot', 'related_products').all()

    def create(self, request, *args, **kwargs):
        """ This action is used to handle session data if it's sent as json str"""
        # We process the data in a background task to handle the case when the payload is large and takes time
        save_session_data.delay(request.data)

        return Response({'detail': 'Session data is being stored'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def create_from_feed_file(self, request, *args, **kwargs):
        """ This action is used to handle session data if it's sent as json file"""

        file_obj = request.data['file']

        # We process the data in a background task to handle the case when the payload is large and takes time
        save_session_data.delay(json.load(file_obj))

        return Response({'detail': 'Session data is being stored'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def list_products(self, request, *args, **kwargs):
        """This action will return one item if its code is provided and return all items otherwise"""
        if request.data.get('code', None):
            code = remove_leading_zeros(request.data['code'])

            item = Item.objects.prefetch_related('lot', 'related_products').filter(code=code).first()
            if item:
                serializer = ItemListSerializer(item)
                return Response(serializer.data, status=status.HTTP_200_OK)

        # in case no code is provided or the code is incorrect we return all the items
        items = Item.objects.prefetch_related('lot', 'related_products').all()
        serializer = ItemListSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
