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
Then, at the root of this repository