Frontend for [Steam PageRank](https://www.steampagerank.com). Code for the API can be found [HERE](https://github.com/TwelfthGhast/SteamPR-Backend).

## Editing your config ##

Please include your own Steam Web API key in config.py. You can generate a Steam Web API key [HERE](https://steamcommunity.com/dev/apikey). If you are self hosting a copy of the API, change it in the config.py file as well. Note that the provided API is subject to change at any time.

## Running the code ##

It is advised to install dependencies in a virtual environment to sandbox this code.
```
$ sudo apt update
$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
$ sudo apt install python3-venv
```
Then navigate to the project directory.
```
$ python3 -m venv venv
$ source venv/bin/activate
```

You will then need to install the following python modules:
- Flask ```pip install Flask```
- Flask-Caching ```pip install Flask-Caching```

You can then run the code
```
$ python3 frontend.py
```
