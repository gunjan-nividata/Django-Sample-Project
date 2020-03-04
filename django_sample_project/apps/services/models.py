import logging
from datetime import timedelta

# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _, get_language
from django.utils import timezone

# Third party package imports
from django_fsm import FSMField, transition
from django_fsm_log.decorators import fsm_log_by
from model_utils.models import TimeStampedModel

# Project level imports
from apps.users.models import User

NEW, APPROVED, REJECTED, RENEW = range(4)

PASSPORT, POLICE, CV, PHOTO, EDU, ADDITIONAL = range(6)

logger = logging.getLogger('api')


def get_tuple_name_by_id(tuple, id=0):
    if id is not None:
        for item in tuple:
            if item[0] == int(id):
                return item[1]
    return _("Unknown")


REQUEST_STATES = (
    (NEW, _('New')),
    (APPROVED, _('Approved')),
    (REJECTED, _('Rejected')),
    (RENEW, _('Rejected')),
)

FILE_TYPES = (
    (PASSPORT, _('Passport')),
    (POLICE, _('Police Clearance Certificate')),
    (CV, _('CV')),
    (PHOTO, _('Colored Personal Photo')),
    (EDU, _('Copy of Educational Certificates')),
    (ADDITIONAL, _('Additional')),
)


def get_file_type_name(type_id):
    return get_tuple_name_by_id(FILE_TYPES, type_id)


class ServiceRequest(TimeStampedModel):
    first_name = models.CharField(_('First Name'), max_length=255)
    last_name = models.CharField(_('Last Name'), max_length=255)
    nationality = models.CharField(_('Nationality'), max_length=255)
    email = models.EmailField(_('Email address'), max_length=255, unique=True)
    mobile = models.CharField(_('Mobile No.'), max_length=255)
    address = models.CharField(_('Address'), max_length=500)
    passport_number = models.CharField(_('Passport NUmber'), max_length=255)
    comment = models.TextField(_('comment'), max_length=500, null=True, blank=True)
    state = FSMField(default=NEW, verbose_name=_('state'))
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='service_requests')

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def state_int(self):
        return int(self.state)

    @property
    def state_type_int(self):
        return int(self.state_type)

    @property
    def is_new(self):
        if self.state_int == NEW:
            return True
        else:
            return False

    @property
    def is_expired(self):
        return (self.created < timezone.now() - timedelta(days=365)) and self.state_type_int != RENEW

    @property
    def display_state(self):
        if self.is_expired:
            return _('Expired')

        if self.state_int in [NEW]:
            return _('Pending')

        if self.state_int in [APPROVED]:
            return _('Approved')
        else:
            return get_tuple_name_by_id(REQUEST_STATES, self.state)

    @fsm_log_by
    @transition(field=state, source=str(NEW), target=str(APPROVED))
    def dm_submit(self):
        to_emails = []
        to_emails += self._admin_emails()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @staticmethod
    def _admin_emails():
        return User.objects.filter(is_superuser=True)

    def can_write(self, user):
        if user.is_superuser or self.user.pk == user.pk:
            return True


class Attachment(TimeStampedModel):
    file = models.FileField(_('File'), upload_to='service_attachments/')
    service_request = models.ForeignKey('ServiceRequest',
                                        verbose_name=_('Service Request'),
                                        related_name='attachments', null=True, blank=True, on_delete=models.SET_NULL)
    attachment_type = models.PositiveSmallIntegerField(_('Type'), choices=FILE_TYPES, default=0)
    user = models.ForeignKey('users.User', verbose_name=_('By'), related_name='attachments',
                             on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(get_file_type_name(self.attachment_type), self.service_request)

    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')


class Comment(TimeStampedModel):
    by = models.ForeignKey('users.User', related_name='service_comments', verbose_name=_('By'), default=None, null=True,
                           on_delete=models.SET_NULL)
    service_request = models.ForeignKey('ServiceRequest', related_name='comments', verbose_name=_('Service Request'),
                                        on_delete=models.CASCADE)
    text = models.TextField(_('Comment'), null=True, blank=True)

    def __str__(self):
        return f'{ self.by.name } - { self.service_request }'
