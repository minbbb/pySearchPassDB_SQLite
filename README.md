# pySearchPassDB_SQLite
Write data to the database and search for a password by email on this database. **SQLite** is used as a database.
## How to use
First you need to create a database.
```
python pySearchPassDB_SQLite.py --create
```
Search for passwords by email.
```
python pySearchPassDB_SQLite.py -s example@example.com
python pySearchPassDB_SQLite.py --search example@example.com
```
Add fields to the database from files. The lines in the file must be in the format *email:password*. Specifies the path to the folder where these files are with passwords. All files and subdirectories are parsed.
```
python pySearchPassDB_SQLite.py -a "path/to/dir"
python pySearchPassDB_SQLite.py --add "path/to/dir"
```
Show count fileds of db.
```
python pySearchPassDB_SQLite.py -c
python pySearchPassDB_SQLite.py --count
```
Clear all db fields.
```
python pySearchPassDB_SQLite.py --clear
```
## Delimiters
There can be different separators in the lists. These delimiters can be changed in the script itself in the tuple *PATTERN_SPLIT*. The default is 2 delimiters (":" and ";").
