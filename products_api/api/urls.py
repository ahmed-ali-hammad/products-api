from api.views import ItemViewset
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register("items", ItemViewset, basename="items")

urlpatterns = [
    path("", include(router.urls)),
]
