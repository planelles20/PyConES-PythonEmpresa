from __future__ import division
from pyomo.environ import *

model = AbstractModel()

#sets
model.I = Set(ordered=True) #ciudades

#parametros
model.A = Param(model.I, model.I)
model.n = Param()
#variables
model.y = Var(model.I, model.I, within=Binary)
model.u = Var(model.I)

print(model.A)
#funcion objetivo
def _objfunc(model):
    return summation(model.A, model.y)
model.OBJ = Objective(rule=_objfunc, sense=minimize)

#constraint
def const1(model, i):
    return sum(model.y[i,j] for j in model.I if (i != j)) == 1
model.CONST1 = Constraint(model.I, rule=const1)

def const2(model, j):
    return sum(model.y[i,j] for i in model.I if (i != j)) == 1
model.CONST2 = Constraint(model.I, rule=const2)

def const3(model, i, j):
    if (i == model.I[1] or j == model.I[1] or j == i):
        return Constraint.Skip
    else:
        return model.u[i] - model.u[j] + model.n*model.y[i,j] <= model.n-1
model.CONST3 = Constraint(model.I, model.I, rule=const3)

#solver = SolverFactory('glpk')
#results = solver.solve(model, tee=True)
