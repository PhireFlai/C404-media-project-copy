from rest_framework.permissions import BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.conf import settings
from socialnetwork.models import RemoteNode  # Import your RemoteNode model

import base64

class MultiAuthPermission(BasePermission):
    """
    Custom permission to allow:
    - Unauthenticated access if the view allows it.
    - Token authentication for local users.
    - Basic authentication for remote nodes.
    """

    def has_permission(self, request, view):
        # Public access (if the view allows it)
        if hasattr(view, "permission_classes") and AllowAny in view.permission_classes:
            return True

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return False  # No authentication provided

        # Token Authentication (Local Users)
        if auth_header.startswith("Token "):
            user_auth = TokenAuthentication()
            try:
                user, _ = user_auth.authenticate_credentials(auth_header.split(" ")[1])
                request.user = user
                return user.is_authenticated
            except Exception:
                return False

        # Basic Authentication (Remote Nodes)
        elif auth_header.startswith("Basic "):

            try:
                auth_decoded = base64.b64decode(auth_header.split(" ")[1]).decode("utf-8")
                username, password = auth_decoded.split(":", 1)

                remote_node = RemoteNode.objects.get(username=username, password=password, is_active=True)
                request.remote_node = remote_node
                return True
            except (RemoteNode.DoesNotExist, ValueError, base64.binascii.Error):
                return False

        return False  # Default to unauthorized

class IPLockPermission(BasePermission):
    """
    Grants access only to requests from allowed IPs.
    """

    def has_permission(self, request, view):
        allowed_ips = getattr(settings, "ALLOWED_ADMIN_IPS", [])
        client_ip = request.META.get("REMOTE_ADDR")

        return client_ip in allowed_ips

class ConditionalMultiAuthPermission(BasePermission):
    """
    - Allows IP-locked local access.
    - Requires MultiAuthPermission for remote access.
    """

    def has_permission(self, request, view):
        allowed_ips = getattr(settings, "ALLOWED_ADMIN_IPS", [])
        client_ip = request.META.get("REMOTE_ADDR")

        # If request is from an allowed IP, grant access without authentication.
        if client_ip in allowed_ips:
            return True

        # Otherwise, require MultiAuthPermission (Basic or Token auth)
        return MultiAuthPermission().has_permission(request, view)