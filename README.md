# StaySafe
This repo includes the source code of website StaySafe.
StaySafe is a website which can recommend uncongested locations.

Developers: Jing Dong, Zheng Hu, Connor Martin, Qinjuan Xie

## Installation
Download the repo.
Please create a Python virtual environment for running the webiste, and activate the venv when running the code in the repo.
 ```
 $ pwd
  /staysafe
 $ python3 -m venv env
 $ source env/bin/activate
 ```
You may exit the venv by ```deactivate``` command when you need.
```
$ deactivate
```
Please install packages needed for running the webiste.
```
pip install -r requirements.txt
sudo apt-get install sqlite3
```

## Usage
Start the server by command
 ```
(env) $ pwd
        /staysafe
        chmod +x ./bin/staysafedb
        chmod +x ./bin/staysaferun
(env) $ ./bin/staysaferun
 ```
 Then you can navigate to http://localhost:8000 and see our webiste.
 A precise name is needed to search its congestion level. For example, you need to type "Angell Hall" to search congestion levels in Angell Hall. Inputs like "Angell," "angell hall," are not support in this release.
