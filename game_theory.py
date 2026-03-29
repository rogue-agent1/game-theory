#!/usr/bin/env python3
"""game_theory: Nash equilibrium finder for 2-player matrix games."""
import sys

def solve_2x2(payoff_a, payoff_b):
    """Find mixed strategy Nash equilibrium for 2x2 game."""
    a11,a12 = payoff_a[0]; a21,a22 = payoff_a[1]
    b11,b12 = payoff_b[0]; b21,b22 = payoff_b[1]
    # Player B's mix to make A indifferent
    denom_a = (a11 - a12 - a21 + a22)
    if abs(denom_a) < 1e-10:
        q = 0.5
    else:
        q = (a22 - a12) / denom_a
    q = max(0, min(1, q))
    # Player A's mix to make B indifferent
    denom_b = (b11 - b12 - b21 + b22)
    if abs(denom_b) < 1e-10:
        p = 0.5
    else:
        p = (b22 - b21) / denom_b
    p = max(0, min(1, p))
    return (p, 1-p), (q, 1-q)

def dominant_strategy(payoff):
    """Find dominant strategy if one exists."""
    rows = len(payoff)
    for i in range(rows):
        dominates_all = True
        for j in range(rows):
            if i == j: continue
            if not all(payoff[i][k] >= payoff[j][k] for k in range(len(payoff[0]))):
                dominates_all = False; break
        if dominates_all: return i
    return None

def expected_payoff(payoff, p, q):
    total = 0
    for i in range(len(payoff)):
        for j in range(len(payoff[0])):
            total += p[i] * q[j] * payoff[i][j]
    return total

def test():
    # Prisoner's Dilemma
    pd_a = [[-1,-3],[0,-2]]  # (C,C)=-1, (C,D)=-3, (D,C)=0, (D,D)=-2
    pd_b = [[-1,0],[-3,-2]]
    assert dominant_strategy(pd_a) == 1  # Defect dominates
    # Matching Pennies (no pure NE)
    mp_a = [[1,-1],[-1,1]]
    mp_b = [[-1,1],[1,-1]]
    p, q = solve_2x2(mp_a, mp_b)
    assert abs(p[0] - 0.5) < 0.01  # Mixed 50/50
    assert abs(q[0] - 0.5) < 0.01
    # Expected payoff at equilibrium
    ep = expected_payoff(mp_a, p, q)
    assert abs(ep) < 0.01  # Should be 0 at equilibrium
    # Battle of Sexes
    bos_a = [[3,0],[0,2]]
    bos_b = [[2,0],[0,3]]
    p2, q2 = solve_2x2(bos_a, bos_b)
    assert 0 <= p2[0] <= 1
    assert 0 <= q2[0] <= 1
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: game_theory.py test")
