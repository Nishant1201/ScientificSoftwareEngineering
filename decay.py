import numpy as np
import matplotlib.pyplot as plt
import logging
import sys
import time 

def solver(I, a, T, dt, theta):
    """Solve u' = -a*u, u(0) = I, for t in (0, T] with steps of dt."""
    dt = float(dt)                  # avoid integer division
    Nt = int(round(T/dt))           # number of time intervals
    T = Nt*dt                       # adjust T to fit time step dt
    u = np.zeros(Nt+1)              # array of u[n] values
    t = np.linspace(0, T, Nt+1)     # time mesh

    u[0] = I                        # assign initial condition
    for n in range(0, Nt):          # n=0,1,....,Nt-1
        u[n+1] = (1 - (1-theta)*a*dt) / (1 + theta*a*dt) * u[n]
    return u, t

def u_exact(t, I, a):
    return I*np.exp(-a*t)

def experiment_print_error():
    I = 1; a = 2; T = 4; dt = 0.4; theta = 1
    u, t = solver(I, a, T, dt, theta)

    error = u_exact(t, I, a) - u
    E = np.sqrt(dt*np.sum(error**2))
    print('Error : ', E)

def experiment_compare_numerical_and_exact():
    I = 1; a = 2; T = 4.0; dt = 0.2; theta = 1.0
    u, t = solver(I, a, T, dt, theta)

    t_e = np.linspace(0, T, 1001)   # very fine mesh for u_e
    u_e = u_exact(t_e, I, a)

    plt.plot(t, u, 'r--o')          # dashed red line with circles
    plt.plot(t_e, u_e, 'b-')        # blue line for u_e
    plt.legend(['numerical', 'theta = %g' % theta, 'exact'])
    plt.xlabel('t')
    plt.ylabel('u')
    plt.show()
    #plotfile = "Images/decay"
    #plt.savefig(plotfile + '.png')
    #plt.savefig(plotfile + '.pdf')

    error = u_exact(t, I, a) - u
    E = np.sqrt(dt*np.sum(error**2))
    print('Error norm: ', E)

def experiment_compare_schemes():
    """ Compare theta = 0.0, 0.5, 1.0 in the same plot """
    I = 1; a = 2.0; T = 4.0; dt = 0.2
    legends = []
    for theta in [0.0, 1.0, 0.5]:
        u, t = solver(I, a, T, dt, theta)
        plt.plot(t, u, '--o')
        legends.append('theta=%g' % theta)
    t_e = np.linspace(0, T, 1001)   # very fine mesh for u_e
    u_e = u_exact(t_e, I, a)
    plt.plot(t_e, u_e, "b-")
    legends.append("exact")
    plt.legend(legends, loc="upper right")
    plt.show()
    #plotfile = "Images/decay"
    #plt.savefig(plotfile + ".png")
    #plt.savefig(plotfile + ".pdf")

# Define a default logger that does nothing
logging.getLogger('decay').addHandler(logging.NullHandler())

def solver_with_logging(I, a, T, dt, theta):
    """Solve u' = -a*u, u(0)=I, for t in (0,T] with steps of dt."""
    dt = float(dt)                    # avoid integer division
    Nt = int(round(T/dt))             # no of time intervals
    T = Nt*dt                         # adjust T to fit time step dt
    u = np.zeros(Nt+1)                # array of u[n] values
    t = np.linspace(0, T, Nt+1)       # time mesh
    logging.debug('solver : dt=%g, Nt=%g, T=%g' % (dt, Nt, T))

    u[0] = I                          # assign initial condition
    for n in range(0, Nt):            # n=0,1, ....,Nt-1
        u[n+1] = (1 - (1-theta)*a*dt)/(1 + theta*dt*a)*u[n]

        logging.info('u[%d]=%g' % (n, u[n]))
        # time.sleep(2)
        logging.debug('1 - (1-theta)*a*dt: %g, %s' %
                      (1 - (1-theta)*a*dt,
                      str(type(1-(1-theta)*a*dt))[7:-1]))
        logging.debug('1 + theta*dt*a: %g, %s' %
                      (1 + theta*dt*a,
                      str(type(1 + theta*dt*a))[7:-1]))
    return u, t

