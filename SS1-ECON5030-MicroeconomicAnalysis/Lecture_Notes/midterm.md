**midterm topics lecture 10/22/2026:**

overall class review:
> preferences (prefs, over state space S) -> is complete (define this), transitive (define this); will be on exam
> rationality axioms : allows us to represent preferences as a fxn; -> if S is finite, then you can represent prefs as a fxn w/ S -> R; x (pref) y <=> u(x) >= u(y)
> optimal choices = argmax (utility fxn)
> X <= R^L; -> continuous (prefs, x); then utility representation of (prefs, x) if complete, transitive, & continuous
> NOT ON MIDTERM: neoclassical demand
> expected utility: what is EU?; what extra assumption is required? -> ans(independence axiom, understand what this is)

> **game theory** (oh boy) -> normal form**** (will 100% ask us to tell him what the normal form is and we fail if we don't know lmao) 3 things: players strategies and payoffs. he asked us to drop out if we can't do it
> fundamental soln concepts in games all are based on/use the normal form.
> define, constructing the normal form
> nonsimultaneous game -> actions are the strategies
> sequentials -> my actions are the strategies, your actions are contingent on mine (strategies = complete, contingent plan for everything that I do) show that you know this via PS2 maybe?
> solution concepts; 3 types: dominant solvable (dominant strategies, design something to work as a game: make it simple so everyone has a dominant strategy), [rationalizable strategies (iterated deletion of strictly dominated strategies), nash equilibrium] <-based on assumptions about people in the game, RAT brutal, NE easy? NE always sits inside the set of rationalizable outcomes. 
> *know*: definition of NE
> finite strategies -> mixed strategy NE.
> ideas of efficiency (pareto) + equity in games in general
> nash equilibrium is generally not efficient or equitable based on whatever concept of equity is come up with
> **market games**: -> natural welfare concepts exist within mkt games (gains from trade for each individual); [consumers: consumer surplus (WTP - price); producers: producer surplus (price - WTS)] using TS (CS + PS) to evaluate welfare. Think deeper about what equity might mean, but TS provides a starting point.
> *pure exchange games*: games where there is no production; NE requires less than perfect int; games from trade is maximized as long as we do not have some form of "transation cost; > crime > scams (information problems) are the only things that get in the way of exchange being inefficient
> >> adding production: (2) how much each firm produces & (1) what each firm produces; focus on (2), using partial equilibrium models (looking at single industry); oligopolies games: underproduction -> make more gains from trade themselves (wanting to sell at high prices -> restrict quantities), the wrong firms are producing things, models from PS(3?) and we're expected to know how to solve those games (**a cournot example from the problem set will probably be on the exam**, there will NOT be an example on the Bertrand model); *know basic oligopoly game*
> >> steps of solving a cournot game: simultaneous game: normal form (players, actions/strategies (quantities), payoffs), then solve for NE. Solving for NE: in a continous cournot game, find the best response of each firm (in a finite game, dots = best responses), step 1: find ea player's best response fxn. For cournot: FOC = 0 -> solve.
```
feel free to fix this if it's inaccurate
ex. P(Q) = 100-Q
Q_i = Q - q_i
c(q_i) = 10q_i
Q = q1 + q2 + q3
NE  { 1, 2, 3 }
pi_i(q_i, Q_i) = (100 - q_i - Q_-i)q_i - 10q_i

step 1: dpi_i (since quadratic, concave) = 0
100 - 2q_i - Q_-i - 10 = 0
100 - 2(b_i)(Q_-i) - Q_-i - 10 = 0
b_i(Q_-i) = (90-Q_-i)/2
best response^
BR to BR (use properties of symmetry)

step 2: focus q_1^c = q_2^c = q_3^c = q_i^c
q^c = (90 - Q_-i^c)/2, Q_-i^c = 2q^c
q^c = 90/4

s3: finding all else in the model: plug it all in
Q^c = 3(90/4) = 270/4

s4: draw graph, intersect, efficient outcome, and Q^c outcome = (67.5 (quantity), 32.5 (price))
> draw the consumer, producer surplus, and deadweight loss <- define deadweight loss
```

**overall**: know the preference stuff (conceptually), know the definitions of things in game theory, construct NF of game, solve for NE, mkt games: know welfare concepts, equity, problems of exchange alone, what production adds, how to solve an oligopoly game (the biggest of the problems on the exam). No proofs (the part of preferences easier than PS1, more definition over proofs)
**grading**: long asf just show what u've learnt