import argparse
from utils import do_something_on_users, launcher


def parser_builder():
    parser = argparse.ArgumentParser(description="reset user passwd")
    parser.add_argument(
        "--user-names",
        required=True,
        type=str,
        nargs="+",
        help="user names, can be a list",
    )
    parser.add_argument(
        "--servers",
        type=int,
        default=None,
        nargs="+",
        help="servers ip address (only last part), default all compute servers",
    )
    parser.add_argument(
        "--use-cache",
        action="store_true",
        help="if set, try to use cached users.json file instead of get a new one, default is False",
    )
    return parser


@launcher(parser_builder)
@do_something_on_users
def main(user_name, user_passwd="HangZhou2022", **kwargs):
    return [f"echo {user_name}:{user_passwd} | chpasswd", f"chage -d0 {user_name}"]


if __name__ == "__main__":
    main()
