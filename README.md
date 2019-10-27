## iGenius Challenge

The application is an online currency converter, which provides a Web API endpoint called ​"c​onvert". 
The endpoint must accept HTTP GET requests.
These are the input parameters:
    -​ amount: the amount to convert (e.g. 12.35)
    - src​_currency: ISO currency code for the source currency to convert (e.g. EUR,
USD, GBP)
    - des​ t_currency: ISO currency code for the destination currency to convert (e.g. EUR,
USD, GBP)
    - re​ference_date: reference date for the exchange rate, in YYYY-MM-DD format
The application converts the pr​ovided ​amount from​ ​src_currency to ​​dest_currency, given the exchange rate at the ​​reference_date.
The response is a JSON object like this:
    
    {
      "amount": 20.23,
      "currency": "EUR" 
    }
    
The xml file with the last 90 days exchange rates is located this link: 
- https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml

## Api

There are three endpoint:

    /api/status: it gives back the status of the application
    /api/convert: it performs the amount converstion
    /api/update-db: it updates the database with the latest data available
    

## How to run the application

### With Docker

To run the application, just run the docker-compose:

```bash
$ docker-compose up --build
```

We have two images:

    - redis: we use the redis server as a cache
    - mongo_db: the database where the exchange rates are stored
    - convert_app: the application

The redis and mongo_db images are necessary in order to run the convert_app application.

You can run the application within the container ``convert_app`` by running:

```bash
$ python3 /app/convert_app/app.py
``` 

This should run the application.

Note: at the beginning, the application should have run with gunicorn. It gave some issues regarding the timeout which it is not solved yet.
This is a big TODO that can be implemented in the future.

### Without docker

Note: This application uses redis-server and mongo_db. Please install them on your device or use the images provided in docker-compose.

#### Set-up virtualenv

**Note:** here we use python 3.7 but the application can run with python 3.6+ (or, at least, it should)

1. Create virtualenv:
```bash
$ virtualenv -p python3.7 venv37
```

2. Activate virtualenv
```bash
$ source ./venv37/bin/activate
```
**Note:** In order to exit from virtual environment use `deactivate`

3. Install all python core libraries
```bash
$ pip install -r requirements.txt
```

#### Execution

You can run the application by executing the module ``app.py``. This will run the application on localhost and the default port is 5000.
There are a bunch of env variables to set:
    
    CONVERT_APP_CONFIG=path/to/conf/file.ini
    LOG_PATH=path/to/logs/
    LOG_LEVEL=log level 
    LOG_CONF=path/to/log/config/file.ini
    REDIS_HOST_ADDRESS=redis host address
    REDIS_PORT_BIND=redis port
    USE_REDIS_CACHE=true if you want to use redis as a cache. false otherwise
    DATABASE_CONNECTION=connection string to connect the db (mongodb:///127.0.0.1:21112)
    DATA_SOURCE_URL=https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml

To run the application in dev mode, you can run the command
```bash
$ python app.py
```
This will run the flask development server at port 5000.


### Tests

```bash
$ pytest --cov=convert_app tests/
```

## Before start making changes...
#### Install git client Hooks

1. Open with a terminal and execute
```bash
$ git config core.hooksPath git-hooks
```

This command set git to use hooks saved in `git-hooks` instead of the default `.git/hooks/`.

The pre-commit hook performs a check using:
 * flake8 (blocking) 
 * pylint (non blocking)
 
After that, it runs all the tests with coverage. If all the tests pass, it performs the commit.
