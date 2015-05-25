# Create your views here.

import requests
import json
from tutor.models import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.conf import settings
from datetime import date
#NLTK 
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
#Preprocesamiento
from pre_procesamiento.functions import *
from pre_procesamiento.tfidf import *
#from pre_procesamiento.preprocessing import *
from SPARQLWrapper import SPARQLWrapper, JSON
import quepy
#normalizacion
from num2words import num2words
import timeit
#SPARQL = SPARQLWrapper("http://localhost:3030/ds/query")
#QUEPY_STIBD = quepy.install("quepy_stibd")

def normalization(text):
	# lower case
	output = text.lower()
	# Cut enumerate numbers
	no_use_numbers = ['0.','1.','2.','3.','4.','5.','6.','7.','8.','9.','10.',' ex ']
	for num in no_use_numbers:
		output = output.replace(num,'.')
	# expanding abbreviations AND #text canonicalization it's = it is
	abbrevs={'\n':' ','\'s':' ', '...':'.','..':'.', ' b ':' ','defines':'is','eer':' enhanced entity relationship', '1:1':'one-to-one','1:n':'one-to-many','n:1':'many-to-one','m:n':'many-to-many',' er ':' entity relationship ', }#esto deberia salir de un file si se vuelve muy grande
	for abbrev in abbrevs:
		output = output.replace(abbrev,abbrevs[abbrev])
	# numbers to words
	#para cada numero restante en el texto, ordenado de mayor a menor, reemplazarlo por su word
	gen = (int(s) for s in output.split() if s.isdigit())
	for number in gen:
		output = output.replace(str(number),num2words(number))
	
	return output
	
def sparql_call(query, target):
	#http://localhost:3030/ds/query   http://dbpedia.org/sparql ab: <http://learningsparql.com/ns/addressbook#>
	#Ya deberia estar abierto so http://esmar.ldc.usb.ve:3030/ds/query  http://localhost:3030/ds/query
	#if sparql is None:
	try:
		sparql = SPARQLWrapper("http://esmar.ldc.usb.ve:3030/ds/query")
		
		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		target = target.replace("?", "") 
		for result in results["results"]["bindings"]:
			try:
				first = result[target]["value"]
				print(result[target]["value"]) 
			except Exception as e:
				#first = None
				print "no pude leer esto", e.message
		print "\n"
	except:
		print "no se pudo alcanzar el servidor sparql"
	try:
		return first, results
	except:
		return None, None
	#return first, results
		
# # # TODO Funcion para interpretar las preguntas realizadas y llevarlas a tripletas a cnsultar. Luego usar sparql call y 
# #        finalmente devolver la respuesta


def question_process(text):#_ajax
	if text is None:
		return False
	else:
		quepy_stibd = quepy.install("quepy_stibd")
		target, query, metadata = quepy_stibd.get_query(text)
		print target, query, metadata	
		target, query, metadata = quepy_stibd.get_query("where in the world is the Eiffel Tower?")
		print target, query, metadata	
		target, query, metadata = quepy_stibd.get_query("List Microsoft software")#Which is Cindy's email? Who is Jon Snow?
		print target, query, metadata			
	return True

'''
def question_process(text):#_ajax
	if text is None:
		return False
	else:
		if what_question(text):
			query = text_to_query()
			answer = sparql_call(query)
			print answer
		if who_question(text):
			query = text_to_query()
			answer = sparql_call(query)
			print answer
		if where_question(text):
			query = text_to_query()
			answer = sparql_call(query)
			print answer			
		if where_question(text):
			query = text_to_query()
			answer = sparql_call(query)
			print answer	
	return True
'''		

def my_ajax(request):
	if request.is_ajax():
		dato = request.POST.get('dato', None)
		try:
			print dato
		except:
			raise Http404
	else:
		raise Http404

def taxonomy_search(question): #funcion para buscar preguntas alternativas. TODO
	if "what is a key?" in question:
		return "what is a primary_key?","Primary key is the candidate key selected to be primary key."
	return None, None	
		
