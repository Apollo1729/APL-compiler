import ply.lex as lex


class Lexer:
    # Token names - Updated with specific keyword tokens
    tokens = (
        "KEYWORD_BEGIN",
        "KEYWORD_END",
        "KEYWORD_LET",
        "KEYWORD_IF",
        "KEYWORD_ELSE",
        "KEYWORD_ELSEIF",
        "KEYWORD_FOR",
        "KEYWORD_WHILE",
        "KEYWORD_PRINT",
        "KEYWORD_TRUE",
        "KEYWORD_FALSE",
        "KEYWORD_FUNCTION",
        "KEYWORD_RETURN",
        "KEYWORD_BREAK",
        "KEYWORD_CONTINUE",
        "IDENTIFIER",
        "INTEGER",
        "FLOAT",
        "PLUS_OP",
        "MINUS_OP",
        "TIMES_OP",
        "DIVIDE_OP",
        "ASSIGNMENT_OP",
        "LPAREN",
        "RPAREN",
        "LT_OP",
        "GT_OP",
        "LE_OP",
        "GE_OP",
        "EQ_OP",
        "NE_OP",
        "STRING",
        "KEYWORD_TO",
        "KEYWORD_STEP",
        "KEYWORD_AND",
        "KEYWORD_OR",
        "KEYWORD_NOT",
        "COMMA",
        "SEMICOLON",
        "LBRACE",
        "RBRACE",
        "NEWLINE",
        "SET_KEYWORD_NATURAL_LANG",
        "ADD_KEYWORD_NATURAL_LANG",
        "SUB_KEYWORD_NATURAL_LANG",
        "MULT_KEYWORD_NATURAL_LANG",
        "DIV_KEYWORD_NATURAL_LANG",
        "FROM_KEYWORD_NATURAL_LANG",
        "BY_KEYWORD_NATURAL_LANG",
        "IS_KEYWORD_NATURAL_LANG",
        "THEN_KEYWORD_NATURAL_LANG",
    )

    # Keywords with specific token types
    keywords = {
        "begin": "KEYWORD_BEGIN",
        "end": "KEYWORD_END",
        "let": "KEYWORD_LET",
        "if": "KEYWORD_IF",
        "else": "KEYWORD_ELSE",
        "elseif": "KEYWORD_ELSEIF",
        "for": "KEYWORD_FOR",
        "while": "KEYWORD_WHILE",
        "print": "KEYWORD_PRINT",
        "to": "KEYWORD_TO",
        "step": "KEYWORD_STEP",
        "and": "KEYWORD_AND",
        "or": "KEYWORD_OR",
        "not": "KEYWORD_NOT",
        "true": "KEYWORD_TRUE",
        "false": "KEYWORD_FALSE",
        "function": "KEYWORD_FUNCTION",
        "return": "KEYWORD_RETURN",
        "break": "KEYWORD_BREAK",
        "continue": "KEYWORD_CONTINUE",
    }

    # Natural language keywords
    natural_language_keywords = {
        "set": "SET_KEYWORD_NATURAL_LANG",
        "add": "ADD_KEYWORD_NATURAL_LANG",
        "sub": "SUB_KEYWORD_NATURAL_LANG",
        "mult": "MULT_KEYWORD_NATURAL_LANG",
        "div": "DIV_KEYWORD_NATURAL_LANG",
        "from": "FROM_KEYWORD_NATURAL_LANG",
        "by": "BY_KEYWORD_NATURAL_LANG",
        "is": "IS_KEYWORD_NATURAL_LANG",
        "then": "THEN_KEYWORD_NATURAL_LANG",
    }

    # Regular expression rules for operators (order matters for multi-character operators)
    t_LE_OP = r"<="
    t_GE_OP = r">="
    t_EQ_OP = r"=="
    t_NE_OP = r"!="
    t_LT_OP = r"<"
    t_GT_OP = r">"
    t_ASSIGNMENT_OP = r"="
    t_PLUS_OP = r"\+"
    t_MINUS_OP = r"-"
    t_TIMES_OP = r"\*"
    t_DIVIDE_OP = r"/"
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACE = r"\{"
    t_RBRACE = r"\}"
    t_COMMA = r","
    t_SEMICOLON = r";"

    def __init__(self):
        """Initialize the lexer with token definitions and rules"""
        # Initialize the lexer
        self.lexer = lex.lex(module=self)
        self.expecting_variable = False
        self.declared_variables = []
        self.current_scope = 0
        self.scope_stack = [set()]
        self.errors = []

    # Scope management functions

    # Comments (ignored - no token returned)
    def t_COMMENT_MULTILINE(self, t):
        r"/\*(.|\n)*?\*/"
        t.lexer.lineno += t.value.count("\n")
        pass  # No return - token is ignored

    def t_COMMENT_SINGLE(self, t):
        r"//.*"
        pass  # No return - token is ignored

    # Match floating point numbers (must come before INTEGER)
    def t_FLOAT(self, t):
        r"-?\d+\.\d+"
        t.value = float(t.value)
        t.lineno = t.lexer.lineno
        return t

    # Match integer numbers (including negative)
    def t_INTEGER(self, t):
        r"-?\d+"
        t.value = int(t.value)
        t.lineno = t.lexer.lineno
        return t

    # Match string literals
    def t_STRING(self, t):
        r'"([^"\\]|\\.)*"'
        t.value = t.value[1:-1]  # Remove quotes
        # Handle escape sequences
        t.value = (
            t.value.replace("\\n", "\n")
            .replace("\\t", "\t")
            .replace('\\"', '"')
            .replace("\\\\", "\\")
        )
        t.lineno = t.lexer.lineno
        return t

    # Match identifiers and keywords
    def t_IDENTIFIER(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        # Check keywords first
        t.lineno = t.lexer.lineno
        if t.value in self.keywords:
            t.type = self.keywords[t.value]
            t.lineno = t.lexer.lineno
            return t
        # Check natural language keywords
        if t.value in self.natural_language_keywords:
            t.type = self.natural_language_keywords[t.value]
            t.lineno = t.lexer.lineno
            return t
        else:
            t.type = "IDENTIFIER"
            return t

    # Rule to track line numbers and preserve newlines for natural language parsing
    def t_NEWLINE(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    # Characters to ignore (spaces and tabs only)
    t_ignore = " \t\r"

    # Error handling rule
    def t_error(self, t):
        print(
            f"Illegal character '{t.value[0]}' at line {t.lineno}, position {t.lexpos}"
        )
        t.lexer.skip(1)

    # Test function with line numbers and positions
    def test_lexer(self, code, test_name="", show_format="detailed"):
        """Test the lexer with given code

        Args:
            code: Source code to tokenize
            test_name: Name for the test
            show_format: 'detailed', 'lextoken', or 'simple'
        """
        self.declared_variables, self.scope_stack, self.current_scope

        # Reset state for each test
        self.declared_variables = []
        self.current_scope = 0
        self.scope_stack = [set()]

        self.lexer.input(code)
        print(f"=== {test_name} ===")
        print("Tokenized Output:\n")
        tokens_list = []

        for token in self.lexer:
            if token.type != "NEWLINE":  # Skip newlines in output for clarity
                if show_format == "lextoken":
                    # PLY LexToken format: LexToken(TYPE,'value',line,position)
                    print(
                        f"LexToken({token.type},'{token.value}',{token.lineno},{token.lexpos})"
                    )
                elif show_format == "detailed":
                    # Detailed format with line and column
                    print(
                        f"{token.type}: '{token.value}' (line {token.lineno}, pos {token.lexpos})"
                    )
                else:
                    # Simple format
                    print(f"{token.type}: {token.value}")
                tokens_list.append(token)

        print(f"\nDeclared variables: {self.declared_variables}")
        print(f"Final scope level: {self.current_scope}")
        return tokens_list

    def analyze_tokens(self, code):
        """Analyze tokens and show detailed position information"""
        self.declared_variables, self.scope_stack, self.current_scope

        # Reset state
        self.declared_variables = []
        self.current_scope = 0
        self.scope_stack = [set()]

        # Split code into lines for reference
        lines = code.split("\n")
        print(lines)

        self.lexer.input(code)
        print("Token Analysis with Line Context:\n")
        print("-" * 60)
        output = []
        for token in self.lexer:
            if token.type != "NEWLINE":
                # Calculate column position
                line_start = 0
                for i in range(token.lineno - 1):
                    if i < len(lines):
                        line_start += len(lines[i]) + 1  # +1 for newline

                col_pos = token.lexpos - line_start + 1

                # Show token with context
                print(
                    f"LexToken({token.type},'{token.value}',{token.lineno},{token.lexpos})"
                )
                output.append(
                    f"LexToken({token.type},'{token.value}',{token.lineno},{token.lexpos})"
                )
                if token.lineno <= len(lines):
                    current_line = lines[token.lineno - 1]
                    print(f"  Line {token.lineno}: {current_line}")
                    print(f"  Column {col_pos}: {' ' * (col_pos - 1)}^")
                    output.append(f"  Line {token.lineno}: {lines[token.lineno-1]}")
                    output.append(f"  Column {col_pos}: {' ' * (col_pos - 1)}^")
        return output

    def get_column_position(token, code_lines):
        """Calculate column position for a token"""
        if token.lineno <= len(code_lines):
            line = code_lines[token.lineno - 1]
            # Find the position within the line
            line_start_pos = sum(
                len(code_lines[i]) + 1 for i in range(token.lineno - 1)
            )
            return token.lexpos - line_start_pos + 1
        return 0
