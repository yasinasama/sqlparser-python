# -*- coding: utf-8 -*-

from .exceptions import LexerException

reserved = {
    'select': 'SELECT',
    'distinct':'DISTINCT',
    'from'  : 'FROM',
    'where' : 'WHERE',
    'inner' : 'INNER',
    'left'  : 'LEFT',
    'right' : 'RIGHT',
    'full'  : 'FULL',
    'join'  : 'JOIN',
    'on'    : 'ON',
    'group' : 'GROUP',
    'by'    : 'BY',
    'having': 'HAVING',
    'order' : 'ORDER',
    'desc'  : 'DESC',
    'asc'   : 'ASC',
    'limit' : 'LIMIT',
    'insert': 'INSERT',
    'into'  : 'INTO',
    'values': 'VALUES',
    'update': 'UPDATE',
    'set'   : 'SET',
    'delete': 'DELETE',

    'create': 'CREATE',
    'table' : 'TABLE',
    'alter' : 'ALTER',
    'drop'  : 'DROP',
    'show'  : 'SHOW',

    'as'    : 'AS',
    'and'   : 'AND',
    'or'    : 'OR',
    'in'    : 'IN',
    'like'  : 'LIKE',
    'between': 'BETWEEN',
    'null'  : 'NULL',
    'count' : 'COUNT',
    'sum'   : 'SUM',
    'avg'   : 'AVG',
    'min'   : 'MIN',
    'max'   : 'MAX'
}

tokens = (
    'COMPARISON',
    'STRING',
    'NUMBER',
    'QSTRING',
    'END',
    'COMMA',
) + tuple(set(reserved.values()))

literals = '(){}@%.*[]:-^'
t_COMPARISON = r'<>|!=|>=|<=|=|>|<'
t_END = r';'
t_COMMA = r','
t_ignore = ' \t\n'

def t_STRING(t):
    r"[a-zA-Z][_a-zA-Z0-9]*"
    t.type = reserved.get(t.value.lower(), 'STRING')
    if t.type != 'STRING':
        t.value = t.value.upper()
    return t

def t_QSTRING(t):
    r"('[^']*')|(\"[^\"]*\")|(`[^`]*`)"
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r"\d+(\.\d+)?"
    t.value = int(t.value)
    return t

def t_error(t):
    raise LexerException("Illegal character '%s' at line %s pos %s"
                        % (t.value[0],t.lineno,t.lexpos))

