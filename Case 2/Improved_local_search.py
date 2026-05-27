#from tabulate import tabulate
import math
from tabulate import tabulate
from roar_net_api.algorithms import greedy_construction
import random
import time 

class Problem:
    def __init__(self,w:list[int],lb: list[list[int]], dis: list[tuple], team:int, stud:int, max_amount, min_amount):
        """specifies the data structure to represent the particular instance of the problem to solve"""
        self.weight = w #Weights
        self.label = lb #Label values lb[student][attribute]
        self.dis = dis #Disagreement between s_x and s_y (s_x,s_y)
        self.team = team #The amount of teams
        self.stud = stud #The amount of students
        self.max_amount = max_amount #Amount of Max size teams
        self.min_amount = min_amount # Amounf of Min size of teams


    
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


    def empty_solution(self): #Empty solution
        return Solution(self)
    
    def construction_neighbourhood(self): #All allowed moved in construction
        return AddNeighbourhood(self)
    
    def local_neighbourhood(self):#All allowed moved in swaps
        return LocalNeighbourhood(self)





class Solution:
    def __init__(self,problem):
        self.problem = problem
        self.team_list = [None] * problem.stud
        self.lookup = [[] for _ in range(problem.team)] #
        self.lb = 0
        num_attr = len(problem.label[0])
        self.team_labels = {
            t: [dict() for _ in range(num_attr)]
            for t in range(problem.team)
        }


    def __str__(self):
        return f"\team_List: {self.team_list }\n\t   Look up students: {self.lookup}\n\t lower boubd: { self.lower_bound}"
    
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
    
    def save_solution(self, f):
        with open(f, "w") as file:
            file.write(" ".join(map(str, self.team_list)))

    def cost_team(self,t):
        #Calculate the objective value for all students
        total = 0
        for id, w in enumerate(self.problem.weight): #Loop over weight both index and elem
            dis = set(self.problem.label[s][id] for s in self.lookup[t]) #Get  distinct values for each team
            total += w* len(dis) #Do Mutilication 
        return total
        

  

class AddMove:
    def __init__(self,stud,team,problem):
        self.stud = stud 
        self.team = team 
        self.problem = problem

    def __str__(self):
        return f"add node {self.stud} to Team {self.team}"


   
    def lower_bound_increment(self, solution):
        counts = solution.team_labels[self.team]      
        stud_lab =  self.problem.label[self.stud]
        lower_bound_incr = 0
        for a, label in enumerate(stud_lab):
            if counts[a].get(label, 0) == 0:          
                lower_bound_incr += self.problem.weight[a]        
        return lower_bound_incr
        
        


    def apply_move(self, solution):
        # 1. Update the objective tracker 
        solution.lb += self.lower_bound_increment(solution)
        
        # 2. Update label counts
        student_labels = self.problem.label[self.stud]
        for a, label in enumerate(student_labels):
            counts = solution.team_labels[self.team][a]
            counts[label] = counts.get(label, 0) + 1   # increment count
        
        # 3. Update lookup and team_list (your existing logic)
        solution.team_list[self.stud] = self.team
        solution.lookup[self.team].append(self.stud)
        return solution


class AddNeighbourhood:
    def __init__(self, Problem):
        self.problem = Problem

    def moves(self,solution):
        """A move is only valid if it forfill our constrains"""
        min_size = min(len(students) for students in solution.lookup)
        max_size = max(len(students) for students in solution.lookup)
        for s,team in enumerate(solution.team_list): #Iterate over teams 
            if team is None: #If there is None
                for t in range(len(solution.lookup)): #Loop over every student in the team 
                    if len(solution.lookup[t]) <= max_size and min_size == len(solution.lookup[t]): #Making sure the smallest team get filled first
                        for a,b in self.problem.dis: #Looking at par in disagreement
                            #print(self.problem.dis)
                            if  (s == a and b in solution.lookup[t]) or (s == b and a in solution.lookup[t]): 
                                break 
                        else:
                            yield AddMove(s, t, self.problem) 

        # print(solution.lookup.items())
        # print(solution.team_list)
        # print(self.problem.dis)
        # print(self.problem.max_amount)
        # print(self.problem.min_amount)
        # print(len(solution.lookup.keys())) #Amount of member

  
#===================================Local search ==================================================================

class LocalMove:
    def __init__(self,s1, s2, neighbourhood):
        self.s1 = s1
        self.s2 = s2  
        self.neighbourhood = neighbourhood
        self.ob_incr = 0
    
    def __str__(self):
        return f"Swap Student {self.s1} with Student {self.s2}"
    
   
    

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
            # t1: s1 leaves, s2 arrives
            if c1.get(l1, 0) == 1:  
                incr -= w           
            if c1.get(l2, 0) == 0:   # l2 new to t1
                incr += w
            # t2: s2 leaves, s1 arrives
            if c2.get(l2, 0) == 1:   # s2 is last holder of l2 in t2
                incr -= w
            if c2.get(l1, 0) == 0:   # l1 new to t2
                incr += w
        return incr

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


class LocalNeighbourhood:
    def __init__(self, problem):
        self.problem = problem

    def swap_conflict(self, s, students):
        """Checks if any two students has a disagreement when we shap"""
        for a, b in self.problem.dis:
            if (s == a and b in students) or (s == b and a in students):
                return True
        return False

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







#Greedy Algorithms
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
        print(f"best move: {best_move}")
        best_move.apply_move(s)
        #print(f"s: {s}\n")
    end_time = time.perf_counter()
    res_time = end_time - start_time
    return s, res_time


#Random
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





