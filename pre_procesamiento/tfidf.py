from __future__ import division, unicode_literals
import math
from textblob import TextBlob as tb
from pre_procesamiento.functions import to_file
#from progress.bar import Bar
from collections import defaultdict
import itertools
import timeit
 
def tf(word, blob):
	return blob.words.count(word) / len(blob.words)
 
def n_containing(word, bloblist):
	return sum(1 for blob in bloblist if word in blob)
 
# el denominador nunca deberia ser 0 ya que se estan procesando las palabras DE LA BLOBLIST 
def idf(word, bloblist):
	return math.log(1 + (len(bloblist) / ( 1 + n_containing(word, bloblist))))
	
def tfidf(word, blob, bloblist):
	return tf(word, blob) * idf(word, bloblist)

def report(so_far, total_size, text):

    percent = float(so_far) / total_size
    percent = round(percent * 100, 2)
    print "Progress on '{0}':  {1} of {2}  {3:3.2g}% \r".format(text, so_far, total_size, percent)
										
# funcion que reciba lla lista de documentos, regresa el diccionario palabra y valor tfidf	
def tfidf_table(doc_list, stoptext, create_csv = True):	
		#import csv
		#c = csv.writer(open("MYFILE.csv", "wb"))
	stopwords = tb(stoptext)	
	# Obtenemos lista de textos procesados con textblob 
	textlist = [tb(doc) for doc in doc_list]
	for j, text in enumerate(textlist):
		print "texto ",str(j+1)
		if create_csv:
			data = ""
			i = 0
		# Obtenemos los valores tfidf para cada palabra y las ordenamos acorde a este valor
		scores = {word: tfidf(word, text, textlist) for word in text.words if word not in stopwords.words	}
		sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
		for word, score in sorted_words:
			if create_csv:
				data += '{},"{}","{}"\n'.format(i, word, round(float(score), 5))
				#c.writerow([str(i),str(word),str(round(score, 5))])
				i+=1
			else:	
				pass
				#print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))	
		if create_csv:
			#pass
			to_file(data, "tfidf_data"+str(j+1)+".csv")
		
		try:
			word_list = [word for word,score in sorted_words[:19] ]#if score > umbral
		except:
			print "error word list"
			word_list = [word for word,score in sorted_words[:10] ]
		
		key_terms = get_key_terms(word_list)
		terms_table = key_terms_table(key_terms, [text], j)
		get_keywords([text], terms_table, word_list, j)
		#print "\n\n",key_terms, "\ncount ", len(key_terms)
	#return sorted_words
		
def get_key_terms(word_list):
	start = timeit.default_timer()
	
	'''
	term_list = [w1+' '+w2 for w1,w2 in itertools.permutations(word_list,2)]
	term_list += [w1+' '+w2+' '+w3 for w1,w2,w3 in itertools.permutations(word_list,3)]
	'''
	clon_list = word_list
	term_list = []
	ternary_list = []
	# obtener 2 o 3-permutaciones de word list, luego buscarlas en los archivos
	for word in word_list:
		clon_list.remove(word)
		for other_word in clon_list:
			term_list.append((word, other_word, word+' '+other_word))	
			ternary_list.append(word+' '+other_word)		
		clon_list.append(word)	
	for w1,w2,tuple in term_list:
		clon_list.remove(w1)
		clon_list.remove(w2)
		for w3 in clon_list:
			ternary_list.append(tuple+' '+w3)
		clon_list.append(w1)	
		clon_list.append(w2)	
	#term_list += ternary_list
	
	stop = timeit.default_timer()
	print stop - start
	return ternary_list #term_list
	
def countTerms(words,term_list):
	# Inicializando en 0
	countDict = defaultdict(int)
	n = 2 # para los terminos compuestos de 2 palabras
	for i in range(len(words)-n+1):
		key = ' '.join(words[i:i+n])
		if key in term_list:
			countDict[key] = countDict[key] + 1
	n = 3 # para los terminos compuestos de 3 palabras	
	for i in range(len(words)-n+1):
		key = ' '.join(words[i:i+n])
		if key in term_list:
			countDict[key] = countDict[key] + 1
	
	return countDict
    	
