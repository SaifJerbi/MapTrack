from django.contrib.gis import admin 
from models import *
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User


admin.site.register(Waypoint, admin.GeoModelAdmin)
from django.contrib import admin
# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserPro
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
models = [Provider, Societe, Chauffeur, Ville, Localite, Pays, Archive, TypeTerminal, Terminal, Mobile, Traduction]
admin.site.register(models)
