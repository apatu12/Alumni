from django.db import models

# Create your models here.
class Municipality(models.Model):
	code = models.CharField(max_length=50, verbose_name='Sigla')
	hckey = models.CharField(max_length=25, verbose_name='Hckey', blank=True, null=True)
	name = models.CharField(max_length=50, verbose_name='Nome Municipio', null=False)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class AdministrativePost(models.Model):
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name='Munisipiu')
	name = models.CharField(max_length=50, verbose_name='Nome Postu', null=False)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Village(models.Model):
	administrativePost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, verbose_name='Postu')
	name = models.CharField(max_length=50, verbose_name='Nome Sucu', null=False)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class SubVillage(models.Model):
	village  = models.ForeignKey(Village, on_delete=models.CASCADE, verbose_name='Suku')
	name = models.CharField(max_length=50, verbose_name='Nome Aldeia', null=False)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Pozisaun(models.Model):
	name = models.CharField(max_length=50, verbose_name='Nome Pozisaun')

	def __str__(self):
		template = '{0.name}'
		return template.format(self)


class Nasaun(models.Model):
	name = models.CharField(max_length=50, verbose_name='Naran Nasaun', null=False)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)


class Relijiaun(models.Model):
	name = models.CharField(max_length=50, verbose_name='Naran Relijiaun', null=False)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Year(models.Model):
	name = models.CharField(max_length=50, verbose_name='Tinan', null=False)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)


class nivelmaster(models.Model):
	code = models.CharField(max_length=50, verbose_name='Sigla')
	name = models.CharField(max_length=50, verbose_name='Naran', null=False)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)


class CarouselSlide(models.Model):
    title = models.CharField(max_length=200, verbose_name="Títulu (h1)", blank=True, null=True)
    subtitle = models.TextField(verbose_name="Deskrisaun (h4)", blank=True, null=True)
    image = models.ImageField(upload_to='carousel/', verbose_name="Imagem")
    button_text = models.CharField(max_length=100, verbose_name="Texto Botão", blank=True, null=True)
    button_link = models.URLField(max_length=200, verbose_name="Link Botão", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem Slide")
    is_active = models.BooleanField(default=True, verbose_name="Ativu")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Slide: {self.title}"

class Informativo(models.Model):
    title = models.CharField(max_length=200, verbose_name="Títulu")
    image = models.ImageField(upload_to='informativo/', verbose_name="Imagem")
    link = models.URLField(max_length=300, verbose_name="Link Artigu")
    is_active = models.BooleanField(default=True, verbose_name="Ativu")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Informasaun"
        verbose_name_plural = "Informasaun"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=30, blank=True, null=True)
    assunto = models.CharField(max_length=150, blank=True, null=True)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_envio']
        verbose_name = "Mensagem de Contato"
        verbose_name_plural = "Mensagens de Contato"

    def __str__(self):
        return f"{self.nome} - {self.email}"