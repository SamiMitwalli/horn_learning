#!/usr/bin/env python3

import itertools

from base import HornClause, HornFormula, Example, true, false, intersect, covers, violates, gen_clauses

def horn(target: HornFormula) -> HornFormula:
    S = []
    H = HornFormula([])
    while(True):
        print(f"Current hypothesis: {H}")
        equal, counter = target.is_equivalent(H)
        if equal:
            print("Success!!!")
            return H
        else:
            if not H.is_member(counter): # is a positive counter example
                print(f"Positive counter example: {counter}")
                print(f"Remove violating clauses from H: {H}")
                H.clauses = list(itertools.filterfalse(lambda c: violates(counter, c), H.clauses)) # remove from H every clause that x violates
                print("Eliminating incorrect clauses...")
                print(f"New H: {H}")
            else: # is a negative counter example
                print(f"Negative counter example: {counter}")
                refined = False
                for i, s in enumerate(S):
                    print(f"Try refining counter example s: {s}")
                    intersected = intersect(s, counter)
                    isSubset = true(intersected).issubset(true(s))
                    isSuperset = true(intersected).issuperset(true(s));
                    isEquivalent = isSubset & isSuperset
                    print(f"Create intersect: {intersected}")
                    if not isEquivalent:
                        print(f"Check if intersected example is refined counter example for s...")
                        if not target.is_member(intersected):
                            print(f"Intersect is a refined negative counter example (false for target '{target}'). Replacing s.")
                            print(f"Replacing counter example in S: {S} ...")
                            S[i] = intersected # refine with the intersection
                            print(f"Replaced counter example in S: {S}")
                            refined = True
                            break
                        else: 
                            print(f"Intersect is a positive counter example (true for target), i.e. no refinement.")
                    else:
                        print(f"Intersect and counter example s is same.")
                if not refined:
                    S.append(counter)
                    print(f"Adding counter example to S: {S}")
                H.clauses = gen_clauses(S) # regenerate H
            print("") # newline


if __name__ == "__main__":
    testClause1 = HornClause(["a", "b"], "d")
    testClause2 = HornClause(["a"], "c")
    testFormula = HornFormula([testClause1, testClause2])

    print(f"Target formula: {testFormula}\n")

    horn(testFormula)

    #print(testFormula.is_member("1110"))
    #print(testFormula.is_equivalent(HornFormula([testClause1])))