def alternative_ajax(request):
	if request.is_ajax():
		question = request.POST.get('question', None)
		print str(question)
		
		# Funcion que determine si hay una pregunta similar
		try:
			pregunta, respuesta = taxonomy_search(question)
			print "lala ", pregunta, "lolo ", respuesta 
			if pregunta is not None:
				return HttpResponse(json.JSONEncoder().encode({"exito":1,"alternativa":pregunta,"respuesta_alt":respuesta}), mimetype="application/json")
			else:	
				return HttpResponse(json.JSONEncoder().encode({"exito":1}), mimetype="application/json")
		except Exception as e:
			print e.message
			raise Http404

	else:
		print " ajax request fails"
		raise Http404

@login_required
def question_ajax(request):
	if request.is_ajax():
		question = request.POST.get('question', None)
		user_id = request.user.id
		user = User.objects.get(pk=user_id)
		print str(question)
		try:
			
			# Variable global para mantener la conexion a quepy.. Tal vez no sea necesario
			#if QUEPY_STIBD is None:
			QUEPY_STIBD = quepy.install("quepy_stibd")	
			if question is not None:
				target, query, metadata = QUEPY_STIBD.get_query(question)
			else:
				return HttpResponse(json.JSONEncoder().encode({"error":"No se obtuvo la pregunta"}), mimetype="application/json")
			# run query
			print query
			try:
				pregunta = Pregunta.objects.get(descripcion__icontains = str(question))
				pregunta.ocurrencias = pregunta.ocurrencias + 1
				pregunta.save()
			except Exception as e:
				print "que paso ", e.message
				pregunta = Pregunta(descripcion = str(question))
				pregunta.save()
			print "almacenada pregunta"
			try:
				pe = PreguntaEstudiante(usuario = user, descripcion = str(question),fecha = date.today() ,pregunta = pregunta)
				pe.save()
			except Exception as e:
				print "aca ", e.message
				pe = PreguntaEstudiante(usuario = user, descripcion = str(question),fecha = date.today() ,pregunta = pregunta)
				pe.save()
				
			try:
				first, results = sparql_call(query,target)
				try:
					respuesta = Respuesta.objects.get(descripcion__icontains = first)
				except Exception as e:
					respuesta = Respuesta(descripcion = first,pregunta = pregunta)
					respuesta.save()
				'''
				try:
					respuesta = Respuesta(descripcion = first,pregunta = pregunta)
					respuesta.save()
				except Exception as e:
					print e.message
				'''	
				return HttpResponse(json.JSONEncoder().encode({"exito":1,"respuesta":first}), mimetype="application/json")
			except Exception as e:
				print e.message
				raise Http404
		except Exception as e:
			print " quepy install fails ", repr(e), e.message
			return HttpResponse(json.JSONEncoder().encode({"error":"No se pudo procesar la pregunta"}), mimetype="application/json")
			#raise Http404
	else:
		print " ajax request fails"
		raise Http404
		
def question(question):
	try:
		# Variable global para mantener la conexion a quepy.. Tal vez no sea necesario
		quepy_stibd = None
		if quepy_stibd is None:
			quepy_stibd = quepy.install("quepy_stibd")	
		target, query, metadata = quepy_stibd.get_query(question)
		print query
		# run query
		try:
			#pass
			a,b = sparql_call(query,target)
			#sparql_call(query,target)
			
		except Exception as e:
			print e.message
			raise Http404
	except Exception as e:
		print "errorrr", e.message
		raise Http404
		
def sparql_call2():
	#http://localhost:3030/ds/query   http://dbpedia.org/sparql ab: <http://learningsparql.com/ns/addressbook#>
	sparql = SPARQLWrapper("http://localhost:3030/ds/query")
	'''
	sparql.setQuery("""
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	SELECT ?label
	WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
	""")
	'''
	try:
		sparql.setQuery("""PREFIX ab: <http://www.w3.org/2000/01/rdf-schema#> 
		SELECT ?craigEmail
		WHERE { ab:craig ab:email ?craigEmail . }	
		""")	
		print "query ", sparql.queryString	
		ok = True
	except Exception as e:
		print "ok ",e.message	
		ok = False
	
	if ok:
		sparql.setReturnFormat(JSON)
		try:
			results = sparql.query().convert()
			 
			for result in results["results"]["bindings"]:
				try:
					print(result["craigEmail"]["value"]) 
				except:
					print "no pude leer esto"
		except Exception as e:
			print "ok ",e.message			

