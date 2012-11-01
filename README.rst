Mother Reminder
===============
Mother Reminder is a system for registering mothers, sending them reminds for care, and sending mass messages with pertinent/useful information.

Mother Reminder is build using the RapidSMS platform

Prerequisites
-------------

* RapidSMS installation
* Python 2.7
* Django 1.3 or later

Installation
------------

Fetch the code from the repository; thus:

    ```bash
    git clone https://github.com/revence27/mother.git
    ```

Initialise and update the submodules:

    ```bash
    cd mother
    git submodule init
    git submodule update
    ```
    
It is now necessary to initialise the database; thus:

    ```bash
    ./manager.py syncdb
    ```

Some initialisation requires that the Django migration tool, South, be disabled. So run the following command (which runs `syncdb` again, but with different environment:

    ```bash
    env WITHOUT_SOUTH=yes ./manager.py syncdb
    ```

At this point, the directory `mother` contains a working instance of Mother Reminder. To test it, and to development, run:

    ```bash
    ./manager.py runserver && $BROWSER http://localhost:8080/
    ```

To complete the installation procedure by recording the cron files, move the file `cron_mother` to your system's cron directory. This will require root privileges.

    ```bash
    sudo cp cron_mother /etc/cron.d/
    ```

The `settings.py` file would have the variables suitable for communicating from the application to the administrators, for the purpose of reporting errors and the like.
