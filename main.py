from Task_3 import * 
#Test objectuve function
import numpy as np

if __name__ == '__main__':
    gam = 10


    #Standard Matrix
    Mat = np.array([
    [1,0], 
    [0,1], 
    [-1,0], 
    [0,-1], 
    [1,1]])
    
    #Original b constrains vector
    b = np.array([1,1,1,1,1.5])
    
    #Gamma applied to row 5 on Matrix 
    Mat_gam = np.array([
        [1,0], 
        [0,1], 
        [-1,0], 
        [0,-1], 
        [gam*1,gam*1]])
    b_gam = np.array([1,1,1,1,gam*1.5]) 

    #Gamma applied to row 5 on vector 

    Mat_normalized = np.array([
        [1,0], 
        [0,1], 
        [-1,0], 
        [0,-1], 
        [1/1.5,1/1.5]])
    b_norm = np.array([1,1,1,1,1])




    x = np.array([0.0,0.0]) #Intia start 
    #x_init = x.copy()

    x_old, arr_x  = newton_method(func,x,Mat,b,50)
    x_new, arr_x = newton_method(func,x,Mat_gam,b_gam,50)
    x_norm, arr_x = newton_method(func,x,Mat_normalized,b_norm,50) 
   

    #=============== Calculating the different on Gamma and Original=================================================#
    #Newton method results original 
    print(f" The steps towards the end point {arr_x}  Centerpoint {x_old}")

    #Computing Newton method on scaled version
    print(f" The old middle point {x_old} and the new middel point {x_new} ")  

    # #Calculating the difference. 
    print(f" The different is {np.linalg.norm(x_old - x_new )}")

    # ============================= Normalization testing =======================================
    # print(f" The old middle point of original region {x_old} and the normalized region middel point {x_norm} ")  
    # print(f" The different is {np.linalg.norm(x_old - x_norm )}") 

    #===================== Trying to print the scaling of each row corresponding in A and b with respected gamma, to see if the center points differs=========
    for row in range(5):
        Mat_gam = Mat.copy()
        b_gam = b.copy()
        Mat_gam[row] = gam * Mat[row]
        b_gam[row]   = gam * b[row]
        
        x_new, _ = newton_method(func, x, Mat_gam, b_gam, 50)
        x_old ,_  = newton_method(func,x,Mat,b,50)

        # print(f"Current Matrix A {Mat_gam}")
        # print(f"Current Vector b  {b_gam}")
        # print(f"Scaling row {row+1} as { Mat_gam[row]} by gamma={gam}: x* = {x_new} and the old point is x*_old {x_old}")
        # print(f" The different is {np.linalg.norm(x_old - x_new )}") 


    #print(f"Center point{x_new}")
    #print(f" Iterations {arr_x}")


    #===================================================Slack===============================================
    # print(f"Each slack tell how far we are from the boundary {constrain(Mat,x_old,b)}")

    # print(f" Minium slack Original   {np.min(constrain(Mat, x_old, b))}")
    # print("""====================================================================================""")
    # print(f'gamma is {gam}')
    
    # print(f"Slack from scaling {constrain(Mat_gam,x_new,b_gam)}")

    # print(f" Miniums slack from scaling  {np.min(constrain(Mat_gam, x_new, b_gam))}")

    #==========================================Plotting======================================================#
    #Original plot 
    #plot_polyhedron(Mat,b,x_old)
    #Normalize plot 
    #plot_polyhedron(Mat_normalized,b_norm,x_norm)
    #Gamma PLot
    plot_polyhedron(Mat_gam,b_gam,x_new)
    
    


    