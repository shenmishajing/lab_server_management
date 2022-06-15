from utils import do_something_on_users


@do_something_on_users
def reset_user_passwd(user_name, user_passwd = 'HangZhou2022', **kwargs):
    return [f'echo {user_name}:{user_passwd} | chpasswd',
            f'chage -d0 {user_name}']


def main():
    reset_user_passwd('zhengwenhao', servers = [241, 247])


if __name__ == '__main__':
    main()