def configure_basic_logger():
    logging.basicConfig(
        filename='decay.log', filemode='w', level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y.%m.%d %I:%M:%S %p')

def read_command_line_positional():
    if len(sys.argv) < 6:
        print('Usage: %s I a T BE/FE/CN dt1 dt2 dt3 ...' % sys.argv[0])
        sys.exit(1)                 # abort

    I = float(sys.argv[1])
    a = float(sys.argv[2])
    T = float(sys.argv[3])

    # Name of schemes: BE(Backward Euler), FE(Forward Euler),
    # CN (Crank Nicolson)
    scheme = sys.argv[4]
    scheme2theta = {'BE' : 1, 'CN' : 0.5, 'FE' : 0}
    if scheme in scheme2theta:
        theta = scheme2theta[scheme]
    else:
        print('Invalid scheme name : ', scheme)
        sys.exit(1)
    
    dt_values = [float(arg) for arg in sys.argv[5:]]

    return I, a, T, theta, dt_values

def define_command_line_options():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--I', '--initial_condition', type=float,
        default=1.0, help='initial condition, u(0)',
        metavar='I')
    parser.add_argument(
        '--a', type=float, default=1.0,
        help='coefficient in ODE', metavar='a')
    parser.add_argument(
        '--T', '--stop_time', type=float,
        default=1.0, help='end time of simulation',
        metavar='T')
    parser.add_argument(
        '--scheme', type=str, default='CN',
        help='FE, BE or CN')
    parser.add_argument(
        '--dt', '--time_step_values', type=float,
        default=[1.0], help='time step values',
        metavar='dt', nargs='+', dest='dt_values')
    return parser

def read_command_line_argparse():
    parser = define_command_line_options()
    args = parser.parse_args()
    scheme2theta = {'BE': 1, 'CN': 0.5, 'FE': 0}
    data = (args.I, args.a, args.T, scheme2theta[args.scheme],
            args.dt_values)
    return data

def experiment_compare_dt(option_value_pairs=False):
    I, a, T, theta, dt_values = \
        read_command_line_argparse() if option_value_pairs else \
        read_command_line_positional()

    legends = []
    for dt in dt_values:
        u, t = solver(I, a, T, dt, theta)
        plt.plot(t, u)
        legends.append('dt=%g' % dt)
    t_e = np.linspace(0, T, 1001)       # very fine mesh for u_e
    u_e = u_exact(t_e, I, a)
    plt.plot(t_e, u_e, '--')
    legends.append('exact')
    plt.legend(legends, loc='upper right')
    plt.title('theta=%g' % theta)
    plt.show()
    #plotfile = 'Images/experiment_compare_dt'
    #plt.savefig(plotfile + '.png')
    #plt.savefig(plotfile + '.pdf')

#def compute4web(I, a, T, dt, theta=0.5):
#    """
#    Run a case with the solver, compute error measure,
#    and plot the numerical and exact solutions in a PNG
#    plot whose data are embedded in an HTML image tag.
#    """
#    u, t = solver(I, a, T, dt, theta)
#    u_e = u_exact(t, I, a)
#    e = u_e - u
#    E = np.sqrt(dt*np.sum(e**2))
#
#    plt.figure()
#    t_e = np.linspace(0, T, 1001)       # fine mesh for u_e
#    u_e = u_exact(t_e, I, a)
#    plt.plot(t,   u,   'r--o')
#    plt.plot(t_e, u_e, 'b-')
#    plt.legend(['numerical', 'exact'])
#    plt.xlabel('t')
#    plt.ylabel('u')
#    plt.title('theta=%g, dt=%g' % (theta, dt))
#    # Save plot to HTML img tag with PNG code as embedded data
#    from parampool.utils import save_png_to_str
#    html_text = save_png_to_str(plt, plotwidth=400)
#
#    return E, html_text

#def main_GUI(I=1.0, a=.2, T=4.0,
#            dt_values=[1.25, 0.75, 0.5, 0.1],
#            theta_values=[0.0, 0.5, 1.0]):
#    # Build HTML code for web page. Arrange plots in columns
#    # corresponding to the theta values, with dt down the rows
#    theta2name = {0: 'FE', 1:'BE', 0.5:'CN'}
#    html_text = '<table>\n'
#    for dt in dt_values:
#        html_text += '<tr>\n'
#        for theta in theta_values:
#            E, html = compute4web(I, a, T, dt, theta)
#            html_text += """
#<td>
#<center><b>%s, dt=%g, error: %.3E</b></center><br>
#%s
#</td>
#""" % (theta2name[theta], dt, E, html)
#        html_text += '</tr>\n'
#    html_text += '</table>\n'
#    return html_text

