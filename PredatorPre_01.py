import PyDSTool as dst
import matplotlib.pyplot as plt
from PyDSTool.Toolbox import phaseplane as pp

pars = {'mu':1,
        'alpha':-1,
        'omega':1,
        'beta':1}

icdict = {'x': 0.5, 'y': 0.1}

xstr = 'mu*x - omega*y + (alpha*x - beta*y)*(x*x + y*y)'
ystr = 'omega*x + mu*y + (beta*x + alpha*y)*(x*x + y*y)'

DSargs = dst.args(name='2D-System')
DSargs.pars = pars
DSargs.varspecs = {'x': xstr, 'y': ystr}
DSargs.ics = icdict
DSargs.tdomain = [0, 15] # set the range of integration.
DSargs.xdomain = {'x': [-3, 3], 'y': [-3, 3]}
DSargs.pdomain = {'mu': [-1, 1]}
DSargs.algparams = {'max_pts': 3000, 'init_step': 0.02, 'stiff':True}
ode = dst.Generator.Vode_ODEsystem(DSargs)

traj = ode.compute('polarization')
pts  = traj.sample(dt=0.01)

plt.plot(pts['t'], pts['x'])
plt.xlabel('time') # Axes labels
plt.ylabel('x')
plt.show()

plt.plot(pts['x'], pts['y'])
plt.xlabel('x') # Axes labels
plt.ylabel('y')
plt.show()

# plot vector field, using a scale exponent to ensure arrows are well spaced
# and sized
pp.plot_PP_vf(ode, 'x', 'y', scale_exp=-1, N=50)

plt.show()

PyCont = dst.ContClass(ode)

PCargs = dst.args(name='EQ1', type='EP-C')
PCargs.freepars = ['mu']
PCargs.StepSize = 0.1
PCargs.MaxNumPoints = 50
PCargs.MaxStepSize = 2
PCargs.MinStepSize = 1e-5
PCargs.LocBifPoints = ['all']
PCargs.verbosity = 2
PCargs.SaveEigen = True
#PCargs.StopAtPoints = 'B'
PyCont.newCurve(PCargs)

print('Computing curve...')
start = dst.clock()
PyCont['EQ1'].forward()
PyCont['EQ1'].backward()
print('done in %.3f seconds!' % (dst.clock()-start))

PyCont['EQ1'].display(['mu','y'], stability=True)
""" 
PCargs = dst.args(name='SN1', type='LC-C')
PCargs.initpoint    = 'EQ1:H1'
PCargs.freepars     = ['mu']
PCargs.MaxStepSize  = 0.01
PCargs.StepSize = 0.001
PCargs.LocBifPoints = 'all  '
PCargs.MaxNumPoints = 400
PCargs.verbosity = 5
PyCont.newCurve(PCargs)
# PyCont['SN1'].forward()
PyCont['SN1'].backward()
PyCont['SN1'].display(['mu','y'], stability=True) """

plt.show()