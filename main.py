import prozarustats as pr
import stihirustats as st


def main(st_login: str, pr_login: str):
    st.print_all_stats(st_login.lower())
    pr.print_all_stats(pr_login.lower())


if __name__ == '__main__':
    try:
        main(input('Введите логин на стихи.ру (введите 0 для пропуска): '),
             input('Введите логин на проза.ру (введите 0 для пропуска): '))
    except:
        ('Что-то пошло не так...')
        exit(1)
