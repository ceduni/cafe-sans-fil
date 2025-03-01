from fastapi import Depends, HTTPException, Request, status

from app.auth.dependencies import get_current_user
from app.cafe.models import Cafe
from app.cafe.service import CafeService
from app.cafe.staff.enums import Role
from app.user.models import User

OWNER = "OWNER"


class BasePermission:
    required_role = None

    async def __call__(
        self,
        request: Request,
        current_user: User = Depends(get_current_user),
    ):
        slug = request.path_params.get("slug")
        if not slug:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[{"msg": "Slug parameter is required"}],
            )

        cafe = await CafeService.get(slug)
        if not cafe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[{"msg": "A cafe with this slug does not exist."}],
            )

        user_role = self._get_user_role(current_user, cafe)
        await self._verify_permission(user_role)

    def _get_user_role(self, user: User, cafe: Cafe):
        """Determine user's role in the cafe"""
        if user.id == cafe.owner_id:
            return OWNER
        if user.id in cafe.staff.admin_ids:
            return Role.ADMIN
        if user.id in cafe.staff.volunteer_ids:
            return Role.VOLUNTEER
        return None

    async def _verify_permission(self, user_role: str):
        """Core permission check logic"""
        if self.required_role is None:
            return

        role_hierarchy = {Role.VOLUNTEER: 1, Role.ADMIN: 2, OWNER: 3}

        if user_role == OWNER:
            return

        if (
            not user_role
            or role_hierarchy[user_role] < role_hierarchy[self.required_role]
        ):
            required_role_str = (
                self.required_role.value
                if isinstance(self.required_role, Role)
                else self.required_role
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=[{"msg": f"Requires {required_role_str} role or higher"}],
            )


class AuthenticatedPermission(BasePermission):
    required_role = None


class VolunteerPermission(BasePermission):
    required_role = Role.VOLUNTEER


class AdminPermission(BasePermission):
    required_role = Role.ADMIN


class OwnerPermission(BasePermission):
    required_role = OWNER
