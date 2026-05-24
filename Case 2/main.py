from Local_search import * 
#from roar_net_api.algorithms import first_improvement, best_improvement
from roar_net_api.algorithms import greedy_construction
if __name__ == '__main__':

    

#================================ Testing Construction Heuristics ========================================#
# #=============================================SMALL FILES==============================================#
#     f_1 = open("tfp_13n_3q_4l_5u_3a_5d.txt")
#     p = Problem.from_textio(f_1)
#     f_1.close()
#     s = greedy_algorithm(p)
#     r = random_greedy(p)
#     w = greedy_construction(p)
#     s.save_solution("own_test_small.py")
#     r.save_solution("own_test_rand_small.py")
#     w.save_solution("roar-api_test.py")
#     print("""=======================================================================================================""")
#     print(f""" \t Small File  \t  \n # 13 tmembers, 3 teams, 3 attributes, 5 disagreements, 4 to 5 tmembers per team
#     \n 13 3 3 5 4 5""")
#     print(f"Objective value Greedy Algorithms: {s.objective_value()}")
#     print(f"Objective value Random Greedy Algorithm: {r.objective_value()}")
   


# #=============================================Medium File==============================================#
#     f_2 = open("tfp_131n_27q_4l_5u_10a_10d.txt")
#     p = Problem.from_textio(f_2)
#     f_2.close()
#     s = greedy_algorithm(p)
#     #r = random_greedy(p)
#     s.save_solution("medium.sol")
#     #r.save_solution("own_test_rand_medium.py")
#     print("""=======================================================================================================""")
#     print(f""" \t Medium File  \t  \n # 131 tmembers, 27 teams, 10 attributes, 10 disagreements, 4 to 5 tmembers per team
#     \n 100 90 80 70 60 50 40 30 20 10""")
#     print(f"Objective value Roar-net-Api: {s.objective_value()}")
#     #sprint(f"Objective value Random Greedy Algorithm: {r.objective_value()}")


# #=============================================Big File==============================================#
#     f_3 = open("tfp_300n_60q_5l_5u_10a_40d.txt")
#     p = Problem.from_textio(f_3)
#     f_3.close()
#     s = greedy_algorithm(p)
#     r = random_greedy(p)
#     print("""=======================================================================================================""")
#     print(f""" \t Big File  \t  \n # 300 tmembers, 60 teams, 10 attributes, 40 disagreements, 5 to 5 tmembers per team
#     \n 300 60 10 40 5 5""")
#     print(f"Objective value Roar-net-Api: {s.objective_value()}")
#     print(f"Objective value Random Greedy Algorithm: {r.objective_value()}")


#================================ Testing Local search Heuristics ========================================#
    f_2 = open("tfp_131n_27q_4l_5u_10a_10d.txt")
    p = Problem.from_textio(f_2)
    f_2.close()
    g = greedy_algorithm(p)
    s = greedy_construction(p)    
    # improved = best_improvement(s)                
    # improved_value = improved.objective_value()
    #result_geo = simulated_annealing(p, geometric)
    print("""=======================================================================================================""")
    print(f""" \t Medium File  \t  \n # 131 tmembers, 27 teams, 10 attributes, 10 disagreements, 4 to 5 tmembers per team
    \n 100 90 80 70 60 50 40 30 20 10""")
    print(f"Objective Construction Roar Api: {s.objective_value()}")
    print(f"Objective Construction implemented: {g.objective_value()}")
    # print(f"Local Search Best improvement : {improved_value}")
    #print(f"Metaheuristic Improvement : {result_geo.objective_value()}")
  





#================================ Meta heuristics  ========================================#

