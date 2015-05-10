# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, m2m_changed

import datetime
from django.utils import timezone
# Create your models here.

class Universidad(models.Model):
    #id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=150)
    siglas = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15, blank=True)
    url = models.CharField(max_length=200)
    direccion = models.CharField(max_length=250)
    class Meta:
        db_table = u'universidad'

'''		
class StibdUsuario(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_mail = models.CharField(max_length=300)
    user_login = models.CharField(max_length=60, unique=True)
    user_pass = models.CharField(max_length=300)
    user_nombre = models.CharField(max_length=150)
    user_apellido = models.CharField(max_length=150)
    user_sexo = models.CharField(max_length=3, blank=True)
    user_fechanac = models.DateField(null=True, blank=True)
    user_cid = models.CharField(max_length=45, blank=True)
    user_telefono = models.CharField(max_length=33, blank=True)
    user_acceso = models.IntegerField()
    user_pais = models.IntegerField(null=True, blank=True)
    user_cambiopass = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'stibd_usuario'
'''		
#Perfil con los datos Adicionales de Usuario
class UserProfile(models.Model):
	# This field is required
	user = models.OneToOneField(User)
	# Other fields here
	#user_nombre = models.CharField(max_length=150)
	#user_apellido = models.CharField(max_length=150)
	user_carnet = models.CharField(max_length=11, blank=True)
	user_universidad = models.ForeignKey(Universidad, db_column='user_universidad', null=True)
	#user_correo = models.CharField(max_length=33, blank=True)
	user_telefono = models.CharField(max_length=33, blank=True)
	user_pais = models.IntegerField(null=True, blank=True)
	user_cambiopass = models.DateField(null=True, blank=True)
	session_key = models.CharField(max_length=40,null=True, blank=True)
	def __unicode__(self):
		return self.user.username

'''		
class PerfilPersona(models.Model):
	id = models.AutoField(primary_key=True)
	SEXO = (('M','Masculino'),('F','Femenino'))
	user_sexo = models.CharField(max_length=3, blank=True, choices=SEXO)
	user_fechanac = models.DateField(null=True, blank=True)
	user_cid = models.CharField(max_length=45, null=True)
	user_profile = models.OneToOneField(UserProfile, db_column='user_profile')
	class Meta:
		db_table = u'perfil_persona'
	def __unicode__(self):
		return self.user_profile.user.username
'''
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

# Si se crea un usuario, se crea el UserProfile común
post_save.connect(create_user_profile, sender=User)

		
# Clase para las preguntas totalizadas		
class Pregunta(models.Model):
	#pregunta_id = models.IntegerField(primary_key=True)
	#usuario = models.ForeignKey(StibdUsuario, db_column='usuario')
	descripcion = models.CharField(max_length=1000)	# Descripcion en lenguaje natural de la pregunta
	ocurrencias = models.IntegerField(default=1)
	#composicion = models.ForeignKey(Tripleta, db_column='composicion') # Descripcion estructura en triple(sparql) de la pregunta
	class Meta:
		db_table = u'pregunta'
	def __unicode__(self):
		return self.choice

# Clase para las preguntas formuladas por los estudiantes		
class PreguntaEstudiante(models.Model):
	#pe_id = models.IntegerField(primary_key=True)
	usuario = models.ForeignKey(User, db_column='usuario')
	#usuario = models.OneToOneField(User)#models.ForeignKey(StibdUsuario, db_column='usuario')
	descripcion = models.CharField(max_length=1000)	# Descripcion en lenguaje natural de la pregunta
	fecha = models.DateField(null=True, blank=True)
	pregunta = models.ForeignKey(Pregunta, db_column='pregunta')
	#composicion = models.ForeignKey(Tripleta, db_column='composicion') # Descripcion estructura en triple(sparql) de la pregunta
	class Meta:
		db_table = u'pregunta_estudiante'
	def __unicode__(self):
		return self.choice
		
# Clase para las respuestas a preguntas frecuentes formuladas por los estudiantes	
class Respuesta(models.Model):
	#respuesta_id = models.IntegerField(primary_key=True)
	pregunta = models.ForeignKey(Pregunta, db_column='pregunta')
	descripcion = models.CharField(max_length=1000)	# Descripcion en lenguaje natural de la Respuesta
	rating = models.IntegerField(default=3)
	#composicion = models.ForeignKey(Tripleta, db_column='composicion') # Descripcion estructura en triple(sparql) de la respuesta
	class Meta:
		db_table = u'respuesta'
	def __unicode__(self):
		return self.choice
	
# Clase para las preguntas formuladas por los estudiantes		
class Evento(models.Model):
	#evento_id = models.IntegerField(primary_key=True)
	#usuario = models.ForeignKey(StibdUsuario, db_column='usuario')
	titulo = models.CharField(max_length=100)	
	ubicacion = models.CharField(max_length=100)	
	fecha = models.DateField(null=True, blank=True)
	class Meta:
		db_table = u'evento'
	def __unicode__(self):
		return self.choice

# Clase para las preguntas formuladas por los estudiantes		
class Noticia(models.Model):
	#noticia_id = models.IntegerField(primary_key=True)
	#usuario = models.ForeignKey(StibdUsuario, db_column='usuario')
	titulo = models.CharField(max_length=100)	
	contenido = models.CharField(max_length=1000)	
	fechapub = models.DateField(null=True, blank=True)
	class Meta:
		db_table = u'noticia'
	def __unicode__(self):
		return self.choice
		
