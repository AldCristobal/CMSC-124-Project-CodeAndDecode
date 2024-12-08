import os
import tkinter as tk
from tkinter import filedialog
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
        self.root.geometry("800x600")
        self.root.resizable(False, False)  # Disable resizing

        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        title_label = tk.Label(header_frame, text="LOLCode Interpreter", font=('Helvetica', 20, 'bold'))
        title_label.pack()

        author_label = tk.Label(header_frame, text="Cristobal & Deocareza\nCMSC 124 ST-1L", font=('Helvetica', 14))
        author_label.pack()

        self.import_button = tk.Button(self.root, text="Select LOLCode File", command=self.select_file)
        self.import_button.pack(side=tk.TOP, padx=10, pady=5)

        # Main Frame (Text Editor and Tokens List)
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configure grid layout for even display
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Text Editor (Left Side)
        editor_frame = tk.Frame(main_frame)
        editor_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))  # Padding between editor and tokens

        self.editor_text = tk.Text(editor_frame, wrap=tk.WORD, font=('Courier New', 12))
        self.editor_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        editor_scrollbar = tk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=self.editor_text.yview)
        editor_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.editor_text.config(yscrollcommand=editor_scrollbar.set)

        # Tokens Output (Right Side)
        tokens_frame = tk.Frame(main_frame)
        tokens_frame.grid(row=0, column=1, sticky="nsew")

        self.output_text = tk.Text(tokens_frame, wrap=tk.WORD, font=('Helvetica', 12), state=tk.DISABLED)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tokens_scrollbar = tk.Scrollbar(tokens_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        tokens_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text.config(yscrollcommand=tokens_scrollbar.set)

    def select_file(self):
        current_working_dir = os.getcwd()  # Get the current working directory
        file_path = filedialog.askopenfilename(initialdir=current_working_dir, filetypes=[("LOLCode files", "*.lol")])

        if file_path:
            # Read the file and display in the text editor
            file_content = Reader(file_path).read()
            self.display_editor_content(file_content)

            # Generate tokens and display in the output area
            tokens, lexemes, rows, columns = LexicalAnalyzer.LexicalAnalyzer().gen_tokens(file_content)

            output = "LEXEME : CLASSIFICATION\n"
            for token, lexeme, row, col in zip(tokens, lexemes, rows, columns):
                if token not in {'COMMENT_START', 'COMMENT', 'NEWLINE'}:
                    output += f"{lexeme} : {token}\n"

            self.display_output(output)

            # Perform syntax analysis
            SyntaxAnalyzer.SyntaxAnalyzer().check_syntax(tokens, rows, columns)

    def display_editor_content(self, content):
        self.editor_text.delete(1.0, tk.END)
        self.editor_text.insert(tk.END, content)

    def display_output(self, output):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)
        self.output_text.config(state=tk.DISABLED)


# Create and run the app
root = tk.Tk()
app = CMSC124Project(root)
root.mainloop()
