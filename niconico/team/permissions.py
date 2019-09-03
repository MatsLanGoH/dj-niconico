from rest_framework.permissions import BasePermission

from team.models import Membership, MembershipStatus


class IsActiveUser(BasePermission):
    """ Allows access only to active users.
    """

    def has_permission(self, request, view):
        pk = request.parser_context["kwargs"]["pk"]
        membership = Membership.objects.get(pk=pk)

        return bool(
            request.user
            and request.user.is_authenticated
            and membership.status == MembershipStatus.ACTIVE.value
        )
