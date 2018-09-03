# sqlparser-python

## usage
```
git clone https://github.com/yasinasama/sqlparser-python.git
cd sqlparser
python setup.py install
```
</br>
```
from sqlparser import parse
parse("select * from blog where name='zhangsan';")

'type':'SELECT',
'column':[{'name':'*'}],
'table':[{'name':'blog'}],
'join': [],
'where':[{'name': 'name', 'value': 'zhangsan', 'compare': '='}],
'group':[],
'having':[],
'order':[],
'limit':[]

```
