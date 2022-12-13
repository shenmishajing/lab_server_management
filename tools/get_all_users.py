import argparse
from utils import get_all_users, launcher


def parser_builder():
    parser = argparse.ArgumentParser(description="get all user info")
    return parser


@launcher(parser_builder=parser_builder)
def main():
    get_all_users()


if __name__ == "__main__":
    main()
