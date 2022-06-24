from utils import do_something_on_users


@do_something_on_users
def change_user_groups(user_name, user_group = 'sudo', is_add = True, **kwargs):
    return [f'gpasswd -{"a" if is_add else "d"} {user_name} {user_group}']


def main():
    change_user_groups('xiaojun', servers = [226])


if __name__ == '__main__':
    main()
