import argparse
from utils import run_ssh_cmd, launcher


def parser_builder():
    parser = argparse.ArgumentParser(description="delete ovpn users")
    parser.add_argument(
        "--user-names",
        required=True,
        type=str,
        nargs="+",
        help="user names, can be a list",
    )
    return parser


@launcher(parser_builder=parser_builder)
def main(user_names):
    if not isinstance(user_names, list):
        user_names = [user_names]

    server = 235
    cmd = [f'sh /data/openvpn_script/del_vpn_user.sh {" ".join(user_names)}']
    run_ssh_cmd(cmd, server)


if __name__ == "__main__":
    main()
