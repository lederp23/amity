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

Set up database

```
$ mkdir app/database
$ python app/models/models.py
```

Run the application

```
$ python main.py -i
```

**Commands**
```
create_room <room_name>...
add_person <first_name> <last_name> <type> [--accommodate=N]
reallocate_person <first_name> <last_name> <new_room_name>
load_people
print_allocations [--o=file_name]
print_unallocated [--o=file_name]
print_room <room_name>
allocate_office <first_name> <last_name>
allocate_livingspace <first_name> <last_name>
save_state [--db=sqlite_database]
load_state <sqlite_database>
quit
reset
clear
restart
```

A tutorial on how to use the app is at https://www.youtube.com/watch?v=nwclBVAvWP0.
