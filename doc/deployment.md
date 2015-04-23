Deployment for the Alpheios App
===

##Remote machine

### Apache
In your `/etc/apache2/sites-enabled` folder, create a new file `alpheios-app.conf` containing the following informations :

```xml
<VirtualHost *>
    ServerName [YourServerName]
    WSGIDaemonProcess perseids-client-apps-prod python-path=/path/to/prod:/path/to/prod/flask/lib/python3.4/site-packages
    WSGIScriptAlias /url/to/prod /path/to/prod/app.wsgi process-group=perseids-client-apps-prod
    <Directory /path/to/prod/>
         WSGIProcessGroup perseids-client-apps-prod
        Require all granted
    </Directory>
</VirtualHost>
<VirtualHost *>
    ServerName [YourServerName]
    WSGIDaemonProcess perseids-client-apps-stage python-path=/path/to/stage:/path/to/stage/flask/lib/python3.4/site-packages
    WSGIScriptAlias /url/to/stage /path/to/stage/app.wsgi process-group=perseids-client-apps-stage
    <Directory /path/to/stage/>
         WSGIProcessGroup perseids-client-apps-stage
        Require all granted
    </Directory>
</VirtualHost>
```

#### Apache EnvVars
Make sure the following informations are set-up in apache2 envvars
```
export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'
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