# SchoolManagement


### Prerequisite:

    * Python 3.5.2+
    

### System Setup:

1. Environment setup:

    * Install pip and virtualenv:
        - sudo apt-get install python3-pip
        - pip install --upgrade pip
        - sudo pip3 install virtualenv or sudo pip install virtualenv

    * Create virtual environment:
        - virtualenv env

        OPTIONAL:- In case finding difficulty in creating virtual environment by
                  above command , you can use the following commands too.

            *   Create virtualenv using Python3:-
                    - virtualenv -p python3 env
            *   Instead of using virtualenv you can use this command in Python3 for creating virtual environment:-
                    - python3 -m venv env

    * Activate environment:
        - source env/bin/activate


    * Checkout to branch
        - git checkout "branch_name"

    * Install the requirements by using command:
        - cd SchoolManagement/

        ```
          pip3 install -r requirements.txt or pip install -r requirements.txt
        ```

    * Add following information in .env file,to get the actual values, please contact to project owner.

        - DB_ENGINE="******"
        - DB_NAME="****"
        - DEBUG=*******
        - SECRET_KEY="*******"
        - SETTINGS="*******"

3. Database migrations:
    ```
    $ python3 manage.py migrate
    ```

4. Run servers:
    ```
     $ python3 manage.py runserver
    ```
