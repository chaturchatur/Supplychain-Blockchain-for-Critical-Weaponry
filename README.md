# CSE-1006 Project 
##### Blockchain based navy inventory management system
##### Indent and Parts contracts are the core elements of the code 
##### The database system act as an catalog to link part details to the part ID
##### The Part contracts store entity (part instance) details 
---
### Installation:
npm and python virtual enviroment required
```
npm install ganache-cli -g
npm install truffle -g
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
---
### Setup:
```
source venv/bin/activate
mkdir db
cd App/server
./manage.py migrate
./manage.py loaddata data.json
```

---
### Usage

#### Start blockchain:
```
ganache-cli --db="db/" -d -m=$(cat mnemonic.txt)
```
#### Start Django:
```
source venv/bin/activate
cd App/server
./manage.py runserver
```
Use creds ```
Username:Ritvik
Paswword:test```
 to login at `http://{host:port}/login/`
---
