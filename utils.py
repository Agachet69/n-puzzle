import sys

def get_format():
    if len(sys.argv) != 2:
        raise ValueError('Wrong number of arguments.')
    
    arg = sys.argv[1]

    if arg.isdigit():
        mon_entier = int(arg)
        if mon_entier < 3:
            print("Can't generate a puzzle with size lower than 3.")
            return
        print(mon_entier)
    else :
        try :
            file = open(sys.argv[1], 'r')
            content = file.read()
            file.close()
            print(content)
        except:
            raise ValueError('Wrong arguments format')


get_format()