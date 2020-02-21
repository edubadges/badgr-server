import cachemodel
from itertools import chain
from django.db import models
from django.forms.models import model_to_dict


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


class PermissionedNodeMixin(models.Model):
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

    def permissions_to_dict(self):
        return model_to_dict(self, fields = ['create', 'read', 'update',
                                            'destroy', 'award', 'administrate_users'])


class InstitutionStaff(PermissionedNodeMixin, cachemodel.CacheModel):
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


class FacultyStaff(PermissionedNodeMixin, cachemodel.CacheModel):
    """
    Many2Many realtionship between Faculty and users, with permissions added to the relationship
    """
    faculty = models.ForeignKey('institution.Faculty', on_delete=models.CASCADE)

    @property
    def object(self):
        return self.faculty

# TODO: Perms: do this one after the others as it replaces the other issuerstaff
# class IssuerStaff(PermissionedNodeMixin, cachemodel.CacheModel):
#     """
#     Many2Many realtionship between Issuer and users, with permissions added to the relationship
#     """
#     issuer = models.ForeignKey('issuer.Issuer', on_delete=models.CASCADE)
#
#     @property
#     def object(self):
#         return self.issuer


class BadgeClassStaff(PermissionedNodeMixin, cachemodel.CacheModel):

    badgeclass = models.ForeignKey('issuer.BadgeClass', on_delete=models.CASCADE)

    @property
    def object(self):
        return self.badgeclass
