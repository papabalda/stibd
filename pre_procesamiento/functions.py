#**** functions.py
#**   Definiciones de Funciones que serviran para el preprocesamiento del texto, de manera
#**   de obtener luego la base de conocimiento del sistema tutorial.

import requests
from tutor.models import *
from django.conf import settings
#NLTK 
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from preprocessing import *
#PDF
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfdevice import PDFDevice
import unicodedata, codecs


# INICIO Funciones para preprocesamiento de texto *******
def pdf_to_text(filename):
	retstr = StringIO()
	try:
		f = open(filename,'rb')
	except:
		print "Error opening ", filename
		return ''
	parser = PDFParser(f)
	try:
		document = PDFDocument(parser)
	except Exception as e:
		print(filename,'is not a readable pdf')
		return ''
	if document.is_extractable:
		rsrcmgr = PDFResourceManager()
		device = TextConverter(rsrcmgr,retstr, codec='ascii' , laparams = LAParams())
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		for page in PDFPage.create_pages(document):
			interpreter.process_page(page)
		f.close()
		device.close()
		return retstr.getvalue()
	else:
		f.close()
		print(filename,"Warning: could not extract text from pdf file.")
		return ''

def to_file(text, filename):
	file = open(filename, 'w')
	file.write(text)
	print "creado archivo ", filename
	file.close()
	
def to_arff(filename):
	text = '0, '
	file = open('LARCTREN.txt', 'r')
	arff_file = open(filename, 'w')
	data = file.readlines()
	i = 0
	for line in data:
		word_tuple_list = line.split(')')
		for tuple in word_tuple_list:
			if 'stopWord' not in tuple:
				stuff = tuple.split(',')
				try:
					tuple_index = word_tuple_list.index(tuple)
					if tuple_index == 0:
						lemma = stuff[1]
					else:
						lemma = stuff[2]
				except:
					lemma = ''
				if "'.'" not in lemma:
					text = text + lemma + ' '
		i = i+1		
		text = text + '\n' + str(i) + ', '
	text = text.replace("u'", "") 	
	text = text.replace("'", "") 	
	arff_file.write(text)
	print "creado archivo ", filename
	file.close()
	arff_file.close()
	
def nltk_call(big_text):
	'''
	Funcion que toma las fuentes de conocimiento en forma de texto, y luego con nltk hace preprocesamiento para llevarlo a tripletas
	
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
	#Chunking NP!'''
	
	#sentence = pos_tag(word_tokenize("Mary saw the cat sit on the mat."))
	sentence = [("Mary", "NN"), ("saw", "VBD"), ("the", "DT"), ("cat", "NN"), ("sit", "VB"), ("on", "IN"), ("the", "DT"), ("mat", "NN")]
	#grammar = "NP: {<DT>?<JJ>*<NN>} VP: {<VB.*><NP>+$} " # expresion regular dt opcional, seguido de cualquier cantidad de jj y nn
	grammar = r"""NP: {<DT|JJ|NN.*>+} 
	PP: {<IN><NP>} 
	VP: {<VB.*><NP|PP|CLAUSE>+\$} 
	CLAUSE: {<NP><VP>} """   
	# Chunk sequences of DT, JJ, NN # Chunk prepositions followed by NP # Chunk verbs and their arguments
	cp = nltk.RegexpParser(grammar, loop=2)
	result = cp.parse(sentence)
	#result.draw()
	print "algo ", result
	#print "algo postag", pos_tag(word_tokenize(big_text))
	text = "The increase will cover all kinds of wheat including durum and milling wheat."
	#text = """What can I say about this place. The staff of the restaurant is nice and the eggplant is not bad. Apart from that, very uninspired food, lack of atmosphere and too expensive. I am a staunch vegetarian and was sorely dissapointed with the veggie options on the menu. Will be the last time I visit, I recommend others to avoid."""
	splitter = Splitter()
	postagger = POSTagger()
	splitted_sentences = splitter.split(big_text)
	#print "\n", splitted_sentences
	pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
	#print "\n", pos_tagged_sentences cleaner positive

	dicttagger = DictionaryTagger([ settings.YML_ROOT+'cleaner.yml'])
	dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)	
	to_file('\n'.join(map(str, dict_tagged_sentences)), "data.txt")
	to_arff("data.csv")
	#print dict_tagged_sentences
	return True


def getPDFText(pdfFilenamePath):
	retstr = StringIO()
	parser = PDFParser(open(pdfFilenamePath,'rb'))
	try:
		document = PDFDocument(parser)
	except Exception as e:
		print(pdfFilenamePath,'is not a readable pdf')
		return ''
	print "Leyendo archivo ", pdfFilenamePath
	if document.is_extractable:
		rsrcmgr = PDFResourceManager()
		device = TextConverter(rsrcmgr,retstr, codec='ascii' , laparams = LAParams())
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		for page in PDFPage.create_pages(document):
			interpreter.process_page(page)
		return retstr.getvalue()
	else:
		print(pdfFilenamePath,"Warning: could not extract text from pdf file.")
		return ''	
		


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str		
#FIN Funciones para preprocesamiento de texto	*******