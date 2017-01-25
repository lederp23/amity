Amity is a room allocation and management system for one of andela's facilities called 'Amity'

Installation

$ git clone  https://github.com/lederp23/amity.git

$ cd amity/

Create and activate a virtual environment


$ mkvirtualenv env

Install dependencies $ pip install -r requirements.txt

Run the application

$ python main.py -i

Commands

main.py (-i | --interactive)
main.py (-h | --help )
Amity>> create_room <room_name>...
Amity>> add_person <first_name> <last_name> <type> [--accommodate=N]
Amity>> reallocate_person <first_name> <last_name> <new_room_name>
Amity>> load_people
Amity>> print_allocations [--o=file_name]
Amity>> print_unallocated [--o=file_name]
Amity>> print_room <room_name>
Amity>> allocate_office <first_name> <last_name>
Amity>> allocate_livingspace <first_name> <last_name>
Amity>> save_state [--db=sqlite_database]
Amity>> load_state <sqlite_database>
Amity>> deallocate_person <first_name> <last_name> <room_type>
Amity>> quit
Amity>> reset
Amity>> clear
