import ply.yacc as yacc
import traceback
from proj.models.finallexer import Lexer
from proj.models.parser import Parser
from proj.models.semantics import SemanticAnalyzer
from proj.utilities.gemini_handler import Gemini_Handler

gemini = Gemini_Handler()

test_code_simple = """begin
    let x = 15;
    let y = 64;
    let result = (x + y) * 8 - 2;
    end"""
    
natural_language_test_code = """function patty(x, y)
        begin
            return x + y;
        end
    print("Sum of 1 and 2 is", patty(1, 2));
    let g = -true;
    print("g is", g);
    let x = 10;
    let score = 100;
    set total to score;
    add 7 to score;
    sub score from total;
    mult total by score ;
    print("Total is", total);
    div total by 5;
   // let add = 5;          // 'add' is reserved — should error
   // set if to 2;          // 'if' is reserved — should error  
   // let while = 10;       // 'while' is reserved — should error
    print("Total is", total);
    print("X is", score);
    //set 10 to total;  // Syntax error: 10 is not an identifier
    score = 100;
    // div total by 0;
    //let score = 90/0;
    
   if score is != 100 then      // Syntax error: missing comparison operator and statement
    print("Hello");         // Syntax error: missing closing parenthesis and semicolon

    if score is > 90  then
        print("Good job!");
    """
#gemini.generate_explanation(natural_language_test_code)
    
t5 = """begin
    let x = 1;
    let y = 20;
    let sum = x + y;
    let product = "Hey";
    let z = 10.5;
    let k= true;
    let k = false + false;
    
    if sum < 50
    begin
        print("Sum is less than 50", sum);
    end
    else
    begin
        print("Sum is too large");
    end

    for let i = 1; to 5
    begin
        print("Looping i",i);
        if x == 3
        begin
            continue;
        end
        print("Current value of x:", x);
    end

    while  (x == 10 and y > 10) or (x > 0 and y < 30)
    begin
        print("Decrementing x:", x);
        x = x - 1;
        if x == 0
        begin
            continue;
        end
    end
    
    function r(a)
    begin
        if a > 10
        begin
            print("Reached limit:", a);
            return a;
        end
        else
        begin
            return r(a + 1);
        end
    end
    
    r(1);
    let a = "adasdasd" + "asasasdasd";
    print(a);

    function greet(name)
    begin
        print("Hello", name);
    end

    greet("Alice");

    result = (x + y) * 2 / (3 - 1);
end"""
# ai_explanation = gemini.generate_explanation(test_code_simple)
# print("AI Explanation:", ai_explanation)

test_code_simple = """begin
    let x = 15;
    let y = 64;
    let result = (x + y) * 8 - 2;
    end"""
code = """
# begin
#     let x = 10;
#     let y = 20;
#     let total = x + y;

#     if total > 15
#     begin
#         print("Total is greater than 15:", total);
#     end

#     for let i = 1; to 5
#     begin
#         print("Loop index:", i);
#     end

#     while total > 0
#     begin
#         total = total - 1;
#     endlet total = x + y;

#     if total > 15
#     begin
#         print("Total is greater than 15:", total);
#     end

#     for let i = 1; to 5
#     begin
#         print("Loop index:", i);
#     end

#     while total > 0
#     begin
#         total = total - 1;
#     end
# end
# """
# # lexerInstance = Lexer()
# # lexerInstance.analyze_tokens(test_code_simple)
# # lexer=Lexer().lexer
# # parser = Parser(lexer)
# #result = parser.parser.parse(test_code_simple, lexer=parser.lexer, debug=False)
# #More comprehensive test
# # test_code_complex = """begin
# #     let count = 0;
# #     let max = 10; let i = 0; 
# #     let r = 3
# #     let make= r/0; 
# #     print(make);

# #     if count < max
# #     begin
# #         print("Count is less than max");
# #         count = count + 1;
# #     end
# #     else
# #     begin
# #         print("Count reached maximum");
# #     end
# #     for let i = 1; to 10 
# #     begin
# #         count = count + i;
# #         if count > 50
# #         begin
# #             break;
# #         end
# #     end
    
# #     while count > 0
# #     begin
# #         count = count - 1;
# #         print(count);
# #     end
# #     end"""

# # print("\nTesting Simple Code:")
# # print("=" * 40)
# # try:
# #     result = parser.parser.parse(test_code_simple, lexer=parser.lexer, debug=False)
# #     print("Parse Result:")
# #     print(result)
# #     print("\nParsing successful!")
# # except Exception as e:
# #     print(f"Parsing failed: {e}")

