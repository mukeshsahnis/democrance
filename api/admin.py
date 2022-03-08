from django.contrib import admin

from api.models import Customer

# Add customer model to admin site
admin.site.register(Customer)
