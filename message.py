from models import Message
from models import User
from database import get_connection, get_cursor, domain_name
import sys
sys.path.append("..")
import clcrypto

if __name__ == '__main__':
    connection = get_connection()
    cursor = get_cursor(connection)

    try:
        pairs = clcrypto.slice_args(sys.argv)
    except KeyError as e:
        print(e)
        exit(1)
    user = User()
    if len(set(("-u", "-p", "-l")) & set(pairs)) == 3:
        ''' print all messages of user'''
        # python3 message.py -u franek12 -p tajne1234 -l
        try:
            hash_u = user.load_users_by_any(cursor, username = pairs['-u'])[0].hashed_password


            if clcrypto.check_password(pairs['-p'], hash_u):
                for message in Message.load_received_messages(cursor, f"{pairs['-u']}@{domain_name}"):
                    print("od: ", message.sender)
                    print("temat: ", message.title)
                    print("treść: ", message.message)
                    print("-----------------------------\n\n")
            else:
                print("Podano błędne haslo")

        except IndexError:
            print("Podany user nie istnieje")

    elif len(set(("-u", "-p", "-t", "-s")) & set(pairs)) == 4:
        ''' send message to user '''
        # python3 message.py -u franek12 -p tajne1234 -t inny_user@test.pl -s 'temat123::wiadomosc testowa'
        hash_u = user.load_users_by_any(cursor, username=pairs['-u'])[0].hashed_password
        if clcrypto.check_password(pairs['-p'], hash_u):
            if user.load_users_by_any(cursor, email=pairs['-t']):
                if pairs['-s']:
                    message = Message()
                    message.title = "Brak tematu" if "::" not in pairs['-s'] else pairs['-s'].split("::")[0]
                    message.message = pairs['-s'] if "::"not in pairs['-s'] else pairs['-s'].split("::")[1]
                    message.sender = user.load_users_by_any(cursor, username=pairs['-u'])[0].email
                    message.receiver = pairs['-t']
                    message.save_to_db(cursor)
                    print("Wiadomość wysłana")
                else:
                    print("Brak wiadomości?")
            else:
                print("podany adresat nie instnieje")
        else:
            print("Podano błędne hasło")

    else:
        print("komunikat pomocy")
        print("-u -p -l Wyświetl wszystkie wiadomości otrzymane przez użytkownika e.g.")
        print("     python3 message.py -u franek12 -p tajne123 -l \n\n")

        print("-u -p -t -s Wyślij wiadomość do innego użytkownika")
        print(" python3 message.py -u franek12 -p tajne1234 -t inny_user@test.pl -s 'temat123::wiadomosc testowa \n\n'")
