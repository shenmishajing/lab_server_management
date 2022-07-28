from utils import run_ssh_cmd


def del_users(user_names):
    if not isinstance(user_names, list):
        user_names = [user_names]

    server = 235
    cmd = [f'sh /data/openvpn_script/del_vpn_user.sh {" ".join(user_names)}']
    run_ssh_cmd(cmd, server)


def main():
    del_users('intern10')


if __name__ == '__main__':
    main()
