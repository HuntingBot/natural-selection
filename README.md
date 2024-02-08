# Natural Selection Simulation

Simulates an evolving set of strategy playing Iterative Prisoner's Dilemma.

The rules: If both side cooperate, they get 2 points each; If one of them betrays, it gets 3 points and the cooperating side gets -1 points; If both side betray, they get 1 point each. This process is repeated 100 times between the two players, so they can be more "clever" and choose their own strategy depending on the opponent's strategy.

## Strategy representation

The strategy is considered a decision tree. The first layer is the opponents' choice in the last round, the second layer is the opponents' choice the second-to-last round, etc.

In the program, it is represented as an integer or an array consisting of three strategies recursively. If the strategy is an integer, it means to choose Cooperate (`0`) or Betray (`1`) this round. If it is an array of three elements and is at depth *k*, 0th element represents "if the opponent cooperates the *k*-to-last round", the 1th represents "if the opponent betrays the *k*-to-last round", and 2th represents "if the *k*-to-last round does not exist".

For example, the strategy `0` always cooperates, the strategy `1` always betrays, the strategy `[0, 1, 0]` is the tit-for-tat strategy, the strategy `[0, [0, 1, 0], 1]` means to betray only in the first round or when the opponent betrayed twice in a row.

Some of the strategies may be the exact same thing. For example, `0` and `[0, 0, 0]` are exactly the same, and `[0, 1, [1, 1, 0]]` and `[0, 1, 0]` are exactly the same. But due to how the mutation function works, they may differ in evolution.

## Selection

The selection process is as follows. In each round, `tournament_length` matches are carried out, and the strategies are sorted according to the total points they have got in the match, the first `threshold` strategies survives and the rest does not survive.

Then the surviving strategies reproduces to keep the pool size stable. The offspring may mutate with a possibility of `mutation_rate`.
