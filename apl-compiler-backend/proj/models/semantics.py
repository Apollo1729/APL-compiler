from proj.models.finallexer import Lexer
from proj.models.parser import Parser
import sys

class SemanticAnalyzer:
    def __init__(self):
        self.variables = {}  # Variable storage
        self.functions = {}  # Function definitions
        self.scope_stack = [{}]  # Stack of scopes for nested blocks
        self.call_stack = []  # Function call stack
        self.loop_stack = []  # Track nested loops for break/continue
        self.return_value = None
        self.should_return = False
        self.should_break = False
        self.should_continue = False
        self.semantic_errors = []  # List to collect semantic errors
        self.compile_results = []  # Store results of compilation
        self.line_number = 0
    
    def is_variable_declared(self,var_name):
        """Check if variable is declared in current scopes"""
        if var_name in self.scope_stack[-1]:
                return True
        return False

    def enter_scope(self):
        """Enter a new scope"""
        self.scope_stack.append({})
        
    def exit_scope(self):
        """Exit current scope """
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            
    def get_variable(self, name,line):
        """Get variable value from current or parent scopes"""
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        self.semantic_errors.append(f"🧠💥Variable '{name}' is not defined at line {line}")
        print(f"Variable '{name}' is not defined at line {line}")
        self.should_break = True
        return None
        
    def set_variable(self, name, value,line):
        """Set variable in current scope"""
        if self.is_variable_declared(name)==False:
            # If variable is not declared, declare it in the current scope
            #print(f"Variable '{name}' declared in current scope at line {line}")
            self.scope_stack[-1][name] = value
        else:
            self.semantic_errors.append(f"🧠💥Variable '{name}' already declared in current scope at line {line}" )
            self.should_break = True
            
    
        
    def update_variable(self, name, value,line):
        """Update existing variable in its original scope"""
        for scope in reversed(self.scope_stack):
            if name in scope:
                scope[name] = value
                return
        self.semantic_errors.append(f"🧠💥 Variable '{name}' is not defined at line {line}")
        self.should_break = True
        
    def interpret(self, node):
        """Main interpretation method - dispatches to specific node handlers"""
        if node is None:
            return None
            
        if isinstance(node, tuple):
            node_type = node[0]
            
            # Dispatch to appropriate handler based on node type
            if node_type == 'program':
                return self.interpret_program(node)
            elif node_type == 'declare':
                return self.interpret_declare(node)
            elif node_type == 'assign':
                return self.interpret_assign(node)
            elif node_type == 'binop':
                return self.interpret_binop(node)
            elif node_type == 'unary':
                return self.interpret_unary(node)
            elif node_type == 'literal':
                return self.interpret_literal(node)
            elif node_type == 'boolean':
                return self.interpret_boolean(node)
            elif node_type == 'var':
                return self.interpret_var(node)
            elif node_type == 'print':
                return self.interpret_print(node)
            elif node_type == 'if':
                return self.interpret_if(node)
            elif node_type == 'for':
                return self.interpret_for(node)
            elif node_type == 'while':
                return self.interpret_while(node)
            elif node_type == 'compare':
                return self.interpret_compare(node)
            elif node_type == 'grouped_condition':
                return self.grouped_condition(node)
            elif node_type == 'logic':
                return self.interpret_logic(node)
            elif node_type == 'cond_expr':
                return self.interpret_cond_expr(node)
            elif node_type == 'function_def':
                return self.interpret_function_def(node)
            elif node_type == 'call':
                return self.interpret_call(node)
            elif node_type == 'return':
                return self.interpret_return(node)
            elif node_type == 'break':
                return self.interpret_break(node)
            elif node_type == 'continue':
                return self.interpret_continue(node)
            elif node_type == 'natural_lang':
                return self.interpret_natural_lang(node)
            elif node_type == 'natural_lang_if':
                return self.interpret_natural_lang_if(node)
            else:
                self.semantic_errors.append(f"🧠💥Unknown node type: {node_type}")
        elif isinstance(node, list):
            # Handle statement lists
            result = None
            for stmt in node:
                if stmt is not None:
                    result = self.interpret(stmt)
                    # Handle control flow
                    if self.should_return or self.should_break or self.should_continue:
                        break
            return result
        else:
            return node
    # Interpret the main program node
    def interpret_program(self, node):
        """Interpret the main program"""
        _, statements,line = node
        self.line_number = line
        return self.interpret(statements)
        
    def interpret_declare(self, node):
        """Handle variable declarations: let x = 5"""
        _, var_name, value,line = node
        self.line_number = line
        computed_value = self.interpret(value)
        if self.loop_stack:
            if self.loop_stack[-1] == 'for' or self.loop_stack[-1] == 'while':
            # Update variable in current scope
                if self.is_variable_declared(var_name)==True:
                    self.update_variable(var_name, computed_value,line)
                else:
                    self.set_variable(var_name, computed_value,line)
        else:
            self.set_variable(var_name, computed_value,line)
        return computed_value
        
    def interpret_assign(self, node):
        """Handle variable assignments: x = 10"""
        _, var_name, value,line = node
        self.line_number = line
        computed_value = self.interpret(value)
        self.update_variable(var_name, computed_value,line)
        return computed_value
        
    def interpret_binop(self, node):
        """Handle binary operations: +, -, *, /"""
        _, op, left, right,line = node
        self.line_number = line
        left_val = self.interpret(left)
        right_val = self.interpret(right)
        if left_val is None or right_val is None:
            self.semantic_errors.append(f"🧠💥Invalid operands for binary operation '{op}' at line {line}")
            return None
        if isinstance(left_val, str) or isinstance(right_val, str):
            self.semantic_errors.append(f"🧠💥Cannot perform binary operation '{op}' on strings at line {line}")
            return None
        if isinstance(left_val, bool) or isinstance(right_val, bool):
            self.semantic_errors.append(f"🧠💥Cannot perform binary operation '{op}' on booleans at line {line}")
            return None
        if left_val is None or right_val is None:
            self.semantic_errors.append(f"🧠💥Invalid operands for binary operation '{op}' at line {line}")
            return None
        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            if right_val == 0:
                self.semantic_errors.append(f"🧠💥Division by zero at line {line}")
                return None
            return left_val / right_val
        else:
             self.semantic_errors.append(f"🧠💥Unknown binary operator: {op} at line {line}")
            
    def interpret_unary(self, node):
        """Handle unary operations: +x, -x"""
        _, op, operand,line = node
        self.line_number = line
        value = self.interpret(operand)
        
        if op == '+':
            return +value
        elif op == '-':
            return -value
        else:
            self.semantic_errors.append(f"🧠💥Unknown unary operator: {op} at line {line}")
            
    def interpret_literal(self, node):
        """Handle number literals"""
        _, value,line = node
        self.line_number = line
        return value
        
    def interpret_boolean(self, node):
        """Handle boolean literals"""
        _, value , line = node
        self.line_number = line
        return value == 'true'
        
    def interpret_var(self, node):
        """Handle variable references"""
        _, var_name,line = node
        self.line_number = line
        val=self.get_variable(var_name,line)
        if val is None:
            self.semantic_errors.append(f"🧠💥Variable '{var_name}' does not have a value at line {line}")
            return None
        return val
        
    def interpret_print(self, node):
        """Handle print statements"""
        _, items,line = node
        self.line_number = line
        output = []
        for item in items:
            if isinstance(item,tuple) and item[0] == 'string':
                # String literal
                output.append(item[1])
            else:
                # Expression to evaluate
                output.append(str(self.interpret(item)))
        print(' '.join(output))
        self.compile_results.append(' '.join(output))
        return None
        
    def interpret_if(self, node):
        """Handle if statements"""
        _, condition, then_block, else_part,line = node
        self.line_number = line
        
        condition_result = self.interpret(condition)
        
        if self.is_truthy(condition_result):
            self.enter_scope()
            try:
                result = self.interpret(then_block)
            finally:
                self.exit_scope()
            return result
        elif else_part:
            if else_part[0] == 'else':
                _, else_block,line = else_part
                self.enter_scope()
                try:
                    result = self.interpret(else_block)
                finally:
                    self.exit_scope()
                return result
            elif else_part[0] == 'elseif':
                # Treat elseif as a nested if
                _, elif_condition, elif_block, elif_else,line = else_part
                elif_node = ('if', elif_condition, elif_block, elif_else)
                return self.interpret(elif_node)
        
        return None
        
    def interpret_for(self, node):
        """Handle for loops"""
        _,type,var_name, start_expr, end_expr, step_expr, body,line = node
        self.line_number = line

        start_val = self.interpret(start_expr)
        end_val = self.interpret(end_expr)
        step_val = self.interpret(step_expr) if step_expr else 1
        self.enter_scope()
        self.loop_stack.append('for')
        if type != 'let':
            val=self.get_variable(var_name,line)
            if val is None:
                return None
        elif type == 'let':
            self.set_variable(var_name, start_val,line)
        # self.enter_scope()
        # self.loop_stack.append('for')
        
        try:
            current = start_val
            while (step_val > 0 and current <= end_val) or (step_val < 0 and current >= end_val):
                self.update_variable(var_name, current,line)
                self.interpret(body)
                if self.should_break:
                    self.should_break = False
                    break
                if self.should_continue:
                    self.should_continue = False
                    current += step_val
                    continue
                if self.should_return:
                    break
                    
                current += step_val
        finally:
            self.loop_stack.pop()
            self.exit_scope()
            
        return None
        
    def interpret_while(self, node):
        """Handle while loops"""
        _, condition, body,line = node
        self.line_number = line
        
        self.enter_scope()
        self.loop_stack.append('while')
        max_iterations = 100000  # Or some reasonable limit
        iteration_count = 0
        try:
            while self.is_truthy(self.interpret(condition)):
                if iteration_count >= max_iterations:
                    self.semantic_errors.append(f"🧠💥Maximum iterations exceeded in while loop at line {line}")
                    break
                self.interpret(body)
                
                if self.should_break:
                    self.should_break = False
                    break
                if self.should_continue:
                    self.should_continue = False
                    continue
                if self.should_return:
                    break
        finally:
            self.loop_stack.pop()
            self.exit_scope()
            
        return None
        
    def interpret_compare(self, node):
        """Handle comparison operations"""
        _, op, left, right,line = node
        self.line_number = line
        left_val = self.interpret(left)
        right_val = self.interpret(right)
        
        if left_val is None or right_val is None:
            self.semantic_errors.append(f"🧠💥Invalid operands for comparison '{op}' at line {line}")
            return None
        if op == '<':
            return left_val < right_val
        elif op == '>':
            return left_val > right_val
        elif op == '<=':
            return left_val <= right_val
        elif op == '>=':
            return left_val >= right_val
        elif op == '==':
            return left_val == right_val
        elif op == '!=':
            return left_val != right_val
        else:
             self.semantic_errors.append(f"🧠💥Unknown comparison operator: {op} at line {line}")
            
    def interpret_logic(self, node):
        """Handle logical operations"""
        if len(node) == 5:
            _, op, left, right,line = node
            self.line_number = line
            if op == 'and':
                return self.is_truthy(self.interpret(left)) and self.is_truthy(self.interpret(right))
            elif op == 'or':
                return self.is_truthy(self.interpret(left)) or self.is_truthy(self.interpret(right))
        else:
            _, op, operand,line = node
            if op == 'not':
                return not self.is_truthy(self.interpret(operand))
                
        self.semantic_errors.append(f"🧠💥Unknown logical operator: {node} at line {line}")
    
    def interpret_cond_expr(self,node):
        _,condition, line = node
        self.line_number = line
        return self.interpret(condition)
    def grouped_condition(self, node):
        _, condition, line = node
        self.line_number = line
        return self.interpret(condition)
    def interpret_function_def(self, node):
        """Handle function definitions"""
        _, func_name, params, body,line = node
        self.line_number = line
        self.functions[func_name] = {
            'params': params,
            'body': body
        }
        return None
        
    def interpret_call(self, node):
        """Handle function calls"""
        _, func_name, args,line = node
        self.line_number = line
        
        if func_name not in self.functions:
             self.semantic_errors.append(f"🧠💥Function '{func_name}' is not defined at line {line}")
            
        func_def = self.functions[func_name]
        self.enter_scope()
        # Evaluate arguments
        arg_values = [self.interpret(arg) for arg in args]
        
        # Check parameter count
        if len(arg_values) != len(func_def['params']):
            self.semantic_errors.append(f"🧠💥Function '{func_name}' expects {len(func_def['params'])} arguments, got {len(arg_values)} at line {line}")
            
        # Create new scope for function
        
        self.call_stack.append(func_name)
        
        try:
            # Bind parameters to arguments
            for param, arg_val in zip(func_def['params'], arg_values):
                self.set_variable(param, arg_val,line)
                
            # Execute function body
            self.interpret(func_def['body'])
            
            # Get return value
            result = self.return_value
            self.return_value = None
            self.should_return = False
            
            return result
            
        finally:
            self.call_stack.pop()
            self.exit_scope()
            
    def interpret_return(self, node):
        """Handle return statements"""
        _, value,line = node
        self.line_number = line
        if value is not None:
            self.return_value = self.interpret(value)
        else:
            self.return_value = None
        self.should_return = True
        return self.return_value
        
    def interpret_break(self, node):
        """Handle break statements"""
        _, line = node
        self.line_number = line
        if not self.loop_stack:
            self.semantic_errors.append(f"🧠💥Break statement outside of loop at line {line}")
        self.should_break = True
        return None
        
    def interpret_continue(self, node):
        """Handle continue statements"""
        _, line = node
        self.line_number = line
        if not self.loop_stack:
           self.semantic_errors.append(f"🧠💥Continue statement outside of loop at line {line}")
        self.should_continue = True
        return None
        
    def interpret_natural_lang(self, node):
        """Handle natural language constructs"""
        _, operation, arg1, connector, arg2, line = node
        self.line_number = line
        if operation == 'set' and connector == 'to':
            # "set x to 5" -> x = 5
            if isinstance(arg1, str):  # Variable name
                value = self.interpret(arg2)
                self.set_variable(arg1, value,line)
                return value
            else:
                self.semantic_errors.append(f"🧠💥Invalid natural language assignment: {operation} {connector} at line {line}")
        elif operation == 'add' and connector == 'to':
            # "add 5 to x" -> x = x + 5
            if isinstance(arg2, str):  # Variable name
                current_val = self.get_variable(arg2,line)
                if current_val is None:
                    return None
                if not isinstance(current_val, (int, float)):
                    self.semantic_errors.append(f"🧠💥Cannot add to non-numeric variable '{arg2}' at line {line}")
                    return None
                add_val = self.interpret(arg1)
                if add_val is None:
                    return None
                if not isinstance(add_val, (int, float)):
                    self.semantic_errors.append(f"🧠💥Cannot add non-numeric value '{add_val}' at line {line}")
                    return None
                new_val = current_val + add_val
                self.update_variable(arg2, new_val,line)
                return new_val
            else:
                self.semantic_errors.append(f"🧠💥Invalid natural language addition: {operation} {connector} at line {line}")
        elif operation == 'sub' and connector == 'from':
            # "subtract 3 from x" -> x = x - 3
            if isinstance(arg2, str):  # Variable name
                current_val = self.get_variable(arg2,line)
                if current_val is None:
                    return None
                if not isinstance(current_val, (int, float)):
                    self.semantic_errors.append(f"🧠💥Cannot subtract from non-numeric variable '{arg2}' at line {line}")
                    return None
                sub_val = self.interpret(arg1)
                if sub_val is None:
                    return None
                if not isinstance(sub_val, (int, float)):
                    self.semantic_errors.append(f"🧠💥Cannot subtract non-numeric value '{sub_val}' at line {line}")
                    return None
                new_val = current_val - sub_val
                self.update_variable(arg2, new_val,line)
                return new_val
            else:
                self.semantic_errors.append(f"🧠💥Invalid natural language subtraction: {operation} {connector} at line {line}")
        elif operation == "mult" and connector == 'by':
            # "multiply x by 2" -> x = x * 2
            if isinstance(arg1, str):  # Variable name
                current_val = self.get_variable(arg1,line)
                if current_val is None:
                    return None
                if not isinstance(current_val, (int, float)):
                    self.semantic_errors.append(f"🧠💥Cannot multiply non-numeric variable '{arg2}' at line {line}")
                    return None
                mult_val = self.interpret(arg2)
                if mult_val is None:
                    return None
                if not isinstance(mult_val, (int, float)):
                    self.semantic_errors.append(f"🧠💥Cannot multiply non-numeric value '{mult_val}' at line {line}")
                    return None
                new_val = current_val * mult_val
                self.update_variable(arg1, new_val,line)
                return new_val
            else:
                self.semantic_errors.append(f"🧠💥Invalid natural language multiplication: {operation} {connector} at line {line}")
        elif operation == "div" and connector == 'by':
            # "divide x by 4" -> x = x / 4
            if isinstance(arg1, str):
                current_val = self.get_variable(arg1,line)
                if current_val is None:
                    return None
                if not isinstance(current_val, (int, float)):
                    self.semantic_errors.append(f"🧠💥Cannot divide non-numeric variable '{arg1}' at line {line}")
                    return None
                div_val = self.interpret(arg2)
                if div_val is None:
                    return None
                if not isinstance(div_val, (int, float)):
                    self.semantic_errors.append(f"🧠💥Cannot divide non-numeric value '{div_val}' at line {line}")
                    return None
                if div_val == 0:
                    self.semantic_errors.append(f"🧠💥Division by zero in natural language operation at line {line}")
                    return None
                new_val = current_val / div_val
                self.update_variable(arg1, new_val,line)
                return new_val
            else:
                self.semantic_errors.append(f"🧠💥Invalid natural language division: {operation} {connector} at line {line}")
        else:
            self.semantic_errors.append(f"🧠💥Unknown natural language construct: {operation} {connector} at line {line}")
        
    def interpret_natural_lang_if(self, node):
        """Handle natural language if statements"""
        _, var_name, op, value, statement, line = node
        self.line_number = line
        
        var_val = self.get_variable(var_name,line)
        condition_val = self.interpret(value)
        if var_val is not None and condition_val is not None:
        # Evaluate condition
            if op == '<':
                result = var_val < condition_val
            elif op == '>':
                result = var_val > condition_val
            elif op == '<=':
                result = var_val <= condition_val
            elif op == '>=':
                result = var_val >= condition_val
            elif op == '==':
                result = var_val == condition_val
            elif op == '!=':
                result = var_val != condition_val
            else:
                self.semantic_errors.append(f"🧠💥Unknown comparison operator in natural language if: {op} at line {line}")
            if result:
                return self.interpret(statement)
        return None
        
    def is_truthy(self, value):
        """Determine if a value is truthy"""
        if isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            return len(value) > 0
        else:
            return value is not None
