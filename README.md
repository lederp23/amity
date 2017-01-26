Amity is a room allocation and management system for one of andela's facilities called 'Amity'

**Installation**

```
$ git clone  https://github.com/lederp23/amity.git
$ cd amity
```

Create and activate a virtual environment

```
$ mkvirtualenv env
$ workon env
```

Install dependencies

```
$ pip install -r requirements.txt
```

Run the application

```
$ python main.py -i
```

**Commands**
```
main.py (-i | --interactive)
main.py (-h | --help )
main.py create_room <room_name>...
main.py add_person <first_name> <last_name> <type> [--accommodate=N]
main.py reallocate_person <first_name> <last_name> <new_room_name>
main.py load_people
main.py print_allocations [--o=file_name]
main.py print_unallocated [--o=file_name]
main.py print_room <room_name>
main.py allocate_office <first_name> <last_name>
main.py allocate_livingspace <first_name> <last_name>
main.py save_state [--db=sqlite_database]
main.py load_state <sqlite_database>
main.py deallocate_person <first_name> <last_name> <room_type>
main.py quit
main.py reset
main.py clear
```