# carga el texto con las stopwords del archivo predeterminado para las mismas			
def load_stopwords():
	stopwords = ""
	try:
		print settings.YML_ROOT+'stopwords.txt'
		f = open(settings.YML_ROOT+'stopwords.txt','rb')
		stopwords = load(f)
		f.close()
	except:
		print "Error opening/loading ", filename
		return ''			
	return stopwords	

def preprocess(request):

	start = timeit.default_timer()
	#---
	#DEscomentar pdf luego Entity relationship Concepts.pdf
	books = ["db1.pdf","db2.pdf", "fundamentos_er_ere.pdf"]#"Entity relationship Concepts.pdf", "fundamentos_er_ere.pdf"
	texts = []
	
	for book in books:
		pdf = pdf_to_text(settings.BOOKS_URL+book)
		#print "ok ", pdf
		#text = normalization(pdf)
		#print "\n\n",text
		# Esta funcion es para preprocesamiento, deberia correrse desde antes de hacer el runserver
		#nltk = clasification(pdf) #A rare black squirrel has become a regular visitor to a suburban garden  --- We saw a little strange dog
		#---
		#texts.append(text)
	# Funcion para obtener los valores tfidf por palabra en el/los documento(s)
	#tfidf_table(texts,load_stopwords()) #, create_csv = ,True
	
	# Comentando por ahora
	#nltk = nltk_call("A rare squirrel has become a regular visitor to a suburban garden.")
	#sparql_call2()
	#ok = question_process("What is a subclass?")
	ok = question("What is a database?")
	ok1 = question("How is represented a entity?")
	#ok2 = question("What does define a entity_relationship_model?")
	ok3 = question("What does a entity contains?")
	
	stop = timeit.default_timer()
	print stop - start
	
	# Para hacer pruebas usar index.html, del resto usar index1.html
	return render_to_response('tutor/index.html', RequestContext(request))

def contact(request):
	# if autenticado index2
	return render_to_response('tutor/index1.html', {'vista': 'contact'}, RequestContext(request))	
	
def faq(request):
	faq_dict = []
	try:
		lista = Pregunta.objects.select_related('descripcion').all().order_by('ocurrencias')
		faq = [pregunta for pregunta in lista[10]]
		for question in faq:
			try:
				answer = Respuesta.objects.select_related('descripcion').get(pregunta = question)
				faq_dict[question.descripcion] = answer.descripcion
			except:
				answer = None
	except:
		pass
		
	# if autenticado index2
	return render_to_response('tutor/index1.html', {'vista': 'faq', 'faq':faq_dict}, RequestContext(request))	

def register(request):
	form = RegistroForm()
	# if autenticado index2
	return render_to_response('tutor/index1.html', {'vista': 'register','form':form}, RequestContext(request))	

def register_call(request):

	try:
		name = request.POST.get('name',None)
		lastname = request.POST.get('lastname',None)
		#sex = request.POST.get('sex',None)
		university = request.POST.get('university',None)
		uc = request.POST.get('uc',None)
		#birthdate = request.POST.get('birthdate',None)
		email = request.POST.get('email',None)
		country = request.POST.get('country',None)
		phone = request.POST.get('phone',None)
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)
	except:
		message = "Registration incomplete, please complete required fields"
		return redirect('/register',request,message)
	print "asd ", name, lastname, university, uc, email, country, phone, username, password, "  done"

	try:
		print 'Registrando!'
		user = User.objects.create_user(username, email, password)
		user.first_name = name
		user.last_name = lastname
		user.save()
		print "user there"
	except Exception as e:
		print "error ", e.message
		message = "Registration Error, please try again later"
		return redirect('/register',request,message)
		
	try:
		uni_obj = Universidad.objects.select_related('nombre').get(nombre=university)
	except:
		#Condicionable
		#uni_obj = Universidad(nombre=university)
		#uni_obj.save()
		uni_obj = None
		
	try:	
		profile = UserProfile(user_carnet = uc, user_universidad = uni_obj, user_telefono = phone, user_pais = 1)
		profile.save()
		message = "Registration Complete"
		return redirect('/',request,message)
	except:
		return redirect('/',request)
		
	return redirect('/',request)		
		
