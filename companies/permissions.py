from rest_framework.permissions import BasePermission

from .models import Company


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        # getattr guard: an AnonymousUser (no token) has no `.company`,
        # so this stays safe even without IsAuthenticated in front of it.
        company = getattr(request.user, "company", None)
        return company is not None and company.role == Company.Role.ADMIN
