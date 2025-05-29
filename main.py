import sys
import parser
import preprocess
from preprocess import init_triggers


def main():
    config = parser.parse_main_input(sys.argv)
    state = preprocess.is_valid_config(config)
    if state[0] == False:
        print(state[2]) # print error hints
        ...
    triggers = init_triggers(config)
    verbose_o = triggers["-v"]
    if verbose_o:
        print("command-line parsing results:\n")
        print(state)
        print(config)


if __name__ == "__main__":
    main()