def home(request):
	'''
	start = timeit.default_timer()
	#---
	#DEscomentar pdf luego Entity relationship Concepts.pdf
	books = ["db1.pdf","db2.pdf", "fundamentos_er_ere.pdf"]#"Entity relationship Concepts.pdf", "fundamentos_er_ere.pdf"
	texts = []
	
	for book in books:
		pdf = pdf_to_text(settings.BOOKS_URL+book)
		#print "ok ", pdf
		text = normalization(pdf)
		#print "\n\n",text
		# Esta funcion es para preprocesamiento, deberia correrse desde antes de hacer el runserver
		#nltk = clasification(pdf) #A rare black squirrel has become a regular visitor to a suburban garden  --- We saw a little strange dog
		#---
		texts.append(text)
	# Funcion para obtener los valores tfidf por palabra en el/los documento(s)
	tfidf_table(texts,load_stopwords()) #, create_csv = ,True
	
	# Comentando por ahora
	#nltk = nltk_call("A rare squirrel has become a regular visitor to a suburban garden.")
	#sparql_call2()
	#ok = question_process("What is a subclass?")
	#ok = question("What is a subclass?")
	
	stop = timeit.default_timer()
	print stop - start
	'''
	# Para hacer pruebas usar index.html, del resto usar index1.html
	return render_to_response('tutor/index1.html', RequestContext(request))
	
def login_call(request):
	message = '¡Usuario ya se encuentra conectado!'
	if request.user is not None:
		name = request.POST.get('login',None)
		user = authenticate(username = name, password=request.POST.get('password',None))
		print 'Autenticando!'
		if user is not None:
			if user.is_active:
				message = "¡Se ha iniciado sesión!"
				login(request, user)
				#Si desea recordar sesión, cambia el tiempo de expiración a una fecha definida en REMEBER_SESSION_TIME en settings.py
				if request.POST.get('remember_me', False):
					request.session['remember_me']=True
					request.session.set_expiry(settings.REMEMBER_SESSION_TIME)
				#groups = set(user.groups.values_list('name',flat=True))
				#profile = user.get_profile()
				#next = request.POST.get('next',None)
				return redirect('/tutor',request,message)
			else:
				messages.info(request, '¡Su usuario ha sido deshabilitado!')
				#message = "¡Su usuario ha sido deshabilitado!"
				return redirect('/',request)
		else:
			messages.info(request, 'Usuario y/o contraseña incorrectos.')
			#message = "Usuario y/o contraseña incorrectos."
			return redirect('/',request)
	else:
		message = request.user.username
	#return render_to_response('audit/index.html', {'message': message},RequestContext(request))
	return redirect('/',request)
	
def logout_call(request):
	message = 'No ha iniciado sesión en el sistema!'
	if request.user is not None:
		message = 'Se ha cerrado la sesión'
		logout(request)
	#return render_to_response('audit/index.html', {'message': message})
	return redirect('/',request, message)
	
@login_required(login_url='/')
def index(request):
	print request.user.id
	'''
	user = request.user
	profile = user.get_profile()
	groups = set(user.groups.values_list('name',flat=True))
	'''
	return render_to_response('tutor/index2.html', RequestContext(request))

'''	
def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('tutor/detail.html', {'poll': p}, context_instance=RequestContext(request))

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('tutor/results.html', {'poll': p})
	
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('tutor/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('tutor.views.results', args=(p.id,)))	
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))
'''