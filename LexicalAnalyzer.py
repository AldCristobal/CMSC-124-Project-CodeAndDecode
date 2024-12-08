import re

class LexicalAnalyzer:
    def __init__(self):
        self.tokens = []
        self.lexemes = []
        self.rows = []
        self.columns = []
        self.lin_num = 1
        self.lin_start = 0

        # Tokens' higher level classifications
        self.token_classifications = {
            "Code Delimiter": ["START", "END"],
            "Var. Dec. List Delimiter": ["VAR_INIT_START", "VAR_INIT_END"],
            "Variable Declaration": ["VAR_INIT"],
            "Comment": ["COMMENT_START", "MULTILINE_COMMENT_START", "MULTILINE_COMMENT_END"],
            "Variable Assignment": ["VAR_INIT_VALUE", "ASSIGNMENT"],
            "Math Operator": ["ARITHMETIC_OPERATOR"],
            "Boolean Operator": ["BOOL_OPERATOR"],
            "Concatenation": ["CONCAT"],
            "Typecast": ["TYPECAST", "RECAST"],
            "Output Keyword": ["PRINT"],
            "Input Keyword": ["INPUT"],
            "If-then Keyword": ["IF_THEN", "IF", "ELIF", "ELSE", "IFSWITCH_END"],
            "Switch-case Keyword": ["SWITCH", "CASE", "CASE_END"],
            "Loop Keyword": ["LOOP_START", "LOOP_END", "LOOP_ITERATOR", "LOOPFUNC_PARAM", "LOOP_BOOL"],
            "Function Keyword": ["FUNC_START", "FUNC_END", "FUNC_RETURN_START", "FUNC_RETURN_END", "FUNC_CALL_START", "FUNC_CALL_END"],
            "Datatype Keyword": ["DATA_TYPE"],
            "Literal": ["TROOF", "NUMBAR", "NUMBR", "YARN"],
            "Identifier": ["VARIABLE"],
            "Whitespace": ["NEWLINE", "TAB", "WHITESPACE"],
            "Print Add Arity": ["PRINT_ADD_ARITY"],
            "Add Arity": ["ADD_ARITY"],
            "Unrecognized": ["UNRECOGNIZED"]
        }

        # Token lower level classifications
        self.rules = [
            ("START", r"HAI"),
            ("END", r"KTHXBYE"),
            ("VAR_INIT_START", r"WAZZUP"),
            ("VAR_INIT_END", r"BUHBYE"),
            ("COMMENT_START", r"BTW"),
            ("MULTILINE_COMMENT_START", r"OBTW"),
            ("MULTILINE_COMMENT_END", r"TLDR"),
            ("VAR_INIT", r"I HAS A"),
            ("VAR_INIT_VALUE", r"ITZ"),
            ("ASSIGNMENT", r"R"),
            ("ARITHMETIC_OPERATOR", r"SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF"),
            ("BOOL_OPERATOR", r"BOTH OF|EITHER OF|WON OF|BOTH SAEM|DIFFRINT|NOT|ALL OF|ANY OF"),
            ("CONCAT", r"SMOOSH"),
            ("TYPECAST", r"MAEK"),
            ("RECAST", r"IS NOW A"),
            ("PRINT", r"VISIBLE"),
            ("INPUT", r"GIMMEH"),
            ("IF_THEN", r"O RLY\?"),
            ("IF", r"YA RLY"),
            ("ELIF", r"MEBBE"),
            ("ELSE", r"NO WAI"),
            ("IFSWITCH_END", r"OIC"),
            ("SWITCH", r"WTF\?"),
            ("CASE", r"OMG"),
            ("CASE_END", r"OMGWTF"),
            ("LOOP_START", r"IM IN YR"),
            ("LOOP_END", r"IM OUTTA YR"),
            ("LOOP_ITERATOR", r"UPPIN|NERFIN"),
            ("LOOPFUNC_PARAM", r"YR"),
            ("LOOP_BOOL", r"TIL|WILE"),
            ("FUNC_START", r"HOW IZ I"),
            ("FUNC_END", r"IF U SAY SO"),
            ("FUNC_RETURN_START", r"FOUND YR"),
            ("FUNC_RETURN_END", r"GTFO"),
            ("FUNC_CALL_START", r"I IZ"),
            ("FUNC_CALL_END", r"MKAY"),
            ("DATA_TYPE", r"(NOOB|TROOF|NUMBAR|NUMBR|YARN)"),
            ("TROOF", r"(WIN|FAIL)"),
            ("ADD_ARITY", r"AN"),
            ("NUMBAR", r"-?\d+\.\d+"),
            ("NUMBR", r"-?\d+"),
            ("YARN", r'"([^"]*)"'),
            ("VARIABLE", r"[a-zA-Z]\w*"),
            ("NEWLINE", r"\n"),
            ("TAB", r"[\t]+"),
            ("WHITESPACE", r"[ ]+"),
            ("PRINT_ADD_ARITY", r"\+"),
            ("UNRECOGNIZED", r"."),
        ]

    def gen_tokens(self, code):
        self.tokens.clear()
        self.lexemes.clear()
        self.rows.clear()
        self.columns.clear()
        
        token_rules = "|".join(f"(?P<{name}>{pattern})" for name, pattern in self.rules)
        comment_flag = False
        multi_comment_flag  = False
        comment = ""
        comment_column = 0

        for match in re.finditer(token_rules, code):
            token_type = match.lastgroup
            token_lexeme = match.group()
            col = match.start() - self.lin_start

            if token_type == "NEWLINE":
                if comment_flag:
                    if not multi_comment_flag:
                        comment_flag = False
                    if comment:
                        self.columns.append(comment_column)
                        self.tokens.append("COMMENT")
                        self.lexemes.append(comment)
                        self.rows.append(self.lin_num)
                        comment, comment_column = "", 0
                self.columns.append(col)
                self.tokens.append(token_type)
                self.lexemes.append("\\n")
                self.rows.append(self.lin_num)
                self.lin_start = match.end()
                self.lin_num += 1
            elif token_type == "MULTILINE_COMMENT_END":
                comment_flag, multi_comment_flag = False, False
                self.columns.append(col)
                self.tokens.append(token_type)
                self.lexemes.append(token_lexeme)
                self.rows.append(self.lin_num)
            elif comment_flag:
                comment += token_lexeme
            elif token_type in ("COMMENT_START", "MULTILINE_COMMENT_START"):
                comment_flag = True
                if token_type == "MULTILINE_COMMENT_START":
                    multi_comment_flag = True
                self.columns.append(col)
                comment_column = col + 1
                self.tokens.append(token_type)
                self.lexemes.append(token_lexeme)
                self.rows.append(self.lin_num)
            elif token_type not in ("TAB", "WHITESPACE"):
                self.columns.append(col)
                classification = next((key for key, value in self.token_classifications.items() if token_type in value), "Unclassified")
                self.tokens.append(classification)
                self.lexemes.append(token_lexeme)
                self.rows.append(self.lin_num)
                print(f"Token: {token_lexeme}, Type: {token_type}, Classification: {classification}")

        return self.tokens, self.lexemes, self.rows, self.columns