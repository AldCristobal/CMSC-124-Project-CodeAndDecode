class SyntaxAnalyzer:
    def __init__(self, token_list):
        self.tokens = token_list  # List of tokens
        self.keys = [list(token.keys())[0] for token in token_list]
        self.types = [list(token.values())[0] for token in token_list]
        self.index = 0
        self.ast = []  # This will hold the abstract syntax tree (AST) or statement list
        self.console = []  # This will hold the console output

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
        self.ast.append(self.parse_statement_list())
        self.expect("KTHXBYE")

    def parse_statement_list(self):
        """Parse a list of statements, separated by logical delimiters."""
        statements = []
        while self.current_token() and self.current_token() not in {"KTHXBYE"}:
            statements.append(self.parse_statement())
            if self.current_token() in {"KTHXBYE"}:
                break  # End of the block or program
        return statements

    def parse_statement(self):
        """Parse a single statement."""
        if self.current_token() == "VISIBLE":
            return self.parse_print()
        elif self.current_token() == "WAZZUP":
            return self.parse_var_dec_list()
        elif self.current_type() == "Identifier":
            if self.index + 1 < len(self.keys) and self.keys[self.index + 1] == "R":
                return self.parse_assignment()
            else:
                return self.parse_expr()
        elif self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF"}:
            return self.parse_math_expr()
        elif self.current_token() == "GIMMEH":
            return self.parse_input()
        else:
            raise SyntaxError(f"Unexpected statement: {self.current_token()}")

    def parse_input(self):
        """<input> ::= GIMMEH varident"""
        self.expect("GIMMEH")
        identifier = self.current_token()
        self.expect_identifier()
        return {"type": "input", "name": identifier}

    def parse_print(self):
        """<print> ::= VISIBLE <generic_operand>"""
        self.expect("VISIBLE")
        operand = self.parse_generic_operand()
        return {"type": "print", "operand": operand}

    def parse_generic_operand(self):
        """<generic_operand> ::= varident | <expr> | <literal>"""
        if self.current_type() in {"Identifier", "Literal"}:
            token = self.current_token()
            self.advance()
            return {"type": "literal" if self.current_type() == "Literal" else "identifier", "value": token}
        elif self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF"}:
            return self.parse_math_expr()
        else:
            raise SyntaxError(f"Expected operand, but got '{self.current_token()}'")

    def parse_var_dec_list(self):
        """<var_dec_list> ::= <var_dec> | <var_dec> <var_dec_list>"""
        self.expect("WAZZUP")
        var_declarations = []
        while self.current_token() != "BUHBYE":
            var_declarations.append(self.parse_var_dec())
            if self.current_token() == "BUHBYE":
                self.advance()
                break  # End of the var declaration block
        return {"type": "var_dec_list", "declarations": var_declarations}

    def parse_var_dec(self):
        """<var_dec> ::= I HAS A varident | I HAS A varident ITZ <generic_operand>"""
        self.expect("I HAS A")
        identifier = self.current_token()
        self.expect_identifier()
        var_dec = {"type": "var_dec", "name": identifier, "initialized": False}

        if self.current_token() == "ITZ":
            self.expect("ITZ")
            operand = self.parse_generic_operand()
            var_dec["initialized"] = {"type": "assignment", "value": operand}

        return var_dec

    def parse_assignment(self):
        """<assignment> ::= varident R <generic_operand>"""
        identifier = self.current_token()
        self.expect_identifier()
        self.expect("R")
        operand = self.parse_generic_operand()
        return {"type": "assignment", "name": identifier, "value": operand}

    def parse_expr(self):
        """<expr> ::= <math_expr> | <bool_expr> | <smoosh_expr>"""
        if self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "BIGGR OF", "SMALLR OF"}:
            return self.parse_math_expr()
        elif self.current_token() in {"BOTH OF", "EITHER OF", "WON OF", "BOTH SAEM", "DIFFRINT", "NOT"}:
            return self.parse_bool_expr()
        elif self.current_token() == "SMOOSH":
            return self.parse_smoosh_expr()
        else:
            raise SyntaxError(f"Unexpected expression: {self.current_token()}")

    def parse_math_expr(self):
        """<math_expr> ::= <math_operand> | <math_operator> <math_expr> AN <math_operand>"""
        left_operand = self.parse_math_operand()
        if self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "BIGGR OF", "SMALLR OF"}:
            operator = self.current_token()
            self.advance()
            right_operand = self.parse_math_expr()
            return {"type": "math_expr", "operator": operator, "left": left_operand, "right": right_operand}
        return left_operand

    def parse_math_operand(self):
        """<math_operand> ::= numbr | numbar | varident | <math_expr>"""
        if self.current_type() in {"Literal", "Identifier"}:
            token = self.current_token()
            self.advance()
            return {"type": "literal" if self.current_type() == "Literal" else "identifier", "value": token}
        elif self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF"}:
            return self.parse_math_expr()
        else:
            raise SyntaxError(f"Expected math operand, but got '{self.current_token()}'")

    def parse_bool_expr(self):
        """<bool_expr> ::= NOT <bool_operand> | <bool_operator> <bool_operand> AN <bool_operand>"""
        # Placeholder for future extension
        pass

    def parse_smoosh_expr(self):
        """<smoosh_expr> ::= SMOOSH <generic_operand> AN <more_smoosh>"""
        self.expect("SMOOSH")
        operand = self.parse_generic_operand()
        if self.current_token() == "AN":
            self.advance()
            more_operands = self.parse_smoosh_expr()
            return {"type": "smoosh_expr", "parts": [operand, *more_operands]}
        return {"type": "smoosh_expr", "parts": [operand]}

    def expect_identifier(self):
        """Expect an identifier."""
        if self.current_type() == "Identifier":
            self.advance()
        else:
            raise SyntaxError(f"Expected identifier, but got '{self.current_token()}'")

    def analyze(self):
        """Start the syntax analysis and return the AST."""
        try:
            self.parse_program()
            print("Syntax analysis completed successfully!")
            return self.ast
        except SyntaxError as e:
            self.console.append(f"Syntax error: {e}")
            print(f"Syntax error: {e}")
            return None
