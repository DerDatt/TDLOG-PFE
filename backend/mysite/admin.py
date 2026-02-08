"""
Django Admin Configuration
Only shows accounts app, hides authentication and polls
"""
from django.contrib import admin
from django.contrib.auth.models import Group

# Customize admin site appearance
admin.site.site_header = "PFE Administration"
admin.site.site_title = "PFE Admin"
admin.site.index_title = "Welcome to PFE Administration"

# Unregister default Django auth models
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# Only accounts models will be visible (registered in accounts/admin.py)
