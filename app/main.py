"""
Usage:
  main.py create_room <room_name>...
  main.py add_person <fname_lname> <type> [--wants_accommodation]
  main.py reallocate_person <fname_lname> <new_room_name>
  main.py load_people
  main.py print_allocations [--o=filename]
  main.py print_unallocated [--o=filename]
  main.py print_room <room_name>
  main.py save_state [--db=sqlite_database]
  main.py load_state <sqlite_database>
  main.py quit
  main.py restart
  main.py clear
  main.py ( -h | --help)
  main.py ( -i | --interactive)

Options:
  -h --help         Show this screen
  -i --interactive
"""

import sys
import cmd
import os
import time
from docopt import docopt, DocoptExit
from colorama import init
from classes.amity import Amity
from pyfiglet import Figlet
from termcolor import colored

init()
font = Figlet(font = 'starwars')
introd = font.renderText('Amity')
os.system('clear')
print(introd)


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn




class AmityCli(cmd.Cmd):
    amity = Amity()
    prompt = 'Amity>> '
    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_name>..."""
        try:
            print(self.amity.create_room(arg['<room_name>']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <fname_lname> <type> [--wants_accommodation=N]"""
        try:
            print(self.amity.add_person(arg['<fname_lname>'], arg['<type>'],\
            arg['--wants_accommodation']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <fname_lname> <new_room_name>"""
        try:
            person = arg['<fname_lname>']
            room = arg['<new_room_name>']
            print(self.amity.reallocate(person, room))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people"""
        print(self.amity.load())

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]"""
        try:
            print(self.amity.print_allocations(arg['--o']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        try:
            print(self.amity.print_unallocated(arg['--o']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        try:
            print(self.amity.print_room(arg['<room_name>']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=amity]"""
        try:
            print(self.amity.save_state(arg['--db']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""
        try:
            print(self.amity.load_state(arg['<sqlite_database>']))
        except ValueError:
            print("Invalid argument")

    @docopt_cmd
    def do_quit(self, arg):
        """Usage: quit"""
        print('System closed.')
        exit()

    @docopt_cmd
    def do_clear(self, arg):
        """Usage: clear"""
        os.system('clear')
        print(introd)
        prompt = 'Amity>> '

    @docopt_cmd
    def do_restart(self, arg):
        """Usage: restart"""
        os.system('clear')
        print("Restarting.")
        time.sleep(0.6)
        os.system('clear')
        print("Restarting..")
        time.sleep(0.6)
        os.system('clear')
        print("Restarting...")
        time.sleep(0.6)
        os.system('clear')
        print(introd)
        AmityCli().cmdloop()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    print(__doc__)
    try:
        AmityCli().cmdloop()
    except KeyboardInterrupt:
        print(colored("\nKeyboard Interrupt"), "yellow")
    AmityCli().cmdloop()
