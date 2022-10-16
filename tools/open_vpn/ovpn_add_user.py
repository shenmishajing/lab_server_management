from utils import get_scp_clients, run_ssh_cmd
import os


def add_users(user_names):
    if not isinstance(user_names, list):
        user_names = [user_names]

    server = 235
    cmd = [f'sh /data/openvpn_script/vpn_user.sh {" ".join(user_names)}']
    run_ssh_cmd(cmd, server)
    scp_client = get_scp_clients(hosts = server)
    for user_name in user_names:
        scp_client.get(f'/data/openvpn_client/{user_name}.zip', os.path.expanduser(f'~/Downloads/{user_name}.zip'))
    scp_client.close()


def main():
    add_users(['wenjiaheng', 'nichiming'])


if __name__ == '__main__':
    main()
