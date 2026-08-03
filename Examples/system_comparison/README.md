# System comparison examples

This directory contains small, executable comparisons with
[TweetyProject](https://tweetyproject.org/) 1.31,
[PASTA](https://github.com/damianoazzolini/pasta) 1.0.1, and
[I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV) 1.1.6. The examples compare
the meaning of conclusions; run times are measured in
[`../asp_comparison/`](../asp_comparison/README.md). Each example uses the
native rules of its formalism.

## Results

| Example | System and semantics | Result |
|---|---|---|
| one query with independent supports `0.5` and `0.6` | PASTA, credal probabilistic ASP | lower = upper = `0.8` |
| one proof requiring independent premises `0.5` and `0.6` | PASTA, credal probabilistic ASP | lower = upper = `0.3` |
| ordinary bird and explicit penguin exception | TweetyProject, Reiter default logic | one extension; Tweety flies, Opus does not |
| ordinary bird and more-specific penguin default | TweetyProject, DeLP with generalized specificity | Tweety flies; Opus does not |
| opposing Nixon defaults | TweetyProject, DeLP | both conclusions are `UNDECIDED` |
| opposing Nixon defaults | PASTA, credal semantics | each conclusion has interval `[0,1]` |
| opposing Nixon defaults | I-DLV plus [clasp](https://potassco.org/clasp/) | two stable models, one for each conclusion |
| bird default with an explicit penguin exception | I-DLV query answering | `flies(tweety)` |

The PASTA values `0.8` and `0.3` equal GK's
[`cumulate.js`](../confidences/cumulate.js) and
[`coin1.js`](../confidences/coin1.js) results. The agreement covers these
positive, independent-evidence cases. PASTA assigns probabilities to
possible worlds and then considers their stable models; GK combines
evidence found in first-order proofs and reports support and conflict.

The three Nixon outputs are of different kinds: DeLP leaves both opposed
arguments undecided; PASTA reports the interval `[0,1]` for each
conclusion across the two stable models; I-DLV with clasp enumerates the
two stable models. Their semantics differ, so the outputs are not one
common numeric quantity, and none corresponds numerically to GK's report
of pure ignorance for the same conflict.

## TweetyProject inputs

`tweety_birds.rdl` uses a normal Reiter default. A strict `!Flies(opus)`
fact prevents the bird default from being applied to Opus.
`tweety_birds.delp` uses a defeasible bird rule and a more-specific
defeasible penguin rule; generalized specificity makes the penguin
argument prevail.

`TweetyComparison.java` runs both formalisms and also queries the opposed
defaults in `tweety_nixon.delp`. With the TweetyProject 1.31 RDL and DeLP
libraries, the captured output was:

```text
RDL extensions=1
RDL Flies(tweety)   skeptical=true  credulous=true
RDL Flies(opus)     skeptical=false credulous=false
RDL !Flies(opus)    skeptical=true  credulous=true
DeLP Flies(tweety)           answer=The answer is: YES
DeLP ~Flies(tweety)          answer=The answer is: NO
DeLP Flies(opus)             answer=The answer is: NO
DeLP ~Flies(opus)            answer=The answer is: YES
DeLP pacifist(nixon)         answer=The answer is: UNDECIDED
DeLP ~pacifist(nixon)        answer=The answer is: UNDECIDED
```

Run it from the repository root, with `tweety-rdl.jar` and
`tweety-delp.jar` standing for the TweetyProject 1.31 libraries with
dependencies:

```sh
javac -cp tweety-rdl.jar:tweety-delp.jar \
  -d tweety-classes Examples/system_comparison/TweetyComparison.java
java -cp tweety-rdl.jar:tweety-delp.jar:tweety-classes \
  TweetyComparison \
  Examples/system_comparison/tweety_birds.rdl \
  Examples/system_comparison/tweety_birds.delp \
  Examples/system_comparison/tweety_nixon.delp
```

## PASTA inputs

`pasta_independent_support.lp` and `pasta_conjunctive_support.lp` isolate
the two ways independent probabilistic facts can support a query. The
Nixon input has no probabilistic facts; its interval comes from the two
stable models of the default conflict.

Run with the PASTA 1.0.1 solver, `pastasolver` standing for the installed
executable:

```sh
pastasolver Examples/system_comparison/pasta_independent_support.lp --query=answer
pastasolver Examples/system_comparison/pasta_conjunctive_support.lp --query=answer
pastasolver Examples/system_comparison/pasta_nixon.lp --query='pacifist(nixon)'
pastasolver Examples/system_comparison/pasta_nixon.lp --query='nonpacifist(nixon)'
```

## I-DLV inputs

I-DLV fully evaluates stratified Datalog programs and answers a supplied
query using Magic Sets. `idlv_birds.lp` is stratified and returns
`flies(tweety)`. It uses a separate `nonflies` predicate for the explicit
exception; in this example that predicate has the same blocker role as
strong negation because no rule can derive both conclusions.

The Nixon program is not stratified. I-DLV grounds it and clasp computes
its two stable models:

```text
quaker(nixon) republican(nixon) pacifist(nixon)
quaker(nixon) republican(nixon) nonpacifist(nixon)
```

Run with the I-DLV 1.1.6 executable, `idlv` standing for it:

```sh
idlv --query --silent Examples/system_comparison/idlv_birds.lp
idlv --silent Examples/system_comparison/idlv_nixon.lp | clasp 0
```

The larger query-focus measurements for I-DLV use the normalized workload
in [`../asp_comparison/`](../asp_comparison/README.md).
