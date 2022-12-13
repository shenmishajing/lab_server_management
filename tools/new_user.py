import argparse

from config import server_config
from utils import run_ssh_cmd, get_all_users, launcher


def get_next_id(used_ids, start_id=2300, end_id=65535):
    all_ids = set(range(start_id, end_id))
    user_id = min(all_ids - set(used_ids))
    return user_id


def parser_builder():
    parser = argparse.ArgumentParser(description="create new user")
    parser.add_argument(
        "--user-names",
        required=True,
        type=str,
        nargs="+",
        help="user names, can be a list",
    )
    parser.add_argument(
        "--servers",
        type=str,
        default=None,
        nargs="+",
        help="servers ip address (only last part), default all compute servers",
    )
    parser.add_argument(
        "--admin-users",
        action="store_true",
        help="if set, create all users as admin users, default is False",
    )
    parser.add_argument(
        "--user-passwd",
        type=str,
        default="HangZhou2022",
        help="user passwd, default HangZhou2022",
    )
    parser.add_argument(
        "--request-change-password",
        action="store_false",
        help="if set, require user to change passwd after first login, default is True",
    )
    parser.add_argument(
        "--use-cache",
        action="store_true",
        help="if set, try to use cached users.json file instead of get a new one, default is False",
    )
    parser.add_argument(
        "--user-id-start",
        type=int,
        default=2300,
        help="the min user id can be used as new user id, default 2300",
    )
    parser.add_argument(
        "--user-id-end",
        type=int,
        default=65535,
        help="the max user id can be used as new user id, default 65535",
    )
    return parser


@launcher(parser_builder=parser_builder)
def main(
    user_names,
    servers=None,
    admin_users=False,
    user_passwd="HangZhou2022",
    request_change_password=True,
    use_cache=False,
    user_id_start=2300,
    user_id_end=65535,
):
    users, already_used_ids, users_to_host = get_all_users(use_cache)

    if not isinstance(user_names, list):
        user_names = [user_names]

    if not isinstance(admin_users, list):
        admin_users = [admin_users] * len(user_names)
    else:
        admin_users.extend([False] * (len(user_names) - len(admin_users)))

    user_ids = {}
    for user_name in user_names:
        if user_name not in users:
            user_id = get_next_id(already_used_ids, user_id_start, user_id_end)
            print(f"uid and gid {user_id} is assigned to {user_name}")
            users[user_name] = user_id, user_id
            already_used_ids.append(user_id)
        user_ids[user_name] = users[user_name]

    if servers is None:
        servers = server_config["servers"]
    for server in servers:
        if isinstance(server, int):
            server = f"192.168.0.{server}"
        cmd = []
        for user_name, admin_user in zip(user_names, admin_users):
            user_id, group_id = user_ids[user_name]

            if user_name not in users_to_host or server not in users_to_host[user_name]:
                cmd.extend(
                    [
                        f"useradd {user_name} -u {user_id} -s /bin/bash -d /data2/{user_name} -m",
                        f"groupmod -g {group_id} {user_name}",
                        f"echo {user_name}:{user_passwd} | chpasswd",
                    ]
                )
                if request_change_password:
                    cmd += [f"chage -d0 {user_name}"]

            if admin_user:
                cmd.append(f"gpasswd -a {user_name} sudo")

        run_ssh_cmd(cmd, server)


if __name__ == "__main__":
    main()
