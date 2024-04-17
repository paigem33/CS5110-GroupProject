A* algorithm to find the shortest lest-cost path to destination
- We could, for now, make destination a range of squares along one edge of the grid. Players disappear once they reach the range, because that's like them exiting the stampede area??

simulation is stored as nodes in tables (OPEN table stored in smallest heap, binary heap to store... all the nodes??)

move players one at a time, each "round" every player moves once. Repeat the "rounds" however many times. (If players can exit, then perhaps repeat until players have all exited?)

Use segregation model as a jumping-off point :)

Each Player has these characteristics:
strength/weakness: int amount (determined by weight, take normal distribution of average weight of the population)
rational/irrational: t/f
optimism/pessimism: might be same as rational/irrational
step time: how long it takes them to walk somewhere

rationality is determined by crowd density p(o \leq p \leq 1), where p is the degree of panic. when p is higher than a certain value, people become irrational.

People are either optimistic or pessimistic. If optimistic, then the amount of crowd-press needed to make them irrational is higher. If optimism 

If the player is irrational, they will push.

If you're rational and other is irrational:
If they queue, you want to queue. If they push, you want to queue.

If you're irrational and other is rational:
If they queue, you want to push. If they push, you want to queue.

Normal form games:
2 v 2, 2 by 2:

decision is conditioned primarily on rationality vs irrationality, since even strong people don't push when they're rational. Second condition is strong vs week. In the final game, there are 12 types of game situations, all of which are laid out in Appendix 5.1 - 5.12

If a person falls and the person behind them is rational and doesn't trample them, then the fallen person gets back up again and continues to move. If the person falls and irrational people behind them trample them more than twice, they die.


They had 500 players. Changed rationality/irrationality distribution to be what they wanted using a var called the rational coefficient (between 0 and 1, with higher meaning more rational people).

TODO:
create player class
set up a* algorithm
put players in a 2D grid


Build off of existing code. You have to give credit, but you can totally find somebody else's code and use that :D

Why did they care? Point it in a direction of what to do next, what we would do if we had more time, what data that would take, what that would show.