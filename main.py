import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import SyntaxAnalyzer
import LexicalAnalyzer


class Reader:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'r') as file:
            return file.read()


class CMSC124Project:
    def __init__(self, root):
        self.root = root
        self.root.title("CMSC 124 Project: LOLCode Interpreter")

        # Set fixed window size
        self.root.geometry("1000x750")
        self.root.resizable(True, True)  

        self.file_path = None  # Initialize file path as None

        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        title_label = tk.Label(header_frame, text="LOLCode Interpreter", font=('Georgia', 20, 'bold'))
        title_label.pack()

        author_label = tk.Label(header_frame, text="Code & Decode | CMSC 124 ST-1L", font=('Georgia', 14))
        author_label.pack()

        self.import_button = tk.Button(self.root, text="File Explorer", font=('Georgia', 12, 'bold'), command=self.select_file)
        self.import_button.pack(side=tk.TOP, padx=10, pady=5)

        # Create a style object for the Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Georgia", 10, "bold"))  # Set font for column headers
        style.configure("Treeview", font=("Verdana", 10))  # Set font for Treeview content

        # Main Frame (Text Editor and Token Tables)
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configure grid layout for even display
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Text Editor (Left Side)
        editor_frame = tk.Frame(main_frame)
        editor_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))  # Padding between editor and tokens

        editor_label = tk.Label(editor_frame, text="Text Editor", font=('Georgia', 12, 'bold'))
        editor_label.pack()

        self.editor_text = tk.Text(editor_frame, wrap=tk.WORD, font=('Courier New', 10), height=10, width=30)
        self.editor_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        editor_scrollbar = tk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=self.editor_text.yview)
        editor_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.editor_text.config(yscrollcommand=editor_scrollbar.set)

        # Lexeme Table (Middle Right)
        lexeme_frame = tk.Frame(main_frame)
        lexeme_frame.grid(row=0, column=1, sticky="nsew")

        lexeme_label = tk.Label(lexeme_frame, text="Lexemes", font=('Georgia', 12, 'bold'))
        lexeme_label.pack()

        self.tokens_table = ttk.Treeview(lexeme_frame, columns=("Lexeme", "Classification"), show="headings")
        self.tokens_table.heading("Lexeme", text="Lexeme")
        self.tokens_table.heading("Classification", text="Classification")
        self.tokens_table.column("Lexeme", width=100, anchor="w")
        self.tokens_table.column("Classification", width=100, anchor="w")
        self.tokens_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tokens_scrollbar = tk.Scrollbar(lexeme_frame, orient=tk.VERTICAL, command=self.tokens_table.yview)
        tokens_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tokens_table.config(yscrollcommand=tokens_scrollbar.set)

        # Symbol Table (Far Right)
        symbol_frame = tk.Frame(main_frame)
        symbol_frame.grid(row=0, column=2, sticky="nsew")

        symbol_label = tk.Label(symbol_frame, text="Symbol Table", font=('Georgia', 12, 'bold'))
        symbol_label.pack()

        self.symbol_table = ttk.Treeview(symbol_frame, columns=("Identifier", "Value"), show="headings")
        self.symbol_table.heading("Identifier", text="Identifier")
        self.symbol_table.heading("Value", text="Value")
        self.symbol_table.column("Identifier", width=100, anchor="w")
        self.symbol_table.column("Value", width=100, anchor="w")
        self.symbol_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        symbol_scrollbar = tk.Scrollbar(symbol_frame, orient=tk.VERTICAL, command=self.symbol_table.yview)
        symbol_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.symbol_table.config(yscrollcommand=symbol_scrollbar.set)

        # Console Text Box Below the Execute Button
        self.console_text = tk.Text(self.root, wrap=tk.WORD, font=('Courier New', 10), height=8)
        self.console_text.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=5)
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, "Console Output:\n")
        self.console_text.config(state=tk.DISABLED)

        # Add the Execute button below the main frame
        self.execute_button = tk.Button(self.root, text="EXECUTE", font=('Georgia', 12, 'bold'), command=self.execute)
        self.execute_button.pack(side=tk.BOTTOM, pady=10)

    def select_file(self):
        current_working_dir = os.getcwd()  # Get the current working directory
        self.file_path = filedialog.askopenfilename(initialdir=current_working_dir, filetypes=[("LOLCode files", "*.lol")])

        if self.file_path:
            # Read the file and display its content in the editor
            file_content = Reader(self.file_path).read()
            self.display_editor_content(file_content)

    def execute(self):
        # Read the current content from the editor
        file_content = self.editor_text.get("1.0", tk.END).strip()

        if file_content:
            # Perform lexical analysis
            tokens, lexemes, rows, columns = LexicalAnalyzer.LexicalAnalyzer().gen_tokens(file_content)

            # Clear previous entries in the token and symbol tables
            for item in self.tokens_table.get_children():
                self.tokens_table.delete(item)
            for item in self.symbol_table.get_children():
                self.symbol_table.delete(item)

            # Populate the lexeme table
            for token, lexeme in zip(tokens, lexemes):
                if token not in {'COMMENT_START', 'COMMENT', 'NEWLINE'}:
                    self.tokens_table.insert("", tk.END, values=(lexeme, token))

            # Populate the symbol table
            for symbol in set(lexemes):  
                self.symbol_table.insert("", tk.END, values=(symbol, "Value"))

            # Display console output
            self.console_text.config(state=tk.NORMAL)
            self.console_text.delete(1.0, tk.END)
            self.console_text.insert(tk.END, "Execution Completed.\n")
            self.console_text.config(state=tk.DISABLED)

            new_dictionary = dict(zip(lexemes,tokens))

            final_tokens = {key: value for key, value in new_dictionary.items() if value not in ['COMMENT_START', 'COMMENT', 'NEWLINE']}

            print(final_tokens)

            # Perform syntax analysis
            analyzer = SyntaxAnalyzer.SyntaxAnalyzer(final_tokens)
            analyzer.analyze()

        else:
            self.console_text.config(state=tk.NORMAL)
            self.console_text.delete(1.0, tk.END)
            self.console_text.insert(tk.END, "No content in the editor! Please enter some code.\n")
            self.console_text.config(state=tk.DISABLED)

    def display_editor_content(self, content):
        self.editor_text.delete(1.0, tk.END)
        self.editor_text.insert(tk.END, content)

    def display_output(self, output):
        # Display output in the console text box if needed
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END)
        self.console_text.insert(tk.END, output)
        self.console_text.config(state=tk.DISABLED)


# Create and run the app
root = tk.Tk()
app = CMSC124Project(root)
root.mainloop()
