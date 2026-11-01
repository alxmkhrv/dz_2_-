import prompt


def welcome():
    print("Первая попытка запустить проект!")
    print_help()

    while True:
        command = prompt.string("Введите команду: ")
        if command == "help":
            print_help()

        elif command == "exit":
            break


def print_help():
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
