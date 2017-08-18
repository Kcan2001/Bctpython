from django.contrib import admin

# Register your models here.
from .models import Trip, TripImage


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
