class cls_parser:

	import string
	from string import strip
	import sympy
	from sympy.parsing.sympy_parser import parse_expr
	# N.B. there is a compatibility error with certain versions of SymPy that cause an infinite recursion
	# using string.strip() when sympy is instanced to the class.  Prevented by importing it in the function.
	import os
	

#######################################
# Functions to check each input field #
#######################################

###
# Symbols
###
	def fun_check_symbols(self,str_argument):
		str_argument = str_argument.rstrip()
		lst_symbols = str_argument.split(' ') # symbols (variables) should have been given in a list separated by a single space
		lst_symbols = [x for x in lst_symbols if x != '']

		# make sure symbols don't contain illegal characters
		# - punctuation 
		# - a digit as the first character
		# - multiple variables of the same name
		# - a protected word (and,or,not,fanout)
		for str_symbol in lst_symbols:
			if (len(set(list(str_symbol)).intersection(list(self.string.punctuation))) != 0) or (str_symbol[0] in list(self.string.digits)) or (lst_symbols.count(str_symbol) > 1) or (str_symbol in ['and','or','not','fanout']):
				raise Illegal_Variable_Error(str_symbol)
		
		# if we didn't raise an error, return the list of checked symbols
		return lst_symbols
			
###
# Formula
###

	# helper function to find the leaf nodes (variables) of the SymPy parse tree
	def fun_sympyParseWalk(self,expr,lst_leaves):
		if len(expr.args) == 0:
			lst_leaves.append(str(expr))
		else:
			for arg in expr.args:
				self.fun_sympyParseWalk(arg,lst_leaves)
		return lst_leaves

	
	def fun_check_formula(self,str_argument,lst_symbols):
		import sympy
		from sympy.parsing.sympy_parser import parse_expr

		# use SymPy's parser to check the formula syntax		
		try:
			obj_parsedExpr = parse_expr(str_argument)
		except sympy.parsing.sympy_tokenize:
			raise Formula_Syntax_Error(str_argument)
		
		print('Input formula: ' + str(obj_parsedExpr))					
		# use fun_sympyParseWalk to walk through SymPy's parse tree and find the variables
		lst_variables = []
		lst_variables = self.fun_sympyParseWalk(obj_parsedExpr,lst_variables)
		
		# those variables should be exactly the symbols declared.  if not, raise an error
		if set(lst_variables) != set(lst_symbols):
			raise Declared_Variable_Error
		
###
# Prism path
###		
			
	def fun_check_path(self,str_argument):
		str_argument = str_argument.rstrip()
		if not self.os.path.exists(str_argument):
			raise Path_Error(str_argument)

###
# Length
###

	def fun_check_length(self,str_argument):
		str_argument = str_argument.rstrip()
		try:
			int_length = int(str_argument)
		except:
			raise Length_Error(str_argument)

		if int_length <= 1:
			raise Length_Error(str_argument)
###
# Tolerance
###

	def fun_check_tolerance(self,str_argument):
		str_argument = str_argument.rstrip()
		try:
			flt_error = float(str_argument)
		except:
			raise Tolerance_Error(str_argument)

		if flt_error <0 or flt_error > 1:
			raise Tolerance_Error(str_argument)



##########################################
# Main routine to parse .dlin input file #
##########################################


	def fun_dlin_parse(self,str_input_file):
		
		try:	
			hdl_f = open(str_input_file,'r')
		except IOError:
			print 'Input file could either not be found or not be opened.  Check the path and try again.'

		lst_g = hdl_f.readlines()
		
		# check the symbols first (because we'll need them to check the formula)
		for str_line in lst_g:
			if str_line[0] == '#':
				pass
			elif '=' in str_line:
				lst_eqSplit = str_line.split('=',1)
				str_field = lst_eqSplit[0]
				str_argument = lst_eqSplit[1]

				# strip out in-line comments
				lst_argSplit = str_argument.split('#',1)
				str_argument = lst_argSplit[0]

				# check the syntax for each field
				if str_field == 'symbols':
					lst_symbols = self.fun_check_symbols(str_argument)
					str_symbols = str_argument.rstrip()
					
		# check the other fields
		for str_line in lst_g:
			if str_line[0] == '#':
				pass
			elif '=' in str_line:
				lst_eqSplit = str_line.split('=',1)
				str_field = lst_eqSplit[0]
				str_argument = lst_eqSplit[1]

				# strip out in-line comments
				lst_argSplit = str_argument.split('#',1)
				str_argument = lst_argSplit[0]

				if str_field == 'formula':
					obj_formula = self.fun_check_formula(str_argument,lst_symbols)
					str_formula = str_argument.rstrip()
				
				elif str_field == 'pathToPrism':
					self.fun_check_path(str_argument)
					str_path = str_argument.rstrip()					

				elif str_field == 'trivial_length':
					self.fun_check_length(str_argument)					
					str_trivLen = str_argument.rstrip()						
	
				elif str_field == 'MCE_tolerance':
					self.fun_check_tolerance(str_argument)
					str_tol = str_argument.rstrip()
					
				elif str_field == 'symbols':
					pass

				else:
					raise Input_Field_Error(str_field)

		return [str_symbols,str_formula,str_path,str_trivLen,str_tol]




##############################################
# Error messages for this module, subclassed #
##############################################

class Error(Exception): 
	# error base class for this module
	pass

class Input_Field_Error(Error):
	# Exception raised for invalid fields in the input file.  There are only five input fields and they must be spelled correctly.
	# This error is raised when an invalid field name is entered by the user. 
	def __init__(self,expr):
		print "'DLCC ERROR MSG: Invalid field in input file: %s.  Valid fields are: symbols, formula, pathToPrism, trivial_length, and MCE_tolerance.  Check the input file and try again. '" %expr

class Illegal_Variable_Error(Error):
	# Exception raised if one of the propositional variables given in the input has an illegal format.
	def __init__(self,expr):
		print "'DLCC ERROR MSG: Invalid formatting of symbol: %s.  Symbols should be given in a list separated by whitespace, should not contain illegal characters, and may not be duplicates of one another.  Please check the formatting and try again.'"%expr

class Formula_Syntax_Error(Error):
	def __init__(self,expr):
		print "'DLCC ERROR MSG: Syntax error in propositional formula: %s.  Caused a token error during parsing.  Please check the formula and try again.'"%expr 

class Declared_Variable_Error(Error):
	def __init__(self):
		print "'DLCC ERROR MSG: The propositional variables in the input formula do not match the variables declared.  Please check and try again.'"

class Path_Error(Error):
	def __init__(self,expr):
		print "'DLCC ERROR MSG: The path to Prism given by %s in the input file is an invalid path.  Please check the path and try again.'"%expr

class Length_Error(Error):
	def __init__(self,expr):
		print "'DLCC ERROR MSG: Trivial length %s is invalid in the input.  It must be an integer greater than or equal to 2.  Please check the input file and try again.'"%expr
				
class Tolerance_Error(Error):
	def __init__(self,expr):
		print "'DLCC ERROR MSG: Missed Chance Error tolerance %s is invalid.  Tolerance must be a decimal between 0 and 1, e.g., 0.35.  Please check the input and try again.'"%expr











	
