# Problema de la Mochila
# Daniel Domene-Lopez y Zuria Bauer

from pyomo.environ import *

model = AbstractModel()

model.ITEMS = Set()

model.v = Param(model.ITEMS, within=PositiveReals)

model.w = Param(model.ITEMS, within=PositiveReals)

model.c = Param(model.ITEMS, within=PositiveReals)

model.u = Param(model.ITEMS, within=PositiveReals)


model.limitW = Param(within=PositiveReals)
model.limitV = Param(within=PositiveReals)

model.x = Var(model.ITEMS, within=NonNegativeIntegers)

#FO
def value_rule(model):
    return sum(model.c[i]*model.x[i] for i in model.ITEMS)
model.value = Objective(sense=maximize, rule=value_rule)

#CONSTR
def weight_rule(model):
    return sum(model.w[i]*model.x[i] for i in model.ITEMS) <= model.limitW
model.weight = Constraint(rule=weight_rule)

def volum_rule(model):
    return sum(model.v[i]*model.x[i] for i in model.ITEMS) <= model.limitV
model.volum = Constraint(rule=volum_rule)

def amount_rule(model,i):
    return model.x[i]  <= model.u[i]
model.amount = Constraint(model.ITEMS, rule=amount_rule)
