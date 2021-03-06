# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Basic questions for DBpedia.
"""

from refo import Group, Plus, Question
from quepy.parsing import Lemma, Pos, QuestionTemplate, Token, Particle, \
                          Lemmas
from quepy.dsl import HasKeyword, IsRelatedTo, HasType
from dsl import DefinitionOf, LabelOf, IsPlace, \
    UTCof, LocationOf, IsRepresented, Defines, Contains, HasName


# Openings
LISTOPEN = Lemma("list") | Lemma("name")


class Thing(Particle):
    regex = Question(Pos("JJ")) + (Pos("NN") | Pos("NNP") | Pos("NNS")) |\
            Pos("VBN")

    def interpret(self, match):
        return HasKeyword(match.words.tokens)


class WhatIs(QuestionTemplate):
    """
    Regex for questions like "What is a database?
    Ex: "What is a entity"
    """

    regex = Lemma("what") + Lemma("be") + Question(Pos("DT")) + \
        Thing() + Question(Pos("."))

    def interpret(self, match):
        label = DefinitionOf(match.thing)

        return label, "define"

class HowIsRepresented(QuestionTemplate):
    """
    Regex for questions like "How is represented an entity?
    Ex: "How is represented an entity"
    """
	#print Lemma("represented")
    regex = Pos("WRB") + Token("is") + Token("represented") + Question(Pos("DT")) + \
        Thing() + Question(Pos("."))

    def interpret(self, match):
        label = IsRepresented(match.thing)
		#rep = LabelOf(label)
        return label, "define"		

class WhatDefines(QuestionTemplate):
    """
    Regex for questions like "What does define a entity_relationship_model?
    Ex: "What does define a entity_relationship_model?"
        "What is Seinfield?"
    """

    regex = Lemma("what") + Token("does") + Token("define") + Question(Pos("DT")) + \
        Thing() + Question(Pos("."))

    def interpret(self, match):
        label = Defines(match.thing)

        return label, "define"	

class WhatContains(QuestionTemplate):
    """
    Regex for questions like "What does a multivalued_attribute contains?
    Ex: "What is a car"
        "What is Seinfield?"
    """

    regex = Lemma("what") + Token("does") + Question(Pos("DT")) + \
        Thing() + Token("contains") + Question(Pos("."))

    def interpret(self, match):
        label = Contains(match.thing)

        return label, "define"	
		
class ListEntity(QuestionTemplate):
    """
    Regex for questions like "List Microsoft software"
    """

    entity = Group(Pos("NNP"), "entity")
    target = Group(Pos("NN") | Pos("NNS"), "target")
    regex = LISTOPEN + entity + target

    def interpret(self, match):
        entity = HasKeyword(match.entity.tokens)
        target_type = HasKeyword(match.target.lemmas)
        target = HasType(target_type) + IsRelatedTo(entity)
        label = LabelOf(target)

        return label, "enum"


class WhatTimeIs(QuestionTemplate):
    """
    Regex for questions about the time
    Ex: "What time is it in Cordoba"
    """

    nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))
    place = Group(nouns, "place")
    openings = (Lemma("what") +
        ((Token("is") + Token("the") + Question(Lemma("current")) +
        Question(Lemma("local")) + Lemma("time")) |
        (Lemma("time") + Token("is") + Token("it")))) | \
               Lemma("time")
    regex = openings + Pos("IN") + place + Question(Pos("."))

    def interpret(self, match):
        place = HasKeyword(match.place.lemmas.title()) + IsPlace()
        utc_offset = UTCof(place)

        return utc_offset, "time"


class WhereIsQuestion(QuestionTemplate):
    """
    Ex: "where in the world is the Eiffel Tower"
    """

    thing = Group(Plus(Pos("IN") | Pos("NP") | Pos("NNP") | Pos("NNPS")),
                  "thing")
    regex = Lemma("where") + Question(Lemmas("in the world")) + Lemma("be") + \
        Question(Pos("DT")) + thing + Question(Pos("."))

    def interpret(self, match):
        thing = HasKeyword(match.thing.tokens)
        location = LocationOf(thing)
        location_name = LabelOf(location)

        return location_name, "enum"
