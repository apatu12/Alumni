from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
import uuid
import datetime
from django.utils import timezone
from config.utils import upload_profile


# Custom manager
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class ProfileType(models.Model):
    type = models.CharField(max_length=100)
    number = models.IntegerField()
    deskrisaun = models.TextField()
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Profiletype_created_by")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Profiletype_updated_by")
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Profiletype_deleted_by")
    deleted_at = models.DateTimeField(null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self):
        return f"{self.type} {self.number}"

    def soft_delete(self, user):
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()

    def undelete(self):
        self.deleted_at = None
        self.deleted_by = None
        self.save()

    def hard_delete(self):
        super().delete()


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey(ProfileType, on_delete=models.CASCADE, related_name='pt', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile', null=True, blank=True)

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=50)

    sex = models.CharField(max_length=10, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')])
    dob = models.DateField(null=True, blank=True)
    pob = models.CharField(max_length=50)

    email = models.EmailField(max_length=100, null=True, blank=True)
    image = models.ImageField(
        upload_to=upload_profile,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        null=True,
        blank=True,
        verbose_name='Imagen'
    )

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Profile_created_by")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Profile_updated_by")
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Profile_deleted_by")
    deleted_at = models.DateTimeField(null=True, blank=True)

    password_reset_token = models.TextField(null=True, blank=True)
    new_activate_token = models.TextField(null=True, blank=True)

    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self):
        return f"{self.name} ({self.type})"

    def soft_delete(self, user):
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()

    def undelete(self):
        self.deleted_at = None
        self.deleted_by = None
        self.save()

    def hard_delete(self):
        super().delete()

    def getAge(self):
        if self.dob:
            return datetime.date.today().year - self.dob.year
        return 0

    def getTotalLogin(self):
        return AuditLogin.objects.filter(user=self.user).count()


class AuditLogin(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    alumni = models.ForeignKey('Alumni', on_delete=models.SET_NULL, null=True, blank=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, null=True, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=[("SUCCESS", "Success"), ("FAILED", "Failed")]
    )
    
    login_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Audit Login"
        ordering = ['-login_at']
    
    def __str__(self):
        return f"{self.user} ({self.status}) - {self.login_at}"

