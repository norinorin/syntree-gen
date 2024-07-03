from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser(
        prog="syntree-gen",
        description="Bracket-based syntax tree builders",
        epilog="Made for schoolwork",
    )
    parser.add_argument("-p", "--path")
    return parser.parse_args()
