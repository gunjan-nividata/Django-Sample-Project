# -*- coding: utf-8 -*-
from datetime import timedelta

# Django imports
from django.db.models import Q
from django.utils import timezone

# Third party package imports
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Project level imports
from .models import ServiceRequest, Attachment, Comment, RENEW
from .serializers import ServiceRequestSerializer, AttachmentSerializer, CommentSerializer


class ServiceRequestViewSet(ModelViewSet):
    queryset = ServiceRequest.objects.all().order_by('-created')
    serializer_class = ServiceRequestSerializer
    permission_classes = (IsAuthenticated,)
    filter_fields = ('state', 'state_type', 'first_name', 'last_name')
    # authentication_classes = (TokenAuthentication,)

    def filter_queryset(self, qs):
        year_diff = timezone.now() - timedelta(days=365)

        _state = self.request.GET.get('state')
        if _state:
            x = [i for i in _state.split(',')]
            qs = qs.filter(state__in=x)

        _is_expired = self.request.GET.get('is_expired')
        if _is_expired and not _state and int(_is_expired) == 1:
                qs = qs.filter(created__lt=year_diff).filter(~Q(state_type=RENEW))

        keyword = self.request.query_params.get("keyword")
        if keyword:
            qs = qs.filter(Q(first_name__icontains=keyword) | Q(first_name__icontains=keyword))

        return qs.order_by("-modified")


class AttachmentViewSet(ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("attachment_type", "service_request")


class CommentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