# # print("\n\nTesting Complex Code:")
# # print("=" * 40)
# # try:
# #     result = parser.parser.parse(test_code_complex, lexer=parser.lexer, debug=False)
# #     print("Parse Result:")
# #     print(result)
# #     print("\nParsing successful!")
# # except Exception as e:
# #     print(f"Parsing failed: {e}")

# # # Interactive mode
# # print("\n" + "=" * 50)
# # print("Interactive Parser Mode (type 'quit' to exit)")
# # print("=" * 50)

# # while True:
# #     try:
# #         code = input('> ')
# #         if code.lower() == 'quit':
# #             break
# #         if code:
# #             result = parser.parser.parse(code, lexer=parser.lexer)
# #             print("Result:", result)
# #     except EOFError:
# #         break
# #     except Exception as e:
# #         print(f"Error: {e}")
        

# # print("=" * 60)
# # print("SEMANTIC ANALYZER TESTING")
# # print("=" * 60)

analyzer = SemanticAnalyzer()
lexer = Lexer()
parser = Parser(lexer)
# #Test 1: Basic arithmetic
# t1 = """begin
#     let x = 15;
#     let y = 64;
#     let result = (x + y) * 2 - 10;
#     print(result);
# end"""
# t2 = """begin
#         let count = 0;
#         let max = 10;
        
#         if count < max
#         begin
#             print("Count is less than max");
#             count = count + 1;
#         end
#         else
#         begin
#             print("Count reached maximum");
#         end
        
#         for i = 1 to 10
#         begin
#             count = count + i;
#             if count > 50
#             begin
#                 break;
#             end
#         end
        
#         while count > 0
#         begin
#             count = count - 1;
#             print(count);
#         end
#         end"""
# t3 = """begin
#     let count = 0;
#     let i = 0;
#     for i = 1 to 5
#     begin
#         count = count + i;quit
#         print(count);
#     end
    
#     if count > 10
#     begin
#         print("Count is greater than 10");
#     end
#     else
#     begin
#         print("Count is not greater than 10");
#     end
# end"""

t4 ="""
    
   /* This is a comment
    Wah gwan, Gabby is hangry
    and her head big */
    begin
    set f to 100;
    let t = 10;
    let u = 20;
    let a =10;
    let b =20;
    let w = t;
    function add(a, b)
    begin
        let b = 100;
        let u= 500000;
        let d = a + b + u;
        return d;
    end
    
    let result = add(a, f);
    print("After adding", a, "and", b, "The result is:", result , "line 1");
# end"""
t5 = """begin
    let x = 1;
    let y = 20;
    let sum = x + y;
    let product = "Hey";
    let z = 10.5;
    // let k= true;
    // let k = false + false;
    if sum < 50
    begin
        print("Sum is less than 50", sum);
    end
    else
    begin
        print("Sum is too large");
    end

    for let i = 1; to 5
    begin
        print("Looping i",i);
        if x == 3
        begin
            continue;
        end
        print("Current value of x:", x);
    end

    while  (x == 10 and y > 10) or (x > 0 and y < 30)
    begin
        print("Decrementing x:", x);
        x = x - 1;
        if x == 0
        begin
            continue;
        end
    end
    
    function r(a)
    begin
        if a > 10
        begin
            print("Reached limit:", a);
            return "Limit reached" ;
        end
        else
        begin
            return r(a + 1);
        end
    end
    
    let a=r(1);
    print("Result of recursive function:", a);

    function greet(name)
    begin
        print("Hello", name);
    end
    let n = "Alice" +1 + true;
    greet("Alice");

end"""
# t6 = """begin
#     let x = 10
#     let y = 20
#     let z = x + y
#     let z ="Hello"
#     if z < 100
#     begin
#         print("Z is under 100" z);  // ❌ Missing comma
#     else
#     begin
#         print("Z is over 100");
#     end

#     for let i = 0 to 10 step
#     begin
#         print(i)
#     end

#     while x > 0
#         print("Still going", x);  // ❌ Missing BEGIN block

#     let bad = (5 + ) * 3;         // ❌ Invalid expression

