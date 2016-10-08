# Required imports
from pyomo.environ import *
from pyomo.dae import *
from pyomo.dae.plugins.finitedifference import Finite_Difference_Transformation

m = ConcreteModel()

m.K1 = Param(initialize=0.05)  #m3/s
m.K2 = Param(initialize=0.015) #m3/s
m.a1 = Param(initialize=0.6)
m.a2 = Param(initialize=0.5)
m.A = Param(initialize=0.5)    #m2
m.g = Param(initialize=10.0)    #m2/s

T = 200.0

#variables del problema
m.t = ContinuousSet(bounds=(0, T))
m.h = Var(m.t, within = NonNegativeReals, initialize = 0.4)

#variables derivadas respecto a las variables independientes x t
m.dhdt = DerivativeVar(m.h, wrt=m.t)

#restricciones que se deben cumplir
def _bdm(m, j): #balance de materia
    if j == 0 :
        return Constraint.Skip
    return m.A*m.dhdt[j] == m.K1*m.a1-m.K2*m.a2*sqrt(2*m.g*m.h[j])
m.bdm = Constraint(m.t, rule=_bdm)

def _initcon(m, j):
    if j != 0:
        return Constraint.Skip
    return m.h[j] == 0.5
m.initcon = Constraint(m.t,  rule=_initcon)

#funcion objetivo "dummy"
m.obj = Objective(expr=1)

#numero de puntos
Nt = 20 #puntos de la coordenada temporal t

#discretizar puntos
discretize = Finite_Difference_Transformation()
disc = discretize.apply(m,nfe=Nt,wrt=m.t,scheme='BACKWARD')

#resolver usando el solver ipopt
solver = SolverFactory('ipopt')
results = solver.solve(m, tee=True)

#obtencion de la solcion en x, t y U
import numpy as np

t = sorted(disc.t)
h = sorted(disc.h)
H = np.zeros((Nt+1,1))

for j in range(Nt+1):
    it = t[j]
    H[j] = value(disc.h[it])

#representacion grafica
import matplotlib.pyplot as plt

plt.plot(t,H)
plt.show()
