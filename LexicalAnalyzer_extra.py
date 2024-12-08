import re

# Dictionary of lexeme patterns and their classifications
lexeme_classification = {
    "^HAI$": "Code Delimiter",
    "^KTHXBYE$": "Code Delimiter",
    "^WAZZUP$": "Variable Declaration Delimiter",
    "^BUHBYE$": "Variable Declaration Delimiter",
    "^BTW$": "Comment Keyword",
    "^OBTW$": "Comment Keyword",
    "^TLDR$": "Comment Keyword",
    "^I HAS A$": "Variable Declaration",
    "^ITZ$": "Variable Assignment",
    "^R$": "Variable Assignment",
    "^SUM OF$": "Math Operator",
    "^DIFF OF$": "Math Operator",
    "^PRODUKT OF$": "Math Operator",
    "^QUOSHUNT OF$": "Math Operator",
    "^MOD OF$": "Math Operator",
    "^BIGGR OF$": "Math Operator",
    "^SMALLR OF$": "Math Operator",
    "^BOTH OF$": "Boolean Operator",
    "^EITHER OF$": "Boolean Operator",
    "^WON OF$": "Boolean Operator",
    "^NOT$": "Boolean Operator",
    "^ANY OF$": "Boolean Operator",
    "^ALL OF$": "Boolean Operator",
    "^BOTH SAEM$": "Boolean Operator",
    "^DIFFRINT$": "Boolean Operator",
    "^SMOOSH$": "Concatenation Keyword",
    "^MAEK$": "Typecast Keyword",
    "^A$": "Typecast Keyword",
    "^IS NOW A$": "Typecast Keyword",
    "^VISIBLE$": "Output Keyword",
    "^GIMMEH$": "Input Keyword",
    "^O RLY\\?$": "If-then Keyword",
    "^YA RLY$": "If-then Keyword",
    "^MEBBE$": "If-then Keyword",
    "^NO WAI$": "If-then Keyword",
    "^OIC$": "If-then Keyword",
    "^WTF\\?$": "Switch-case Keyword",
    "^OMG$": "Switch-case Keyword",
    "^OMGWTF$": "Switch-case Keyword",
    "^IM IN YR$": "Loop Keyword",
    "^UPPIN$": "Loop Keyword",
    "^NERFIN$": "Loop Keyword",
    "^YR$": "Loop Keyword",
    "^TIL$": "Loop Keyword",
    "^WILE$": "Loop Keyword",
    "^IM OUTTA YR$": "Loop Keyword",
    "^HOW IZ I$": "Function Keyword",
    "^IF U SAY SO$": "Function Keyword",
    "^GTFO$": "Function Keyword",
    "^FOUND YR$": "Function Keyword",
    "^I IZ$": "Function Keyword",
    "^MKAY$": "Function Keyword",
    "^[a-zA-Z]\w*$": "Identifier",
    "^-?\d+$": "Literal",
    "^-?\d+\.\d+$": "Literal",
    "^\"([^\"]*)\"$": "Literal",
    "^(WIN|FAIL)$": "Literal",
    "^(NOOB|TROOF|NUMBAR|NUMBR|YARN)$": "Type Literal",
}

class LexicalAnalyzer:
    def __init__(self):
        self.tokens = []
        self.lexemes = []
        self.rows = []
        self.columns = []
        self.lin_num = 1
        self.lin_start = 0

    def gen_tokens(self, code):
        self.tokens.clear()
        self.lexemes.clear()
        self.rows.clear()
        self.columns.clear()

        # Combine all patterns into one large regex
        combined_pattern = "|".join(
            f"(?P<{name}>{pattern})" for name, pattern in lexeme_classification.items()
        )

        for m in re.finditer(combined_pattern, code):
            for name, pattern in lexeme_classification.items():
                if m.lastgroup == name:
                    token_type = lexeme_classification[pattern]
                    token_lexeme = m.group(name)

                    # Avoid adding whitespace and newline tokens if needed
                    if token_type not in {"WHITESPACE", "NEWLINE"}:
                        col = m.start() - self.lin_start
                        self.columns.append(col)
                        self.tokens.append(token_type)
                        self.lexemes.append(token_lexeme)
                        self.rows.append(self.lin_num)

            # Handle line changes and update line number
            if "\n" in m.group(0):
                self.lin_num += m.group(0).count("\n")
                self.lin_start = m.end()

        return self.tokens, self.lexemes, self.rows, self.columns

class LexicalAnalyzer:
    def __init__(self):
        # Compile regex patterns
        self.regex_patterns = {pattern: classification for pattern, classification in lexeme_classification.items()}
        self.compiled_patterns = [(re.compile(pattern), classification) for pattern, classification in self.regex_patterns.items()]

    def gen_tokens(self, code):
        tokens = []
        lines = code.splitlines()
        
        for line_number, line in enumerate(lines, start=1):
            # Ignore comments and empty lines
            if line.strip().startswith(('BTW', 'OBTW', 'TLDR')):
                continue

            words = line.split()
            for word in words:
                matched = False
                for regex, classification in self.compiled_patterns:
                    if regex.fullmatch(word):
                        tokens.append((word, classification))
                        matched = True
                        break
                if not matched:
                    tokens.append((word, "Unknown"))
        
        return tokens


