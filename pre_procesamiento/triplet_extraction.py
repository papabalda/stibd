#A sentence (S) is represented by the parser as a tree having
#three children: a noun phrase (NP), a verbal phrase (VP)
#and the full stop (.). The root of the tree will be S.

def TRIPLET_EXTRACTION(sentence):
	try:
		# Obtenemos NP_subtree, VP_subtree y VP_siblings
		result = [EXTRACT_SUBJECT(NP_subtree), EXTRACT_PREDICATE(VP_subtree), EXTRACT_OBJECT(VP_siblings)]
	except:
		print "error"
		return false
	return result

def EXTRACT_ATTRIBUTES(word):
	try:
		// search among the word’s siblings
			if adjective(word):
				result = all RB siblings
			else:
				if noun(word):
					result = all DT, PRP$, POS, JJ, CD, ADJP, QP, NP siblings #adjective phrase, Quantifier phrase, noun phrase
				else:
					if verb(word):
						result = all ADVP siblings #adverb phrase ..ej He graduated [AdvP very recently]
						
		// search among the word’s uncles
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

	
def EXTRACT_SUBJECT(NP_subtree):
	try:
		subject = first noun found in NP_subtree
		subjectAttributes = EXTRACT_ATTRIBUTES(subject)
		result = subject union subjectAttributes
	except:
		print "error"
		return false
	return result
	
def EXTRACT_PREDICATE(VP_subtree):
	try:
		predicate = deepest verb found in VP_subtree
		predicateAttributes = EXTRACT_ATTRIBUTES(predicate)
		result = predicate union predicateAttributes
	except:
		print "error"
		return false
	return result
	
def EXTRACT_OBJECT(VP_sbtree):
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