#     continue;                     // ❌ Not inside a loop
# end"""
test = """begin
    let total = 2 + 5;
    if total > 15
    begin
        print("Total is greater than 15:", total);
    end

    for let i = 1; to 5
    begin
        print("Loop index:", i);
    end

    while total > 0
    begin
        total = total - 1;
    end
    // Outer for loop
    /* This is a comment
    Wah gwan, Gabby is hangry
    and her head big */
    set f to 100;
    let t = 10;
    let u = 20;
    let a =10;
    let b =20;
    let w = t;
    function mad(a, b)
    begin
        //let b = 100;
        let u= 500000;
        let d = a + b + u;
        return d;
    end
    let result = mad(a, f);
    print("After adding", a, "and", b, "The result is:", result , "line 1");

    let x = 1;
    let y = 20;
    let sum = x + y;
    let product = "Hey";
    let z = 10.5;
     if sum < 50
    begin
        print("Sum is less than 50", sum);
    end
    else
    begin
        print("Sum is too large");
    end

    for let p = 1; to 5
    begin
        print("Looping i",p);
        if x == 3
        begin
            continue;
        end
        print("Current value of x:", x);
    end

    while  (x == 10 and y > 10) or (x > 0 and y < 30)
    begin
        print("Decrementing x:", x);
        x = x - 1;
        if x == 0
        begin
            continue;
        end
    end
    
    function r(a)
    begin
        if a > 10
        begin
            print("Reached limit:", a);
            return "Limit reached" ;
        end
        else
        begin
            return r(a + 1);
        end
    end
    
    let q=r(1);
    print("Result of recursive function:", q);

    function greet(name)
    begin
        print("Hello", name);
    end
    //let n = "Alice" +1 + true;
    greet("Alice");
    // let k= true;
    let i = 0;
    for i = 0 to 3
    begin
        print("i =", i);

        // Inner while loop
        let j = 0;
	//j= 5;
       while j < 2
       begin
            print("    j =", j);
            j = j+1;
       end
    end
end
""" 
print("\nTest 1: Basic Arithmetic")
print("-" * 30)
print("Code:", test.strip())
print("Output:")
try:
    ast = parser.parser.parse(test, lexer=lexer.lexer)
    print("AST:", ast)
    analyzer.interpret(ast)
    if analyzer.semantic_errors:
        print("Semantic Errors:")
        for error in analyzer.semantic_errors:
            print(error)
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()


    # def t_IDENTIFIER(self,t):
    #     r'[a-zA-Z_][a-zA-Z0-9_]*'
    #     # Check keywords first
    #     if t.value in self.keywords:
    #         t.type = self.keywords[t.value]
    #         if t.value == 'let' or t.value == 'function':
    #             self.expecting_variable = True
    #             if t.value == 'function':
    #                 self.enter_scope()
    #         elif t.value in ['begin', 'if', 'for', 'while']:
    #             self.enter_scope()
    #         elif t.value == 'end':
    #             self.exit_scope()
    #         return t
    #     # Check natural language keywords
    #     if t.value in self.natural_language_keywords:
    #         t.type = self.natural_language_keywords[t.value]
    #         return t
        
    #     # Handle variable declaration and usage
    #     if self.expecting_variable:
    #         self.expecting_variable = False
    #         self.declare_variable(t.value)
    #         return t
    #     elif self.is_variable_declared(t.value):
    #         return t
    #     else:
    #         print(f"Error: Variable '{t.value}' not declared in current scope (line {t.lineno})")
    #         self.errors.append(f"Error: Variable '{t.value}' not declared in current scope (line {t.lineno})")
    #         return None


# Build the parser


# # Test code

# # Test driver
# if __name__ == '__main__':
#     test_code_simple = """begin
#     let x = 15;
#     let y = 64;
#     let result = (x + y) * 8 - 2;
#     end"""

#     lexer = Lexer()
#     parser = Parser(lexer)
# # More comprehensive test
#     test_code_complex = """begin
#         let count = 0;
#         let max = 10;
        
#         if count < max
#         begin
#             print("Count is less than max");
#             count = count + 1;
#         end
#         else
#         begin
#             print("Count reached maximum");
#         end
        
#         for let i = 1 to 10
#         begin
#             count = count + i;
#             if count > 50
#             begin
#                 break;
#             end
#         end
        
#         while count > 0
#         begin
#             count = count - 1;
#             print(count);
#         end
#         end"""

#     print("\nTesting Simple Code:")
#     print("=" * 40)
#     try:
#         result = parser.parse(test_code_simple, lexer=lexer, debug=False)
#         print("Parse Result:")
#         print(result)
#         print("\nParsing successful!")
#     except Exception as e:
#         print(f"Parsing failed: {e}")
    
#     print("\n\nTesting Complex Code:")
#     print("=" * 40)
#     try:
#         result = parser.parse(test_code_complex, lexer=lexer, debug=False)
#         print("Parse Result:")
#         print(result)
#         print("\nParsing successful!")
#     except Exception as e:
#         print(f"Parsing failed: {e}")
    
#     # Interactive mode
#     print("\n" + "=" * 50)
#     print("Interactive Parser Mode (type 'quit' to exit)")
#     print("=" * 50)
    
#     while True:
#         try:
#             code = input('> ')
#             if code.lower() == 'quit':
#                 break
#             if code:
#                 result = parser.parse(code, lexer=lexer)
#                 print("Result:", result)
#         except EOFError:
#             break
#         except Exception as e:
#             print(f"Error: {e}")


