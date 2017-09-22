from django.contrib import admin
from accounts.models import Account
from .models import Trip, TripDate, TripImage, Excursion


# Will add users who payed for tour to tour date edit/save page
class UserInline(admin.StackedInline):
    model = Account.trips.through
    can_delete = True
    verbose_name = 'Client'
    verbose_name_plural = 'Clients'


class TripDateAdmin(admin.ModelAdmin):
    # Which inline we use here:
    inlines = [UserInline]
    # Which fields will show at tour save/edit page:
    fields = ('trip', 'arrival', 'departure', 'price')
    # Hierarchy by arrival field at Tour list page
    date_hierarchy = 'arrival'
    # Will order our tours at Tour list for descending arrival date
    ordering = ['-arrival']
    # Will use this fields while search
    search_fields = ['trip__title', 'arrival', 'departure', 'price']
    # Will show this fields at Tour list page
    list_display = ['trip', 'arrival', 'departure', 'get_trip_excursions_count', 'price', 'get_user_trips_count']
    # Will use this fields for filter
    list_filter = ['arrival', 'departure', 'price']

    class Meta:
        model = TripDate

    # Count how many orders for tour
    def get_user_trips_count(self, obj):
        query = TripDate.objects.get(pk=obj.pk)
        return query.account.count()
    get_user_trips_count.short_description = 'Orders'

    # Count how many excursions in tours
    def get_trip_excursions_count(self, obj):
        query = TripDate.objects.get(pk=obj.pk)
        return query.excursions.count()
    get_trip_excursions_count.short_description = 'Excursions'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(TripDateAdmin, self).get_inline_instances(request, obj)

    def get_queryset(self, request):
        return super(TripDateAdmin, self).get_queryset(request).select_related('trip').prefetch_related('excursions',
                                                                                                        'account')


class ExcursionAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'price']
    list_filter = ['price', 'duration']

    class Meta:
        model = Excursion

    def get_queryset(self, request):
        return super(ExcursionAdmin, self).get_queryset(request).prefetch_related('trip')


class TripImageAdmin(admin.ModelAdmin):
    list_display = ['trip', 'featured', 'thumbnail', 'active', 'updated']
    list_filter = ['featured', 'thumbnail', 'active']

    class Meta:
        model = TripImage

    def get_queryset(self, request):
        return super(TripImageAdmin, self).get_queryset(request).select_related('trip')


admin.site.register(Trip)
admin.site.register(TripDate, TripDateAdmin)
admin.site.register(TripImage, TripImageAdmin)
admin.site.register(Excursion, ExcursionAdmin)
