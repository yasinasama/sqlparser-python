# sqlparser-python

## usage
```
git clone https://github.com/yasinasama/sqlparser-python.git
cd sqlparser
python setup.py install
```
</br>
```
>> from sqlparser import parse
>> parse('select a from b where c=1 group by a')
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
