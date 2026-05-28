from Improved_local_search import * 
#from roar_net_api.algorithms import first_improvement, best_improvement
#from roar_net_api.algorithms import greedy_construction
import statistics, time

if __name__ == '__main__':

    

#================================ Testing Construction Heuristics ========================================#
#=============================================SMALL FILES==============================================#
    # f_1 = open("tfp_13n_3q_4l_5u_3a_5d.txt")
    # p = Problem.from_textio(f_1)
    # f_1.close()
    # #s,t = greedy_algorithm(p)
    # w, t = random_greedy(p)
    # w.save_solution("own_test_small.py")
    # print("""=======================================================================================================""")
    # print(f""" \t Small File  \t  \n # 13 tmembers, 3 teams, 3 attributes, 5 disagreements, 4 to 5 tmembers per team
    # \n 13 3 3 5 4 5""")
    # #print(f"Objective value Greedy Algorithms: {s.objective_value()}")
    # print(f"Objective value Greedy Algorithms: {w.objective_value()}")
    # print(f" The time is : {t}")
    



# #=============================================Medium File 1 ==============================================#
    # f_2 = open("tfp_131n_27q_4l_5u_10a_10d.txt")
    # p = Problem.from_textio(f_2)
    # f_2.close()
    # s,t = greedy_algorithm(p)
    # s.save_solution("own_test_medium.py")
    # print("""=======================================================================================================""")
    # print(f""" \t Medium File  \t  \n 131 tmembers, 27 teams, 10 attributes, 10 disagreements, 4 to 5 tmembers per team
    # \n131 27 10 10 4 5""")
    # print(f"Objective value Greedy Algorithms: {s.objective_value()}")
    # print(f" The time is : {t}")
    

# #=============================================Medium File 2 ==============================================#

    # f_3 = open("tfp_200n_40q_5l_5u_10a_15d.txt")
    # p = Problem.from_textio(f_3)
    # f_3.close()
    # s,t = greedy_algorithm(p)
    # s.save_solution("own_test_bigger_medium.py")
    # print("""=======================================================================================================""")
    # print(f""" \t Medium File  \t  \n 200 tmembers, 40 teams, 10 attributes, 15 disagreements, 5 to 5 tmembers per team
    # \n200 40 10 15 5 5""")
    # print(f"Objective value Greedy Algorithms: {s.objective_value()}")
    # print(f" The time is : {t}")
    



# #=============================================Big File==============================================#
    # f_3 = open("tfp_300n_60q_5l_5u_10a_40d.txt")
    # p = Problem.from_textio(f_3)
    # f_3.close()
    # s,t = greedy_algorithm(p)
    # s.save_solution("own_test_big.py")
    # print("""=======================================================================================================""")
    # print(f""" \t Big File  \t  \n # 300 tmembers, 60 teams, 10 attributes, 40 disagreements, 5 to 5 tmembers per team
    # \n 300 60 10 40 5 5""")
    # print(f"Objective value Roar-net-Api: {s.objective_value()}")
    # print(f" The time is : {t}")



#================== Testing Random Greedy #===================


    # f_1 = open("tfp_13n_3q_4l_5u_3a_5d.txt")
    # p = Problem.from_textio(f_1)
    # f_1.close()

    # results = []
    # times = []
    # for run in range(10):                        
    #     start = time.perf_counter()
    #     s = random_greedy(p)               
    #     elapsed = time.perf_counter() - start
    #     results.append(s.objective_value())
    #     times.append(elapsed)

    # print(f"Best:   {min(results)}")
    # print(f"Median: {statistics.median(results)}")
    # print(f"Avg time: {statistics.mean(times):.4f}s")



#================================ Testing Local search Heuristics ========================================#
    # f_2 = open("tfp_300n_60q_5l_5u_10a_40d.txt")
    # p = Problem.from_textio(f_2)
    # f_2.close()
    # g,t = greedy_algorithm(p)
    # first = first_improvement(g)
    # improved,t = best_improvement(g)                
    # improved_value = improved.objective_value()
    # first_value = first.objective_value()
    # print("""=======================================================================================================""")
    # print(f""" \t Medium File  \t  \n # 131 tmembers, 27 teams, 10 attributes, 10 disagreements, 4 to 5 tmembers per team
    # \n 100 90 80 70 60 50 40 30 20 10""")
    # print(f"Objective Construction Roar Api: {g.objective_value()}")
    # print(f"Local Search Best improvement : {improved_value}")
    # print(f"Local Search first improvement : {first_value}")