def solver_with_doctest(I=0.8, a=1.2, T=1.5, dt=0.5, theta=0.5):
    """
    Solve u'=-a*u, u(0)=I, for t in (0,T] with steps of dt.

    >>> u, t = solver(I=0.8, a=1.2, T=1.5, dt=0.5, theta=0.5)
    >>> for n in range(len(t)):
    ...     print('t=%.1f, u=%.14f' % (t[n], u[n]))
    t=0.0, u=0.80000000000000
    t=0.5, u=0.43076923076923
    t=1.0, u=0.23195266272189
    t=1.5, u=0.12489758761948
    """
    dt = float(dt)                  # avoid integer division
    Nt = int(round(T/dt))           # no of time intervals
    T = Nt*dt                       # adjust T to fit time step dt
    u = np.zeros(Nt+1)              # array of u[n] values
    t = np.linspace(0, T, Nt+1)     # time mesh

    u[0] = I                    # assign initial condition
    for n in range(0, Nt):
        u[n+1] = (1- (1-theta)*a*dt) / (1 + theta*dt*a) * u[n]
    return u, t

def u_discrete_exact(n, I, a, theta, dt):
    """Return exact discrete solution of the numerical schemes."""
    dt = float(dt)                  # avoid integer division
    A = (1- (1 - theta)*a*dt)/(1 + theta*dt*a)
    return I*A**n

def test_u_discrete_exact():
    """Check that the solver reproduces the exact discrete solution."""
    theta = 0.8; a = 2; I = 0.1; dt = 0.8
    Nt = int(8/dt)                  # number of time steps
    u, t = solver(I=I, a=a, T=Nt*dt, dt=dt, theta=theta)

    # Evaluate exact discrete solution on the mesh
    u_de = np.array([u_discrete_exact(n, I, a, theta, dt)
                    for n in range(Nt+1)])

    # Find largest deviation
    diff = np.abs(u_de - u).max()
    tol = 1E-16
    success = diff < tol
    print("Max absolute deviation, u_de - u = ", diff)
    assert success  

def test_potential_integer_division():
    """Choose variables that can trigger integer division."""
    theta = 1; a = 1; I = 1; dt = 2
    Nt = 4
    u, t = solver(I=I, a=a, T=Nt*dt, dt=dt, theta=theta)
    u_de = np.array([u_discrete_exact(n, I, a, theta, dt)
                    for n in range(Nt+1)])
    diff = np.abs(u_de - u).max()
    print("Test Potential integer division, Max absolute deviation, u_de - u = ", diff)
    assert diff < 1E-14

def test_read_command_line_positional():
    # Decide on a data set of input parameters
    I = 1.6; a = 1.8; T = 2.2; theta = 0.5
    dt_values = [0.1, 0.2, 0.05]
    # Expected return from read_command_line_positional
    expected = [I, a, T, theta, dt_values]
    # Construct corresponding sys.argv array
    sys.argv = [sys.argv[0], str(I), str(a), str(T), 'CN'] + \
                [str(dt) for dt in dt_values]
    computed = read_command_line_positional()
    for expected_arg, computed_arg in zip(expected, computed):
        print("expected_arg = ", expected_arg, " , computed_arg = ", computed_arg)
        assert expected_arg == computed_arg

def test_read_command_line_argparse():
    I = 1.6; a = 1.8; T = 2.2; theta = 0.5
    dt_values = [0.1, 0.2, 0.05]
    # Expected return from read_command_line_argparse
    expected = [I, a, T, theta, dt_values]
    # Construct corresponding sys.argv array
    command_line = "%s --a %s --I %s --T %s --scheme CN --dt " % \
                    (sys.argv[0], a, I, T)
    command_line += ' '.join([str(dt) for dt in dt_values])
    sys.argv = command_line.split()
    computed = read_command_line_argparse()
    for expected_arg, computed_arg in zip(expected, computed):
        print("expected_arg = ", expected_arg, " , computed_arg = ", computed_arg)
        assert expected_arg == computed_arg 

if __name__ == "__main__":
    #experiment_compare_numerical_and_exact()
    #experiment_compare_dt(option_value_pairs=True)
    #experiment_compare_dt()

    #import doctest
    #doctest.testmod()

    #test_u_discrete_exact()

    #test_potential_integer_division()

    #test_read_command_line_positional()

    test_read_command_line_argparse()