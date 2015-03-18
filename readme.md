#Dependencies

#Setting up

- Have virtualenv installed : `sudo apt-get install python-virtualenv`
- Create virtualenv : `virtualenv flask`
- *(Optional)* Source virtualenv  : `source env/bin/activate`

# i18n
Here is a few commands you might need. The translations are located in `app/translations` and follow `.po` standards. Feel free to use apps such as [PoEdit](http://poedit.net/) to enhance, add corections.

- Update Catalog : `pybabel extract -F babel.cfg -o messages.pot app`
- Create a lang  : `pybabel init -i messages.pot -d app/translations -l $LANGUAGE`

#Alpheios Copyright
```
  Copyright 2014 The Alpheios Project, Ltd.
  http://alpheios.net
  
  This file is part of Alpheios.
  
  Alpheios is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  Alpheios is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
```