import argparse

from utils import do_something_on_users, launcher


def parser_builder():
    parser = argparse.ArgumentParser(description="change user groups")
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
    parser.add_argument(
        "--user-group",
        type=str,
        default="sudo",
        help="user group to set, default sudo",
    )
    parser.add_argument(
        "--is-delete",
        action="store_true",
        help="delete user from group instead of add, default is add",
    )
    return parser


@launcher(parser_builder)
@do_something_on_users
def main(user_name, user_group="sudo", is_delete=False, **kwargs):
    return [f'gpasswd -{"d" if is_delete else "a"} {user_name} {user_group}']


if __name__ == "__main__":
    main()
