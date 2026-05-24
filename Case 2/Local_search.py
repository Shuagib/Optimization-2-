
#from tabulate import tabulate
import math
from tabulate import tabulate
from roar_net_api.algorithms import greedy_construction
import random
import time 

class Problem:
    def __init__(self,w:list[int],lb: list[list[int]], dis: list[tuple], team:int, stud:int, max_amount, min_amount):
        self.weight = w #Weights
        self.label = lb #Label values lb[student][attribute]
        self.dis = dis #Disagreement between s_x and s_y (s_x,s_y)
        self.team = team #The amount of teams
        self.stud = stud #The amount of students
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
        self.team_list = [None] * problem.stud #List of teams indexed by student e.g. [1,1,0,3,2,0,1,2,3,3] each element is a team and each index is a student
        self.lookup = {t: [] for t in range(problem.team)} #Reverse version of team_list: a dictionary with team mapping to students team[0]: [4,2,5], team[1]: [1,3,0]
        self.lb = 0 #Lower bound increment


    def __str__(self):
        return f"\team_List: {self.team_list }\n\t   Look up students: {self.lookup}\n\t lower boubd: { self.lower_bound}"
    
    def copy_solution(self):
        new = Solution(self.problem)
        new.team_list = self.team_list.copy()
        new.lookup = {t: students.copy() for t, students in self.lookup.items()}
        
        return new

    
    def objective_value(self):
        """" Calculating the objective function """
        #Caluclate the objective value for all students
        total = 0
        for i in self.lookup: #Loop over the teams 
            for id, w in enumerate(self.problem.weight): #Loop over weight both index and element
                dis = set(self.problem.label[s][id] for s in self.lookup[i]) #Get  distinct values by computing it form labeel 
                total += w* len(dis) #Do Mutilication with each weight and dinstct in label list 
        return total
    
    def lower_bound(self):
        return -self.ub
    
    def save_solution(self, f):
        """ Saving our file for checker.py """
        with open(f, "w") as file:
            file.write(" ".join(map(str, self.team_list))) #Saving our solution files 

    def cost_team(self,t):
        """ Calcaulting the objective value for 1 team - Helper function in  LocalMove"""
        total = 0
        for id, w in enumerate(self.problem.weight): #Loop over weight both index and elem
            dis = set(self.problem.label[s][id] for s in self.lookup[t]) #Get  distinct values for each team
            total += w* len(dis) #Do Mutilication 
        return total
        

  

class AddMove:
    """ All student in each team"""
    def __init__(self,stud,team,problem):
        self.stud = stud  #student
        self.team = team #Team
        self.lb_incr = None #lower bound incremenentation
        self.problem = problem

    def __str__(self):
        return f"add node {self.stud} to Team {self.team}"


   
    def lower_bound_increment(self, solution):
            """ Lower bound measure affinity in each team. 
                If a affinity increases, then we add our lower bound"""
            if self.lb_incr is None:
                    self.lb_incr = 0
            for id, val in enumerate(self.problem.weight):
                dis = set(self.problem.label[s][id] for s in solution.lookup[self.team]) 
                if self.problem.label[self.stud][id] not in dis:
                    self.lb_incr += val 
            return self.lb_incr
    
    


    def apply_move(self, solution):
        solution.team_list[self.stud] = self.team #Adding a team to a list and index is the student
        solution.lookup[self.team].append(self.stud) #The key is the team and append students index to pair
        return solution 

class AddNeighbourhood:
    def __init__(self, Problem):
        self.problem = Problem

    def moves(self,solution):
        """A move is only valid if it forfill our constrains"""
        min_size = min(len(solution.lookup[k]) for k in solution.lookup)
        max_size = max(len(solution.lookup[k]) for k in solution.lookup)
        for s,team in enumerate(solution.team_list): #Iterate over teams 
            if team is None: #If there is None
                for t in solution.lookup: #Loop over every student in the team 
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

  


class LocalMove:
    def __init__(self,s1, s2, neighbourhood):
        self.s1 = s1
        self.s2 = s2  
        self.neighbourhood = neighbourhood
        self.ob_incr = 0
    
    def __str__(self):
        return f"Swap Student {self.s1} with Student {self.s2}"
    
   
    

    def objective_value_increment(self, solution):
        if self.ob_incr is 0:
            t1 = solution.team_list[self.s1]
            t2 = solution.team_list[self.s2]
            
            obj_before = solution.cost_team(t1) + solution.cost_team(t2)
            
            self.apply_move(solution)
            
            after = solution.cost_team(t1) + solution.cost_team(t2)
            
            self.apply_move(solution) 

            self.ob_incr  = after - obj_before
                    
            return  self.ob_incr 



    def apply_move(self, solution):
  
        t1 = solution.team_list[self.s1]
        t2 = solution.team_list[self.s2]
        

        solution.team_list[self.s2] = t1
        solution.team_list[self.s1] = t2
        

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
        teams = list(solution.lookup.keys())
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
    return s

#Use GASP aswell



def best_improvement(solution):
    p = solution.problem
    local_nb = p.local_neighbourhood()
    s = solution.copy_solution()
    
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
    return s





def geometric(temp, k):
    return temp * 0.99

def linear(temp, k):
    return temp - 5

def logarithmic(temp, k, temp0=1000):
    return temp0 / math.log(k + 2)



def simulated_annealing(problem, schedule, temp=5, inner=100, temp_min=0.01, time_limit=60):
    s = greedy_algorithm(problem)
    neigh = problem.local_neighbourhood()
    best = s.copy_solution()
    best_val = s.objective_value()
    
    start = time.time()
    k = 0
    while temp > temp_min and time.time() - start < time_limit:  
        for _ in range(inner):
            move = random.choice(list(neigh.moves(s)))
            delta = move.objective_value_increment(s)
            if delta < 0 or random.random() < math.exp(-delta / temp):
                move.apply_move(s)
                val = s.objective_value()
                if val < best_val:
                    best, best_val = s.copy_solution(), val
        k += 1
        temp = schedule(temp, k)
        
    return best


