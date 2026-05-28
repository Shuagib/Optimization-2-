from numpy import linalg as la 
from autograd import hessian 
import matplotlib.pyplot as plt 
import autograd.numpy as np   
from autograd import grad


# Function
def barrier_func(x, A):
    s_x = 1 - A @ x
    t_x = 1 - x
    u_x = 1 + x
    barrier = - np.sum(np.log(s_x)) - np.sum(np.log(t_x)) - np.sum(np.log(u_x))
    return barrier

# Search Direction - Gradient method and Newton-type method
def grad_desc(f, x, A, k_max=1000, eta=1e-6):
    gfunc = grad(f)

    values = []
    steps = []

    for _ in range(k_max):
        gradient = gfunc(x, A)

        if np.linalg.norm(gradient) <= eta:
            break

        descent_dir = -gradient
        alpha = backtracking_line_search(f,x,descent_dir,A)

        x = x + alpha * descent_dir
        values.append(f(x,A))
        steps.append(alpha)
    
    return x, values, steps

def newton_method(f, x, A, k_max=100, eta=1e-6):
    hes = hessian(f)
    fir = grad(f)

    values = []
    steps = []
    
    for _ in range(k_max):
        gradient = fir(x, A)

        if np.linalg.norm(gradient) <= eta:
            break
        
        H = hes(x, A)
        descent_dir = -la.solve(H, gradient)
        
        alpha = backtracking_line_search(f, x, descent_dir, A)

        x = x + alpha * descent_dir

        values.append(f(x,A))
        steps.append(alpha)

    return x, values, steps

# Backtracking line search
def backtracking_line_search(f, x, d, A, alpha=1, p=0.5, beta=1e-4):
    g = grad(f)(x, A)

    while not feasible(x + alpha*d, A):
        alpha *= p

    while f(x + alpha*d, A) > f(x,A) + beta*alpha*(g@d):
        alpha *= p

    return alpha

# Feasibility Ensurance
def feasible(x, A):
    return (
        np.all(A @ x < 1.0) and
        np.all(x < 1.0) and
        np.all(x > -1.0)
    )

# Example
sizes = [
    (1,1),
    (2, 8),
    (5, 20),
    (10, 40),
    (40, 160),
    (1000,1000)
]

for n, m in sizes:
    np.random.seed(1)

    A = np.random.randn(m, n) * 0.2
    x0 = np.zeros(n)

    x_gd, f_gd, a_gd = grad_desc(barrier_func, x0, A)
    x_nt, f_nt, a_nt = newton_method(barrier_func, x0, A, eta=1e-8)

    print("n =", n, "m =", m)
    print("Gradient Descent: ")
    print("Iterations:", len(f_gd))
    print("Final Objective:", f_gd[-1])
    print("\nNewton Method:")
    print("Iterations:", len(f_nt))
    print("Final Objective", f_nt[-1])
    print("=====================================")

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Objective values
    ax[0].plot(f_gd, label="Gradient descent")
    ax[0].plot(f_nt, label="Newton")
    ax[0].set_xlabel("Iteration")
    ax[0].set_ylabel("Objective value")
    ax[0].set_title("Objective")
    ax[0].legend()
    ax[0].grid()

    # Step lengths
    ax[1].plot(a_gd, label="Gradient descent")
    ax[1].plot(a_nt, label="Newton")
    ax[1].set_xlabel("Iteration")
    ax[1].set_ylabel("Step length")
    ax[1].set_title("Step length")
    ax[1].legend()
    ax[1].grid()

    plt.tight_layout()
    plt.show()
