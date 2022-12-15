import argparse
from utils import do_something_on_users, launcher


def parser_builder():
    parser = argparse.ArgumentParser(description="change user id")
    parser.add_argument(
        "--user-names",
        required=True,
        type=str,
        help="user name, must be only one name",
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
        "--user-id",
        type=int,
        default=None,
        help="the user id to change, default not change",
    )
    parser.add_argument(
        "--group-id",
        type=int,
        default=None,
        help="the group id to change, default not change",
    )
    return parser


@launcher(parser_builder)
@do_something_on_users
def main(
    user_name,
    user_id=None,
    group_id=None,
    cur_user_id=None,
    cur_group_id=None,
    **kwargs,
):
    cmd = []
    if user_id is not None and cur_user_id is not None and user_id != cur_user_id:
        cmd.append(f"usermod -u {user_id} {user_name}")

    if (
        group_id is not None
        and cur_group_id is not None
        and cur_group_id != cur_group_id
    ):
        cmd.append(f"groupmod -g {group_id} {user_name}")

    return cmd


if __name__ == "__main__":
    main()
