class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens  # Dictionary of tokens
        self.keys = list(tokens.keys())  # Token keys (lexemes)
        self.types = list(tokens.values())  # Corresponding types
        self.index = 0

    def current_token(self):
        """Get the current token."""
        return self.keys[self.index] if self.index < len(self.keys) else None

    def current_type(self):
        """Get the type of the current token."""
        return self.types[self.index] if self.index < len(self.types) else None

    def advance(self):
        """Move to the next token."""
        self.index += 1

    def expect(self, expected_token):
        """Expect a specific token and advance."""
        if self.current_token() == expected_token:
            self.advance()
        else:
            raise SyntaxError(f"Expected '{expected_token}', but got '{self.current_token()}'")

    def parse_program(self):
        """<program> ::= HAI <linebreak> <statement> <linebreak> KTHXBYE"""
        self.expect("HAI")  # Code Delimiter
        self.parse_linebreak()
        self.parse_statement_list()
        self.parse_linebreak()
        self.expect("KTHXBYE")  # Code Delimiter

    def parse_linebreak(self):
        """Allow linebreaks (for simplicity)."""
        while self.current_type() == "NEWLINE":
            self.advance()

    def parse_statement_list(self):
        """Parse a recursive list of statements."""
        while self.current_token() not in {"KTHXBYE", None}:
            self.parse_statement()
            self.parse_linebreak()

    def parse_statement(self):
        """Parse a single statement."""
        if self.current_token() == "VISIBLE":
            self.parse_print()
        elif self.current_token() == "WAZZUP":
            self.parse_var_dec_list()
        elif self.current_type() == "Identifier":
            if self.keys[self.index + 1] == "R":
                self.parse_assignment()
        elif self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF"}:
            self.parse_math_expr()
        else:
            raise SyntaxError(f"Unexpected statement: {self.current_token()}")

    def parse_print(self):
        """<print> ::= VISIBLE <generic_operand>"""
        self.expect("VISIBLE")
        self.parse_generic_operand()

    def parse_generic_operand(self):
        """<generic_operand> ::= varident | <expr> | <literal>"""
        if self.current_type() in {"Identifier", "Literal"}:
            self.advance()
        elif self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF"}:
            self.parse_math_expr()
        else:
            raise SyntaxError(f"Expected operand, but got '{self.current_token()}'")

    def parse_var_dec_list(self):
        """<var_dec_list> ::= <var_dec> | <var_dec> <linebreak> <var_dec_list>"""
        self.expect("WAZZUP")  # Var. Dec. List Delimiter
        while self.current_token() != "BUHBYE":  # Var. Dec. List Delimiter
            self.parse_var_dec()
            self.parse_linebreak()
        self.expect("BUHBYE")

    def parse_var_dec(self):
        """<var_dec> ::= I HAS A varident | I HAS A varident ITZ <generic_operand>"""
        print(f"Parsing variable declaration at token: {self.current_token()}")
        self.expect("I HAS A")  # Expect 'I HAS A'
        self.expect_identifier()  # Expect a variable identifier
        if self.current_token() == "ITZ":  # Optional ITZ clause
            print(f"Found ITZ at token: {self.current_token()}")
            self.expect("ITZ")
            self.parse_generic_operand()
        print("Finished parsing variable declaration.")


    def parse_assignment(self):
        """<assignment> ::= varident R <generic_operand>"""
        self.expect_identifier()
        self.expect("R")
        self.parse_generic_operand()

    def parse_math_expr(self):
        """<math_expr> ::= <math_operand> | <math_operator> <math_expr> AN <math_operand>"""
        self.parse_math_operator()
        self.parse_math_operand()
        self.expect("AN")
        self.parse_math_operand()

    def parse_math_operator(self):
        """<math_operator> ::= SUM OF | DIFF OF | PRODUKT OF | QUOSHUNT OF"""
        if self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF"}:
            self.advance()
        else:
            raise SyntaxError(f"Expected math operator, but got '{self.current_token()}'")

    def parse_math_operand(self):
        """<math_operand> ::= numbr | numbar | varident | <math_expr>"""
        if self.current_type() in {"Literal", "Identifier"}:
            self.advance()
        elif self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF"}:
            self.parse_math_expr()
        else:
            raise SyntaxError(f"Expected math operand, but got '{self.current_token()}'")

    def expect_identifier(self):
        """Expect an identifier."""
        if self.current_type() == "Identifier":
            self.advance()
        else:
            raise SyntaxError(f"Expected identifier, but got '{self.current_token()}'")

    def analyze(self):
        """Start the syntax analysis."""
        try:
            self.parse_program()
            print("Syntax analysis completed successfully!")
        except SyntaxError as e:
            print(f"Syntax error: {e}")

