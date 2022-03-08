from django.contrib import admin

from api.models import Customer, Policy

# Add customer model to admin site
admin.site.register(Customer)

# Register Policy model to admin site
admin.site.register(Policy)
