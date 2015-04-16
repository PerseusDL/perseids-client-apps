Deployment for the Alpheios App
===

##Remote machine

### Apache
In your `/etc/apache2/sites-enabled` folder, create a new file `alpheios-app.conf` containing the following informations :

```xml
<VirtualHost *>
    ServerName localhost

    WSGIScriptAlias /url/to/prod /path/to/prod/folder/app.wsgi

    <Directory /path/to/prod/folder/>
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>
<VirtualHost *>
    ServerName localhost

    WSGIScriptAlias /url/to/stage /path/to/stage/folder/app.wsgi

    <Directory /path/to/stage/folder/>
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
</VirtualHost>
```

### Local machine

Make sure you have fabfile installed (On ubuntu : `sudo apt-get install fabric`) !
Then, at the root of this repository, create a file fabconf.py which contains the following informations :

```python
# the user to use for the remote commands
user = 'thibault'
# the servers where the commands are executed
hosts = ['127.0.0.1']
# Path where we should install
path = "/home/thibault/alpheios"

# Available hosts for stage and prod
available_hosts = {
    "prod": {
        "user": "thibault",
        "host": ["192.168.0.1"],
        "remote_path": "/home/thibault/alpheios",
        "remote_cache_path": "/home/thibault/.alpheios-prod"
    },
    "stage": {
        "user": "thibault",
        "host": ["192.168.0.1"],
        "remote_cache_path": "/home/thibault/alpheios",
        "remote_cache_path": "/home/thibault/.alpheios-stage"
    }
}

```