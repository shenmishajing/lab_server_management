import os
import re
import time

import paramiko

from config import server_config

cmd_finish_flag = ['#', '$', '?', '%', ':']

ansi_escape = re.compile(r'''
            \x1B  # ESC
            (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
            |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', re.VERBOSE)


def get_ssh_config(config_path = '~/.ssh/config'):
    if os.path.exists(os.path.expanduser(config_path)):
        return paramiko.SSHConfig.from_path(os.path.expanduser(config_path))
    else:
        return paramiko.SSHConfig.from_text('')


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
            host = f'192.168.0.{host}'

        if isinstance(host, str):
            res_hosts.append(host)
            param = lookup_params_from_system_host_keys(host, ssh_config)
            if host in server_config and 'user' in server_config[host] and (
                    'user' not in param or server_config[host]['user'] == param['user']):
                param.update(server_config[host])
        elif isinstance(host, dict):
            res_hosts.append(host['hostname'])
            param = host
        else:
            print(f'Unknown host type: {type(host)}, {host}')
            continue

        if 'username' not in param:
            param['username'] = param['user']
        if 'user' in param:
            del param['user']
        params.append(param)
    return res_hosts, params


def ssh_connect(**kwargs):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.load_system_host_keys()
    ssh_client.connect(timeout = 1, **kwargs)
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
        return paramiko.SFTPClient.from_transport(ssh_clients.get_transport())
    else:
        return [paramiko.SFTPClient.from_transport(ssh_client.get_transport()) for ssh_client in ssh_clients]


def get_output_from_shell(shell, show_output = True, start_cmd = None, debug = False):
    shell.settimeout(1)
    res = ''
    started = start_cmd is None
    finished = False
    while True:
        try:
            resp = ansi_escape.sub('', shell.recv(1024 * 1024).decode('utf-8'))
            if debug:
                print(resp, end = '<!--- resp end ---!>')
            res += resp

            if not started:
                cmd_index = res.find(start_cmd)
                if cmd_index != -1:
                    cmd_index += len(start_cmd)
                    res = res[cmd_index:].lstrip()
                    started = True

            if started:
                if (len(res) > 1 and res[-1] in cmd_finish_flag) or (len(res) > 2 and res[-2] in cmd_finish_flag):
                    res = res.strip()
                    index = res.rfind('\n')
                    if index == -1:
                        res = ''
                    else:
                        res = res[:index].strip()
                    finished = True

            if finished:
                if show_output:
                    print(res, end = '' if res.endswith('\n') else '\n')
                return res
        except Exception as e:
            print(e)
            break
    if show_output:
        print(res)
    return res


def run_one_cmd_on_shell(shell, cmd, use_start_cmd = True, **kwargs):
    shell.send(cmd if cmd.endswith('\n') else cmd + '\n')
    return get_output_from_shell(shell, start_cmd = cmd if use_start_cmd else None, **kwargs)


def run_ssh_cmd(cmds, hosts = None, root = True, show_output = True, **kwargs):
    res = {}
    if not isinstance(cmds, list):
        cmds = [cmds]
    hosts, params = get_ssh_params(hosts)
    for host, param in zip(hosts, params):
        try:
            print(f'run cmd on {host}')
            ssh_client = ssh_connect(**param)
            shell = ssh_client.invoke_shell()
            time.sleep(.1)
            run_one_cmd_on_shell(shell, 'bash', show_output = False)
            if root and param['username'] != 'root' and cmds:
                if 'password' in server_config[host]:
                    run_one_cmd_on_shell(shell, f'sudo su', show_output = False)
                    run_one_cmd_on_shell(shell, server_config[host]["password"], show_output = False, use_start_cmd = False)
                else:
                    print(f'No password found for user root')
            for cmd in cmds:
                if host not in res:
                    res[host] = []
                res[host].append(run_one_cmd_on_shell(shell, cmd, show_output = show_output, **kwargs))
            ssh_client.close()
        except Exception as e:
            print(host, e)
    return res
