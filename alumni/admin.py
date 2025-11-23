from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Alumni, AlumniAddress, AcademicRecord,
    Career, FurtherStudy, AlumniUser
)

# ===============================
# RESOURCES
# ===============================
class AlumniResource(resources.ModelResource):
    class Meta:
        model = Alumni
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('registration_no',)

class AlumniAddressResource(resources.ModelResource):
    class Meta:
        model = AlumniAddress
        skip_unchanged = True
        report_skipped = True

class AcademicRecordResource(resources.ModelResource):
    class Meta:
        model = AcademicRecord
        skip_unchanged = True
        report_skipped = True

class CareerResource(resources.ModelResource):
    class Meta:
        model = Career
        skip_unchanged = True
        report_skipped = True

class FurtherStudyResource(resources.ModelResource):
    class Meta:
        model = FurtherStudy
        skip_unchanged = True
        report_skipped = True

class AlumniUserResource(resources.ModelResource):
    class Meta:
        model = AlumniUser
        skip_unchanged = True
        report_skipped = True

# ===============================
# INLINE
# ===============================
class CareerInline(admin.TabularInline):
    model = Career
    extra = 1
    show_change_link = True

class StudyInline(admin.TabularInline):
    model = FurtherStudy
    extra = 1
    show_change_link = True

# ===============================
# ADMIN
# ===============================
@admin.register(Alumni)
class AlumniAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = AlumniResource
    list_display = ("registration_no", "name", "sex", "email", "phone_number", "is_active")
    list_filter = ("sex", "is_active", "created_at")
    search_fields = ("registration_no", "name", "email", "phone_number")
    inlines = [CareerInline, StudyInline]

    # History display
    history_list_display = [
        'history_date',
        'history_user',
        'get_history_type_display',
    ]

@admin.register(AlumniAddress)
class AlumniAddressAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = AlumniAddressResource
    list_display = ("alumni", "mun", "post", "suk", "ald", "detail_address")
    list_filter = ("mun", "post")
    search_fields = ("alumni__name",)
    history_list_display = [
        'history_date',
        'history_user',
        'get_history_type_display',
    ]

@admin.register(AcademicRecord)
class AcademicRecordAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = AcademicRecordResource
    list_display = ("alumni", "faculty", "department", "year_start", "year_graduation", "gpa", "predicate")
    list_filter = ("faculty", "department")
    search_fields = ("alumni__name",)
    history_list_display = [
        'history_date',
        'history_user',
        'get_history_type_display',
    ]

@admin.register(Career)
class CareerAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = CareerResource
    list_display = ("alumni", "job_field", "institution", "department", "position", "country")
    list_filter = ("job_field", "country")
    search_fields = ("alumni__name", "institution", "position")
    history_list_display = [
        'history_date',
        'history_user',
        'get_history_type_display',
    ]

@admin.register(FurtherStudy)
class FurtherStudyAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = FurtherStudyResource
    list_display = ("alumni", "study_level", "major", "university", "country")
    search_fields = ("alumni__name", "major", "university")
    list_filter = ("study_level",)
    history_list_display = [
        'history_date',
        'history_user',
        'get_history_type_display',
    ]

@admin.register(AlumniUser)
class AlumniUserAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = AlumniUserResource
    list_display = ("alumni", "user")
    search_fields = ("alumni__name", "user__username")
    history_list_display = [
        'history_date',
        'history_user',
        'get_history_type_display',
    ]
