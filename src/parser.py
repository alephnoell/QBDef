#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 12:38:01 2019

@author: alephnoell
"""


from lark import Lark, Transformer, v_args
from representation import QBF

try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass



formula_family_grammar = """

    start: value* formula_family
    
    ?value : "value:" NAME "=" EXPRESSION ";" -> handle_value

    formula_family : name format parameters? variables finish
 
    name: "name:" FAMILY_NAME -> set_name
    
    format: "format:" FORMAT -> set_format
    
    parameters: "parameters:" parameter_declaration+ "end"
    
    parameter_declaration: NAME ":" PARAM_TYPE ("," EXPRESSION)* ";" -> add_parameter 

    variables : "variables:"  "end"
    
    finish : -> return_formula
    
    FAMILY_NAME : /[a-zA-Z]([a-zA-Z0-9])*/
    NAME : /[a-z]([a-zA-Z0-9])*/
    FORMAT : "CNF" | "circuit"
    PARAM_TYPE : "natural"
    EXPRESSION : /[^,;]+/
    
    %import common.NUMBER
    %import common.WS_INLINE
    %import common.NEWLINE
    %ignore WS_INLINE
    %ignore NEWLINE
    
"""

@v_args(inline=True)    # Affects the signatures of the methods
class TraverseTree(Transformer):
    #from operator import lt, le, eq, ne, ge, gt, mod, add, sub, mul, truediv as div, neg
    #number = int

    def __init__(self):
        self.formula = QBF()

    def handle_value(self, name, expr):
        print("VALUE: Handling parameter {} with value {}".format(name, expr))
        self.formula.set_value(str(name), str(expr))

    def set_name(self, name):
        print("NAME: setting name {}".format(name))
        self.formula.set_name(str(name))
        
    def set_format(self, f):
        print("FORMAT: setting format {}".format(f))
        self.formula.set_format(str(f))
        
    def add_parameter(self, p, t, *c):
        constr = []
        for elem in c:
            constr.append(str(elem))
        print("PARAMETER: adding parameter {} of type {} with constraints {}".format(p, t, constr))
        self.formula.add_parameter(str(p), str(t), constr)
        
    def return_formula(self):
        return self.formula
        
parser = Lark(formula_family_grammar, parser='lalr', transformer=TraverseTree())
parse = parser.parse

#def main():
#    while True:
#        try:
#            s = input('> ')
#        except EOFError:
#            break
#        c = parse(s)
#        
#        for sub in c.iter_subtrees():
#            if sub.data == "formula_family":
#                chil = sub.children
#                o = chil[len(chil) - 1]
#                print(o)
#                name = o.get_name()
#                print(name)
#                f = o.get_format()
#                print(str(f))
#     

def main():
    f = open("test_def.txt", "r")
    s = f.read()
    parsed_formula = parse(s)
    formula = None
    for sub in parsed_formula.iter_subtrees():
        if sub.data == "formula_family":
            chil = sub.children
            formula = chil[len(chil) - 1]
    print(formula)
    params = formula.get_parameters()
    p = params[1]
    print(p.paramRestrictions)

#def test():
#    print(calc("a = 1+2"))
#    print(calc("1+a*-3"))


if __name__ == '__main__':
    # test()
    main()
