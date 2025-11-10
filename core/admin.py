from django.contrib import admin
from .models import Role, User, Receta, Ingrediente, PasoProcedimiento, Canasta
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_rol")

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + ((None, {"fields": ("rol","semestre","carrera")}),)
admin.site.register(User, UserAdmin)

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ("id","nombre_receta","autor","porciones_base","tiempo_preparacion_min")

admin.site.register(Ingrediente)
admin.site.register(PasoProcedimiento)
admin.site.register(Canasta)
