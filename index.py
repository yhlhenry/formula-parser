from flask import Flask, request, render_template
# import PySimpleGUIWeb as sg
import os
import sys


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
	for i, c in enumerate(formula_string):	
		if c == '"':
			is_between_quote = not(is_between_quote)		
		if c == '(':
			ToBeInsertedPosition.append([i,len(bracket_queue)])
			bracket_queue.append(c)
		elif c == ')':
			ToBeInsertedPosition.append([i-1,len(bracket_queue)-2])
			bracket_queue.pop()
		elif c == ',':
			ToBeInsertedPosition.append([i,len(bracket_queue)-1])
			

	newFormula = formula_string
	for p in reversed(ToBeInsertedPosition):
		newFormula = insertStringToString(newFormula, '\n'+'    '*(p[1]+1), p[0]+1)
	# print(ToBeInsertedPosition)
	return newFormula


def replaceBracketWithoutArgument(formula_string):
	newFormulaString = formula_string.replace('()', 'BracketWithoutArgument')
	return newFormulaString 

def replaceBackBracketWithoutArgument(formula_string):
	newFormulaString = formula_string.replace('BracketWithoutArgument', '()')
	return newFormulaString 

def autoFormat(formula_string):
	formula_string = formula_string.replace('\t','').replace('\n','')
	print(formula_string)
	formula_string = replaceBracketWithoutArgument(formula_string)
	bracket_list = ['(', ')']
	bracket_queue = []
	start_position_of_IF = 0
	end_position_of_IF = 0
	is_between_quote = False
	IF_comma_position = []
	formula_string = insertIndentToFormula(formula_string)
	for i, c in enumerate(formula_string):	
		# print(i,c)	
		if c == '"':
			is_between_quote = not(is_between_quote)

		if c == '(':
			if len(bracket_queue) == 0:	 
				start_position_of_IF = i
			bracket_queue.append(c)
		elif c == ')':
			bracket_queue.pop()
			if len(bracket_queue) == 0:	
				end_position_of_IF = i

		if isThisACommaBelongToIf(c, is_between_quote, bracket_queue):
			IF_comma_position.append(i)

	formula_string = replaceBackBracketWithoutArgument(formula_string)
	return formula_string



app = Flask(__name__)

@app.route("/") ##www.domain.com
def index():


    return render_template("index.html")

@app.route("/parse", methods=['GET', 'POST'])
def parsedFormula():
    if request.method == 'POST':
        # 偷看一下 request.form 
        print(request.form)
        parsedFormula = autoFormat(request.form['formula_input'])
        print(parsedFormula)
        return render_template("index.html", parsedFormula=parsedFormula)
    else:
        return render_template("index.html")

if __name__ == "__main__":

    app.run(debug=False)