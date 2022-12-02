import json
import os

from .utils import run_ssh_cmd


def _get_all_users(cache_path = 'cache/users.json', users = None):
    cmd = f'cut -d: -f1,3,4 /etc/passwd'
    user = run_ssh_cmd(cmd, show_output = False, root = False)

    if users is not None:
        host_to_users = users['host_to_users']
    else:
        host_to_users = {}
    for host in user:
        res = [r.split(':') for r in user[host][0].split('\r\n')]
        res = {r[0]: [int(r[1]), int(r[2])] for r in res if len(r) == 3 and r[1].isdigit() and r[2].isdigit()}
        if host not in host_to_users:
            host_to_users[host] = res
        else:
            host_to_users[host].update(res)

    users = {}
    for host in host_to_users:
        for user in host_to_users[host]:
            if user not in users:
                users[user] = {}

            if tuple(host_to_users[host][user]) in users[user]:
                users[user][tuple(host_to_users[host][user])].append(host)
            else:
                users[user][tuple(host_to_users[host][user])] = [host]

    res_users = {user: max(users[user].items(), key = lambda x: len(x[1]))[0] for user in users}

    users_to_host = {}
    for host in host_to_users:
        for user in host_to_users[host]:
            if user not in users_to_host:
                users_to_host[user] = []
            users_to_host[user].append(host)

    already_used_ids = set()
    for user in users:
        for id_tuple in users[user]:
            already_used_ids |= set(id_tuple)
    already_used_ids = sorted(list(already_used_ids))

    for user in users:
        users[user] = {str(k): v for k, v in users[user].items()}

    multi_id_users = {user: users[user] for user in users if len(users[user]) > 1}

    user_dict = {
        'users': res_users,
        'multi_id_users': multi_id_users,
        'already_used_ids': already_used_ids,
        'already_used_names': sorted([user for user in res_users]),
        'users_to_host': users_to_host,
        'host_to_users': host_to_users,
        'all_users': users
    }
    cache_dir = os.path.dirname(cache_path)
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    json.dump(user_dict, open(cache_path, 'w'), indent = 4)
    return res_users, already_used_ids, users_to_host


def get_all_users(use_cache = False, cache_path = 'cache/users.json'):
    if os.path.exists(cache_path):
        users = json.load(open(cache_path, 'r'))
    else:
        users = None

    if use_cache and users:
        return users['users'], users['already_used_ids'], users['users_to_host']
    else:
        return _get_all_users(cache_path, users)


def main():
    get_all_users()


if __name__ == '__main__':
    main()
