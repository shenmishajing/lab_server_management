import copy

from config import server_config
from .get_all_users import get_all_users
from .utils import run_ssh_cmd


def do_something_on_users(func):
    def wrapper(user_names, servers = None, use_cache = False, **kwargs):
        users, already_used_ids, users_to_host = get_all_users(use_cache)

        if not isinstance(user_names, list):
            user_names = [user_names]

        if servers is None:
            servers = server_config['servers']
        elif not isinstance(servers, list):
            servers = [servers]

        for server in servers:
            if isinstance(server, int):
                server = f'192.168.0.{server}'
            cmd = []
            for user_name in user_names:
                if user_name in users_to_host and server in users_to_host[user_name]:
                    cur_kwarg = copy.deepcopy(kwargs)
                    cur_kwarg.setdefault('user_id', users[user_name])
                    cmd.extend(func(user_name = user_name, server = server, **cur_kwarg))
            run_ssh_cmd(cmd, server)

    return wrapper
