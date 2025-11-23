from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import ProfileType, Profile, AuditLogin

# ===============================
#  RESOURCES FOR IMPORT/EXPORT
# ===============================

class ProfileTypeResource(resources.ModelResource):
    class Meta:
        model = ProfileType
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('id',)

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('id',)

class AuditLoginResource(resources.ModelResource):
    class Meta:
        model = AuditLogin
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('id',)


# ===============================
#  ADMIN REGISTRATION
# ===============================

@admin.register(ProfileType)
class ProfileTypeAdmin(ImportExportModelAdmin):
    resource_class = ProfileTypeResource
    list_display = ('type', 'number', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('type', 'deskrisaun')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource
    list_display = ('name', 'type', 'user', 'sex', 'email', 'is_active', 'getAge')
    list_filter = ('type', 'sex', 'is_active')
    search_fields = ('name', 'first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
  
    fieldsets = (
        ('Personal Info', {
            'fields': ('name', 'first_name', 'last_name', 'sex', 'dob', 'pob', 'email', 'image')
        }),
        ('Account Info', {
            'fields': ('user', 'type', 'is_active', 'password_reset_token', 'new_activate_token')
        }),
        ('Audit Info', {
            'fields': ('created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_by', 'deleted_at')
        }),
    )

@admin.register(AuditLogin)
class AuditLoginAdmin(ImportExportModelAdmin):
    resource_class = AuditLoginResource
    list_display = ('user', 'ip_address', 'user_agent', 'status', 'login_at')
    list_filter = ('status', 'login_at')
    search_fields = ('user__username', 'ip_address', 'user_agent')
    readonly_fields = ('login_at', 'created_at', 'updated_at')
