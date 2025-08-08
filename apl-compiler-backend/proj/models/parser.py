import ply.yacc as yacc
from .finallexer import Lexer

# --------------------------
# PROGRAM STRUCTURE
# --------------------------
class Parser:
    tokens = Lexer.tokens
    
    RESERVED_WORDS = {
    'set', 'add', 'sub', 'mult', 'div', 'to',  # Natural language ops
    'begin', 'end', 'let', 'if', 'else', 'elseif', 'for', 'while',
    'print', 'step', 'and', 'or', 'not', 'true', 'false',
    'function', 'return', 'break', 'continue', 'from', 'by', 'is', 'then'
    }  # Merge natural language keywords and Lexer.keywords
    precedence = (
    ('right', 'ASSIGNMENT_OP'),
    ('left', 'KEYWORD_OR'),
    ('left', 'KEYWORD_AND'),
    ('right', 'KEYWORD_NOT'),
    ('nonassoc', 'LT_OP', 'GT_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP'),
    ('left', 'PLUS_OP', 'MINUS_OP'),
    ('left', 'TIMES_OP', 'DIVIDE_OP'),
    # ('right', 'UMINUS', 'UPLUS')  # For unary -x or +x
    )
    def __init__(self,lex):
        self.lexer = lex
        self.parser = yacc.yacc(module=self)
        self.parseError = False
        self.parseErrorMessage = []
        #self.scope_stack = [{}] 
    # def declare_variable(self, name):
    #     if name in self.scope_stack[-1]:
    #         raise SyntaxError(f"Variable '{name}' already declared in current scope.")
    #     self.scope_stack[-1][name] = True

    # def is_variable_declared(self, name):
    #     for scope in reversed(self.scope_stack):
    #         if name in scope:
    #             return True
    #     return False
    
    def is_variable_keyword(self, name,line):
        """
        Check if the name is a reserved keyword or a natural language keyword.
        """
        if isinstance(name,tuple):
            return # Skip if it's a tuple (like a declaration node)
        if name in self.RESERVED_WORDS:
            self.parseErrorMessage.append(f" ❌'{name}' is a reserved keyword and cannot be used as a variable name at line {line}.")
            print(f" ❌'{name}' is a reserved keyword and cannot be used as a variable name at line {line}.")
            
    def p_program(self,p):
        '''program : KEYWORD_BEGIN statement_list KEYWORD_END
                | statement_list'''
       
        if len(p) == 4:
            p[0] = ('program', p[2],p.lineno(1))
        else:
            p[0] = ('program', p[1],p.lineno(1))
        

    def p_statement_list(self,p):
        '''statement_list : statement statement_list
                        | control_statement statement_list
                        | empty'''
       
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = []

    def p_statement(self,p):
        '''statement : assignment_statement
                    | expression SEMICOLON   
                    | print_statement
                    | natural_language'''
       
        if len(p) == 3 and p[2] == ';':
            p[0] = p[1] 
        else:
            p[0] = p[1]

    # --------------------------
    # ASSIGNMENT & DECLARATION
    # --------------------------

    def p_assignment_statement(self,p):
        '''assignment_statement : declaration
                                | IDENTIFIER ASSIGNMENT_OP expression SEMICOLON'''
    
        self.is_variable_keyword(p[1], p.lineno(1))
            
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('assign', p[1], p[3],p.lineno(1))

    def p_declaration(self,p):
        'declaration : KEYWORD_LET IDENTIFIER ASSIGNMENT_OP expression SEMICOLON'
        self.is_variable_keyword(p[2],   p.lineno(1))
        p[0] = ('declare', p[2], p[4],p.lineno(2))

    # --------------------------
    # EXPRESSIONS
    # --------------------------
    def p_expression_binop(self,p):
        '''expression : expression PLUS_OP term
                    | expression MINUS_OP term'''
       
        p[0] = ('binop', p[2], p[1], p[3],p.lineno(2))

    def p_expression_term(self,p):
        'expression : term'
       
        p[0] = p[1]

    def p_term_binop(self,p):
        '''term : term TIMES_OP factor
                | term DIVIDE_OP factor'''
       
        p[0] = ('binop', p[2], p[1], p[3],p.lineno(2))

    def p_term_factor(self,p):
        '''term : factor
                | function_call'''
       
        p[0] = p[1]

    def p_factor_number(self,p):
        '''factor : INTEGER
                | FLOAT 
                | STRING'''
       
        p[0] = ('literal', p[1],p.lineno(1))

    def p_factor_variable(self,p):
        'factor : IDENTIFIER'
        self.is_variable_keyword(p[1],   p.lineno(1))
         
        p[0] = ('var', p[1], p.lineno(1))
        
    

    def p_factor_boolean(self,p):
        '''factor : KEYWORD_TRUE
                | KEYWORD_FALSE'''
       
        p[0] = ('boolean', p[1],p.lineno(1))

    def p_factor_grouped(self,p):
        'factor : LPAREN expression RPAREN'
       
        p[0] = p[2]

    def p_factor_unary(self,p):
        '''factor : PLUS_OP factor
                | MINUS_OP factor'''
       
        p[0] = ('unary', p[1], p[2],p.lineno(1))

    # --------------------------
    # CONTROL STATEMENTS
    # --------------------------

    def p_control_statement(self,p):
        '''control_statement : if_statement
                            | for_statement
                            | while_statement
                            | function_call SEMICOLON'''
        p[0] = p[1]

    def p_if_statement(self,p):
        'if_statement : KEYWORD_IF condition block else_part'
       
        p[0] = ('if', p[2], p[3], p[4],p.lineno(1))
        
        

    def p_else_part(self,p):
        '''else_part : KEYWORD_ELSE block
                    | KEYWORD_ELSEIF condition block else_part
                    | empty'''
       
        if len(p) == 3:
            p[0] = ('else', p[2],p.lineno(1))
        elif len(p) == 5:
            p[0] = ('elseif', p[2], p[3], p[4],p.lineno(1))
        else:
            p[0] = None

    def p_for_statement(self,p):
        '''for_statement : KEYWORD_FOR IDENTIFIER ASSIGNMENT_OP expression KEYWORD_TO expression block
                        | KEYWORD_FOR IDENTIFIER ASSIGNMENT_OP expression KEYWORD_TO expression KEYWORD_STEP expression block
                        | KEYWORD_FOR declaration KEYWORD_TO expression KEYWORD_STEP expression block 
                        | KEYWORD_FOR declaration KEYWORD_TO expression block '''
        self.is_variable_keyword(p[2],   p.lineno(1))
       
        if isinstance(p[2], tuple) and p[2][0] == 'declare':
                # p[2] is a declaration node: ('declare', var, start)
                var_name = p[2][1]
                start_expr = p[2][2]
                if len(p) == 6:
                    # FOR declaration TO expression block
                    p[0] = ('for','let', var_name, start_expr, p[4], None, p[5],p.lineno(1))
                else:
                    p[0] = ('for','let', var_name, start_expr, p[4], p[6], p[7],p.lineno(1))
        else: 
            if len(p) == 8:
                p[0] = ('for',None, p[2], p[4], p[6], None, p[7],p.lineno(1))
            else:
                p[0] = ('for',None, p[2], p[4], p[6], p[8], p[9],p.lineno(1))

    def p_while_statement(self, p):
        'while_statement : KEYWORD_WHILE condition block'
        p[0] = ('while', p[2], p[3],p.lineno(1))

    def p_block(self,p):
        '''block : KEYWORD_BEGIN statement_list KEYWORD_END
                | statement'''
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = [p[1]]  # Single statement in a block

    # --------------------------
    # CONDITIONS
    # --------------------------

    def p_condition_comparison(self,p):
        '''condition : expression LT_OP expression
                    | expression GT_OP expression
                    | expression LE_OP expression
                    | expression GE_OP expression
                    | expression EQ_OP expression
                    | expression NE_OP expression'''
        p[0] = ('compare', p[2], p[1], p[3], p.lineno(2))

    def p_condition_logical(self,p):
        '''condition : condition KEYWORD_AND condition
                    | condition KEYWORD_OR condition
                    | KEYWORD_NOT condition'''
        if len(p) == 4:
            p[0] = ('logic', p[2], p[1], p[3], p.lineno(2))
        else:
            p[0] = ('logic', p[1], p[2],p.lineno(1))

    def p_condition_expr(self, p):
        'condition : expression'
        p[0] = ('cond_expr', p[1], p.lineno(1)) 

    def p_condition_grouped(self, p):
        'condition : LPAREN condition RPAREN'
        p[0] = ('grouped_condition', p[2], p.lineno(1))

    # --------------------------
    # NATURAL LANGUAGE SUPPORT
    # --------------------------

    def p_natural_language(self, p):
        '''natural_language : SET_KEYWORD_NATURAL_LANG IDENTIFIER KEYWORD_TO expression SEMICOLON
                            | ADD_KEYWORD_NATURAL_LANG expression KEYWORD_TO IDENTIFIER SEMICOLON
                            | SUB_KEYWORD_NATURAL_LANG expression FROM_KEYWORD_NATURAL_LANG IDENTIFIER SEMICOLON
                            | MULT_KEYWORD_NATURAL_LANG IDENTIFIER BY_KEYWORD_NATURAL_LANG expression SEMICOLON
                            | DIV_KEYWORD_NATURAL_LANG IDENTIFIER BY_KEYWORD_NATURAL_LANG expression SEMICOLON'''

        op = p[1].lower()
        connector = p[3].lower()

        # figure out which side is the variable
        if op == 'set' or op == 'div':
            var = p[2]
        else:
            var = p[4]

        self.is_variable_keyword(var, p.lineno(1))

        p[0] = ('natural_lang', op, p[2], connector, p[4], p.lineno(1))

    def p_natural_language_if(self, p):
        '''natural_language : KEYWORD_IF IDENTIFIER IS_KEYWORD_NATURAL_LANG LT_OP expression THEN_KEYWORD_NATURAL_LANG statement_list
                            | KEYWORD_IF IDENTIFIER IS_KEYWORD_NATURAL_LANG GT_OP expression THEN_KEYWORD_NATURAL_LANG statement_list
                            | KEYWORD_IF IDENTIFIER IS_KEYWORD_NATURAL_LANG LE_OP expression THEN_KEYWORD_NATURAL_LANG statement_list
                            | KEYWORD_IF IDENTIFIER IS_KEYWORD_NATURAL_LANG GE_OP expression THEN_KEYWORD_NATURAL_LANG statement_list
                            | KEYWORD_IF IDENTIFIER IS_KEYWORD_NATURAL_LANG EQ_OP expression THEN_KEYWORD_NATURAL_LANG statement_list
                            | KEYWORD_IF IDENTIFIER IS_KEYWORD_NATURAL_LANG NE_OP expression THEN_KEYWORD_NATURAL_LANG statement_list'''
        self.is_variable_keyword(p[2],   p.lineno(1))
        p[0] = ('natural_lang_if', p[2], p[4], p[5], p[7], p.lineno(1))


    # --------------------------
    # FUNCTION CALL
    # --------------------------

    def p_function_call(self,p):
        'function_call : IDENTIFIER LPAREN parameter_list RPAREN'
        self.is_variable_keyword(p[1],   p.lineno(1))
        p[0] = ('call', p[1], p[3], p.lineno(1))

    def p_parameter_list(self,p):
        '''parameter_list : expression COMMA parameter_list
                        | expression
                        | empty'''
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        elif len(p) == 2:
            if p[1] is None:
                p[0] = []
            else:
                p[0] = [p[1]]

    # --------------------------
    # PRINT STATEMENT
    # --------------------------

    def p_print_statement(self, p):
        '''print_statement : KEYWORD_PRINT LPAREN print_arguments RPAREN SEMICOLON'''
        p[0] = ('print', p[3], p.lineno(1))  # Store the string or expression to print

        
    def p_print_arguments_multiple(self, p):
        '''print_arguments : printable_item COMMA print_arguments'''
        p[0] = [p[1]] + p[3]

    def p_print_arguments_single(self, p):
        '''print_arguments : printable_item'''
        p[0] = [p[1]]

    def p_printable_item_string(self, p):
        '''printable_item : STRING'''
        p[0] = ('string', p[1], p.lineno(1))

    def p_printable_item_expr(self, p):
        '''printable_item : expression'''
        p[0] = p[1]  # Already a full expression node (like 'binop' or 'var')
    
    
    
    
    # --------------------------
    # FUNCTION DEFINITION
    # --------------------------

    def p_function_definition(self, p):
        '''function_definition : KEYWORD_FUNCTION IDENTIFIER LPAREN parameter_declaration_list RPAREN block
                           | KEYWORD_FUNCTION IDENTIFIER LPAREN RPAREN block'''
        self.is_variable_keyword(p[2],   p.lineno(1))
        if len(p) == 7:
            p[0] = ('function_def', p[2], p[4], p[6], p.lineno(1))
        else:
            p[0] = ('function_def', p[2], [], p[5],p.lineno(1))

    def p_parameter_declaration_list(self,p):
        '''parameter_declaration_list : IDENTIFIER COMMA parameter_declaration_list
                                    | IDENTIFIER'''
        self.is_variable_keyword(p[1],   p.lineno(1))
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]

    # --------------------------
    # CONTROL FLOW STATEMENTS
    # --------------------------

    def p_return_statement(self, p):
        '''return_statement : KEYWORD_RETURN expression SEMICOLON
                        | KEYWORD_RETURN SEMICOLON'''
        if len(p) == 4:
            p[0] = ('return', p[2],p.lineno(1))
        else:
            p[0] = ('return', None,p.lineno(1))

    def p_break_statement(self, p):
        'break_statement : KEYWORD_BREAK SEMICOLON'
        p[0] = ('break',p.lineno(1))
        
    def p_continue_statement(self, p):
        'continue_statement : KEYWORD_CONTINUE SEMICOLON'
        p[0] = ('continue',p.lineno(1))

    # Update statement rule to include new statements
    def p_statement_extended(self,p):
        '''statement : return_statement
                    | break_statement
                    | continue_statement
                    | function_definition'''
        p[0] = p[1]

    # --------------------------
    # UTILITY RULES
    # --------------------------

    def p_empty(self,p):
        'empty :'
        p[0] = None

    def p_error(self,p):
        self.parseError = True
        if p:
            value = str(p.value).lower()
            if value in self.RESERVED_WORDS:
                msg = f"❌ Syntax Error: '{value}' is a reserved keyword and cannot be used in this context (line {p.lineno})"
                print(msg)
                self.parseErrorMessage.append(msg)
            print(f"\n❌ Syntax Error on line {p.lineno}:")
            print(f"   Unexpected token '{p.value}' of type {p.type}")
            self.parseErrorMessage.append(f"❌ Syntax error at line {p.lineno}: Unexpected token '{p.value}' of type {p.type}")
        else:
            print("Syntax error at EOF")
            self.parseErrorMessage.append("Syntax error at EOF")
