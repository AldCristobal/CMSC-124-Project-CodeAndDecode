import re

class LexicalAnalyzer:
    def __init__(self):
        self.tokens = []
        self.lexemes = []
        self.rows = []
        self.columns = []
        self.lin_num = 1
        self.lin_start = 0
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
        
        token_rules = "|".join(f"(?P<{x[0]}>{x[1]})" for x in self.rules)

        comment_bool = False
        multi_comment_bool = False
        comment = ""
        comment_column = 0

        for m in re.finditer(token_rules, code):
            token_type = m.lastgroup
            token_lexeme = m.group(token_type)

            # print(token_lexeme, token_type)
            if token_type == "NEWLINE":
                if comment_bool:
                    if not multi_comment_bool:
                        comment_bool = False
                    if comment != '':
                        col = m.start() - self.lin_start
                        self.columns.append(comment_column)
                        self.tokens.append("COMMENT")	
                        self.lexemes.append(comment)
                        self.rows.append(self.lin_num)
                        comment = ""
                        comment_column = 0
                col = m.start() - self.lin_start
                self.columns.append(col)
                self.tokens.append(token_type)
                self.lexemes.append("\\n")
                self.rows.append(self.lin_num)
                self.lin_start = m.end()
                self.lin_num += 1
            elif token_type == "MULTILINE_COMMENT_END":
                comment_bool = False
                multi_comment_bool = False
                col = m.start() - self.lin_start
                self.columns.append(col)
                self.tokens.append(token_type)
                self.lexemes.append(token_lexeme)
                self.rows.append(self.lin_num)
            elif comment_bool:
                comment += token_lexeme
            elif token_type == "COMMENT_START" or token_type == "MULTILINE_COMMENT_START":
                comment_bool = True
                if token_type == "MULTILINE_COMMENT_START":
                    multi_comment_bool = True
                
                col = m.start() - self.lin_start
                comment_column = col+1

                self.columns.append(col)
                self.tokens.append(token_type)
                self.lexemes.append(token_lexeme)
                self.rows.append(self.lin_num)
            elif token_type in ("TAB", "WHITESPACE"):
                continue
            # elif token_type == "UNRECOGNIZED":
            #     error = f"ERROR: {token_lexeme[0]} unexpected on line {self.lin_num}"
            #     return False, error, False, False
            else:
    
                col = m.start() - self.lin_start
                self.columns.append(col)
                self.tokens.append(token_type)
                self.lexemes.append(token_lexeme)
                self.rows.append(self.lin_num)
        # print(self.tokens)
        return self.tokens, self.lexemes, self.rows, self.columns
