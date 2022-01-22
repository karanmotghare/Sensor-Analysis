# Sensor-Analysis

## How to run
- Clone the repo
- Make sure you have Django installed
- Then inside **Sensor-Analysis** move to **sensor_analysis** directory
- To migrate django models to your local mysql db, execute the following:
    ```bash
    python manage.py migrate
    ```
- Inside the directory execute the command in terminal 
    ```bash
    python manage.py runserver
    ```
- Within the terminal local host address will be displayed go to that link and done.
***
## To setup mysql in your machine for python
- Make sure to have python3 (don't install newest python version as it is in bugs cluttering stage)
- Inside terminal run the code
    ```bash
    pip install mysqlclient
    pip install pymysql
    ```
- Once installed go to **settings.py** file in **sensor_analysis** directory and do the following changes ->
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '',#Add your database name that you will create in MySQL
            'USER': '',#Add your own user of MySQL 
            'PASSWORD': '',# Add your own password of MySQL
            'HOST':'localhost',
            'PORT':'3306',
        }
    }
    ```
    
    ***
    ## Dependencies
    - pip install statsmodels
    - pip install cryptography
