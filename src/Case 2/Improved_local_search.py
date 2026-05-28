#from tabulate import tabulate
import math
from tabulate import tabulate
from roar_net_api.algorithms import greedy_construction
import random
import time 

class Problem:
    def __init__(self,w:list[int],lb: list[list[int]], dis: list[tuple], team:int, stud:int, max_amount, min_amount):
        """specifies the data structure to represent the particular instance of the problem to solve"""
        self.weight = w 
        self.label = lb
        self.dis = dis 
        self.team = team 
        self.stud = stud 
        self.max_amount = max_amount 
        self.min_amount = min_amount


    
    def __str__(self):
        return f" \t Learners {self.stud}, \t teams {self.team}, \t attributes{len(self.label[0])} \n weight {self.weight} \n labels {self.label}"
    
    @classmethod
    def from_textio(cls, f):
        lines = iter([l for l in f.readlines() if not l.startswith('#')])
        stud, team, attr, ndis, min_amount, max_amount = map(int, next(lines).split())
        weights = list(map(int, next(lines).split()))
        labels = [list(map(int, next(lines).split())) for _ in range(stud)]
        dis = [tuple(map(int, next(lines).split())) for _ in range(ndis)]
        return cls(weights, labels, dis, team, stud, max_amount, min_amount)


    def empty_solution(self): 
        return Solution(self)
    
    def construction_neighbourhood(self):
        return AddNeighbourhood(self)
    
    def local_neighbourhood(self):
        return LocalNeighbourhood(self)





class Solution:
    def __init__(self,problem):
        self.problem = problem
        self.team_list = [None] * problem.stud
        self.lookup = [[] for _ in range(problem.team)] 
        self.lb = 0
        num_attr = len(problem.label[0])
        self.team_labels = {
            t: [dict() for _ in range(num_attr)]
            for t in range(problem.team)
        }


    def __str__(self):
        return f"\team_List: {self.team_list }\n\t   Look up students: {self.lookup}\n\t lower bound: { self.lower_bound}"

#Copy a solution for the problem
    def copy_solution(self):
        new = Solution(self.problem)
        new.team_list = self.team_list.copy()
        new.lookup = [students.copy() for students in self.lookup]
        new.lb = self.lb
        new.team_labels = {
            t: [d.copy() for d in attrs]
            for t, attrs in self.team_labels.items()
        }
        return new
    
    def objective_value(self):
        return self.lb

    def lower_bound(self):
        return -self.ub
#Save current solution
    def save_solution(self, f):
        with open(f, "w") as file:
            file.write(" ".join(map(str, self.team_list)))

#Helper function to calcuate score of only one team
    def cost_team(self,t):
        total = 0
        for id, w in enumerate(self.problem.weight): 
            dis = set(self.problem.label[s][id] for s in self.lookup[t]) 
            total += w* len(dis) 
        return total
        

  

class AddMove:
    def __init__(self,stud,team,problem):
        self.stud = stud 
        self.team = team 
        self.problem = problem

    def __str__(self):
        return f"add node {self.stud} to Team {self.team}"


# Cost of adding this student to the team sums the weight of each
# attribute where the student introduces a label the team doesn't have yet. 
    def lower_bound_increment(self, solution):
        counts = solution.team_labels[self.team]      
        stud_lab =  self.problem.label[self.stud]
        lower_bound_incr = 0
        for a, label in enumerate(stud_lab):
            if counts[a].get(label, 0) == 0:          
                lower_bound_incr += self.problem.weight[a]        
        return lower_bound_incr
        
        

#Apply move 
#applying student to team and update the score between labels
    def apply_move(self, solution):
        solution.lb += self.lower_bound_increment(solution)
        
  
        student_labels = self.problem.label[self.stud]
        for a, label in enumerate(student_labels):
            counts = solution.team_labels[self.team][a]
            counts[label] = counts.get(label, 0) + 1  
        
 
        solution.team_list[self.stud] = self.team
        solution.lookup[self.team].append(self.stud)
        return solution


class AddNeighbourhood:
    def __init__(self, Problem):
        self.problem = Problem

#Applying all valid move for team construction
    def moves(self,solution):
      
        min_size = min(len(students) for students in solution.lookup)
        max_size = max(len(students) for students in solution.lookup)
        for s,team in enumerate(solution.team_list): 
            if team is None:
                for t in range(len(solution.lookup)):
                    if len(solution.lookup[t]) <= max_size and min_size == len(solution.lookup[t]): 
                        for a,b in self.problem.dis: 
                        
                            if  (s == a and b in solution.lookup[t]) or (s == b and a in solution.lookup[t]): 
                                break 
                        else:
                            yield AddMove(s, t, self.problem) 

        # print(solution.lookup.items())
        # print(solution.team_list)
        # print(self.problem.dis)
        # print(self.problem.max_amount)
        # print(self.problem.min_amount)
        # print(len(solution.lookup.keys())) 

  
#===================================Local search ==================================================================
#LocalMove
class LocalMove:
    def __init__(self,s1, s2, neighbourhood):
        self.s1 = s1
        self.s2 = s2  
        self.neighbourhood = neighbourhood
        self.ob_incr = 0
    
    def __str__(self):
        return f"Swap Student {self.s1} with Student {self.s2}"
    
   
    
