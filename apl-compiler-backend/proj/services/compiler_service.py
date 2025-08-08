from proj.models.semantics import SemanticAnalyzer
from proj.models.parser import Parser
from proj.models.finallexer import Lexer
from proj.utilities.gemini_handler import Gemini_Handler
import asyncio
from flask import jsonify


def compile_code(code: str) -> str:
    """
    Compiles the given code by parsing it and performing semantic analysis.
    
    Args:
        code (str): The code to compile.
    
    Returns:
        str: The result of the compilation, which could be an error message or a success message.
    """
    try:
        # TOKENIZE CODE
        gemini= Gemini_Handler()

        ai_explanation = gemini.generate_explanation(code)

        lexInstance = Lexer()
        lexOutput = lexInstance.analyze_tokens(code)
      
        # PARSE CODE
        lex= Lexer().lexer
        try:
            parserInstance = Parser(lex)
            parseResult = parserInstance.parser.parse(code, lexer=lex, debug=False)
        except Exception as e:
        # Check if parserInstance has an error message
            if parserInstance.parseErrorMessage:
                message = parserInstance.parseErrorMessage
            else:
                # Fallback error using internal line number if available
                line = 1
                message = [f"Syntax Error present: {str(e)}"]
            
            return jsonify({
                "tokens": lexOutput,
                "parseTree": None,
                "explanation": ai_explanation,
                "output": message
            }), 200
            
        if parserInstance.parseErrorMessage:
            return jsonify({
                "tokens": lexOutput,
                "parseTree": None,
                "explanation": ai_explanation,
                "output": parserInstance.parseErrorMessage
            }), 200

        # Perform semantic analysis
        try:
            semantic_analyzer = SemanticAnalyzer()
            semantic_analyzer.interpret(parseResult)
        except Exception as e:
        # Check if semantic analyzer has error message
            if  semantic_analyzer.semantic_errors:
                message = semantic_analyzer.semantic_errors
            else:
                line = semantic_analyzer.line_number
                message = [ f"Semantic Error at line {line}: {str(e)}" ]

            return jsonify({
                "tokens": lexOutput,
                "parseTree": parseResult,
                "explanation": ai_explanation,
                "output": message
            }), 200

        if semantic_analyzer.semantic_errors:
            return jsonify({
                "tokens": lexOutput,
                "parseTree": parseResult,
                "explanation": ai_explanation,
                "output": semantic_analyzer.semantic_errors
            }), 200
            
        return jsonify({
        "tokens": lexOutput, 
        "parseTree": parseResult,
        "explanation": ai_explanation,
        "output": semantic_analyzer.compile_results
        }), 200

    except Exception as e:
        return jsonify({
            "tokens": None,
            "parseTree": None,
            "explanation": ai_explanation,
            "output": f"❌ Compilation failed: {str(e)}"
        }), 500