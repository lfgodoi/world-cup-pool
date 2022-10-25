import pandas as pd
from sources.utils import generate_matches, estimate_results

class Simulator:

    # Initializing the simulator
    def __init__(self, groups):
        self.groups = groups
        self.content_group_stage = ""
        self.content_knockout = ""
        self.build_groups()

    # Building the result structure for the group stage
    def build_groups(self):
        self.group_results = {}
        for group_name in self.groups:
            self.group_results[group_name] = {}
            group = self.groups[group_name]
            for team_name in group:
                self.group_results[group_name][team_name] = {
                    "P": 0,
                    "W": 0,
                    "D": 0,
                    "L": 0,
                    "GD": 0,
                    "GS": 0
                }

    # Selecting teams qualified from the group stage        
    def select_qualified(self):
        self.round_16_results = {}        
        i = 0
        for group_name in self.group_results:
            group = pd.DataFrame(self.group_results[group_name]).transpose()
            group = group.sort_values(by=["P", "GD", "GS"], ascending=False)
            qualified = group.index[:2]
            self.round_16_results[i] = {"team": qualified[0], "power": self.groups[group_name][qualified[0]]}
            self.round_16_results[i+1] = {"team": qualified[1], "power": self.groups[group_name][qualified[1]]}
            i += 2

    # Iterating over every group to simulate the matches
    def run_group_stage(self):
        matches = generate_matches()
        for group_name in self.groups:
            self.content_group_stage += f"<h4>{group_name}</h4>"
            group = self.groups[group_name]
            team_names = list(group)
            for match in matches:
                team_a = team_names[match[0]]
                team_b = team_names[match[1]]
                a, b = estimate_results(group[team_a], group[team_b])
                self.content_group_stage += f"<p>{team_a} {a} x {b} {team_b}</p>"
                if a > b:
                    self.group_results[group_name][team_names[match[0]]]["W"] += 1 
                    self.group_results[group_name][team_names[match[1]]]["L"] += 1       
                    self.group_results[group_name][team_names[match[0]]]["P"] += 3
                    self.group_results[group_name][team_names[match[0]]]["GD"] += (a - b)
                    self.group_results[group_name][team_names[match[1]]]["GD"] += (b - a)
                elif a < b:
                    self.group_results[group_name][team_names[match[0]]]["L"] += 1
                    self.group_results[group_name][team_names[match[1]]]["W"] += 1
                    self.group_results[group_name][team_names[match[1]]]["P"] += 3
                    self.group_results[group_name][team_names[match[0]]]["GD"] += (a - b)
                    self.group_results[group_name][team_names[match[1]]]["GD"] += (b - a)
                else:
                    self.group_results[group_name][team_names[match[0]]]["D"] += 1
                    self.group_results[group_name][team_names[match[1]]]["D"] += 1
                    self.group_results[group_name][team_names[match[0]]]["P"] += 1
                    self.group_results[group_name][team_names[match[1]]]["P"] += 1
                self.group_results[group_name][team_names[match[0]]]["GS"] += a
                self.group_results[group_name][team_names[match[1]]]["GS"] += b
            self.content_group_stage += "<br>"
        self.select_qualified()

    # Algorithm for processing knockout stages
    def run_knockout(self, current_stage, matches, stage_name):
        self.content_knockout += "<br>"
        next_stage = current_stage.copy()
        self.content_knockout += f"<h4>{stage_name}</h4>"
        for match in matches:
            team_a = current_stage[match[0]]["team"]
            team_b = current_stage[match[1]]["team"]
            power_a = current_stage[match[0]]["power"]
            power_b = current_stage[match[1]]["power"]
            a, b = estimate_results(power_a, power_b)
            if a < b:
                self.content_knockout += f"<p>{team_a} {a} x {b} {team_b}</p>"
                next_stage.pop(match[0])
            elif b < a:
                self.content_knockout += f"<p>{team_a} {a} x {b} {team_b}</p>"
                next_stage.pop(match[1])    
            else:
                A = a
                B = b
                while a == b:
                    a, b = estimate_results(power_a, power_b, True)
                if a < b:
                    self.content_knockout += f"<p>{team_a} {a} x {b} {team_b}</p>"
                    next_stage.pop(match[0])
                elif b < a:
                    self.content_knockout += f"<p>{team_a} {A} ({a}) x ({b}) {B} {team_b}</p>"
                    next_stage.pop(match[1])
        return next_stage

    # Knockout stage - Round of 16
    def run_round_16(self):
        round_16_matches = [[0, 3], [1, 2], [4, 7], [5, 6], [8, 11], [9, 10], [12, 15], [13, 14]]
        self.quarter_finals_results = self.run_knockout(self.round_16_results, round_16_matches, "Round of 16")
            
    # Knockout stage - Quarter finals
    def run_quarter_finals(self):
        q = list(self.quarter_finals_results)
        quarter_finals_matches = [[q[0], q[1]], [q[2], q[3]], [q[4], q[5]], [q[6], q[7]]]   
        self.semifinals_results = self.run_knockout(self.quarter_finals_results, quarter_finals_matches, "Quarter Finals")
                
    # Knockout stage - Semifinals
    def run_semifinals(self):
        s = list(self.semifinals_results)
        semifinals_matches = [[s[0], s[1]], [s[2], s[3]]]   
        self.final_results = self.run_knockout(self.semifinals_results, semifinals_matches, "Semifinals")
                
    # Knockout stage - Final
    def run_final(self):
        f = list(self.final_results)
        final_match = [[f[0], f[1]]]  
        self.champion = self.run_knockout(self.final_results, final_match, "Final")
        self.content_knockout += "<br>"
        self.content_knockout += f"<h4>Champion</h4>"
        self.content_knockout += f"<p>{self.champion[list(self.champion)[0]]['team']}</p>"    