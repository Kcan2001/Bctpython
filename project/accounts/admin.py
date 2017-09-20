from django.contrib import admin
from .models import Account, UserStripeSubscription, StripePlanNames, UserStripe
from django.contrib.auth.models import User


# Will add user account to user edit/save page
class UserInline(admin.StackedInline):
    model = Account
    can_delete = False


# ModelAdmin for Users in django admin site
class UserAdmin(admin.ModelAdmin):
    # Which inline we use here:
    inlines = [UserInline]
    # Will show this fields at User list page
    list_display = ['username', 'get_user_name', 'email', 'get_user_membership', 'is_active', 'is_staff',
                    'is_superuser']
    # Will order our Users for date joined field
    ordering = ['date_joined']

    class Meta:
        model = User

    # Will get Users first&last name to show in one field
    def get_user_name(self, obj):
        return '%s %s' % (obj.first_name, obj.last_name)
    get_user_name.short_description = 'Name'

    # Determine if our User has bought premium membership
    def get_user_membership(self, obj):
        return obj.account.is_membership
    get_user_membership.short_description = 'Premium Member'

    # Optimization for sql queries
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

    def get_queryset(self, request):
        return super(UserAdmin, self).get_queryset(request).prefetch_related('account')


# ModelAdmin for Accounts in django admin site
class AccountAdmin(admin.ModelAdmin):
    # Will show this fields at Accounts list page
    list_display = ['user', 'get_user_names', 'get_user_email', 'get_user_trips_count', 'email_confirmed',
                    'is_membership']

    class Meta:
        model = Account

    # Get users email address from User Model
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User email'

    # Get users first&last name from User Model
    def get_user_names(self, obj):
        return '%s %s' % (obj.user.first_name, obj.user.last_name)
    get_user_names.short_description = 'User Name'

    # Determine how many trips has bought our users
    def get_user_trips_count(self, obj):
        query = obj.trips.count()
        return query
    get_user_trips_count.short_description = 'How many trips bought'

    # Optimization
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(AccountAdmin, self).get_inline_instances(request, obj)

    def get_queryset(self, request):
        return super(AccountAdmin, self).get_queryset(request).select_related('user').prefetch_related('trips')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(UserStripeSubscription)
admin.site.register(StripePlanNames)
admin.site.register(UserStripe)
