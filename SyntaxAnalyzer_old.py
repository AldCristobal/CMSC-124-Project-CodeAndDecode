import re

class SyntaxAnalyzer:
    def __init__(self):
        self.tokens = []
        self.rows = []
        self.columns = []
        self.index = 0
        self.body_location = 0
        self.grammar = {
            "comment": lambda: ["COMMENT_START", "MULTILINE_COMMENT_START", "COMMENT", "MULTILINE_COMMENT_END"],
            "linebreak": lambda: ["NEWLINE"],
            "start": lambda: ["START"],
            "end": lambda: ["END"],
            "statement": lambda: ["PRINT", "INPUT", "VAR_INIT_START", ],
            "variable": lambda: ["VARIABLE"],
            "literal": lambda: ["TROOF", "NUMBAR", "NUMBR", "YARN"],
            "expression": lambda: ["ARITHMETIC_OPERATOR", "BOOL_OPERATOR", "CONCAT"],
            "generic_operand": lambda: self.grammar["variable"]() + self.grammar["literal"]() + self.grammar["expression"](), 
            "var_dec": lambda: ["VAR_INIT", "VAR_INIT_VALUE"],
            "var_dec_end": lambda: ["VAR_INIT_END"],
            "var_dec_value": lambda: ["VAR_INIT_VALUE"],	
        }


    def check_syntax(self, tokens, rows, columns):
        # print(self.group_tokens(tokens))
        # print(tokens)
        self.rows = rows
        self.columns = columns
        [err_code, err_msg] = self.check_start_end(tokens)
        if err_code:
            return err_code, print(err_msg)
        # print(self.tokens[self.body_location])
        print(self.tokens)


        
    def check_start_end(self, tokens):
        group = []
        start = False
        end = False
        self.index = 0
        print(tokens)
        while self.index in range(len(tokens)):
            token = tokens[self.index]
        
            if start:
                if end:
                    if token in self.grammar["comment"]():
                        group = []
                        while token in self.grammar["comment"]():
                            group.append(token)
                            self.index += 1
                            token = tokens[self.index]
                        if token in self.grammar["linebreak"]():
                            self.tokens.append(group)
                            group = []
                        else: 
                            return [1, f"ERROR: Unexpected {token} on line {self.rows[self.index]}, expected NEWLINE"]
                    else:
                        return [1, f"ERROR: Unexpected {token} on line {self.rows[self.index]}"]
                elif token == "END":
                    end = True
                    self.tokens.append(group)
                    group = []
                    self.tokens.append(token)
                else:
                    if token in self.grammar["comment"]():
                        igroup = []
                        while token in self.grammar["comment"]():
                            igroup.append(token)
                            self.index += 1
                            token = tokens[self.index]
                        if token in self.grammar["linebreak"]():
                            group.append(igroup)
                        else: 
                            return [1, f"ERROR: Unexpected {token} on line {self.rows[self.index]}, expected NEWLINE"]
                    elif token in self.grammar['statement']():
                        match token:
                            case "PRINT":
                                if tokens[self.index+1] in self.grammar["generic_operand"]():
                                    group.append([token, tokens[self.index+1]])
                                    self.index += 2
                                else:
                                    return [1, f"ERROR: Unexpected {tokens[self.index+1]} on line {self.rows[self.index+1]}, expected OPERAND"]
                            case "INPUT":
                                if tokens[self.index+1] in self.grammar["variable"]():
                                    group.append([token, tokens[self.index+1]])
                                    self.index += 2
                                else:
                                    return [1, f"ERROR: Unexpected {tokens[self.index+1]} on line {self.rows[self.index+1]}, expected VARIABLE"]
                            case "VAR_INIT_START":
                                igroup = []
                                if tokens[self.index+1] in self.grammar["linebreak"]():
                                    print(tokens[self.index])
                                    self.index += 2
                                    print(tokens[self.index])
                                    while True:
                                        if tokens[self.index] in self.grammar["comment"]():
                                            jgroup = []
                                            self.index += 1
                                            while tokens[self.index] in self.grammar["comment"]():
                                                jgroup.append(tokens[self.index])
                                                self.index += 1
                                            if tokens[self.index] in self.grammar["linebreak"]():
                                                igroup.append(jgroup)
                                                self.index += 1
                                            else: 
                                                return [1, f"ERROR: Unexpected {tokens[self.index]} on line {self.rows[self.index]}, expected NEWLINE"]
                                        elif tokens[self.index] in self.grammar["var_dec"]():
                                            jgroup = [tokens[self.index]]
                                            self.index += 1
                                            if tokens[self.index] in self.grammar["variable"]():
                                                jgroup.append(tokens[self.index])
                                                self.index += 1
                                                if tokens[self.index] in self.grammar["var_dec_value"]():
                                                    jgroup.append(tokens[self.index])
                                                    self.index += 1
                                                    if tokens[self.index] in self.grammar["generic_operand"]():
                                                        jgroup.append(tokens[self.index])
                                                        self.index += 1
                                                        if tokens[self.index-1] in self.grammar["expressions"]():
                                                            
                                                            if tokens[self.index] in self.grammar["linebreak"]():
                                                                igroup.append(jgroup)
                                                                self.index += 1
                                                            else:
                                                                return [1, f"ERROR: Unexpected {tokens[self.index]} on line {self.rows[self.index]}, expected NEWLINE"]
                                                            
                                                        if tokens[self.index] in self.grammar["linebreak"]():
                                                            igroup.append(jgroup)
                                                            self.index += 1
                                                        else:
                                                            return [1, f"ERROR: Unexpected {tokens[self.index]} on line {self.rows[self.index]}, expected NEWLINE"]
                                                    else:
                                                        return [1, f"ERROR: Unexpected {tokens[self.index]} on line {self.rows[self.index]}, expected OPERAND"]
                                                elif tokens[self.index] in self.grammar["linebreak"]():
                                                    igroup.append(jgroup)
                                                    self.index += 1
                                                else:
                                                    return [1, f"ERROR: Unexpected {tokens[self.index]} on line {self.rows[self.index]}, expected NEWLINE"]
                                            else:
                                                return [1, f"ERROR: Unexpected {tokens[self.index]} on line {self.rows[self.index]}, expected VARIABLE"]	
                                        
                                        elif tokens[self.index] in self.grammar["var_dec_end"]():
                                            igroup.append(token)
                                            self.index += 1
                                            break
                                        elif tokens[self.index] in self.grammar["linebreak"]():
                                            self.index += 1
                                        else:
                                            return [1, f"ERROR: Unexpected {tokens[self.index]} on line {self.rows[self.index]}, expected COMMENT or VAR_INIT"]
                                    group.append(igroup)
                                else:
                                    return [1, f"ERROR: Unexpected {tokens[self.index+1]} on line {self.rows[self.index+1]}, expected NEWLINE"]
                            case "_":
                                return [1, f"ERROR: Unexpected {token} on line {self.rows[self.index]}, expected STATEMENT"]

            else:
                if token == "START":
                    start = True
                    self.tokens.append(token)
                    if tokens[self.index+1] in self.grammar["linebreak"]():
                        self.index += 1
                        self.body_location = self.index
                    else:
                        return [1, f"ERROR: Unexpected {tokens[self.index+1]} on line {self.rows[self.index+1]}, expected NEWLINE"]
                elif token in self.grammar["comment"]():
                    group = []
                    while token in self.grammar["comment"]():
                        group.append(token)
                        self.index += 1
                        token = tokens[self.index]
                    if token in self.grammar["linebreak"]():
                        self.tokens.append(group)
                        group = []
                    else: 
                        return [1, f"ERROR: Unexpected {token} on line {self.rows[self.index]}, expected NEWLINE"]
                else:
                    return [1, f"ERROR: Unexpected {token} on line {self.rows[self.index]}"]      
            self.index += 1
        return [0, '']
            
                
    # def group_tokens(self, tokens):
    #     grouped_tokens = []
    #     group = []
    #     for i in range(len(tokens)):
    #         if tokens[i] == "NEWLINE":
    #             if group:
    #                 grouped_tokens.append(group)
    #                 group = []
    #         else:
    #             group.append(tokens[i])
    #     if group:
    #         grouped_tokens.append(group)
    #     return grouped_tokens
