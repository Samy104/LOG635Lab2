# -*- coding: utf-8 -*-

import nltk
import re
from nltk import *

historyPron = {"masc": {"sing":"nom", "plur":"nom"},
            "fem": {"sing":"nom", "plur":"nom"},
            "glob":"nom"}

with open ("lexic.txt", "r") as myfile:
    grammaireText=myfile.read()
    
with open("ruleset.txt", "r") as mytext:
    translateText=mytext.read()

def gType(self):
    return self.label().items()[-1][1]
Tree.gType = gType

def translate(text):
    toTranslate = ""
    if text.find("ambassade") != -1:
        content = text.split('(')[2].split(',')
        pays = content[0].replace(')','')
        place = content[1].replace(')','')
        toTranslate = "(ambassade " + pays +" "+place+")"
    elif text.find("marie") != -1:
        couple = text.split('(')[1].replace(')','').split(',')
        p1 = couple[0]
        p2 = couple[1]
        toTranslate = "(marie " + p1 + " " + p2+")"
    elif text.find("enfant") != -1:
        couple = text.split('(')[1].replace(')','').split(',')
        p1 = couple[0]
        p2 = couple[1]
        toTranslate = "(enfant " + p1 + " " + p2+")"
    elif text.find("allie") != -1:
        couple = text.split('(')[1].replace(')','').split(',')
        p1 = couple[0]
        p2 = couple[1]
        toTranslate = "(alliance " + p1 + " " + p2+")"
    elif text.find("location") != -1:
        #arrayLocation = text.split('(')
        #personne = text.split(')')[1].split(')')[0]
        #location = arrayLocation[1].split(',')[0]
        #timeRange = arrayLocation[2].replace('))','').split(',')
        #t1 = timeRange[0]
        #t2 = timeRange[1]
        splitted = text.replace('(',' ').replace(',',' ').replace(')',' ')
        text2 = splitted.split(' ')
        print "(personne-at " + text2[6] + " " + text2[1] + " from-t " + text2[3] + " to-t " +text2[4] +")"
        toTranslate = "(personne-at " + text2[6] + " " + text2[1] + " from-t " + text2[3] + " to-t " +text2[4] +")"
    elif text.find("travailler") != -1:
        content = text.split('(')[1].split(',')
        personne = content[0]
        location = content[1].replace(")","")
        toTranslate = "(personne-travaille " + personne + " " + location + ")"
    elif text.find("amant") != -1:
        couple = text.split('(')[1].replace(')','').split(',')
        p1 = couple[0]
        p2 = couple[1]
        toTranslate = "(amant " + p1 + " " + p2+")"
    elif text.find("associe") != -1:
        couple = text.split('(')[1].replace(')','').split(',')
        p1 = couple[0]
        p2 = couple[1]
        toTranslate = "(associe " + p1 + " " + p2+")"
    #elif text.find("impact") != -1:
    #    toTranslate = text.replace("impact(","(impact ").replace(',',' ')
    elif text.find ("impact") != -1:
        splitted = text.replace('(',' ').replace(',',' ').replace(')',' ')
        text2 = splitted.split(' ')
        toTranslate = "("+text2[1] + " " + text2[2] + " " + text2[3] + " " + text2[5] + ")"
    elif text.find ("tourcellulaire") != -1:
        splitted = text.replace('(',' ').replace(',',' ').replace(')',' ')
        text2 = splitted.split(' ')
        toTranslate = "(tour-cellulaire " + text2[2] + " " + text2[4] + ")"
    if text.find("--") != -1:
        toTranslate = "(not" + toTranslate + ")"
    return toTranslate
    
        
def depronomise(tree):
    sentence = str(tree.label()['SEM'])
    sentence = findNames(tree, sentence)
    return sentence
        
def findNames(tree, sentence):
    try:
        genre = str(tree.label()['GENRE'])
        num = str(tree.label()['NUM'])
        if genre != '?g' and num != '?n':
            if tree.gType() == 'Nom' :
                historyPron[genre][num] = str(tree.label()['SEM'])
                historyPron["glob"] = str(tree.label()['SEM'])
                print "-Found Nom %s with genre %s and num %s" % (historyPron[genre][num],genre,num)
                return sentence
            elif tree.gType() == "Pronom" :
                print "-Replaced Pronom with genre %s and num %s" % (genre, num)
                sentence = sentence.replace('pronom', historyPron[genre][num])
                return sentence
            elif tree.gType() == "PronRel" :
                print "-Replaced PronRel with genre %s and num %s" % (genre, num)
                sentence = sentence.replace('pronom', historyPron["glob"])
                return sentence
    except(KeyError):
        pass
    for t in tree:
        if(isinstance(t, Tree)):
            sentence = findNames(t, sentence)
    return sentence

