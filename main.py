import sys

import parser
import preprocess
from common import ERROR_MANUALS

norm_command = ["-i", "input.txt", "-o", "output", "-v", "-s", "symbols"]

def main():

    """
    if len(sys.argv) == 1:
        print("\nexit code : -1")
        print(ERROR_MANUALS[-1]["msg"])
        print(ERROR_MANUALS[-1]["hint"])
        sys.exit(-1)"""

    config = parser.parse_main_input(norm_command)
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

    _input = config["-i"]
    if not "-o" in config:
        _output = config["-i"]
    if not "-s" in config:
        config["-s"] = ""   #invalid path -> empty table

    try:
        res = preprocess.preprocess(config)
    except int as code:
        res = code

    print(f"\nexit code : {res}")
    if verbose_o:
        print(ERROR_MANUALS[res]["msg"])
        print(ERROR_MANUALS[res]["hint"])

    sys.exit(res)

if __name__ == "__main__":
    main()