
import autograd.numpy as gradz
from numpy import linalg as la 
from autograd import hessian 
import matplotlib.pyplot as plt 
import autograd.numpy as np   
from autograd import grad
import random

#Functions
def func(x, A, b):
    g_x = b - A @ x 
    barrier = -np.sum(np.log(g_x))
    return barrier


#Newton method 
#Probably has to check for eigen values aswell
def newton_method(f, x, Mat, b, k_max):
    hes = hessian(f)
    fir = grad(f)
    ep = 0.001 
    #num1 = random.random() #Random Start
    #num2 = random.random() # Random Start 
    arr_x = []
    while k_max > ep:
        g = fir(x, Mat, b)
        H = hes(x, Mat, b)
        d = la.inv(H) @ g
        x = x - d
        arr_x.append(x.copy())
        k_max = k_max - 1
    return x, arr_x

#Checking if our points are inside of polyhedron if
# If positive slack
def constrain(A,x,b):
    return b - A @ x 

def plot_polyhedron(Mat, b, x_star):
    x1 = np.linspace(-2, 2, 100)
    x2 = np.linspace(-2, 2, 100)
    X1, X2 = np.meshgrid(x1, x2)

    # feasible region
    feasible = np.ones(X1.shape, dtype=bool)
    for i in range(len(b)):
        feasible &= (Mat[i,0]*X1 + Mat[i,1]*X2 <= b[i])
    plt.contourf(X1, X2, feasible, levels=[0.5, 1.5], colors=['tab:blue'], alpha=0.3)

    # constraint lines
    x_plot = np.linspace(-2, 2, 100)
    for i in range(len(b)):
        if Mat[i,1] != 0:
            x2_line = (b[i] - Mat[i,0]*x_plot) / Mat[i,1]
            plt.plot(x_plot, x2_line, label=f'c{i+1}')
        else:
            # vertical line
            x_vert = b[i] / Mat[i,0]
            plt.axvline(x=x_vert, label=f'c{i+1}')


    # center point
    plt.scatter(*x_star, color='red', zorder=5, s=100, label='x*')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()


    