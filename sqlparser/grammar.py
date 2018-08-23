# -*- coding: utf-8 -*-

from ply import lex,yacc

from . import lexer
from .exceptions import GrammarException

def p_expression(p):
    """ expression : dml END
    """
    p[0] = p[1]

# def p_expression(p):
#     """ expression : dml END
#                    | ddl END
#     """
#     p[0] = p[1]

def p_dml(p):
    """ dml : select
    """
    p[0] = p[1]

# def p_dml(p):
#     """ dml : select
#             | update
#             | insert
#             | delete
#     """
#     p[0] = p[1]

# def p_ddl(p):
#     """ ddl : create
#             | alter
#             | drop
#     """
#     p[0] = p[1]


###################################################
############         select            ############
###################################################
def p_select(p):
    """ select : SELECT distinct columns FROM STRING where group_by having order_by limit
    """
    p[0] = {
        'type'  : p[1],
        'distinct': p[2],
        'column': p[3],
        'table' : p[5],
        'where' : p[6],
        'group' : p[7],
        'having': p[8],
        'order' : p[9],
        'limit' : p[10]
    }

def p_distinct(p):
    """ distinct : DISTINCT
                 | empty
    """
    if 'DISTINCT' in p:
        p[0] = 'Y'
    else:
        p[0] = 'N'

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


# p[0] => [x,x..] | [x]
def p_columns(p):
    """ columns : columns COMMA columns
                | DISTINCT column
                | column
    """
    if len(p) > 2:
        p[0] = p[1] + p[3]
    else:
        p[0] = [p[1]]

def p_column(p):
    """ column : COUNT "(" item ")"
               | SUM "(" STRING ")"
               | AVG "(" STRING ")"
               | MIN "(" STRING ")"
               | MAX "(" STRING ")"
               | item
    """
    p[0] = {'name' : p[1],'func' : ''}
    if len(p) > 2:
        p[0]['name'] = p[3]
        p[0]['func'] = p[1]

def p_item(p):
    """ item : QSTRING
             | STRING
             | NUMBER
             | "*"
    """
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
        'left' : p[1],
        'right': p[3],
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





