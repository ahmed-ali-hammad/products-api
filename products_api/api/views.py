import json

from api.models import Item
from api.serializers import (
    AcceptCodeSerializer,
    AcceptFileSerializer,
    ItemListSerializer,
    SessionCreateSerializer,
)
from api.tasks import save_session_data
from api.utils import remove_leading_zeros
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ItemViewset(GenericViewSet):
    serializer_class = ItemListSerializer
    parser_classes = [
        MultiPartParser,
        JSONParser,
    ]

    serializer_action_classes = {
        "list_products": AcceptCodeSerializer,
        "get_product": AcceptCodeSerializer,
        "import_from_feed_json": SessionCreateSerializer,
        "import_from_feed_file": AcceptFileSerializer,
    }

    def get_serializer_class(self):
        """To retrun a specific serializer based on the action"""
        try:
            return self.serializer_action_classes[self.action]
        except Exception:
            return super().get_serializer_class()

    @extend_schema(tags=["Products - Create"])
    @action(detail=False, methods=["post"], url_path="import-products-from-json")
    def import_from_feed_json(self, request):
        """This action is used to handle session data if it's sent as json str"""
        data = request.data
        # Validate the data inside the file
        content_serializer = SessionCreateSerializer(data=data)
        content_serializer.is_valid(raise_exception=True)

        # We process the data in a background task to handle the case when the payload is large and takes time
        save_session_data.delay(data)

        return Response(
            {"detail": "Session data is being stored"}, status=status.HTTP_200_OK
        )

    @extend_schema(tags=["Products - Create"])
    @action(detail=False, methods=["post"], url_path="import-products-from-file")
    def import_from_feed_file(self, request):
        """
        This endpoint accepts a JSON file and processes its contents asynchronously.
        """
        # Validate file input
        input_serializer = AcceptFileSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        file_obj = input_serializer.validated_data["product_feed"]

        if not file_obj.name.endswith(".json"):
            return Response(
                {"detail": "Please provide a JSON file"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Load file content once
            data = json.load(file_obj)
        except json.JSONDecodeError:
            return Response(
                {"detail": "Invalid JSON content in the uploaded file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate the data inside the file
        content_serializer = SessionCreateSerializer(data=data)
        content_serializer.is_valid(raise_exception=True)

        # Trigger background processing
        save_session_data.delay(data)

        return Response(
            {"detail": "Session data is being stored."},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="code",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Product code",
                required=True,
            )
        ],
        tags=["Products - Get"],
    )
    @action(detail=False, methods=["get"], url_path="get/product")
    def get_product(self, request, *args, **kwargs):
        """This action will return one item if its code is provided and return all items otherwise"""
        code = request.query_params.get("code")

        serializer = AcceptCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = remove_leading_zeros(
            str(code)
        )  # We use str in case a number is provided instead of a str

        item = (
            Item.objects.prefetch_related("lot", "related_products")
            .filter(code=code)
            .first()
        )
        if item:
            serializer = ItemListSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Message": "Item not found"})

    @extend_schema(tags=["Products - Get"])
    @action(detail=False, methods=["get"], url_path="list/products")
    def list_products(self, request):
        """List all Products"""
        items = Item.objects.prefetch_related("lot", "related_products").all()
        serializer = ItemListSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
