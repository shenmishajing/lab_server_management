import os
import argparse
from utils import get_scp_clients, run_ssh_cmd, launcher


def parser_builder():
    parser = argparse.ArgumentParser(description="add ovpn users")
    parser.add_argument(
        "--user-names",
        required=True,
        type=str,
        nargs="+",
        help="user names, can be a list",
    )
    return parser


@launcher(parser_builder)
def main(user_names):
    if not isinstance(user_names, list):
        user_names = [user_names]

    server = 235
    cmd = [f'sh /data/openvpn_script/vpn_user.sh {" ".join(user_names)}']
    run_ssh_cmd(cmd, server)
    scp_client = get_scp_clients(hosts=server)
    for user_name in user_names:
        scp_client.get(
            f"/data/openvpn_client/{user_name}.zip",
            os.path.expanduser(f"~/Downloads/{user_name}.zip"),
        )
    scp_client.close()


if __name__ == "__main__":
    main()
