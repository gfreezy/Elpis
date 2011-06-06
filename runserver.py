#!/usr/bin/env python2
import sys
sys.path.append(sys.path[0])
sys.path.append('/home/alex/src/Elpis/elpis/tasks/')

#print sys.path

from elpis import app
#, db

#db.create_all()
app.run(debug=True)
