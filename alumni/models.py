from django.db import models
from config.utils import alumni_photo 
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from custom.models import Faculdade, Departamento, Municipality, AdministrativePost, Village, SubVillage, Nasaun, Year

# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s_created")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s_updated")
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s_deleted")

    class Meta:
        abstract = True


class Alumni(BaseModel):
    registration_no = models.CharField(max_length=50, unique=True, verbose_name="Registration Number")
    full_name = models.CharField(max_length=120, verbose_name="Full Name")

    sex = models.CharField(
        max_length=10,
        choices=[('M', 'Masculino'), ('F', 'Femenino')],
        verbose_name="Gender"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=120)
    father_name = models.CharField(max_length=120, null=True, blank=True)
    mother_name = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(upload_to="alumni/photos/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} ({self.registration_no})"

class AlumniAddress(BaseModel):
    alumni = models.OneToOneField(Alumni, on_delete=models.CASCADE, related_name="address")
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True)
    administrative_post = models.ForeignKey(AdministrativePost, on_delete=models.SET_NULL, null=True)
    suco = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True)
    aldeia = models.ForeignKey(SubVillage, on_delete=models.SET_NULL, null=True)
    detail_address = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f"Address of {self.alumni.full_name}"

class AcademicRecord(BaseModel):
    alumni = models.OneToOneField(Alumni, on_delete=models.CASCADE, related_name="academic")
    faculty = models.ForeignKey(Faculdade, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    year_start = models.CharField(max_length=4, null=True, blank=True)
    year_graduation = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True, related_name="graduated_alumni")
    thesis_title = models.CharField(max_length=255, null=True, blank=True)
    advisor_1 = models.CharField(max_length=120, null=True, blank=True)
    advisor_2 = models.CharField(max_length=120, null=True, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    predicate = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.alumni.full_name} - {self.department}"

class Career(BaseModel):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name="careers")
    job_field = models.CharField(
        max_length=50,
        choices=[('Relevant', 'Relevant'), ('Not Relevant', 'Not Relevant')]
    )
    institution = models.CharField(max_length=150, null=True, blank=True)
    department = models.CharField(max_length=150, null=True, blank=True)
    position = models.CharField(max_length=150, null=True, blank=True)
    country = models.ForeignKey(Nasaun, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.alumni.full_name} - {self.position}"

class FurtherStudy(BaseModel):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name="further_studies")
    study_level = models.ForeignKey(nivelmaster, on_delete=models.SET_NULL, null=True)
    major = models.CharField(max_length=255, null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(Nasaun, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.alumni.full_name} - {self.university}"

class AlumniUser(BaseModel):
    alumni = models.OneToOneField(Alumni, on_delete=models.CASCADE, related_name="account")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.alumni.full_name} - {self.user.username}"
