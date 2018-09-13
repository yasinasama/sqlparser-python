# -*- coding: utf-8 -*-

import unittest

from sqlparser import parse

class TestParser(unittest.TestCase):

    def test_simple(self):
        result = parse("select * from blog;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*'}],
            'table':[{'name':'blog'}],
            'join':[],
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_column(self):
        result = parse("select count(*) as cnt from blog;")
        expected = {
            'type':'SELECT',
            'column':[{'name':{'COUNT':'*'},'alias':'cnt'}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_distinct(self):
        result = parse("select distinct name,age from blog;")
        expected = {
            'type':'SELECT',
            'column':[{'name':{'DISTINCT':'name'}},
                      {'name': 'age'}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_distinct_2(self):
        result = parse("select avg(distinct(name)) from blog;")
        expected = {
            'type':'SELECT',
            'column':[{'name':{'AVG':{'DISTINCT':'name'}}}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_table(self):
        result = parse("select b.name as name,b.age as age from blog b;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'b.name','alias':'name'},
                      {'name':'b.age','alias':'age'}],
            'table':[{'name':'blog','alias':'b'}],
            'join': [],
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_where_1(self):
        result = parse("select * from blog where name='zhangsan';")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*'}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':[{'name': 'name', 'value': 'zhangsan', 'compare': '='}],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_where_2(self):
        result = parse("select * from blog where name='zhangsan' and (age<18 or age>30);")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*'}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':
            [
                {'name': 'name', 'value': 'zhangsan', 'compare': '='},
                'AND',
                [
                    {'name':'age','value':18,'compare':'<'},
                    'OR',
                    {'name': 'age', 'value': 30, 'compare': '>'}
                ]
            ],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_where_3(self):
        result = parse("select * from blog where age is not null;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*'}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':[{'name': 'age', 'value': 'NOT NULL', 'compare': 'IS'}],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_where_4(self):
        result = parse("select * from blog where age not in (13,12,11);")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*'}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':[{'name': 'age', 'value': [13,12,11], 'compare': 'NOT IN'}],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_left_join(self):
        result = parse("select * from blog b left join user u on b.name = u.name;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*'}],
            'table':[{'name':'blog','alias':'b'}],
            'join': [{'type':'LEFT','table':[{'name':'user','alias':'u'}],'on':['b.name','u.name']}],
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_join(self):
        result = parse("select * from blog b JOIN user u on b.name = u.name join tags t on b.tag=t.tag;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*'}],
            'table':[{'name':'blog','alias':'b'}],
            'join': [{'type':'INNER','table':[{'name':'user','alias':'u'}],'on':['b.name','u.name']},
                     {'type': 'INNER', 'table': [{'name': 'tags', 'alias': 't'}], 'on': ['b.tag', 't.tag']}],
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_like(self):
        result = parse("select * from blog where name like '%张%';")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*'}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':
            [
                {'name': 'name', 'value': '%张%', 'compare': 'LIKE'},
            ],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_group_by(self):
        result = parse("select name,age,count(*) from blog group by name,age;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'name'},
                      {'name':'age'},
                      {'name':{'COUNT':'*'}}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':[],
            'group':['name','age'],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_group_by_2(self):
        result = parse("select blog.name,blog.age,count(u.*) from blog as b,username as u;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'blog.name'},
                      {'name':'blog.age'},
                      {'name':{'COUNT':'u.*'}}],
            'table':[{'name':'blog','alias':'b'},
                     {'name':'username','alias':'u'}],
            'join': [],
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_having(self):
        result = parse("select name,age,count(*),avg(age) from blog group by name,age having count(*)>2 and avg(age)<20;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'name'},
                      {'name':'age'},
                      {'name': {'COUNT': '*'}},
                      {'name':{'AVG':'age'}}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':[],
            'group':['name','age'],
            'having':[{'name': {'COUNT':'*'}, 'value': 2, 'compare': '>'},
                      'AND',
                      {'name': {'AVG':'age'}, 'value': 20, 'compare': '<'}],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_order_by(self):
        result = parse("select * from blog order by age desc,name;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*'}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':[],
            'group':[],
            'having':[],
            'order':[{'name':'age','type':'DESC'},
                     {'name':'name','type':'ASC'}],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_limit(self):
        result = parse("select * from blog limit 100;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*'}],
            'table':[{'name':'blog'}],
            'join': [],
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[0,100]
        }
        self.assertEqual(result,expected)

    def test_update(self):
        result = parse("update blog set name=cc where name=dd;")
        expected = {
            'type':'UPDATE',
            'table': [{'name':'blog'}],
            'column'  : [{'name':'name','value':'cc'}],
            'where' : [{'name': 'name', 'value': 'dd','compare': '='}]
        }
        self.assertEqual(result,expected)

    def test_update_2(self):
        result = parse("update blog set name=cc,age=18 where name=dd;")
        expected = {
            'type':'UPDATE',
            'table': [{'name':'blog'}],
            'column'  : [{'name':'name','value':'cc'},
                         {'name':'age','value':18}],
            'where' : [{'name': 'name', 'value': 'dd','compare': '='}]
        }
        self.assertEqual(result,expected)

    def test_delete(self):
        result = parse("delete from blog where name=dd;")
        expected = {
            'type':'DELETE',
            'table': [{'name':'blog'}],
            'where' : [{'name': 'name', 'value': 'dd','compare': '='}]
        }
        self.assertEqual(result,expected)

    def test_insert(self):
        result = parse("insert into blog (name,age) values (cc,18),('dd',2);")
        expected = {
            'type':'INSERT',
            'table': [{'name':'blog'}],
            'columns' : [{'name': 'name'},
                         {'name': 'age'}],
            'values' : [['cc',18],
                        ['dd',2]]
        }
        self.assertEqual(result,expected)

    def test_create(self):
        result = parse("create table blog (name varchar(30),age int);")
        expected = {
            'type':'CREATE',
            'table': 'blog',
            'columns' : [{'name': 'name','type':'VARCHAR(30)'},
                         {'name': 'age','type':'INT'}]
        }
        self.assertEqual(result,expected)

    def test_drop(self):
        result = parse("drop table blog;")
        expected = {
            'type':'DROP',
            'table': 'blog'
        }
        self.assertEqual(result,expected)

    def test_alter(self):
        result = parse("alter table blog add tag varchar(5);")
        expected = {
            'type':'ALTER',
            'table': 'blog',
            'columns': {'ADD':{'name':'tag','type':'VARCHAR(5)'}}
        }
        self.assertEqual(result,expected)


if __name__=='__main__':
    unittest.main()