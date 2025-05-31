import sys

import parser
import preprocess
from common import ERROR_MANUALS

norm_command = ["-i", "input.txt", "-o", "output", "-v", "-s", "symbols"]

def main():
    config = parser.parse_main_input(sys.argv)
    state = preprocess.is_valid_config(config)
    if state != 0:
        print("command parse state: " + str(state)) # print error hints
        print(ERROR_MANUALS[state]["msg"])
        print(ERROR_MANUALS[state]["hint"])

    triggers = preprocess.init_triggers(config)
    verbose_o = triggers["-v"]
    if verbose_o:
        print("\ncommand-line parsing results:")
        print(state)
        print(config)

    res = preprocess.preprocess(config["-i"])
    print(f"\nexit code : {res}")
    if verbose_o:
        print(ERROR_MANUALS[res]["msg"])
        print(ERROR_MANUALS[res]["hint"])

    sys.exit(res)

if __name__ == "__main__":
    main()