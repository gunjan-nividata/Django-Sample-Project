# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from os.path import basename

# Django imports
from django.contrib.auth import get_user_model

# Third party package imports
from django_fsm_log.models import StateLog
from rest_framework import serializers

# Project level imports
from .models import ServiceRequest, Comment, Attachment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    by = UserSerializer(read_only=True)
    author = serializers.IntegerField(write_only=True)
    file_name = serializers.SerializerMethodField()

    @staticmethod
    def get_file_name(obj):
        return basename(obj.file.name)

    def create(self, validated_data):
        # remap input user
        author = validated_data.pop('author', None)
        instance = super(CommentSerializer, self).create(validated_data)
        instance.by_id = author
        instance.save()
        return instance

    class Meta:
        model = Comment
        fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    type_name = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()

    def get_file_name(self, obj):
        return basename(obj.file.name)

    def get_type_name(self, obj):
        from .models import get_file_type_name
        return get_file_type_name(obj.attachment_type)

    class Meta:
        model = Attachment
        fields = ['id', 'file', 'service_request', 'attachment_type', 'type_name', 'user', 'file_name']


class ServiceRequestSerializer(serializers.ModelSerializer):
    last_state_change = serializers.SerializerMethodField()
    number_of_requests = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    action = serializers.CharField(read_only=True)
    write_status = serializers.SerializerMethodField(read_only=True)

    def get_state_name(self, obj):
        return obj.display_state

    def get_last_state_change(self, obj):
        q = StateLog.objects.filter(
            object_id=obj.id).order_by('-timestamp').first()
        if q:
            return q.timestamp
        return None

    def get_number_of_requests(self, obj):
        return self.context['request'].data

    def _request_data(self):
        return self.context.get("request").data

    def _request_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user

    def get_write_status(self, obj):
        return obj.can_write(user=self._request_user())

    class Meta:
        model = ServiceRequest
        fields = ('id', 'first_name', 'last_name', 'nationality', 'email', 'mobile', 'address', 'passport_number',
                  'attachments', 'comment', 'number_of_requests',
                  'state', 'state_int', 'is_new', 'is_expired', 'user', 'created', 'modified', 'last_state_change',
                  'comments', 'action', 'write_status')

