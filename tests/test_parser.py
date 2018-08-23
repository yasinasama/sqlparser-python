# -*- coding: utf-8 -*-

import unittest

from sqlparser import parse

class TestParser(unittest.TestCase):

    def test_simple(self):
        result = parse("select * from blog;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*','func':''}],
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
            'column':[{'name':'*','func':''}],
            'table':'blog',
            'where':[{'left': {'name': 'name', 'func': ''}, 'right': 'zhangsan', 'compare': '='}],
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
            'column':[{'name':'*','func':''}],
            'table':'blog',
            'where':
            [
                {'left': {'name': 'name', 'func': ''}, 'right': 'zhangsan', 'compare': '='},
                'AND',
                [
                    {'left':{'name':'age','func':''},'right':18,'compare':'<'},
                    'OR',
                    {'left': {'name': 'age', 'func': ''}, 'right': 30, 'compare': '>'}
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
            'column':[{'name':'*','func':''}],
            'table':'blog',
            'where':
            [
                {'left': {'name': 'name', 'func': ''}, 'right': '%张%', 'compare': 'LIKE'},
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
            'column':[{'name':'name','func':''},{'name':'age','func':''},{'name':'*','func':'COUNT'}],
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
            'column':[{'name':'name','func':''},
                      {'name':'age','func':''},
                      {'name':'*','func':'COUNT'},
                      {'name':'age','func':'AVG'}],
            'table':'blog',
            'where':[],
            'group':['name','age'],
            'having':[{'left': {'name': '*', 'func': 'COUNT'}, 'right': 2, 'compare': '>'},
                      'AND',
                      {'left': {'name': 'age', 'func': 'AVG'}, 'right': 20, 'compare': '<'}],
            'order':[],
            'limit':[]
        }
        self.assertEqual(result,expected)

    def test_order_by(self):
        result = parse("select * from blog order by age desc,name;")
        expected = {
            'type':'SELECT',
            'column':[{'name':'*','func':''}],
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
            'column':[{'name':'*','func':''}],
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