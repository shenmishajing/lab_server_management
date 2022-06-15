from utils import do_something_on_users


@do_something_on_users
def change_user_id(user_name, user_id = None, group_id = None, **kwargs):
    cmd = []
    if user_id is not None:
        cmd.append(f'usermod -u {user_id} {user_name}')

    if group_id is not None:
        cmd.append(f'groupmod -g {group_id} {user_name}')

    return cmd


def main():
    change_user_id('zhuyiheng', servers = [243], group_id = 2205)


if __name__ == '__main__':
    main()
