# relative path script
import os

# modules
import Reader

if __name__ == '__main__':
    # get the current directory of the script + relative path
    script_dir = os.path.dirname(__file__)
    rel_path = "samplecodes/01_variables.lol"
    abs_file_path = os.path.join(script_dir, rel_path)

    file = Reader.Reader(abs_file_path).read()
