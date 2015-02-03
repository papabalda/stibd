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
from tutor.preprocessing import *

def nltk_call(big_text):
	'''
	#Vamos a hacer varias pruebas
	print "algo ", sent_tokenize(big_text)
	print "algo ", sent_tokenize("Hello Mr. Anderson. How you doing?")
	#
	print "algo ", word_tokenize("This is NLTK")
	print "algo ", word_tokenize("What's up?")
	#
	print "algo punct ", wordpunct_tokenize("What's up?")
	#Buscar las tag list 
	words = word_tokenize("And now for something completely different")
	print "pos tag ", pos_tag(words)
	#Chunking
	print "algo ", ne_chunk(pos_tag(word_tokenize("My name is John Smith.")))
	'''
	text = """What can I say about this place. The staff of the restaurant is nice and the eggplant is not bad. Apart from that, very uninspired food, lack of atmosphere and too expensive. I am a staunch vegetarian and was sorely dissapointed with the veggie options on the menu. Will be the last time I visit, I recommend others to avoid."""
	splitter = Splitter()
	postagger = POSTagger()
	splitted_sentences = splitter.split(text)
	print "\n", splitted_sentences
	pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
	print "\n", pos_tagged_sentences

	dicttagger = DictionaryTagger([ 'C:/Users/Carlo/Desktop/stibd/tutor/positive.yml', 'C:/Users/Carlo/Desktop/stibd/tutor/negative.yml'])
	dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)	
	print dict_tagged_sentences
	print "score, ", sentiment_score(dict_tagged_sentences)
	return True
	
def home(request):
	nltk = nltk_call("Hello SF Python. This is NLTK")
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