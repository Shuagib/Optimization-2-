from Task_3 import * 
#Test objectuve function
import numpy as np

if __name__ == '__main__':
    gam = 100

    Mat = np.array([
    [1,0], 
    [0,1], 
    [-1,0], 
    [0,-1], 
    [1,1]])
    
    Mat_gam = np.array([
        [1,0], 
    [0,1], 
    [-1,0], 
    [0,-1], 
    [gam*1,gam*1]])
    

    

    # Task 3.1
    b = np.array([1,1,1,1,1.5])

    b_gam = np.array([1,1,1,1,gam*1.5]) 

    b_norm = np.array([1,1,1,1,1])

    x = np.array([0.0,0.0]) #Intia start 
    x_init = x.copy()

    x_old, arr_x  = newton_method(func,x,Mat,b,10)
    x_new, arr_x = newton_method(func,x,Mat_gam,b_gam,10)
    x_norm, arr_x = newton_method(func,x,Mat,b_norm,10)

    #print(f" The old middle point {x_old} and the new middel point {x_new} ")  
    #print(f" The different is {np.linalg.norm(x_old - x_new )}") 


    #print(f" The old middle point of original region {x_old} and the normalized region middel point {x_norm} ")  
    #print(f" The different is {np.linalg.norm(x_old - x_norm )}") 


    #print(f"Center point{x_new}")
    #print(f" Iterations {arr_x}")
    #print(f"Each slack tell how far we are from the boundary {constrain(Mat,x_new,b)}")
    #print(f" Minium slack tells how close a point are to the boundary {np.min(constrain(Mat, x_new, b))}") 

    plot_polyhedron(Mat,b,x_old,x_init)
    #plot_polyhedron(Mat,b_norm,x_norm)
    #plot_polyhedron(Mat_gam,b_gam,x_new)
    


    