#================================ Testing Best Improvement Heuristics ========================================#
    # f_1 = open("tfp_13n_3q_4l_5u_3a_5d.txt")
    # p = Problem.from_textio(f_1)
    # f_1.close()
    # g_1 = greedy_algorithm(p)

    # results = []
    # times = []
    # for run in range(10):                        
    #     start = time.perf_counter()
    #     s = best_improvement(g_1)               
    #     elapsed = time.perf_counter() - start
    #     results.append(s.objective_value())
    #     times.append(elapsed)

    # print(f"Best:   {min(results)}")
    # print(f"Median: {statistics.median(results)}")
    # print(f"Avg time: {statistics.mean(times):.4f}s")


    # f_1 = open("tfp_131n_27q_4l_5u_10a_10d.txt")
    # p = Problem.from_textio(f_1)
    # f_1.close()
    # g_ = greedy_algorithm(p)

    # results = []
    # times = []
    # for run in range(10):                        
    #     start = time.perf_counter()
    #     s = best_improvement(g_)               
    #     elapsed = time.perf_counter() - start
    #     results.append(s.objective_value())
    #     times.append(elapsed)

    # print(f"Best:   {min(results)}")
    # print(f"Median: {statistics.median(results)}")
    # print(f"Avg time: {statistics.mean(times):.4f}s")


    # f_1 = open("tfp_200n_40q_5l_5u_10a_15d.txt")
    # p = Problem.from_textio(f_1)
    # f_1.close()
    # g_2 = greedy_algorithm(p)

    # results = []
    # times = []
    # for run in range(10):                        
    #     start = time.perf_counter()
    #     s = best_improvement(g_2)               
    #     elapsed = time.perf_counter() - start
    #     results.append(s.objective_value())
    #     times.append(elapsed)

    # print(f"Best:   {min(results)}")
    # print(f"Median: {statistics.median(results)}")
    # print(f"Avg time: {statistics.mean(times):.4f}s")


    # f_1 = open("tfp_300n_60q_5l_5u_10a_40d.txt")
    # p = Problem.from_textio(f_1)
    # f_1.close()
    # g_3 = greedy_algorithm(p)

    # results = []
    # times = []
    # for run in range(10):                        
    #     start = time.perf_counter()
    #     s = best_improvement(g_3)               
    #     elapsed = time.perf_counter() - start
    #     results.append(s.objective_value())
    #     times.append(elapsed)

    # print(f"Best:   {min(results)}")
    # print(f"Median: {statistics.median(results)}")
    # print(f"Avg time: {statistics.mean(times):.4f}s")




#================================ Testing First improvement Heuristics ========================================#

    f_1 = open("tfp_300n_60q_5l_5u_10a_40d.txt")
    p = Problem.from_textio(f_1)
    f_1.close()
    g = greedy_algorithm(p)

    results = []
    times = []
    for run in range(10):                        
        start = time.perf_counter()           
        elapsed = time.perf_counter() - start
        results.append(g.objective_value())
        times.append(elapsed)

    print(f"Best:   {min(results)}")
    print(f"Median: {statistics.median(results)}")
    print(f"Avg time: {statistics.mean(times):.4f}s")


    # f_1 =open("tfp_300n_60q_5l_5u_10a_40d.txt")
    # p = Problem.from_textio(f_1)
    # f_1.close()

    # results = []
    # times = []
    # for run in range(10):                        
    #     start = time.perf_counter()
    #     s = first_improvement(p)               
    #     elapsed = time.perf_counter() - start
    #     results.append(s.objective_value())
    #     times.append(elapsed)

    # print(f"Best:   {min(results)}")
    # print(f"Median: {statistics.median(results)}")
    # print(f"Avg time: {statistics.mean(times):.4f}s")


    # f_1 = open("tfp_200n_40q_5l_5u_10a_15d.txt")
    # p = Problem.from_textio(f_1)
    # f_1.close()

    # results = []
    # times = []
    # for run in range(10):                        
    #     start = time.perf_counter()
    #     s = first_improvement(p)               
    #     elapsed = time.perf_counter() - start
    #     results.append(s.objective_value())
    #     times.append(elapsed)

    # print(f"Best:   {min(results)}")
    # print(f"Median: {statistics.median(results)}")
    # print(f"Avg time: {statistics.mean(times):.4f}s")


    # f_1 = open("tfp_300n_60q_5l_5u_10a_40d.txt")
    # p = Problem.from_textio(f_1)
    # f_1.close()

    # results = []
    # times = []
    # for run in range(10):                        
    #     start = time.perf_counter()
    #     s = first_improvement(p)               
    #     elapsed = time.perf_counter() - start
    #     results.append(s.objective_value())
    #     times.append(elapsed)

    # print(f"Best:   {min(results)}")
    # print(f"Median: {statistics.median(results)}")
    # print(f"Avg time: {statistics.mean(times):.4f}s")




#================================ Meta heuristics  ========================================#


