from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models.signals import post_delete


class AdminMembersQuerySet(models.query.QuerySet):
    def get_queryset(self):
        return super(AdminMembersQuerySet, self).get_queryset().filter(

        )


@python_2_unicode_compatible
class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_closed = models.BooleanField(blank=True, default=False)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='Membership',
        related_name='organizations',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organization_detail', kwargs={'pk': self.pk})

    @property
    def admin_members(self):
        return self.users.filter(
            organization_membership__membership__organization=self,
            organization_membership__membership__is_admin=True,
        )

    @property
    def members(self):
        return self.users.filter(
            organization_membership__membership__isnull=False,
        )

    @property
    def total_member_shift_hours(self):
        return self.members.aggregate(
            total_shift_length=Sum('shifts__shift_length'),
        )['total_shift_length'] or 0


class MembershipRequestQuerySet(models.query.QuerySet):
    use_for_related_fields = True

    def not_confirmed(self):
        return self.filter(membership__isnull=True)


class MembershipRequest(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='organization_membership')
    organization = models.ForeignKey('Organization', related_name='organization_membership')

    objects = MembershipRequestQuerySet.as_manager()

    class Meta:
        unique_together = (
            ('user', 'organization'),
        )


class Membership(MembershipRequest):
    is_admin = models.BooleanField(default=False)


def cleanup_memberless_organizations(sender, instance, **kwargs):
    if not instance.organization.members.exists():
        instance.organization.delete()
    elif not instance.organization.admin_members.exists():
        membership = Membership.objects.filter(
            organization=instance.organization,
        ).order_by('created_at').first()
        membership.is_admin = True
        membership.save()


post_delete.connect(cleanup_memberless_organizations, sender=MembershipRequest)
