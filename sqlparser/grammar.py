# -*- coding: utf-8 -*-

from ply import lex,yacc

from . import lexer
from .exceptions import GrammarException


def p_expression(p):
    """ expression : dml END
                   | ddl END
    """
    p[0] = p[1]

def p_dml(p):
    """ dml : select
            | update
            | insert
            | delete
    """
    p[0] = p[1]


def p_ddl(p):
    """ ddl : create
            | alter
            | drop
    """
    p[0] = p[1]


###################################################
############         select            ############
###################################################
def p_select(p):
    """ select : SELECT columns FROM table join where group_by having order_by limit
    """
    p[0] = {
        'type'  : p[1],
        'column': p[2],
        'table' : p[4],
        'join'  : p[5],
        'where' : p[6],
        'group' : p[7],
        'having': p[8],
        'order' : p[9],
        'limit' : p[10]
    }

def p_table(p):
    """ table : table COMMA table
              | STRING AS STRING
              | STRING STRING
              | STRING
    """
    if ',' in p:
        p[0] = p[1] + p[3]
    else:
        if len(p) == 2:
            p[0] = [{'name':p[1]}]
        if len(p) == 3:
            p[0] = [{'name':p[1],'alias':p[2]}]
        if len(p) == 4:
            p[0] = [{'name':p[1],'alias':p[3]}]


def p_join(p):
    """ join : INNER JOIN table on join
             | LEFT JOIN table on join
             | RIGHT JOIN table on join
             | FULL JOIN table on join
             | JOIN table on join
             | empty
    """
    p[0] = []
    if len(p) == 5:
        p[0] = [{'type':'INNER','table':p[2],'on':p[3]}]+p[4]
    if len(p) == 6:
        p[0] = [{'type':p[1],'table':p[3],'on':p[4]}]+p[5]

def p_on(p):
    """ on : ON item COMPARISON item
    """
    p[0] = [p[2],p[4]]

def p_where(p):
    """ where : WHERE conditions
              | empty
    """
    p[0] = []
    if len(p) > 2:
        p[0] = p[2]

def p_group_by(p):
    """ group_by : GROUP BY strings
                 | empty
    """
    p[0] = []
    if len(p) > 2:
        p[0] = p[3]

def p_having(p):
    """ having : HAVING conditions
               | empty
    """
    p[0] = []
    if len(p) > 2:
        p[0] = p[2]

def p_order_by(p):
    """ order_by : ORDER BY order
                 | empty
    """
    p[0] = []
    if len(p) > 2:
        p[0] = p[3]


def p_limit(p):
    """ limit : LIMIT numbers
              | empty
    """
    p[0] = []
    if len(p) > 2:
        p[0] = p[2]

def p_order(p):
    """ order : order COMMA order
              | string order_type
    """
    if len(p) > 3:
        p[0] = p[1] + p[3]
    else:
        p[0] = [{'name': p[1],'type': p[2]}]

def p_order_type(p):
    """ order_type : ASC
                   | DESC
                   | empty
    """
    if p[1] == 'DESC':
        p[0] = 'DESC'
    else:
        p[0] = 'ASC'


###################################################
############         update            ############
###################################################
def p_update(p):
    """ update : UPDATE table SET set where
    """
    p[0] = {
        'type'  : p[1],
        'table': p[2],
        'column'  : p[4],
        'where' : p[5]
    }

def p_set(p):
    """ set : set COMMA set
            | item COMPARISON item
    """
    if '=' in p:
        p[0] = [{'name':p[1],'value':p[3]}]
    else:
        p[0] = p[1] + p[3]

###################################################
############         insert            ############
###################################################
def p_insert(p):
    """ insert : INSERT into table insert_columns VALUES values
    """
    p[0] = {
        'type': p[1],
        'table': p[3],
        'columns': p[4],
        'values': p[6]
    }

def p_into(p):
    """ into : INTO
             | empty
    """
    pass

def p_insert_columns(p):
    """ insert_columns : "(" columns ")"
                       | empty
    """
    p[0] = []
    if len(p) > 2:
        p[0] = p[2]

def p_value(p):
    """ value : value COMMA value
              | string
              | NUMBER
    """
    if len(p) > 2:
        p[0] = p[1] + p[3]
    else:
        p[0] = [p[1]]

def p_values(p):
    """ values : values COMMA values
               | "(" value ")"
    """
    if ',' in p:
        p[0] = p[1] + p[3]
    else:
        p[0] = [p[2]]

###################################################
############         delete            ############
###################################################
def p_delete(p):
    """ delete : DELETE FROM table where
    """
    p[0] = {
        'type': p[1],
        'table': p[3],
        'where': p[4]
    }

