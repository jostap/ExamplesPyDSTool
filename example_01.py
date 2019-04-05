import PyDSTool as dst
import numpy as np
from matplotlib import pyplot as plt

# we must give a name
DSargs = dst.args(name='Calcium channel model')
# parameters
DSargs.pars = { 'vl': -60,
               'vca': 120,
                 'i': 0,
                'gl': 2,
               'gca': 4,
                 'c': 20,
                'v1': -1.2,
                'v2': 18  }
# auxiliary helper function(s) -- function name: ([func signature], definition)
DSargs.fnspecs  = {'minf': (['v'], '0.5 * (1 + tanh( (v-v1)/v2 ))') }
# rhs of the differential equation, including dummy variable w
DSargs.varspecs = {'v': '( i + gl * (vl - v) - gca * minf(v) * (v-vca) )/c',
                   'w': 'v-w' }
# initial conditions
DSargs.ics      = {'v': 0, 'w': 0 }

DSargs.tdomain = [0,30]                         # set the range of integration.
ode  = dst.Generator.Vode_ODEsystem(DSargs)     # an instance of the 'Generator' class.
traj = ode.compute('polarization')              # integrate ODE
pts  = traj.sample(dt=0.1)                      # Data for plotting

# PyPlot commands
plt.plot(pts['t'], pts['v'])
plt.xlabel('time')                              # Axes labels
plt.ylabel('voltage')                           # ...
plt.ylim([0,65])                                # Range of the y axis
plt.title(ode.name)                             # Figure title from model name
plt.show()
