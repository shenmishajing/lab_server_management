from config import server_config
from utils import run_ssh_cmd, get_all_users


def get_next_id(used_ids, start_id = 2300, end_id = 65535):
    all_ids = set(range(start_id, end_id))
    user_id = min(all_ids - set(used_ids))
    return user_id


def add_users(user_names, servers = None, admin_users = False, user_passwd = 'HangZhou2022', use_cache = False, user_id_start = 2300,
              user_id_end = 65535):
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
            print(f'uid and gid {user_id} is assigned to {user_name}')
            users[user_name] = user_id, user_id
            already_used_ids.append(user_id)
        user_ids[user_name] = users[user_name]

    if servers is None:
        servers = server_config['servers']
    for server in servers:
        if isinstance(server, int):
            server = f'lab_{server}'
        cmd = []
        is_data_server = server in server_config['data_servers']
        for user_name, admin_user in zip(user_names, admin_users):
            if user_name in users_to_host and server in users_to_host[user_name]:
                continue
            user_id, group_id = user_ids[user_name]
            cmd.extend([
                           f'mkdir -p /data2/{user_name}',
                           f'chown -R {user_id}:{group_id} /data2/{user_name}',
                       ] if is_data_server else ([
                                                     f'useradd {user_name} -s /bin/bash -d /home/{user_name} -m',
                                                     f'echo {user_name}:{user_passwd} | chpasswd',
                                                     f'usermod -u {user_id} {user_name}',
                                                     f'groupmod -g {group_id} {user_name}',
                                                     f'chage -d0 {user_name}'
                                                 ] + ([f'usermod -G sudo {user_name}'] if admin_user else [])))
        run_ssh_cmd(cmd, server)


def main():
    add_users(['wenjiaheng', 'nichiming'], servers = [217, 240])


if __name__ == '__main__':
    main()
