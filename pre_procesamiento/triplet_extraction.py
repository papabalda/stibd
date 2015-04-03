#A sentence (S) is represented by the parser as a tree having
#three children: a noun phrase (NP), a verbal phrase (VP)
#and the full stop (.). The root of the tree will be S.
from collections import defaultdict, deque
import nltk
#NLTK 
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.tree import *

def search(tree):
	#print "\n aux, ",tree
	return (child for child in tree if type(child) is nltk.Tree)

def search_np(tree):
	#print "\n aux, ",tree
	return (child for child in tree if child.label()=='NP')

def search_vp(tree):
	#print "\n aux, ",tree
	return (child for child in tree if child.label()=='VP')
	
# Construye un 	
def breadth_first(tree, children=iter, maxdepth=-1):
    """Traverse the nodes of a tree in breadth-first order.
    (No need to check for cycles.)
    The first argument should be the tree root;
    children should be a function taking as argument a tree node
    and returning an iterator of the node's children.
    """
    queue = deque([(tree, 0)])
    #print "asd"

    while queue:
        node, depth = queue.popleft()
        yield node

        if depth != maxdepth:
            try:
                queue.extend((c, depth + 1) for c in children(node))
                #print "bbbb"
            except Exception as e:
                #print "aa ", e.message
                pass
				
def TRIPLET_EXTRACTION_FROM_TEXT(text_sentence):
			
	try:
		
		print "triplet extraction"
		#sentence = pos_tag(word_tokenize("An interesting squirrel has become a regular visitor to a small garden."))
		sentence = pos_tag(word_tokenize(text_sentence))
		#print sentence
		grammar = """
		NP: {<DT>?<JJ>*<NN><PP>?} 
		PP: {<IN><NP>|<TO><NP>}
		VP: {<VB.*|VP><NP><PP>|<VB.*><VP>+} 
		""" # expresion regular dt opcional, seguido de cualquier cantidad de jj y nn  <VB.*|VP><NP|PP>+
		
		# Chunk sequences of DT, JJ, NN # Chunk prepositions followed by NP # Chunk verbs and their arguments
		cp = nltk.RegexpParser(grammar, loop=3)
		# Obtenemos el chunk tree 
		result = cp.parse(sentence)
		
		#EXTRACT_SUBJECT
		np_subtrees = breadth_first(result,search_np)
		for subtree in np_subtrees:
			if subtree.label()=='NP':
				subject, attributes = EXTRACT_SUBJECT(subtree)
				break
				
		#EXTRACT_PREDICATE		
		vp_subtrees = breadth_first(result,search)
		for subtree in vp_subtrees:
			if subtree.label()=='VP':
				for a in subtree:
					if type(a) is tuple:
						word,tag = a
						if 'VB' in tag:
							predicate = word

		#EXTRACT_OBJECT
		found = False
		for tree in result:
			if type(tree) is nltk.Tree:
				if tree.label()=='VP':
					for subtree in tree.subtrees(filter=lambda x: x.label() == 'NP' or x.label() == 'PP'):
						for leave in subtree:
							if type(leave) is tuple:
								word,tag = leave
								if 'NN' in tag:
									object = word
									found = True
									break
						if found:
							break
						print "\n subtree del vp ", subtree
			if found:
				break
		
		# Obtenemos NP_subtree, VP_subtree y VP_siblings
		result = (subject, predicate, object)#EXTRACT_OBJECT(VP_siblings)
	except:
		print "error"
		return None
	return result

# Funcion para extraer tripletas usando ya el procesamiento con lematizacion y diccionarios en lugar del basico nltk	
def TRIPLET_EXTRACTION(sentence_of_tuples):
			
	try:
		sentence = []
		for (word,lemma,tag_array) in sentence_of_tuples:
			sentence.append((lemma,tag_array[0]))
			
		print "triplet extraction"
		print sentence, "\n"
		grammar = """
		NP: {<DT>?<JJ>*<NN><PP>?} 
		PP: {<IN><NP>|<TO><NP>}
		VP: {<VB.*|VP><NP><PP>|<VB.*><VP>+} 
		""" # expresion regular dt opcional, seguido de cualquier cantidad de jj y nn  <VB.*|VP><NP|PP>+
		
		# Chunk sequences of DT, JJ, NN # Chunk prepositions followed by NP # Chunk verbs and their arguments
		cp = nltk.RegexpParser(grammar, loop=3)
		# Obtenemos el chunk tree 
		result = cp.parse(sentence)
		
		#EXTRACT_SUBJECT
		np_subtrees = breadth_first(result,search_np)
		for subtree in np_subtrees:
			if subtree.label()=='NP':
				subject, attributes = EXTRACT_SUBJECT(subtree)
				break
				
		#EXTRACT_PREDICATE		
		vp_subtrees = breadth_first(result,search)
		for subtree in vp_subtrees:
			if subtree.label()=='VP':
				for a in subtree:
					if type(a) is tuple:
						word,tag = a
						if 'VB' in tag:
							predicate = word

		#EXTRACT_OBJECT
		found = False
		for tree in result:
			if type(tree) is nltk.Tree:
				if tree.label()=='VP':
					for subtree in tree.subtrees(filter=lambda x: x.label() == 'NP' or x.label() == 'PP'):
						for leave in subtree:
							if type(leave) is tuple:
								word,tag = leave
								if 'NN' in tag:
									object = word
									found = True
									break
						if found:
							break
						print "\n subtree del vp ", subtree
			if found:
				break
		
		# Obtenemos NP_subtree, VP_subtree y VP_siblings
		result = (subject, predicate, object)#EXTRACT_OBJECT(VP_siblings)
	except:
		print "error"
		return None
	return result
	