###################################################
############         create            ############
###################################################
def p_create(p):
    """ create : CREATE TABLE string "(" create_columns ")"
    """
    p[0] = {
        'type': p[1],
        'table': p[3],
        'columns': p[5]
    }


def p_create_columns(p):
    """ create_columns : create_columns COMMA create_columns
                       | string datatype
    """
    if len(p) > 3:
        p[0] = p[1] + p[3]
    else:
        p[0] = [{'name':p[1],'type':p[2]}]

def p_datatype(p):
    """ datatype : INT
                 | INTEGER
                 | TINYINT
                 | SMALLINT
                 | MEDIUMINT
                 | BIGINT
                 | FLOAT
                 | DOUBLE
                 | DECIMAL
                 | CHAR "(" NUMBER ")"
                 | VARCHAR "(" NUMBER ")"
    """
    if len(p) > 2:
        p[0] = '%s(%s)'%(p[1],p[3])
    else:
        p[0] = p[1]

###################################################
############         alter              ###########
###################################################
def p_alter(p):
    """ alter : ALTER TABLE string change_column
    """
    p[0] = {
        'type': p[1],
        'table': p[3],
        'columns': p[4]
    }

def p_change_column(p):
    """ change_column : ADD string datatype
                      | DROP COLUMN string
                      | ALTER COLUMN string datatype
    """
    if p[1] == 'ADD':
        p[0] = {'ADD':{'name':p[2],'type':p[3]}}
    if p[1] == 'DROP':
        p[0] = {'DROP': {'name': p[2]}}
    if p[1] == 'ALTER':
        p[0] = {'ALTER': {'name': p[3],'type':p[4]}}

###################################################
############         drop              ############
###################################################
def p_drop(p):
    """ drop : DROP TABLE string
    """
    p[0] = {
        'type': p[1],
        'table': p[3]
    }

###################################################
############         column            ############
###################################################
# p[0] => [x,x..] | [x]
def p_columns(p):
    """ columns : columns COMMA columns
                | column_as
                | column
    """

    if len(p) > 2:
        p[0] = p[1] + p[3]
    else:
        p[0] = [p[1]]

def p_column_as(p):
    """ column_as : column AS item
                  | column item
    """
    p[0] = p[1]
    if len(p) > 3:
        p[0]['alias'] = p[3]
    else:
        p[0]['alias'] = p[2]

def p_column(p):
    """ column : function "(" distinct_item ")"
               | function "(" item ")"
               | distinct_item
               | item
    """
    if len(p) > 2:
        p[0] = {'name': {p[1]:p[3]}}
    else:
        p[0] = {'name':p[1]}

def p_distinct_item(p):
    """ distinct_item : DISTINCT item
                      | DISTINCT "(" item ")"
    """
    if len(p) > 3:
        p[0] = {p[1]:p[3]}
    else:
        p[0] = {p[1]:p[2]}

def p_function(p):
    """ function : COUNT
                 | SUM
                 | AVG
                 | MIN
                 | MAX
    """
    p[0] = p[1]

def p_item(p):
    """ item : string
             | NUMBER
             | "*"
             | string "." item
    """
    if len(p)>2:
        p[0] = p[1]+'.'+p[3]
    else:
        p[0] = p[1]


# p[0] => [1,2] | [1]
def p_numbers(p):
    """ numbers : NUMBER COMMA NUMBER
                | NUMBER
    """
    if len(p) > 2:
        p[0] = [p[1], p[3]]
    else:
        p[0] = [0, p[1]]

def p_strings(p):
    """ strings : strings COMMA strings
                | string
    """
    if len(p) > 2:
        p[0] = p[1] + p[3]
    else:
        p[0] = [p[1]]


def p_string(p):
    """ string : STRING
               | QSTRING
    """
    p[0] = p[1]


def p_conditions(p):
    """ conditions : conditions AND conditions
                   | conditions OR conditions
                   | "(" conditions ")"
                   | compare
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if '(' in p:
            p[0] = [p[2]]
        else:
            p[0] = p[1] + [p[2]] + p[3]

def p_compare(p):
    """ compare : column COMPARISON item
                | column LIKE QSTRING
    """
    p[0] = {
        'name' : p[1]['name'],
        'value': p[3],
        'compare' : p[2]
    }


# empty return None
# so expression like (t : empty) => len()==2
def p_empty(p):
    """empty :"""
    pass

def p_error(p):
    raise GrammarException("Syntax error in input!")


tokens = lexer.tokens

DEBUG = True

L = lex.lex(module=lexer, optimize=False, debug=DEBUG)
P = yacc.yacc(debug=DEBUG)

def parse_handle(sql):
    return P.parse(input=sql,lexer=L,debug=DEBUG)





