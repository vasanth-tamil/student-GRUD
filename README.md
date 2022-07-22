#### STUDENT GRUD SYSTEM
**set up**
```bash
pip3 install -r requirements.txt
```
**run**
```bash
python3 students-GRUD.py
```
**edit config file**
```bash
config = {
	"port": 8080,
	"secret_key": "3601e469065cf2f99691c0cb1aff8dff",
	"database_file": "sqlite:///database.db"	
}
```
**debug**
```bash
http://localhost:8080/
```