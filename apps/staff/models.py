import cachemodel
from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict
from signing.models import SymmetricKey


class PermissionedModelMixin(object):
    """
    Abstract class used for inheritance by all the Models (Badgeclass, Issuer, Faculty & Institution that have a related
    Staff model. Used for retrieving permissions and staff members.
    """

    def _get_local_permissions(self, user):
        permissions = {}
        staff = self.get_staff_member(user)
        if staff:
            return staff.permissions
        else:
            return None

    def get_permissions(self, user):
        try:
            parent_perms = self.parent.get_permissions(user)
            local_perms = self._get_local_permissions(user)
            if not parent_perms:
                return local_perms
            elif not local_perms:
                return parent_perms
            else:
                combined_perms = {}
                for key in local_perms:
                    combined_perms[key] = local_perms[key] if local_perms[key] > parent_perms[key] else parent_perms[key]
                return combined_perms
        except AttributeError:  # recursive base case
            return self._get_local_permissions(user)

    @property
    def staff_items(self):
        return self.cached_staff

    def get_staff_member(self, user):
        for staff in self.staff_items:
            if staff.user == user:
                return staff


class PermissionedRelationshipMixin(models.Model):
    """
    Abstract base class used for inheritance in all the Staff Many2Many relationship models
    """

    user = models.ForeignKey('badgeuser.BadgeUser', on_delete=models.CASCADE)
    create = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    destroy = models.BooleanField(default=False)
    award = models.BooleanField(default=False)
    sign = models.BooleanField(default=False)
    administrate_users = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def permissions(self):
        return model_to_dict(self, fields = ['create', 'read', 'update',
                                            'destroy', 'award', 'administrate_users'])


class InstitutionStaff(PermissionedRelationshipMixin, cachemodel.CacheModel):
    """
    Many2Many realtionship between Institution and users, with permissions added to the relationship
    """
    institution = models.ForeignKey('institution.Institution', on_delete=models.CASCADE)

    class Meta:
        # For now only one institution per user
        constraints = [
            models.UniqueConstraint(fields=['user', 'institution'], name='unique_institution_staff_membership')
        ]

    @property
    def object(self):
        return self.institution


class FacultyStaff(PermissionedRelationshipMixin, cachemodel.CacheModel):
    """
    Many2Many realtionship between Faculty and users, with permissions added to the relationship
    """
    faculty = models.ForeignKey('institution.Faculty', on_delete=models.CASCADE)

    @property
    def object(self):
        return self.faculty


class IssuerStaff(PermissionedRelationshipMixin, cachemodel.CacheModel):
    """
    Many2Many realtionship between Issuer and users, with permissions added to the relationship
    """

    # ROLE_OWNER = 'owner'
    # ROLE_EDITOR = 'editor'
    # ROLE_STAFF = 'staff'
    # ROLE_CHOICES = (
    #     (ROLE_OWNER, 'Owner'),
    #     (ROLE_EDITOR, 'Editor'),
    #     (ROLE_STAFF, 'Staff'),
    # )
    issuer = models.ForeignKey('issuer.Issuer', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # role = models.CharField(max_length=254, choices=ROLE_CHOICES, default=ROLE_STAFF)
    # is_signer = models.BooleanField(default=False)

    @property
    def object(self):
        return self.issuer

    class Meta:
        unique_together = ('issuer', 'user')

    def publish(self):
        super(IssuerStaff, self).publish()
        self.issuer.publish()
        self.user.publish()

    def delete(self, *args, **kwargs):
        publish_issuer = kwargs.pop('publish_issuer', True)
        super(IssuerStaff, self).delete()
        if publish_issuer:
            self.issuer.publish()
        self.user.publish()

    @property
    def may_become_signer(self):
        return self.user.may_sign_assertions and SymmetricKey.objects.filter(user=self.user, current=True).exists()

    @property
    def is_signer(self):
        return self.sign

    @property
    def cached_user(self):
        from badgeuser.models import BadgeUser
        return BadgeUser.cached.get(pk=self.user_id)

    @property
    def cached_issuer(self):
        from issuer.models import Issuer
        return Issuer.cached.get(pk=self.issuer_id)


class BadgeClassStaff(PermissionedRelationshipMixin, cachemodel.CacheModel):

    badgeclass = models.ForeignKey('issuer.BadgeClass', on_delete=models.CASCADE)

    @property
    def object(self):
        return self.badgeclass
