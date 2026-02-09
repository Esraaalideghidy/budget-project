from rest_framework.permissions import BasePermission
from .models import User
class IsRiskTeqniaMember(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        role= user.role
        if role == User.RISK_TEQNIA_MEMBER:
            return True
        return False