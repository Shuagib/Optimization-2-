#from tabulate import tabulate
import math
from tabulate import tabulate
import numpy as np 

class Problem:
    def __init__(self,w:list[int],lb: list[list[int]], dis: tuple, team:int, stud:int):
        self.weight = w #Weights
        self.label = lb #Label values lb[student][attribute]
        self.dis = dis #Disagreement between s_x and s_y (s_x,s_y)
        self.team = team #The amount of teams
        self.stud = stud #The amount of students
        self.up_bound = 0 

    
    def __str__(self):
        return f" \t Learners {self.stud}, \t teams {self.team}, \t attributes{len(self.label[0])} \n weight {self.weight} \n labels {self.label}"

    def empty_solution(self):
        return Solution(self, [], {}, self.up_bound)
    
class Solution:
    def __init__(self,Problem):
        self.team_List = list[int] #A list of teams and where each team is assigned 
        self.lookup = dict[int,list[int]] #A dictionary where teams are key and students are pairs 
        self.ub = 0
        self.Problem = Problem


    def __str__(self):
        return f"\team_List: {self.team_List }\n\t   Look up students: {self.lookup}\n\t lower boubd: { self.low_bound}"
    
    def copy_solution(self):
        return Solution(self.problem, self.team_List.copy(), self.lookup.copy(), self.ub)
    
    def objective_value(self):
        #Use the objective function evaluation 
        total = 0
        for i in self.lookup: #Loop over the teams 
            for id, w in enumerate(self.w): #Loop over weight both index and elem
                dis = set(self.label[s][id] for s in self.lookup[i]) #Get  distinct values for each team
                total += w* len(dis) #Do Mutilication 
        return total
    
    def lower_bound(self):
        return -self.ub
  

class AddMove:
    def __init__(self,stud,team):
        self.stud = stud 
        self.team = team 
        self.lb_incr = None #lower bound 


class AddNeighbourhood:
    def __init__(self, Problem):
        self.problem = Problem
    
    def moves(self,Solution):
        Solution.

        