def key_terms_table(term_list, textlist, j, create_csv = True):
	if create_csv:
		data = ""
		i = 0
	for text in textlist:#1
		#print("\nTop words in document: ")
		# Obtenemos la frecuencia para cada termino y las ordenamos acorde a este valor
		scores = countTerms(text.words,term_list)
		sorted_terms = sorted(scores.items(), key=lambda x: x[1], reverse=True)
		for term, score in sorted_terms:
			if create_csv:
				data += '{},"{}","{}"\n'.format(i, term, score)
				#c.writerow([str(i),str(term),str(score)])
				i+=1
			else:	
				print("Term: {}, Frequency: {}".format(term, score))	
		if create_csv:
			to_file(data, "data_terms"+str(j+1)+".csv")		
			#pass
	return sorted_terms

# this wont be here	
def get_keywords(textlist, key_terms, word_list, j, create_csv = True):
	if create_csv:
		data = ""
		i = 0
		#import csv
		#c = csv.writer(open("MYFILE.csv", "wb"))
	# key_terms = (key for key, freq in key_terms if freq > 0)
	# Obtenemos lista de textos procesados con textblob 
	#textlist = [tb(doc) for doc in doc_list]
	for text in textlist:
		print "sentence COUNT", len(text.sentences)
		for k,sentence in enumerate(text.sentences):
			if k < 2:
				print "sentence ", sentence
			# Obtenemos las keywords incluidas en la oracion
			keywords0 = (key for key in word_list if key in sentence) # palabras (1)
			keywords = (key for key, freq in key_terms if key in sentence and freq > 0) # frases(2 o 3 palabras)
			csv_text = ''
			for keyword in keywords:
				csv_text += '"{}",'.format(keyword)#join 
			if csv_text is not '':	
				#print csv_text	
				pass
			for words in keywords0:
				csv_text += '"{}",'.format(words)#join 
			if create_csv:
				data += '{},"{}",{}\n'.format(i, sentence, csv_text)
				#c.writerow([str(i),str(sentence),str(keywords)])
				i+=1
			else:	
				print("Sentence: {}, Keywords: {}".format(sentence, csv_text))	
	if create_csv:
		to_file(data, "data_sentences"+str(j+1)+".csv")		
		#pass
	
def main():
	document1 = tb("""Python is a 2000 made-for-TV horror movie directed by Richard
	Clabaugh. The films features several cult favorite actors, including William
	Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy,
	Keith Coogan, Robert Englund (best known for his role as Freddy Krueger in the
	A Nightmare on Elm Street series of films), Dana Barron, David Bowe, and Sean
	Whalen. The films concerns a genetically engineered snake, a python, that
	escapes and unleashes itself on a small town. It includes the classic final
	girl scenario evident in films like Friday the 13th. It was filmed in Los Angeles,
	California and Malibu, California. Python was followed by two sequels: Python
	II (2002) and Boa vs. Python (2004), both also made-for-TV films.""")
	 
	document2 = tb("""Python, from the Greek word (p????/p????a?), is a genus of
	nonvenomous pythons[2] found in Africa and Asia. Currently, 7 species are
	recognised.[2] A member of this genus, P. reticulatus, is among the longest
	snakes known.""")
	 
	document3 = tb("""The Colt Python is a .357 Magnum caliber revolver formerly
	manufactured by Colt's Manufacturing Company of Hartford, Connecticut.
	It is sometimes referred to as a "Combat Magnum".[1] It was first introduced
	in 1955, the same year as Smith & Wesson's M29 .44 Magnum. The now discontinued
	Colt Python targeted the premium revolver market segment. Some firearm
	collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy
	Thompson, Renee Smeets and Martin Dougherty have described the Python as the
	finest production revolver ever made.""")
	 
	bloblist = [document1, document2, document3]
	for i, blob in enumerate(bloblist):
		print("Top words in document {}".format(i + 1))
		scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
		sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
		for word, score in sorted_words[:3]:
			print("Word: {}, TF-IDF: {}".format(word, round(score, 5))) 
#main()			