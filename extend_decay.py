import numpy as np
import matplotlib.pyplot as plt

import decay as dc

def experiment_compare_schemes():
    """Compare theta = 0.0 , 0.5, 1.0 in the same plot"""
    I = 1; a = 2; T = 4.0; dt = 0.2
    legends = []

    for theta in [0.0, 1.0, 0.5]:
        u, t = dc.solver(I, a, T, dt, theta)
        plt.plot(t, u, '--o')
        legends.append('theta = %g' % theta)
    
    t_e = np.linspace(0, T, 1001)
    u_e = dc.u_exact(t_e, I, a)

    plt.plot(t_e, u_e, "b-")
    legends.append("exact")
    plt.legend(legends, loc="upper right")
    plt.show()

if __name__ == "__main__":
    #experiment_compare_schemes()
    #dc.configure_basic_logger()
    #u, t = dc.solver_with_logging(I=1, a=0.5, T=10, dt=0.5, theta=0.5)

    #I, a, T, theta, dt_values = dc.read_command_line_positional()
    #print(I, a, T, theta, dt_values)

    dc.experiment_compare_dt(option_value_pairs=True)    