def getSubTrees(fullTree):
    # Phrases de forme ___ et ___. On trouve deux S que l'on va traiter indépendament
    subtrees = []
    for t in fullTree:
        if(t.gType() == "S"):
            subtrees.append(t)
    if(len(subtrees) == 0):
        subtrees.append(fullTree)
        
    # Find GVR sentences
    gvr = list(subtrees)
    for tree in subtrees:
        for i, t in enumerate(tree):
            if(t.gType() == "GVR"):
                gvr.append(t)
                del tree[i]
            
    return gvr
    
def unAggregate(sentence):
    newSub = []
    print sentence
    m = re.search("(.*?)\(aggregate\((.*?)\)\)", sentence)
    if (m != None):
        newSub.append(re.sub("(.*?)\(aggregate\((.*?)\)\)", m.group(1)+"("+m.group(2)+")", sentence))
    #if (sentence.find("marie") != -1) and (sentence.find("aggregate") != -1):
    #    m = re.search("aggregate\((.*?)\)",sentence)
        
        
    elif sentence.find("aggregate") != -1:
        m = re.search("aggregate\((.*?)\)",sentence)
        noms = m.group(1).split(",")
        for val in noms:
            newSub.append(re.sub("aggregate\((.*?)\)", val, sentence))
    else:
        newSub.append(sentence)
    return newSub

persons = {'Arnold Schwarzenegger':'ArnoldSchwarzenegger',
    'Jenna Jameson':'JennaJameson',
    'Kim Kardashian':'KimKardashian',
    'Justin Bieber':'JustinBieber',
    'Michael Jackson':'MichaelJackson',
    'Katy Perry':'KatyPerry',
    'Jacky Chan':'JackyChan',
    'Johnny Cash':'JohnnyCash'}
pays = {'Coree du Nord':'CoreeduNord',
    'Royaume Uni':'royaumeuni'}
lieux = {'Tokyo Beach':'TokyoBeach',
    'Downtown Tokyo':'DowntownTokyo',
    'Tokyo Stadium':'TokyoStadium',
    'Tokyo Park':'TokyoPark',
    'Tokyo Port':'TokyoPort',
    'Tokyo Cinema':'TokyoCinema',
    'Tokyo Broadcast Station':'TokyoBroadcastStation',
    'Residential Tokyo':'ResidentialTokyo',
    'Cyber Cafe':'CyberCafe',
    'Gas Station':'GasStation'}

for p in persons:
    translateText = translateText.replace(p, persons[p])
for p in pays:
    translateText = translateText.replace(p, pays[p])
for l in lieux:
    translateText = translateText.replace(l, lieux[l])

translateText = translateText.lower()
translateText = translateText.replace(',', ' ,')
translateText = translateText.replace("'", "' ")
translateText = translateText.replace("é", "e")
translateText = translateText.replace("è", "e")
translateText = translateText.replace("ê", "e")
translateText = translateText.replace("à", "a")
translateText = translateText.replace("â", "a")
translateText = translateText.replace("ç", "c")
translateText = translateText.replace("ô", "o")


gr = grammar.FeatureGrammar.fromstring(grammaireText)
parser = nltk.ChartParser(gr)

arraySentence = re.split('\.', translateText)
finalSem = []
unfoundSentences = []
ambigueSentences = []
print(arraySentence)
for sent in arraySentence:
    print(sent)
    tokens = sent.lower().split()
    parser = parse.FeatureEarleyChartParser(gr)
    trees = parser.parse(tokens)
    numTrees = 0
    for fullTree in trees:
        numTrees+=1
        if(numTrees > 1):
            ambigueSentences.append(sent)
        #print(fullTree)
        subTrees = getSubTrees(fullTree)
        print "------ %d subsentences" % len(subTrees)
        for i, tree in enumerate(subTrees):
            if(i > 0):
                print "---"
            print("SEM: "+ str(tree.label()["SEM"]))
            translation = depronomise(tree)
            print("Depronominized : " + translation)
            unaggregated = unAggregate(translation)
            for j, sentence in enumerate(unaggregated):
                print "Unaggregationized %d : %s" % (j,sentence)
                sentence = translate(sentence)
                print(" Jessized : " + sentence)
                if sentence not in finalSem:
                    finalSem.append(sentence)
    if(numTrees == 0 and len(sent) > 0):
        unfoundSentences.append(sent)

if(len(unfoundSentences) != 0):
    print "------------Not all sentences were found-------------"
    print unfoundSentences
else:
    print "-- All is well --"
if(len(ambigueSentences) != 0):
    print "-- Grammaire ambigue --"
    print ambigueSentences

print "--------- JESS Output ----------"
for s in finalSem:
    print s