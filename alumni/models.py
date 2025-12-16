from django.db import models
from config.utils import alumni_photo 
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import uuid
from custom.models import Faculdade, Departamento, Municipality, \
     AdministrativePost, Village, SubVillage, Nasaun, Year, nivelmaster
from simple_history.models import HistoricalRecords
from PIL import Image

# Create your models here.
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class Alumni(models.Model):
    registration_no = models.CharField(max_length=50, verbose_name="Nu Registo do Antigo Aluno/NRE", unique=True, db_index=True)
    name = models.CharField(max_length=120, verbose_name="Nome Completo")
    sex = models.CharField(max_length=10, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], verbose_name="Sexo")
    dob= models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    pob = models.CharField(max_length=120, null=True, blank=True, verbose_name="Naturalidade")
    father_name = models.CharField(max_length=120, null=True, blank=True, verbose_name='Nome Do Pai')
    mother_name = models.CharField(max_length=120, null=True, blank=True, verbose_name='Nome Da Mãe')
    email = models.EmailField(max_length=150, null=True, blank=True, verbose_name='E-Mail')
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Nu Telemovel')
    pos = models.CharField(max_length=50, verbose_name='Status Ataul', choices=[('Em Estudo','Em Estudo'),('No Trabalho','No Trabalho'),('Em Estudo e No Trabalho','Em Estudo e No Trabalho'),('Outro','Outro')],  null=True, blank=True)
    pos_outro = models.CharField(max_length=150, null=True, blank=True, verbose_name="Outro Descrição")
    photo = models.ImageField(upload_to=alumni_photo, verbose_name='Imagen', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])], null=True, blank=True) 
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="alumnicreatedbys")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="alumniupdatetedbys")
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="alumnideletedbys")
    deleted_at = models.DateTimeField(null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    history = HistoricalRecords()
    def __str__(self):
        nk = self.registration_no + " " + self.name
        return nk
    
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            target_size = (480, 640) 
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            img.save(self.photo.path)

    objects = models.Manager()  
    active_objects = ActiveManager()

    class Meta:
        verbose_name_plural='01-Dadus_Alumni_Pessoal'

class AlumniAddress(models.Model):
    alumni = models.OneToOneField(Alumni, on_delete=models.CASCADE, related_name="address")
    mun = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, verbose_name='Município')
    post = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True, verbose_name='Posto Administrativo')
    suk = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, verbose_name="Suco")
    ald = models.ForeignKey(SubVillage, on_delete=models.CASCADE, null=True, verbose_name="Aldeia")
    detail_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Detailho Endereso")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Addresscreatedbys")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Addressupdatetedbys")
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Addressdeletedbys")
    deleted_at = models.DateTimeField(null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    history = HistoricalRecords()
    def __str__(self):
        #template = '{0.name}'
        nk = self.alumni.name + " " + self.municipality.name
        return nk
    
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

    objects = models.Manager()  # The default manager
    active_objects = ActiveManager()

    class Meta:
        verbose_name_plural='02-Dadus_Alumni_Enderesu'

class AcademicRecord(models.Model):
    alumni = models.OneToOneField(Alumni, on_delete=models.CASCADE, related_name="academic")
    faculty = models.ForeignKey(Faculdade, on_delete=models.CASCADE, null=True, verbose_name="Faculdade")
    department = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, verbose_name="Departamento")
    year_start = models.CharField(max_length=4, null=True, blank=True, verbose_name="Ano Início")
    year_graduation = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, verbose_name="Ano Termina")
    thesis_title = models.CharField(max_length=255, null=True, blank=True, verbose_name="Titulo De Teze")
    advisor_1 = models.CharField(max_length=120, null=True, blank=True, verbose_name=" Oreintador I")
    advisor_2 = models.CharField(max_length=120, null=True, blank=True, verbose_name=" Oreintador II")
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="IPC")
    predicate = models.CharField(max_length=50, null=True, blank=True, verbose_name="Predicado")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Academiccreatedbys")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Academicupdatetedbys")
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Academicdeletedbys")
    deleted_at = models.DateTimeField(null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    history = HistoricalRecords()
    def __str__(self):
        #template = '{0.name}'
        nk = self.alumni.name + " " + self.faculty.name
        return nk
    
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

    objects = models.Manager()  
    active_objects = ActiveManager()

    class Meta:
        verbose_name_plural='03-Dadus_Alumni_Academica'

class Career(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name="careers")
    job_field = models.CharField(
        max_length=50,
        choices=[('Relevante', 'Relevante'), ('Não Relevante', 'Não Relevante')], verbose_name="Estado Servico")
    institution = models.CharField(max_length=150, null=True, blank=True, verbose_name="instituticão")
    department = models.CharField(max_length=150, null=True, blank=True, verbose_name="Departamento")
    position = models.CharField(max_length=150, null=True, blank=True, verbose_name="Posicão")
    country = models.ForeignKey(Nasaun, on_delete=models.CASCADE, null=True, verbose_name="País")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Careiracreatedbys")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Careiraupdatetedbys")
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Careiradeletedbys")
    deleted_at = models.DateTimeField(null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    history = HistoricalRecords()
    def __str__(self):
        #template = '{0.name}'
        nk = self.alumni.name + " " + self.job_field
        return nk
    
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

    objects = models.Manager()  
    active_objects = ActiveManager()

    class Meta:
        verbose_name_plural='04-Dadus_Alumni_Careira'

class FurtherStudy(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, null=True, blank=True, related_name="further_studies")
    study_level = models.ForeignKey(nivelmaster, on_delete=models.CASCADE, null=True, verbose_name="Nivel Estudo")
    major = models.CharField(max_length=255, null=True, blank=True, verbose_name="Especialidade")
    university = models.CharField(max_length=255, null=True, blank=True, verbose_name="Univesidade")
    country = models.ForeignKey(Nasaun, on_delete=models.CASCADE, null=True, blank=True, verbose_name="País")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="estudocreatedbys")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="estudoupdatetedbys")
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="estudodeletedbys")
    deleted_at = models.DateTimeField(null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    history = HistoricalRecords()
    def __str__(self):
        #template = '{0.name}'
        nk = self.alumni.name + " " + self.study_level.name
        return nk
    
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

    objects = models.Manager() 
    active_objects = ActiveManager()

    class Meta:
        verbose_name_plural='05-Dadus_Alumni_Estudo'

class AlumniUser(models.Model):
    alumni = models.OneToOneField(Alumni, on_delete=models.CASCADE, null=True, blank=True, related_name="account" )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Alumnicreatedbys")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Alumniupdatetedbys")
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Alumnideletedbys")
    deleted_at = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()
    hashed = models.CharField(max_length=32, null=True, blank=True)
    
    def __str__(self):
        #template = '{0.name}'
        nk = self.alumni.name + " " + self.user
        return nk
    
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

    objects = models.Manager()  # The default manager
    active_objects = ActiveManager()

    class Meta:
        verbose_name_plural='06-Dadus_Alumni_user'
