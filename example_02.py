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
""" plt.plot(pts['t'], pts['v'])
plt.xlabel('time')                              # Axes labels
plt.ylabel('voltage')                           # ...
plt.ylim([0,65])                                # Range of the y axis
plt.title(ode.name)                             # Figure title from model name
plt.show()

plt.clf()                                       # Clear the figure
plt.hold(True)                                  # Sequences of plot commands will not clear the existing figure """
for i, v0 in enumerate(np.linspace(-80,80,20)):
    ode.set( ics = { 'v': v0 } )                # Initial condition
    # Trajectories are called pol0, pol1, ...
    # sample them on the fly to create Pointset tmp
    tmp = ode.compute('pol%3i' % i).sample()    # or specify dt option to sample to sub-sample
    plt.plot(tmp['t'], tmp['v'])
plt.xlabel('time')
plt.ylabel('voltage')
plt.title(ode.name + ' multi ICs')
plt.show()