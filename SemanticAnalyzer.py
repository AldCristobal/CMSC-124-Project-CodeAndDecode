class SemanticAnalyzer:
    def __init__(self, token_list):
        self.tokens = token_list
        print(self.tokens)
        self.symbol_table = {} 
        self.index = 0

    def current_token(self):
        """Get the current token."""
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def advance(self):
        """Move to the next token."""
        self.index += 1

    def analyze_var_dec(self):
        """Analyze variable declarations and add to the symbol table."""
        if self.current_token().get("WAZZUP"):
            self.advance()  
            while self.current_token() and self.current_token().get("Identifier"):
                identifier = self.current_token()["Identifier"]
                if identifier in self.symbol_table:
                    raise NameError(f"Variable '{identifier}' already declared.")
                self.symbol_table[identifier] = None
                self.advance()
                if self.current_token() == "ITZ":
                    self.advance()
                    self.analyze_expr()  
                    self.symbol_table[identifier] = "Assigned"
                if self.current_token() == "BUHBYE":
                    break

    def analyze_expr(self):
        """Analyze expressions and update the symbol table if needed."""
        if self.current_token().get("Identifier"):
            self.expect_identifier()
        elif self.current_token().get("Literal"):
            self.expect_literal()
        elif self.current_token() in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF"}:
            self.advance()  # Move past the operator
            self.analyze_expr()  # Check left operand
            self.analyze_expr()  # Check right operand
        else:
            raise SyntaxError(f"Unexpected token in expression: '{self.current_token()}'")

    def expect_identifier(self):
        """Expect an identifier and check if it is declared."""
        if self.current_token() and self.current_token().get("Identifier"):
            identifier = self.current_token()["Identifier"]
            if identifier not in self.symbol_table:
                raise NameError(f"Undeclared variable '{identifier}' used.")
            self.advance()
        else:
            raise SyntaxError(f"Expected identifier, but got '{self.current_token()}'")

    def expect_literal(self):
        """Expect a literal and check type."""
        if self.current_token() and self.current_token().get("Literal"):
            self.advance()
        else:
            raise SyntaxError(f"Expected a literal, but got '{self.current_token()}'")

    def analyze_print(self):
        """Analyze print statements."""
        self.advance()  # Skip 'VISIBLE'
        self.analyze_expr()  # The expression inside the print must be valid

    def analyze_assignment(self):
        """Analyze assignments and ensure correct types."""
        identifier = self.current_token().get("Identifier")
        if identifier not in self.symbol_table:
            raise NameError(f"Variable '{identifier}' not declared.")
        self.advance()
        if self.current_token().get("R"):
            self.advance()
            self.analyze_expr()
            # Update symbol table with assigned value
            self.symbol_table[identifier] = "Assigned"

    def analyze_statement(self):
        """Analyze a single statement based on its type."""
        if self.current_token().get("VISIBLE"):
            self.analyze_print()
        elif self.current_token().get("WAZZUP"):
            self.analyze_var_dec()
        elif self.current_token().get("Identifier"):
            if self.index + 1 < len(self.tokens) and self.tokens[self.index + 1].get("R"):
                self.analyze_assignment()
            else:
                self.analyze_expr()
        else:
            raise SyntaxError(f"Unexpected statement: {self.current_token()}")

    def analyze_program(self):
        """Analyze the whole program."""
        self.advance()  # Skip 'HAI'
        while self.current_token() and self.current_token().get("KTHXBYE") is None:
            self.analyze_statement()
            if self.current_token().get("BUHBYE"):
                break  # End of the block or program
        if self.current_token() and self.current_token().get("KTHXBYE"):
            self.advance()  # Skip 'KTHXBYE'

    def analyze(self):
        """Start the semantic analysis."""
        try:
            self.analyze_program()
            print(self.symbol_table)
            print("Semantic analysis completed successfully!")
        except (SyntaxError, NameError) as e:
            print(f"Semantic error: {e}")