#Evaluation function of a swap operation
#Student leave a team and their label counted for the team decrease (increment goes down)
#Student leave a team and their label counted for the team increase (increment goes go)
    def objective_value_increment(self, solution):
        t1 = solution.team_list[self.s1]
        t2 = solution.team_list[self.s2]
        s1_labels = solution.problem.label[self.s1]   
        s2_labels = solution.problem.label[self.s2]
        incr = 0
        for a in range(len(s1_labels)):
            l1 = s1_labels[a]  
            l2 = s2_labels[a]   
            w = solution.problem.weight[a]
            if l1 == l2:
                continue        
            c1 = solution.team_labels[t1][a]   
            c2 = solution.team_labels[t2][a]   
            if c1.get(l1, 0) == 1:  
                incr -= w           
            if c1.get(l2, 0) == 0:
                incr += w
         
            if c2.get(l2, 0) == 1:   
                incr -= w
            if c2.get(l1, 0) == 0:  
                incr += w
        return incr

#Swap operation and checkking if swap has increase or decrease affinity among teams 
# compute increment before updating counts. Increment measures change from current state.
    def apply_move(self, solution):                              
        solution.lb += self.objective_value_increment(solution)
        
        t1 = solution.team_list[self.s1]
        t2 = solution.team_list[self.s2]
        s1_labels = solution.problem.label[self.s1]             
        s2_labels = solution.problem.label[self.s2]             
        
        for a in range(len(s1_labels)):
            l1, l2 = s1_labels[a], s2_labels[a]
            c1 = solution.team_labels[t1][a]
            c2 = solution.team_labels[t2][a]
            c1[l1] -= 1
            if c1[l1] == 0: del c1[l1]
            c2[l2] -= 1
            if c2[l2] == 0: del c2[l2]
            c1[l2] = c1.get(l2, 0) + 1
            c2[l1] = c2.get(l1, 0) + 1
        
        solution.team_list[self.s1] = t2
        solution.team_list[self.s2] = t1
        solution.lookup[t1].remove(self.s1)
        solution.lookup[t2].append(self.s1)
        solution.lookup[t2].remove(self.s2)
        solution.lookup[t1].append(self.s2)
        return solution

#Local neighbhbourhood
class LocalNeighbourhood:
    def __init__(self, problem):
        self.problem = problem
#Helper function to detect disagreement
    def swap_conflict(self, s, students):
        for a, b in self.problem.dis:
            if (s == a and b in students) or (s == b and a in students):
                return True
        return False

#All valid swaps 
    def moves(self, solution):
        """ All the applied swappeds avaible for us """
        teams = list(range(len(solution.lookup)))
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                t1 = teams[i]
                t2 = teams[j]
                for s1 in solution.lookup[t1]:
                    for s2 in solution.lookup[t2]:
                        if self.swap_conflict(s1, solution.lookup[t2]) or  self.swap_conflict(s2, solution.lookup[t1]):
                            continue
                        yield LocalMove(s1, s2, self)




#=================================== Heuristics ==================================================================

#First improvement 
def first_improvement(solution):
    p = solution.problem
    local_nb = p.local_neighbourhood()
    s = solution.copy_solution()
    while True:
        improved = False
        for move in local_nb.moves(s):
            if move.objective_value_increment(s) < 0:
                move.apply_move(s)
                improved = True
                break             
        if not improved:
            break                  
    return s

#Greedy search
def greedy_algorithm(problem):
    constr_rule = problem.construction_neighbourhood()
    s = problem.empty_solution()
    start_time = time.perf_counter()
    while True:
        best_move, best_incr = None, math.inf
        moves = constr_rule.moves(s)
        for move in moves:
            incr = move.lower_bound_increment(s)
            if incr is not None and incr < best_incr:
                best_move, best_incr = move, incr
                if incr == 0:
                    break
        if best_move is None:
            break
        #print(f"best move: {best_move}")
        best_move.apply_move(s)
        #print(f"s: {s}\n")
    end_time = time.perf_counter()
    res_time = end_time - start_time
    return s

#Random Greedy search
def random_greedy(problem):
    constr_rule = problem.construction_neighbourhood()
    s = problem.empty_solution()
    while True:
        moves = list(constr_rule.moves(s))  
        if not moves:
            break
        move = random.choice(moves)       
        move.apply_move(s)
    return s

#Best improvement
def best_improvement(solution):
    p = solution.problem
    local_nb = p.local_neighbourhood()
    s = solution.copy_solution()
    start_time = time.time()
    while True:
        best_move, best_incr = None, math.inf
        for move in local_nb.moves(s):
            incr = move.objective_value_increment(s)
            if incr is not None and incr < best_incr:
                best_move, best_incr = move, incr
        if best_move is None or best_incr >= 0:
            break
        best_move.apply_move(s)
        print(f"best_incr: {best_incr}")
    end_time = time.time()
    res_time = end_time - start_time
    return s, res_time

#Scheduler simulated annealing 
def geometric(temp,k):
    return temp * 0.995

#Simulated annealing 
def simulated_annealing(problem, schedule=geometric, time_limit=60):
    s = greedy_algorithm(problem)
    neigh = problem.local_neighbourhood()

    best = s.copy_solution()
    best_val = s.objective_value()

    # Initial temperature
    typical_delta = s.objective_value() * 0.01 
    temp = -typical_delta / math.log(0.20)   
    temp_min = 0.01

    # Number of sampled moves per temperature level
    inner = max(100, problem.stud)
    
    start = time.time()
    k = 0

    while temp > temp_min and time.time() - start < time_limit:
        move_list = list(neigh.moves(s))
        if not move_list:
            break

        for _ in range(inner):
            if time.time() - start >= time_limit:
                break

            move = random.choice(move_list)   

            if s.team_list[move.s1] == s.team_list[move.s2]:
                continue

            delta = move.objective_value_increment(s)

            if delta < 0 or random.random() < math.exp(-delta / temp):
                move.apply_move(s) 
                val = s.objective_value()
                if val < best_val:
                    best, best_val = s.copy_solution(), val

        if s.objective_value() > best_val * 1.10:
            s = best.copy_solution()

        k += 1
        temp = schedule(temp, k)
            
    return best







