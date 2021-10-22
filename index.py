from flask import Flask, request, render_template
# import PySimpleGUIWeb as sg
import os
import sys
import re




def isThisACommaBelongToIf(cha, is_between_quote, bracket_queue):
	if(cha == ','):
		if is_between_quote:
			return False
		if len(bracket_queue) == 1:
			return True
		else:
			return False

def insertStringToString(targetString, StringToBeInserted, position):
	InsertedString = targetString[:position] + StringToBeInserted + targetString[position:]
	return InsertedString


def insertIndentToFormula(formula_string):
	ToBeInsertedPosition = []
	bracket_queue = []
	is_between_quote = False
	previousBracket = ''
	candidateList = []
	targetBracket = ['(',')','&']
	for i, c in enumerate(formula_string):	
		if(c in targetBracket):
			candidateList.append(c)
	targetCount = 0
	for i, c in enumerate(formula_string):
		if c == '"':
			is_between_quote = not(is_between_quote)		
		if c == '(':
			if candidateList[targetCount+1] != ')':
				ToBeInsertedPosition.append([i,len(bracket_queue)])
			bracket_queue.append(c)
			previousBracket = c
		elif c == ')':
			if candidateList[targetCount-1] != '(':
				ToBeInsertedPosition.append([i-1,len(bracket_queue)-2])
			bracket_queue.pop()
			previousBracket = c
		elif c == ',':
			ToBeInsertedPosition.append([i,len(bracket_queue)-1])
		elif c == '&' and candidateList[targetCount-1] == '&':
			ToBeInsertedPosition.append([i-2,len(bracket_queue)-2])

		if(c in targetBracket):
			targetCount = targetCount + 1
	newFormula = formula_string
	for p in reversed(ToBeInsertedPosition):
		newFormula = insertStringToString(newFormula, '\n'+'	'*(p[1]+1), p[0]+1)
	return newFormula

def stripwhite(text):
    lst = text.split('"')
    for i, item in enumerate(lst):
        if not i % 2:
            lst[i] = re.sub("\s+", "", item)
    return '"'.join(lst)

def autoFormat(formula_string):
	print('origin text', formula_string)
	formula_string = stripwhite(formula_string)
	formula_string = formula_string.replace('\t','').replace('\n','').replace('\r','').replace('&&',' && ').replace('||',' || ')
	bracket_list = ['(', ')']
	bracket_queue = []
	start_position_of_IF = 0
	end_position_of_IF = 0
	is_between_quote = False
	IF_comma_position = []
	formula_string = insertIndentToFormula(formula_string)
	# for i, c in enumerate(formula_string):	
	# 	if c == '"':
	# 		is_between_quote = not(is_between_quote)

	# 	if c == '(':
	# 		if len(bracket_queue) == 0:	 
	# 			start_position_of_IF = i
	# 		bracket_queue.append(c)
	# 	elif c == ')':
	# 		bracket_queue.pop()
	# 		if len(bracket_queue) == 0:	
	# 			end_position_of_IF = i

	# 	if isThisACommaBelongToIf(c, is_between_quote, bracket_queue):
	# 		IF_comma_position.append(i)

	return formula_string


app = Flask(__name__)

@app.route("/") ##www.domain.com
def index():


	return render_template("index.html")

@app.route("/parse", methods=['GET', 'POST'])
def parsedFormula():
	if request.method == 'POST':
		try:
			print(request.form)
			
			parsedFormula = autoFormat(request.form['formula_input'])
			print(parsedFormula)
			return render_template("index.html", parsedFormula=parsedFormula, unparsedFormula=request.form['formula_input'])
		except:
		 	errorMessage = '*****Syntax error. Please check your raw formula. the number of left bracket should be equal to the number of right bracket.*****'
		 	return render_template("index.html", parsedFormula=errorMessage, unparsedFormula=request.form['formula_input'])
	else:
		return render_template("index.html")

if __name__ == "__main__":

	app.run(debug=True)