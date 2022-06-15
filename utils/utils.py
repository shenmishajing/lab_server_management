import os

import paramiko
from scp import SCPClient

from config import server_config


def get_ssh_config(config_path = '~/.ssh/config'):
    return paramiko.SSHConfig.from_path(os.path.expanduser(config_path))


def lookup_params_from_system_host_keys(host, ssh_config = None):
    if ssh_config is None:
        ssh_config = get_ssh_config()
    params = ssh_config.lookup(host)
    return params


def get_ssh_params(hosts = None, ssh_config = None):
    if ssh_config is None:
        ssh_config = get_ssh_config()

    if hosts is None:
        hosts = server_config['servers']
    elif not isinstance(hosts, list):
        hosts = [hosts]

    res_hosts = []
    params = []
    for host in hosts:
        if isinstance(host, int):
            host = f'lab_{host}'

        if isinstance(host, str):
            res_hosts.append(host)
            param = lookup_params_from_system_host_keys(host, ssh_config)
            if host in server_config and 'user' in server_config[host] and server_config[host]['user'] != param['user']:
                param.update(server_config[host])
        elif isinstance(host, dict):
            res_hosts.append(host['hostname'])
            param = host
        else:
            print(f'Unknown host type: {type(host)}, {host}')
            continue

        if 'port' in param and param['port'] == '22':
            del param['port']
        if 'username' not in param:
            param['username'] = param['user']
        if 'user' in param:
            del param['user']
        params.append(param)
    return res_hosts, params


def ssh_connect(**kwargs):
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.connect(**kwargs)
    return ssh_client


def get_ssh_clients(hosts = None):
    hosts, params = get_ssh_params(hosts)
    ssh_clients = [ssh_connect(**param) for host, param in zip(hosts, params)]
    if len(ssh_clients) == 1:
        ssh_clients = ssh_clients[0]
    return ssh_clients


def get_scp_clients(ssh_clients = None, hosts = None):
    if ssh_clients is None:
        ssh_clients = get_ssh_clients(hosts)
    if not isinstance(ssh_clients, list):
        return SCPClient(ssh_clients.get_transport())
    else:
        return [SCPClient(ssh_client.get_transport()) for ssh_client in ssh_clients]


def get_output_from_shell(shell, show_output = True):
    shell.settimeout(0.5)
    res = ''
    while True:
        try:
            resp = shell.recv(1024).decode('utf-8')
            if show_output:
                print(resp, end = '')
            res += resp
        except Exception:
            break
    return res


def run_one_cmd_on_shell(shell, cmd, show_output = True):
    shell.send(cmd + '\n')
    return get_output_from_shell(shell, show_output)


def run_ssh_cmd(cmds, hosts = None, root = True, show_output = True):
    res = {}
    if not isinstance(cmds, list):
        cmds = [cmds]
    hosts, params = get_ssh_params(hosts)
    for host, param in zip(hosts, params):
        try:
            print(f'run cmd on {host}')
            ssh_client = ssh_connect(**param)
            shell = ssh_client.invoke_shell()
            get_output_from_shell(shell, show_output = show_output)
            if root and param['username'] != 'root' and cmds:
                if 'password' in server_config[host]:
                    run_one_cmd_on_shell(shell, 'sudo su', show_output = show_output)
                    run_one_cmd_on_shell(shell, server_config[host]['password'], show_output = show_output)
                else:
                    print(f'No password found for user root')
            for cmd in cmds:
                if host not in res:
                    res[host] = []
                res[host].append(run_one_cmd_on_shell(shell, cmd, show_output = show_output))
            ssh_client.close()
        except Exception as e:
            print(host, e)
    return res
