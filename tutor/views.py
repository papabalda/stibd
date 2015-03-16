# Create your views here.

import requests
from tutor.models import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.conf import settings
#NLTK 
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
#Preprocesamiento
from pre_procesamiento.functions import *
#from pre_procesamiento.preprocessing import *
from SPARQLWrapper import SPARQLWrapper, JSON
 
def sparql_call():
	#http://localhost:3030/ds/query   http://dbpedia.org/sparql ab: <http://learningsparql.com/ns/addressbook#>
	sparql = SPARQLWrapper("http://localhost:3030/ds/query")
	'''
	sparql.setQuery("""
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	SELECT ?label
	WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
	""")
	'''
	sparql.setQuery("""
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	SELECT * {?s ?p ?o}
	""")	
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	 
	for result in results["results"]["bindings"]:
		try:
			print(result["s"]["value"],result["p"]["value"],result["o"]["value"]) 
		except:
			print "no pude leer esto"
		
# # # TODO Funcion para interpretar las preguntas realizadas y llevarlas a tripletas a cnsultar. Luego usar sparql call y 
# #        finalmente devolver la respuesta
		
def sparql_call2():
	#http://localhost:3030/ds/query   http://dbpedia.org/sparql ab: <http://learningsparql.com/ns/addressbook#>
	sparql = SPARQLWrapper("http://localhost:3030/ds/query")
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
			
def home(request):
	#fundamentos_er_ere convert_pdf_to_txt
	#pdf = pdf_to_text(settings.STATIC_ROOT+"/books/example.pdf")
	#pdf = getPDFText(settings.STATIC_ROOT+"/books/example.pdf")
	#print "ok ", pdf
	#DEscomentar pdf2 luego
	#pdf2 = pdf_to_text(settings.STATIC_ROOT+"/books/example.pdf")
	#print "ok2 ", pdf2
	
	#nltk = nltk_call(pdf2) A rare black squirrel has become a regular visitor to a suburban garden  --- We saw a little strange dog
	
	# Comentando por ahora
	#nltk = nltk_call("A rare squirrel has become a regular visitor to a suburban garden.")
	sparql_call2()
	# Para hacer pruebas usar index.html, del resto usar index1.html
	return render_to_response('tutor/index.html', RequestContext(request))
	
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
	

def index(request):
	return render_to_response('tutor/index2.html', RequestContext(request))

'''	
def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('tutor/detail.html', {'poll': p}, context_instance=RequestContext(request))

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('tutor/results.html', {'poll': p})
'''
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