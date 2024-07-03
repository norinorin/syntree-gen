from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser(
        prog="syntree-gen",
        description="Bracket-based syntax tree builders.",
        epilog="Made for schoolwork.",
    )
    parser.add_argument("path", nargs="?", default="", help="path to save the image to")
    parser.add_argument(
        "--colour-scheme",
        "--color-scheme",
        help="a .json file containing the colour scheme (see config.py for an example)",
    )
    return parser.parse_args()


ARGS = get_args()
