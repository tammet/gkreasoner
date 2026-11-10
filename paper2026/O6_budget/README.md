# O6: the time budget

This part reproduces the paragraph "The time budget" of Section 7.4 of the
paper. gk's recursive method stops its searches at a deadline, 10 s by
default. A longer deadline can move the value in either direction, because
new evidence may support or oppose. The paragraph gives three inputs, each
at two deadlines.

**Status of this part.** Each row keeps one search strategy and varies the
deadline. Every run of this part is marked `alone`: the run store ran it
on 2026-11-10 with no other run of the folder active, but other processes
of the machine were not controlled, so every value that depends on the
deadline comes from an uncontrolled run. The 2-s run of the delivery plan
has two stored repeats. The paper makes no measured claim about the
budget. The strategy is gk's automatic one, except for the
English case, which uses the strategy that the translation pipeline
stores.

## Files

```text
O6_budget/
  results.tsv  runs.tsv
  delivery/plan32.gkp
  grid/corner56.gkp
  berries/gk.js
  pipeline/axioms_std.js  strategy.json
```

| file | input | the same input in another part |
|---|---|---|
| `delivery/plan32.gkp` | the cold-chain delivery plan of 32 legs, the control plan: a persistence default over situation terms, one uncertain warming event per leg | part O3, the delivery family, the control plan of 32 legs |
| `grid/corner56.gkp` | the ProbLog corner grid of 56 edges: each edge a fact `0.5::edge`, two rules for `path`, the question from the corner at distance 4 | part O3, the ProbLog grids, the corner grid of 56 edges |
| `berries/gk.js` | "Does John eat berries?", the extraction of the English case N4 | part O7, `n4/gk.js` |
| `pipeline/axioms_std.js`, `pipeline/strategy.json` | the standard axioms and the stored strategy of the translation pipeline | part O7, `pipeline/` |

The files are copies of the files that were run. `berries/` and
`pipeline/` have the same places relative to each other as `n4/` and
`pipeline/` in part O7, so the commands of the two parts are the same.

## Rerun gk

From the repository root:

```sh
./bin/gk paper2026/O6_budget/delivery/plan32.gkp -seconds 2
./bin/gk paper2026/O6_budget/delivery/plan32.gkp
./bin/gk paper2026/O6_budget/grid/corner56.gkp
./bin/gk paper2026/O6_budget/grid/corner56.gkp -seconds 60
./bin/gk paper2026/O6_budget/pipeline/axioms_std.js \
  -strategy paper2026/O6_budget/pipeline/strategy.json -seconds 60 \
  paper2026/O6_budget/berries/gk.js \
  -defaults -confidence 0.1 -keepconfidence 0.1 -datafolder data -recursive
```

A command without `-seconds` uses the default deadline of 10 s. The English
case runs with `-seconds 10` and `-seconds 60`; part O7 explains its
options. Every row of `runs.tsv` is marked `alone`: the store runs it with
no other run active. The 60-s runs take about 40 s each.

## Results

| input | target | shorter deadline | longer deadline | what the added time found |
|---|---|---|---|---|
| delivery, 32 legs | .0294 | 2 s: .1760 | 10 s: .0294 | the exception searches of the remaining legs |
| "Does John eat berries?" | (0, .9801, 0, .0199), the tool on a ground abstraction | 10 s: (.98, 0, 0, .02), the opposition search stopped | 60 s: (.0004, .9608, .0192, .0196) | the strict clause against the eating default |
| corner grid, 56 edges | .5323 | 10 s: .181 | 60 s: .181 | nothing: gk finds the same proofs |

The targets: the delivery value is the hand value .9 × .9^32 × .95 =
.029358 (cold at the start, no warming on any of the 32 legs, the
handover), and ProbLog 2.3.0 gives .029357997 on the ProbLog encoding of
part O3. The grid target is ProbLog's value on its encoding in part O3; the
reference tool gives (.533, 0, 0, .467) there. The English target is the
tool's value on the ground abstraction `n4/mcref_ground.gkp` of part O7.

`results.tsv` writes each gk value with its four shares, for example
(.1760, 0, 0, .8240) for the paper's .1760.

**Delivery at 2 s.** gk spends the 2-s budget before the exception search
of every leg has run. A missed warming event leaves the persistence of that
leg unopposed, so the value lies above the target. At 10 s gk finds every
exception and returns the hand value. In the run of 2026-11-04, 82
applications entered the value at 2 s and 99 at 10 s. The 2-s value
depends on how many exception searches end within the budget, so it
changes from run to run. The three stored runs of gk 1.2.5 on 2026-11-10
(`plan32.gk.2s`, `.r2`, `.r3`) gave .2173 (80 applications) and .1956
twice (81 applications); three earlier check runs of that day gave .2173
twice and .1956 once, and gk 1.2.3, the version of the paper's run, also
gave .2173. So the paper's .1760 is one value of a range, and every 2-s
value lies above the target. Part O3 gives the 2-s values of
the other delivery plans.

**The English case.** At 10 s gk cuts the nested search for opposition to
the eating default, and the answer is on the for side. At 60 s the
opposition is found, and the value crosses to the against side, near the
target, with .0192 of conflict.

**The grid.** gk's initial search finds the same few proofs at both
deadlines, so the value stays at .181 against a target of .5323. Part O3
explains this limit: the search does not find the alternative derivations
of one ground question. The dated record has no saved output of the 60-s
run under the automatic strategy; the value .181 at 60 s rests on a memo
statement. A check run of gk 1.2.5 on 2026-11-10 gave (.1808, 0, 0, .8192)
at 60 s.

## Further rows of the appendix

The appendix's budget table also lists inputs that this part does not
rerun: the checkpoints of the Tweety example (part O1), the equipment input
with 16 components at 2 s and 10 s, the corner grid of 33 edges under the
strategy `hyper`, the tree of 364 nodes, Smokers with 16 and 20 persons,
the node `pc2prt` of Win95pts and the chain of 1,000 defaults (part O3).

## The controlled measurement: not done

A controlled measurement would run a fixed set of inputs with reference
values at 1, 10 and 60 s, with repetitions and one fixed strategy per
input. It would record the elapsed time, the applications found and
evaluated, the checkpoint displayed, the stop reason and the peak memory.
It would include inputs on which the value rises, falls and stays. No such
measurement was made. Part O2 measures one deadline only.

## Versions

The paper's values came from gk 1.2.3 on 2026-11-04. Every row of this part
names a stored run of gk 1.2.5 of 2026-11-10. These give the paper's values
on the 32-leg plan at 10 s, on the English case at 10 s and 60 s and on the
grid at 10 s and 60 s. At 2 s they give other values, as stated above.