def EXTRACT_ATTRIBUTES(word):
	''' 
	try:
		# search among the words siblings
			if adjective(word):
				result = all RB siblings
			else:
				if noun(word):
					result = all DT, PRP$, POS, JJ, CD, ADJP, QP, NP siblings #adjective phrase, Quantifier phrase, noun phrase
				else:
					if verb(word):
						result = all ADVP siblings #adverb phrase ..ej He graduated [AdvP very recently]
						
		# search among the words uncles
			if noun(word) or adjective(word):
				if uncle = PP: # prepositional phrases ..ej than his brother de la adjp taller than his brother
					result = uncle subtree
				else
					if verb(word) and (uncle = verb):
						result = uncle subtree
	except:
		print "error"
		return false
	return result
	'''
	
def EXTRACT_SUBJECT(NP_subtree):
	
	try:
		for (word,tag) in NP_subtree:
			if 'NN' in tag:
				subject = word
				break	
				
		subjects = [word for (word,tag) in NP_subtree if 'NN' in tag]		
		subject = subjects[0]
		subjectAttributes = "" #EXTRACT_ATTRIBUTES(subject)
		result = subject, subjectAttributes
	except:
		print "error"
		return None
	return result
	
def EXTRACT_PREDICATE(VP_subtree):
	'''
	try:
		predicate = deepest verb found in VP_subtree
		predicateAttributes = EXTRACT_ATTRIBUTES(predicate)
		result = predicate union predicateAttributes
	except:
		print "error"
		return false
	return result
	'''
def EXTRACT_OBJECT(VP_sbtree):
	'''
	try:
		siblings = find NP, PP and ADJP siblings of VP_subtree
		for each value in siblings:
			if value = NP or PP:
				object = first noun in value
			else
				object = first adjective in value
			objectAttributes = EXTRACT_ATTRIBUTES(object)
		result = object union objectAttributes
	except:
		print "error"
		return false
	return result
	'''
	
def main():
	print "triplet extraction"
	sentence = pos_tag(word_tokenize("An interesting squirrel has become a regular visitor to a small garden."))
	#sentence = [("Mary", "NN"), ("saw", "VBD"), ("the", "DT"), ("cat", "NN"), ("sit", "VB"), ("on", "IN"), ("the", "DT"), ("mat", "NN")]
	grammar = """
	NP: {<DT>?<JJ>*<NN>+<PP>?} 
	PP: {<IN><NP>|<TO><NP>}
	VP: {<VB.*|VP><NP><PP>|<VB.*><VP>+} 
	""" # expresion regular dt opcional, seguido de cualquier cantidad de jj y nn  <VB.*|VP><NP|PP>+
	'''
 
	'''
	# Chunk sequences of DT, JJ, NN # Chunk prepositions followed by NP # Chunk verbs and their arguments
	cp = nltk.RegexpParser(grammar, loop=3)
	result = cp.parse(sentence)
	#result.draw()
	#print "funcion ", aux, type(result) is nltk.Tree
	found = False
	for tree in result:
		if type(tree) is nltk.Tree:
			if tree.label()=='VP':
				for subtree in tree.subtrees(filter=lambda x: x.label() == 'NP' or x.label() == 'PP'):
					for leave in subtree:
						if type(leave) is tuple:
							word,tag = leave
							if 'NN' in tag:
								object = word
								found = True
								break
					if found:
						break
					print "\n subtree del vp ", subtree
		if found:
			break					
	print "DONE ", object				
	'''
	trees = breadth_first(result,search)
	for subtree in trees:
		if subtree.label()=='VP':
			print subtree
			
			for a in subtree:
				print type(a)
				if type(a) is tuple:
					word,tag = a
					print tag, word
					if 'VB' in tag:
						sentence = word
		
	print "DONE ", sentence
	
	queue = deque([(result, 0)])
	print "\n queue, ",queue
	node, depth = queue.popleft()
	print "\n node, ",node, "\n queue, ", queue
	queue.extend((c, depth + 1) for c in aux(node))
	
	for a in node:
		if type(a) is nltk.Tree:
			print "\n a, ", a
	
	print queue[0], "\n", queue[1]
	'''
#print TRIPLET_EXTRACTION_FROM_TEXT("Entity relationship model is the conceptual view of database.")	
#print TRIPLET_EXTRACTION_FROM_TEXT("An interesting squirrel has become a regular visitor to a small garden.")	
#print TRIPLET_EXTRACTION("It works around real world entity and association among them")
#main()	
'''
from nltk.corpus import wordnet
for word,tag in wordnet.tagged_words():
	if 'defines' in word:
		print word,tag
'''		
