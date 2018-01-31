'''
Command to run this python file: 

	$python3.4 pcfg_create_improved.py parses.train hw4_improved.pcfg

'''


import sys
import os
import re
import nltk 
from nltk import Tree

#stores (A,B,C) -> count for binary rules 
#(A,'x') -> count mapping for unit productions
RuleCountDict = {} 
LHSCountDict = {}

#START_SYMBOL= None #initialize start symbol variable with None value
#CountTotalRules = 0.0 #count of total rules in this grammar

def OpenAndReadFile(fileName): 
	'''
	Args: 
		filename(string): filename as a string
	Returns: 
		String: Opens and reads the given file 
	'''
	return open(fileName,"r").read()

def traverseTree(t,parent): 
	'''
	Recursive function to: 
	- traverse the given tree and 
	- populate the RuleCountDict with the rules found in given parse tree
	'''

	LHS = t.label(), parent ## A, Parent label  

	if len(t) == 1: 
		#base case - unit productions
		RHS = "\""+str(t[0])+"\"" , "" #get the word for the terminal symbol
		storeRule(LHS,RHS)	

	else: 
		#binary productions
		RHS = t[0].label(), t[1].label()  #(B,C)
		storeRule(LHS,RHS)	
		traverseTree(t[0],LHS[0]) #traverse next LHS - sending current LHS as the parent
		traverseTree(t[1],LHS[0]) #traverse next RHS - sending current LHS as the parent

def storeRule(thisLHS,thisRHS):
	#increment count for the given rule in the RuleCountDict

	global RuleCountDict
	global CountTotalRules

	if thisLHS in LHSCountDict: 
		LHSCountDict[thisLHS] += 1
	else: 
		LHSCountDict[thisLHS] = 1.0

	#add to the Rule count dict
	thisKey = thisLHS,thisRHS
	if thisKey in RuleCountDict: 
		RuleCountDict[thisKey] += 1 #increment count if rule already counted once
	else: 
		RuleCountDict[thisKey] = 1.0  #add rule and set count to 1, if counted for first time	

	#CountTotalRules +=1	
		
def main(): 
	'''
	Reads in a treebank and outputs a PCFG
	'''
	global CountTotalRules
	global RuleCountDict
	#global START_SYMBOL

	treebank_sentences = OpenAndReadFile(sys.argv[1]).split("\n")

	for sent in treebank_sentences: 
		if sent: #to avoid empty lines
			#sent = treebank_sentences[2]
			t = Tree.fromstring(sent)
			START_SYMBOL = t.label()
			#traverse the parse tree for this sentence and add to the RuleCountDict
			traverseTree(t,None)
	
	#print (RuleCountDict)
	for rule_tuple in RuleCountDict: 
		thisLHS = rule_tuple[0]

		if thisLHS[0] == START_SYMBOL: 
			print ("%start "+str(START_SYMBOL))
			this_prob = str(RuleCountDict[rule_tuple]/LHSCountDict[thisLHS])

			if rule_tuple[1][1] == "": 
				print (str(thisLHS[0]) + "^" +str(thisLHS[1])+ " -> " + str(rule_tuple[1][0]) + " [" + this_prob + "]")
			else: 
				print (str(thisLHS[0]) + " -> " + str(rule_tuple[1][0]) + "^" +thisLHS[0] + " " +str(rule_tuple[1][1] + "^" +thisLHS[0]) +" [" + this_prob + "]")

		else: 

			this_prob = str(RuleCountDict[rule_tuple]/LHSCountDict[thisLHS])

			if rule_tuple[1][1] == "": 
				print (str(thisLHS[0]) + "^" +str(thisLHS[1])+ " -> " + str(rule_tuple[1][0]) + " [" + this_prob + "]")
			else: 
				print (str(thisLHS[0]) + "^" + str(thisLHS[1])+" -> " + str(rule_tuple[1][0]) + "^" +thisLHS[0] + " " +str(rule_tuple[1][1] + "^" +thisLHS[0]) +" [" + this_prob + "]")

if __name__ == "__main__": 
	main()	