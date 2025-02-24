from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from socialnetwork.models import User,Post

# Custom UserAdmin class
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'profile_picture')  # Add profile_picture to list view
    search_fields = ('username', 'email')  # Fields to search in the admin panel
    readonly_fields = ('id',)  # Make the UUID field read-only in the admin panel

    # Use filter_horizontal for many-to-many fields
    filter_horizontal = ('friends', 'followers', 'groups', 'user_permissions')

    # Ensure the admin form works with UUIDField
    fieldsets = (
        (None, {'fields': ('id', 'username', 'password', 'profile_picture')}),  
        ('Friends and Followers', {'fields': ('friends', 'followers')}),  # Add friends and followers
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        
    )

admin.site.register(User, CustomUserAdmin)
# admin.site.register(User)
admin.site.register(Post)