# # Test with different formats
# if __name__ == '__main__':
#     # Test code that matches your example
#     test_code_simple="""begin
#     let x = 15
#     let y = 64
#     let result = (x + y) * 8 - 2
# end"""

#     lexer = Lexer()
    
#     # Test 1: PLY LexToken format
#     print("=" * 50)
#     print("PLY LEXTOKEN FORMAT")
#     print("=" * 50)
#     lexer.test_lexer(test_code_simple, "Basic Example", "lextoken")
    
#     print("\n" + "=" * 50)
#     print("DETAILED TOKEN ANALYSIS")
#     print("=" * 50)
#     lexer.analyze_tokens(test_code_simple)
    
#     # Test 2: More complex example
#     test_code_complex = """begin
#     // Variable declarations
#     let count = 0
#     let max = 10.5

#     if count < max
#     begin
#         print("Valid count")
#     end
    
#     for i = 1 to 10
#     begin
#         count = count + i
#     end
# end"""
    
#     print("\n" + "=" * 50)
#     print("COMPLEX EXAMPLE - LEXTOKEN FORMAT")
#     print("=" * 50)
#     lexer.test_lexer(test_code_complex, "Complex Example", "lextoken")
    
#     # Test 3: Show line-by-line breakdown
#     print("\n" + "=" * 50)
#     print("LINE-BY-LINE ANALYSIS")
#     print("=" * 50)
#     lexer.analyze_tokens(test_code_complex)


# # Test the semantic analyzer
# def test_semantic_analyzer():
#     print("=" * 60)
#     print("SEMANTIC ANALYZER TESTING")
#     print("=" * 60)
     
#     analyzer = SemanticAnalyzer()
    
#     # Test 1: Basic arithmetic
#     test_code1 = """begin
#         let x = 15;
#         let y = 64;
#         let result = (x + y) * 2 - 10;
#         print(result);
#     end"""
    
#     print("\nTest 1: Basic Arithmetic")
#     print("-" * 30)
#     print("Code:", test_code1.strip())
#     print("Output:")
#     try:
#         ast = parser.parse(test_code1, lexer=lexer)
#         analyzer.interpret(ast)
#     except Exception as e:
#         print(f"Error: {e}")
        
#     # Test 2: Control flow
#     test_code2 = """
#     begin
#         let count = 0;
#         let i = 0;
#         for i = 1 to 5
#         begin
#             count = count + i;quit
#             print(count);
#         end
        
#         if count > 10
#         begin
#             print("Count is greater than 10");
#         end
#         else
#         begin
#             print("Count is not greater than 10");
#         end
#     end"""
    
#     print("\n\nTest 2: Control Flow")
#     print("-" * 30)
#     print("Code:", test_code2.strip())
#     print("Output:")
#     try:
#         analyzer = SemanticAnalyzer()  # Fresh analyzer
#         ast = parser.parse(test_code2, lexer=lexer)
#         analyzer.interpret(ast)
#     except Exception as e:
#         print(f"Error: {e}")
        
#     # Test 3: Functions
#     test_code3 = """
#     begin
#         let a =0;
#         let b =0;
#         function add(a, b)
#         begin
#             return a + b;
#         end
        
#         let result = add(10, 20);
#         print(result);
#     end"""
    
#     print("\n\nTest 3: Functions")
#     print("-" * 30)
#     print("Code:", test_code3.strip())
#     print("Output:")
#     try:
#         analyzer = SemanticAnalyzer()  # Fresh analyzer
#         ast = parser.parse(test_code3, lexer=lexer)
#         analyzer.interpret(ast)
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == '__main__':
#     test_semantic_analyzer()
    
#     # Interactive mode
#     print("\n" + "=" * 60)
#     print("INTERACTIVE INTERPRETER MODE")
#     print("Type 'quit' to exit, 'vars' to see variables")
#     print("=" * 60)
    
#     analyzer = SemanticAnalyzer()
#     lexer = Lexer().lexer
#     parser = Parser(lexer).parser
    
#     while True:
#         try:
#             code = input('\n> ')
#             if code.lower() == 'quit':
#                 break
#             elif code.lower() == 'vars':
#                 print("Variables:", analyzer.scope_stack[-1])
#                 continue
#             elif code.lower() == 'functions':
#                 print("Functions:", list(analyzer.functions.keys()))
#                 continue
                
#             if code.strip():
#                 try:
#                     ast = parser.parse(code, lexer=lexer)
#                     if ast:
#                         result = analyzer.interpret(ast)
#                         if result is not None:
#                             print("Result:", result)
#                 except Exception as e:
#                     print(f"Error: {e}")
#         except EOFError:
#             break
#         except KeyboardInterrupt:
#             print("\nGoodbye!")
#             break