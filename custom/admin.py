from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (
    Faculdade, Departamento, Municipality, AdministrativePost,
    Village, SubVillage, Pozisaun, Nasaun, Relijiaun, Year,
    nivelmaster, CarouselSlide, Informativo, ContactMessage
)

# ===============================
# RESOURCES
# ===============================
class FaculdadeResource(resources.ModelResource):
    class Meta:
        model = Faculdade
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class DepartamentoResource(resources.ModelResource):
    class Meta:
        model = Departamento
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class MunicipalityResource(resources.ModelResource):
    class Meta:
        model = Municipality
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class AdministrativePostResource(resources.ModelResource):
    class Meta:
        model = AdministrativePost
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class VillageResource(resources.ModelResource):
    class Meta:
        model = Village
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class SubVillageResource(resources.ModelResource):
    class Meta:
        model = SubVillage
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class PozisaunResource(resources.ModelResource):
    class Meta:
        model = Pozisaun
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class NasaunResource(resources.ModelResource):
    class Meta:
        model = Nasaun
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class RelijiaunResource(resources.ModelResource):
    class Meta:
        model = Relijiaun
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class YearResource(resources.ModelResource):
    class Meta:
        model = Year
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class NivelMasterResource(resources.ModelResource):
    class Meta:
        model = nivelmaster
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class CarouselSlideResource(resources.ModelResource):
    class Meta:
        model = CarouselSlide
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class InformativoResource(resources.ModelResource):
    class Meta:
        model = Informativo
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

class ContactMessageResource(resources.ModelResource):
    class Meta:
        model = ContactMessage
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True

# ===============================
# REGISTER MODELS WITH ADMIN
# ===============================
@admin.register(Faculdade)
class FaculdadeAdmin(ImportExportModelAdmin):
    resource_class = FaculdadeResource
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(Departamento)
class DepartamentoAdmin(ImportExportModelAdmin):
    resource_class = DepartamentoResource
    list_display = ('code', 'name', 'faculdade')
    search_fields = ('code', 'name', 'faculdade__name')
    list_filter = ('faculdade',)

@admin.register(Municipality)
class MunicipalityAdmin(ImportExportModelAdmin):
    resource_class = MunicipalityResource
    list_display = ('code', 'name', 'hckey')
    search_fields = ('code', 'name', 'hckey')

@admin.register(AdministrativePost)
class AdministrativePostAdmin(ImportExportModelAdmin):
    resource_class = AdministrativePostResource
    list_display = ('name', 'municipality')
    search_fields = ('name', 'municipality__name')
    list_filter = ('municipality',)

@admin.register(Village)
class VillageAdmin(ImportExportModelAdmin):
    resource_class = VillageResource
    list_display = ('name', 'administrativePost')
    search_fields = ('name', 'administrativePost__name')
    list_filter = ('administrativePost',)

@admin.register(SubVillage)
class SubVillageAdmin(ImportExportModelAdmin):
    resource_class = SubVillageResource
    list_display = ('name', 'village')
    search_fields = ('name', 'village__name')
    list_filter = ('village',)

@admin.register(Pozisaun)
class PozisaunAdmin(ImportExportModelAdmin):
    resource_class = PozisaunResource
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Nasaun)
class NasaunAdmin(ImportExportModelAdmin):
    resource_class = NasaunResource
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Relijiaun)
class RelijiaunAdmin(ImportExportModelAdmin):
    resource_class = RelijiaunResource
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Year)
class YearAdmin(ImportExportModelAdmin):
    resource_class = YearResource
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(nivelmaster)
class NivelMasterAdmin(ImportExportModelAdmin):
    resource_class = NivelMasterResource
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(CarouselSlide)
class CarouselSlideAdmin(ImportExportModelAdmin):
    resource_class = CarouselSlideResource
    list_display = ('title', 'subtitle', 'order', 'is_active')
    search_fields = ('title', 'subtitle')
    list_filter = ('is_active',)

@admin.register(Informativo)
class InformativoAdmin(ImportExportModelAdmin):
    resource_class = InformativoResource
    list_display = ('title', 'link', 'is_active', 'created_at')
    search_fields = ('title', 'link')
    list_filter = ('is_active',)

@admin.register(ContactMessage)
class ContactMessageAdmin(ImportExportModelAdmin):
    resource_class = ContactMessageResource
    list_display = ('nome', 'email', 'telefone', 'assunto', 'data_envio')
    search_fields = ('nome', 'email', 'assunto')
    list_filter = ('data_envio',)
