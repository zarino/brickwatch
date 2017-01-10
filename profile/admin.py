from django.contrib import admin
from profile.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False

def get_name(self):
    return self.profile.name
get_name.short_description = 'Name'
get_name.admin_order_field = 'profile__name'

class UserAdmin(AuthUserAdmin):
    list_display = (
        'username',
        get_name,
        'email',
        'is_active',
        'last_login',
        'is_staff',
    )

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [ProfileInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)
