import sys

import parser
import preprocess
from common import ERROR_MANUALS, DEPTH, ErrorCode

norm_command = ["-i", "sample/script.py", "-o", "sample/target.py", "-v", "-s", "sample/symbols.ini", "-d", "10"]

def main():

    if len(sys.argv) == 1:
        print("\nexit code : -1")
        print(ERROR_MANUALS[-1]["msg"])
        print(ERROR_MANUALS[-1]["hint"])
        sys.exit(-1)

    config = parser.parse_main_input(norm_command)
    state = parser.is_valid_config(config)
    if state != 0:
        print("command parse state: " + str(state)) # print error hints
        print(ERROR_MANUALS[state]["msg"])
        print(ERROR_MANUALS[state]["hint"])

    triggers = parser.init_triggers(config)
    verbose_o = triggers["-v"]
    if verbose_o:
        print(f"\ncommand-line parsing results: {state}")
        print(config)

    # setting default config block
    _input = config["-i"]
    if not "-o" in config:
        _output = config["-i"]
    if not "-s" in config:
        config["-s"] = ""   # invalid path -> empty table
    if not "-d" in config:
        config["-d"] = DEPTH    # default including depth

    res = 0
    try:
        preprocess.preprocessing(config)
    except ErrorCode as e:
        res = e.code
    except TypeError:
        res = -2
    except ValueError:
        res = -2

    print(f"\nexit code : {res}")
    if verbose_o:
        print(ERROR_MANUALS[res]["msg"])
        print(ERROR_MANUALS[res]["hint"])

    sys.exit(res)

if __name__ == "__main__":
    main()