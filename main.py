import os
import re
import tkinter as tk
from tkinter import filedialog


class Reader:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'r') as file:
            return file.read()

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

class CMSC124Project:
    def __init__(self, root):
        self.root = root
        self.root.title("CMSC 124 Project: LOLCode Interpreter")
        self.root.geometry("600x600")  # Set initial window size (width x height)

        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self.root)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        title_label = tk.Label(header_frame, text="LOLCode Interpreter", font=('Helvetica', 20, 'bold'))
        title_label.pack()

        author_label = tk.Label(header_frame, text="Cristobal & Deocareza\nCMSC 124 ST-1L", font=('Helvetica', 14))
        author_label.pack()

        self.import_button = tk.Button(self.root, text="Select LOLCode File", command=self.select_file)
        self.import_button.pack(side=tk.TOP, padx=10, pady=5)

        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)

        self.output_text = tk.Text(self.text_frame, height=30, width=80, wrap=tk.WORD, font=('Helvetica', 12))
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text.config(yscrollcommand=self.scrollbar.set)
        self.output_text.config(state=tk.DISABLED)

    def select_file(self):
        current_working_dir = os.getcwd()  # Get the current working directory
        file_path = filedialog.askopenfilename(initialdir=current_working_dir, filetypes=[("LOLCode files", "*.lol")])
        
        if file_path:
            file = Reader(file_path).read()
            tokens, lexemes, rows, columns = LexicalAnalyzer().gen_tokens(file)

            output = "LEXEME : CLASSIFICATION\n"
            for token, lexeme, row, col in zip(tokens, lexemes, rows, columns):
                if token != 'COMMENT_START' and token != 'COMMENT' and token != 'NEWLINE':
                    # output += f"Lexeme: '{lexeme}' Classification: {token} | Row: {row}, Column: {col} \n"
                    output += f"{lexeme} : {token}\n"

            self.display_output(output)

            SyntaxAnalyzer().check_syntax(tokens, rows, columns)

    def display_output(self, output):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)
        self.output_text.config(state=tk.DISABLED)


# Create and run the app
root = tk.Tk()
app = CMSC124Project(root)
root.mainloop()
