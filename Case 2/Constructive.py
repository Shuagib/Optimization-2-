#from tabulate import tabulate
import math
from tabulate import tabulate
from roar_net_api.algorithms import greedy_construction
import random

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



class Solution:
    def __init__(self,problem):
        self.problem = problem
        self.team_list = [None] * problem.stud
        self.lookup = {t: [] for t in range(problem.team)}
        self.lb = 0


    def __str__(self):
        return f"\team_List: {self.team_List }\n\t   Look up students: {self.lookup}\n\t lower boubd: { self.low_bound}"
    
    def copy_solution(self):
        return Solution(self.problem)
    
    def objective_value(self):
        #Use the objective function evaluation 
        total = 0
        for i in self.lookup: #Loop over the teams 
            for id, w in enumerate(self.problem.weight): #Loop over weight both index and elem
                dis = set(self.problem.label[s][id] for s in self.lookup[i]) #Get  distinct values for each team
                total += w* len(dis) #Do Mutilication 
        return total
    
    def lower_bound(self):
        return -self.ub
    
    def save_solution(self, f):
        with open(f, "w") as file:
            file.write(" ".join(map(str, self.team_list)))
        

  

class AddMove:
    def __init__(self,stud,team,problem):
        self.stud = stud 
        self.team = team 
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

  