from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import ServiceRequestViewSet, AttachmentViewSet, CommentViewSet

router = DefaultRouter(trailing_slash=False)
router.register("service-request", ServiceRequestViewSet, basename="service_request")
router.register("attachment", AttachmentViewSet, basename="service_attachment")
router.register("comment", CommentViewSet, basename="comment")

urlpatterns = router.urls