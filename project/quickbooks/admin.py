from django.contrib import admin
from .models import QuickBooksDiscoveryDocument, QuickBooksToken, QuickBooksErrorRequest


admin.site.register(QuickBooksDiscoveryDocument)
admin.site.register(QuickBooksToken)
admin.site.register(QuickBooksErrorRequest)