#Formularios
class InformesForm(forms.Form):

	CHOICES = (('7', '7 dias (Agudos)',),('14', '14 dias (Agudos)',),('30', '1 mes (Agudos)',),
		('90', '3 meses',),('180', '6 meses',),('270', '9 meses',),('365', '12 meses',))
	RADIO_CHOICES=[('1','Medicamento'),('2','Principio Activo')]
	
	fecha_informe = forms.DateField(label='Fecha:', widget=forms.DateInput(format='%d/%m/%Y',attrs={'class':'datePicker fecha_informe inputbox01', 'readonly':'true'}))
	duracion_informe = forms.ChoiceField(choices=CHOICES, initial=180,label='Duracion:', widget=forms.Select(attrs={'class':'duracion selectbox01', 'size':'1'}))
	patologia = forms.CharField(widget=forms.TextInput(attrs={'class':'pat inputbox03'}), max_length=150, label='Patologia:')
	medicamento = forms.CharField(widget=forms.TextInput(attrs={'class':'med inputbox04'}), max_length=150, label='Medicamento:')
	medico = forms.CharField(widget=forms.TextInput(attrs={'class':'medico inputbox02', 'style':'margin-top:0px;text-transform:uppercase;' , 'id':'medico'}), max_length=150, label='Médico:')
	nombre_medicamento = forms.CharField(widget=forms.HiddenInput(), max_length=150)
	num_medicamento = forms.IntegerField(widget=forms.HiddenInput())
	uni_medicamento = forms.FloatField(widget=forms.HiddenInput())
	adm_medicamento = forms.IntegerField(widget=forms.HiddenInput())
	dosis_medicamento = forms.FloatField(widget=forms.HiddenInput())
	vehiculo_medicamento = forms.FloatField(widget=forms.HiddenInput())
	
	prin_dosis_unidad = forms.CharField(widget=forms.HiddenInput()) # Contiene unidad si es Principio con Dosis
	
	cantidad = forms.IntegerField(label='Cantidad:',widget=forms.TextInput(attrs={'class':'cantidad_text positive-integer inputbox01'}))
	
	#FARMACIA
	precio = forms.DecimalField(label='Precio:',widget=forms.TextInput(attrs={'class':'positive inputbox01'}),min_value=0.00,decimal_places=2)
	iva = forms.BooleanField(initial=False,label='IVA:', widget=forms.CheckboxInput(attrs={'class':'iva checkboxstyle'}))
	#/FARMACIA
	
	num_informe = forms.IntegerField(widget=forms.HiddenInput())

	status_calculadora = forms.IntegerField(initial=0,widget=forms.HiddenInput())
	cantidad_calculadora = forms.IntegerField(widget=forms.HiddenInput())
	medida_calculadora = forms.IntegerField(widget=forms.HiddenInput())
	duracion_calculadora = forms.IntegerField(widget=forms.HiddenInput())
	frecuencia_calculadora = forms.IntegerField(widget=forms.HiddenInput())
	
	id_farmacia = forms.IntegerField(widget=forms.HiddenInput())
	farmacia = forms.CharField(widget=forms.TextInput(attrs={'class':'farm inputbox04'}), max_length=50, label='Farmacia:')
	total_factura = forms.IntegerField(label='Total Factura:',widget=forms.TextInput(attrs={'class':'positive inputbox01'}))
	observaciones = forms.CharField(widget=forms.Textarea(attrs={'class':'ind_textarea'}),max_length=500)
	medicamento_opcion = forms.ChoiceField(choices=RADIO_CHOICES, initial=1, widget=forms.RadioSelect(attrs={'style':'float:inherit;'}))
	
class ContactoForm(forms.Form):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'inputbox05 submit','placeholder':'Nombre y Apellido'}), max_length=150,)
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'inputbox05 submit','placeholder':'Correo Electrónico'}), max_length=150,)
	comentario = forms.CharField(widget=forms.Textarea(attrs={'class':'inputbox06','cols':'25', 'rows':'2','placeholder':'Comentarios'}), max_length=150,)
	
class RecuperarForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'inputbox05 submit','placeholder':'Correo Electrónico'}), max_length=150,)
	
class RegistroForm(forms.Form):
	SEXO_CHOICES = (('M','Masculino',),('F','Femenino',))
	#CI_CHOICES = (('V', 'V',),('E', 'E',),('M', 'M',))
	nombre = forms.CharField(label='Name',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your name'}))
	apellido = forms.CharField(label='Lastname',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your lastname'}))
	sexo = forms.ChoiceField(label='Sex',choices=SEXO_CHOICES,widget=forms.Select(attrs={'class':'selectbox01','size':'1'}) )
	universidad = forms.CharField(label='University', max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your University'}),required=False)
	uc = forms.CharField(label='University Card', max_length=11, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your University Card number'}))
	birthdate = forms.DateField(label='Birthdate', widget=forms.DateInput(format='%d/%m/%Y',attrs={'class':'inputbox01 datePicker',}),input_formats=('%d/%m/%Y',))
	correo = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Email'}), max_length=150,)
	pais = forms.CharField(label='Country', max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Country'}),required=False)
	telefono = forms.IntegerField(label='Phone',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your contact phone number'}))
	user = forms.CharField(label='Username',max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Choose your username'}))
	password = forms.CharField(label='Password',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Choose a password for your account'}))
	usuario = forms.IntegerField(widget=forms.HiddenInput(attrs={}))
	
class TutorForm(forms.Form):
	pregunta = forms.CharField(widget=forms.TextInput(attrs={'class':'med inputbox04'}), max_length=150, label='Pregunta:')
	respuesta = forms.CharField(widget=forms.HiddenInput(), max_length=150)