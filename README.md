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
```

## Usage
The website can be viewed through opening up the ‘index.html' file from the folder staysafe/templates in Google Chrome. 
To try out the search function, you can type in 'duder library' in the building input.
The website will negivate to a sample result page.

The search function is still under construction, and therefore only the duder library sample can be viewed.

Start the server by command
 ```
(env) $ pwd
        /staysafe
(env) $ ./bin/staysaferun
 ```
 Then you can navigate to http://localhost:8000 and see our webiste.
