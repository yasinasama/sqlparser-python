# -*- coding: utf-8 -*-

import unittest

from sqlparser import parse

class TestParser(unittest.TestCase):

    def test_simple(self):
        result = parse("select * from blog;")
        expected = {
            'type':'SELECT',
            'column':[{'value':'*'}],
            'table':'blog',
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_distinct(self):
        result = parse("select distinct name from blog;")
        expected = {
            'type':'SELECT',
            'column':[{'value':{'DISTINCT':'name'}}],
            'table':'blog',
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_distinct_2(self):
        result = parse("select avg(distinct name) from blog;")
        expected = {
            'type':'SELECT',
            'column':[{'value':{'AVG':{'DISTINCT':'name'}}}],
            'table':'blog',
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
            'column':[{'value':'*'}],
            'table':'blog',
            'where':[{'left': {'value': 'name'}, 'right': 'zhangsan', 'compare': '='}],
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
            'column':[{'value':'*'}],
            'table':'blog',
            'where':
            [
                {'left': {'value': 'name'}, 'right': 'zhangsan', 'compare': '='},
                'AND',
                [
                    {'left':{'value':'age'},'right':18,'compare':'<'},
                    'OR',
                    {'left': {'value': 'age'}, 'right': 30, 'compare': '>'}
                ]
            ],
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
            'column':[{'value':'*'}],
            'table':'blog',
            'where':
            [
                {'left': {'value': 'name'}, 'right': '%张%', 'compare': 'LIKE'},
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
            'column':[{'value':'name'},
                      {'value':'age'},
                      {'value':{'COUNT':'*'}}],
            'table':'blog',
            'where':[],
            'group':['name','age'],
            'having':[],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_having(self):
        result = parse("select name,age,count(*),avg(age) from blog group by name,age having count(*)>2 and avg(age)<20;")
        expected = {
            'type':'SELECT',
            'column':[{'value':'name'},
                      {'value':'age'},
                      {'value': {'COUNT': '*'}},
                      {'value':{'AVG':'age'}}],
            'table':'blog',
            'where':[],
            'group':['name','age'],
            'having':[{'left': {'value': {'COUNT':'*'}}, 'right': 2, 'compare': '>'},
                      'AND',
                      {'left': {'value': {'AVG':'age'}}, 'right': 20, 'compare': '<'}],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_order_by(self):
        result = parse("select * from blog order by age desc,name;")
        expected = {
            'type':'SELECT',
            'column':[{'value':'*'}],
            'table':'blog',
            'where':[],
            'group':[],
            'having':[],
            'order':[{'name':'age','type':'DESC'},{'name':'name','type':'ASC'}],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_limit(self):
        result = parse("select * from blog limit 100;")
        expected = {
            'type':'SELECT',
            'column':[{'value':'*'}],
            'table':'blog',
            'where':[],
            'group':[],
            'having':[],
            'order':[],
            'limit':[0,100]
        }
        self.assertEqual(result,expected)



if __name__=='__main__':
    unittest.main()