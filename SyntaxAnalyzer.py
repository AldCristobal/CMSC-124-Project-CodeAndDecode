class SyntaxAnalyzer:
    def __init__(self, token_list):
        self.tokens = token_list                                        # example [{'HAI': 'Code Delimiter'}, {'VISIBLE': 'Output Keyword'}, {'8': 'Literal'}, {'VISIBLE': 'Output Keyword'}, {'5': 'Literal'}, {'KTHXBYE': 'Code Delimiter'}]
        self.keys = [list(token.keys())[0] for token in token_list]     
        self.types = [list(token.values())[0] for token in token_list]  
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
        """<program> ::= HAI <statement_list> KTHXBYE"""
        self.expect("HAI")
        self.parse_statement_list()
        self.expect("KTHXBYE")

    def parse_statement_list(self):
        """Parse a list of statements, separated by logical delimiters."""
        while self.current_token() and self.current_token() not in {"KTHXBYE", "BUHBYE"}:
            self.parse_statement()
            if self.current_token() in {"BUHBYE", "KTHXBYE"}:
                break  # End of the block or program

    def parse_statement(self):
        """Parse a single statement."""
        if self.current_token() == "VISIBLE":
            self.parse_print()
        elif self.current_token() == "WAZZUP":
            self.parse_var_dec_list()
        elif self.current_type() == "Identifier":
            if self.index + 1 < len(self.keys) and self.keys[self.index + 1] == "R":
                self.parse_assignment()
            else:
                self.parse_expr()
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
        """<var_dec_list> ::= <var_dec> | <var_dec> <var_dec_list>"""
        self.expect("WAZZUP")
        while self.current_token() != "BUHBYE":
            self.parse_var_dec()
            if self.current_token() == "BUHBYE":
                break  # End of the var declaration block

    def parse_var_dec(self):
        """<var_dec> ::= I HAS A varident | I HAS A varident ITZ <generic_operand>"""
        self.expect("I HAS A")
        self.expect_identifier()
        if self.current_token() == "ITZ":
            self.expect("ITZ")
            self.parse_generic_operand()

    def parse_assignment(self):
        """<assignment> ::= varident R <generic_operand>"""
        self.expect_identifier()
        self.expect("R")
        self.parse_generic_operand()

    def parse_expr(self):
        """<expr> ::= <math_expr> | <bool_expr> | <smoosh_expr>"""
        if self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "BIGGR OF", "SMALLR OF"}:
            self.parse_math_expr()
        elif self.current_token() in {"BOTH OF", "EITHER OF", "WON OF", "BOTH SAEM", "DIFFRINT", "NOT"}:
            self.parse_bool_expr()
        elif self.current_token() == "SMOOSH":
            self.parse_smoosh_expr()
        else:
            raise SyntaxError(f"Unexpected expression: {self.current_token()}")

    def parse_math_expr(self):
        """<math_expr> ::= <math_operand> | <math_operator> <math_expr> AN <math_operand>"""
        self.parse_math_operand()
        if self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "BIGGR OF", "SMALLR OF"}:
            self.parse_math_operator()
            self.parse_math_expr()

    def parse_math_operand(self):
        """<math_operand> ::= numbr | numbar | varident | <math_expr>"""
        if self.current_type() in {"Literal", "Identifier"}:
            self.advance()
        elif self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF"}:
            self.parse_math_expr()
        else:
            raise SyntaxError(f"Expected math operand, but got '{self.current_token()}'")

    def parse_math_operator(self):
        """<math_operator> ::= SUM OF | DIFF OF | PRODUKT OF | QUOSHUNT OF"""
        if self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF"}:
            self.advance()
        else:
            raise SyntaxError(f"Expected math operator, but got '{self.current_token()}'")

    def parse_bool_expr(self):
        """<bool_expr> ::= NOT <bool_operand> | <bool_operator> <bool_operand> AN <bool_operand>"""
        # Placeholder, extend as needed
        pass

    def parse_smoosh_expr(self):
        """<smoosh_expr> ::= SMOOSH <generic_operand> AN <more_smoosh>"""
        self.expect("SMOOSH")
        self.parse_generic_operand()
        if self.current_token() == "AN":
            self.advance()
            self.parse_smoosh_expr()

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
