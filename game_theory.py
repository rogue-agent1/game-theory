#!/usr/bin/env python3
"""Game theory solver — Nash equilibrium, minimax, dominant strategies."""
import sys

def dominant_strategy(payoff_matrix):
    rows, cols = len(payoff_matrix), len(payoff_matrix[0])
    p1_dom = None
    for i in range(rows):
        if all(all(payoff_matrix[i][j][0] >= payoff_matrix[k][j][0] for j in range(cols)) for k in range(rows)):
            p1_dom = i
    p2_dom = None
    for j in range(cols):
        if all(all(payoff_matrix[i][j][1] >= payoff_matrix[i][k][1] for i in range(rows)) for k in range(cols)):
            p2_dom = j
    return p1_dom, p2_dom

def pure_nash(payoff_matrix):
    rows, cols = len(payoff_matrix), len(payoff_matrix[0])
    equilibria = []
    for i in range(rows):
        for j in range(cols):
            p1_best = all(payoff_matrix[i][j][0] >= payoff_matrix[k][j][0] for k in range(rows))
            p2_best = all(payoff_matrix[i][j][1] >= payoff_matrix[i][k][1] for k in range(cols))
            if p1_best and p2_best: equilibria.append((i, j))
    return equilibria

def minimax(matrix):
    rows, cols = len(matrix), len(matrix[0])
    row_mins = [min(matrix[i][j] for j in range(cols)) for i in range(rows)]
    col_maxs = [max(matrix[i][j] for i in range(rows)) for j in range(cols)]
    maximin = max(row_mins); minimax_val = min(col_maxs)
    return {"maximin": maximin, "minimax": minimax_val, "saddle": maximin == minimax_val}

def main():
    if len(sys.argv) < 2: print("Usage: game_theory.py <demo|test>"); return
    if sys.argv[1] == "test":
        # Prisoner's dilemma
        pd = [[(3,3),(0,5)],[(5,0),(1,1)]]
        nash = pure_nash(pd); assert (1,1) in nash
        d1, d2 = dominant_strategy(pd); assert d1 == 1 and d2 == 1
        # Coordination game
        coord = [[(2,2),(0,0)],[(0,0),(1,1)]]
        nash2 = pure_nash(coord); assert (0,0) in nash2 and (1,1) in nash2
        # Zero-sum minimax
        zs = [[3,2,5],[4,1,6],[2,3,4]]
        mm = minimax(zs); assert mm["maximin"] == 2; assert mm["minimax"] == 3
        print("All tests passed!")
    else:
        pd = [[(3,3),(0,5)],[(5,0),(1,1)]]
        print(f"Nash: {pure_nash(pd)}"); print(f"Dominant: {dominant_strategy(pd)}")

if __name__ == "__main__": main()
