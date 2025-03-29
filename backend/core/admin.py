from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from socialnetwork.models import *

@admin.action(description='Approve selected users')
def approve_users(modeladmin, request, queryset):
    queryset.update(is_approved=True)

# Custom UserAdmin class
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'profile_picture', 'is_approved')  # Add profile_picture to list view
    search_fields = ('username', 'email')  # Fields to search in the admin panel
    readonly_fields = ('id', 'github_etag', 'remote_fqid')  # Make the UUID and github Etag field read-only in the admin panel

    actions = [approve_users]

    # Use filter_horizontal for many-to-many fields
    filter_horizontal = ('friends', 'followers', 'groups', 'user_permissions')

    # Ensure the admin form works with UUIDField
    fieldsets = (
        (None, {'fields': ('id', 'username', 'password', 'profile_picture', 'remote_fqid')}),  
        ('Friends and Followers', {'fields': ('friends', 'followers')}),  # Add friends and followers
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Approval', {'fields': ('is_approved',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('GitHub', {'fields': ('github', 'github_etag')}),
        
    )

@admin.register(RemoteNode)
class RemoteNodeAdmin(admin.ModelAdmin):
    list_display = ("url", "username", "is_active")
    actions = ["disable_node", "enable_node"]

    def disable_node(self, request, queryset):
        queryset.update(is_active=False)
    disable_node.short_description = "Disable selected nodes"

    def enable_node(self, request, queryset):
        queryset.update(is_active=True)
    enable_node.short_description = "Enable selected nodes"

admin.site.register(User, CustomUserAdmin)
# admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(FollowRequest)
admin.site.register(Like)
# admin.site.register(CommentLike)
admin.site.register(EnvironmentSetting)
