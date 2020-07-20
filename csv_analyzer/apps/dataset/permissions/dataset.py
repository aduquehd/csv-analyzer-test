"""Circles permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsDataSetOwner(BasePermission):
    """Allow access only to worker image owner."""

    def has_object_permission(self, request, view, obj):
        """Verify user have a ownership in the obj."""
        try:
            return obj.owner.id == request.user.id
        except Exception:
            return False
