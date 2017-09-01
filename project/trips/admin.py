from django.contrib import admin

from .models import Trip, TripImage, Excursion


class TripAdmin(admin.ModelAdmin):
    date_hierarchy = 'arrival'
    search_fields = ['title', 'description']
    list_display = ['title', 'price', 'arrival', 'departure']
    list_filter = ['price', 'arrival']
    prepopulated_field = {'slug': ('title',)}

    class Meta:
        model = Trip


admin.site.register(Trip, TripAdmin)
admin.site.register(TripImage)
admin.site.register(Excursion)
