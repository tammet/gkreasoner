# System comparison examples

This directory contains small, executable comparisons with
[TweetyProject](https://tweetyproject.org/),
[PASTA](https://github.com/damianoazzolini/pasta), and
[I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV). The examples compare the
meaning of conclusions, not performance. Each example uses the native rules
of its formalism.

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

The PASTA values `0.8` and `0.3` agree with gk's
[`cumulate.js`](../confidences/cumulate.js) and
[`coin1.js`](../confidences/coin1.js), respectively. This agreement is limited
to these positive, independent-evidence cases. PASTA assigns probabilities to
possible worlds and then considers their stable models. gk combines evidence
found in first-order proofs and reports an assessment of support and conflict.

The Nixon results express the same ambiguity in three different result types:
two DeLP arguments remain undecided, PASTA reports the lower and upper
probability across stable models, and I-DLV with a solver enumerates the two
stable models. None is a numeric equivalent of gk's support calculation.

## TweetyProject inputs

`tweety_birds.rdl` uses a normal Reiter default. A strict `!Flies(opus)` fact
prevents the bird default from being applied to Opus. `tweety_birds.delp` uses
a defeasible bird rule and a more-specific defeasible penguin rule;
generalized specificity makes the penguin argument prevail.

`TweetyComparison.java` runs both formalisms and also queries the opposed
defaults in `tweety_nixon.delp`. With the self-contained TweetyProject 1.31
JARs, the captured output was:

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

The two downloaded JARs had these SHA-256 values:

```text
34f7602c725f9b27302717418450fd781a29493fa8d0dbcaf4110b2dfcab41a8  rdl
44c458eaa84cdf8dd3f6c6ec76660b1cf2ce158c9fdcd6a417f65a421f4e7465  delp
```

Reproduce the run from the repository root:

```sh
curl -fL https://tweetyproject.org/builds/1.31/org.tweetyproject.logics.rdl-1.31-with-dependencies.jar \
  -o /tmp/tweety-rdl.jar
curl -fL https://tweetyproject.org/builds/1.31/org.tweetyproject.arg.delp-1.31-with-dependencies.jar \
  -o /tmp/tweety-delp.jar
mkdir -p /tmp/tweety-classes
javac -cp /tmp/tweety-rdl.jar:/tmp/tweety-delp.jar \
  -d /tmp/tweety-classes Examples/system_comparison/TweetyComparison.java
java -cp /tmp/tweety-rdl.jar:/tmp/tweety-delp.jar:/tmp/tweety-classes \
  TweetyComparison \
  Examples/system_comparison/tweety_birds.rdl \
  Examples/system_comparison/tweety_birds.delp \
  Examples/system_comparison/tweety_nixon.delp
```

## PASTA inputs

`pasta_independent_support.lp` and `pasta_conjunctive_support.lp` isolate the
two ways independent probabilistic facts can support a query. The Nixon input
has no probabilistic facts; its interval comes from the two stable models of
the default conflict.

The runs used PASTA 1.0.1 at commit
`ba2a92b0ee4e66462d2be600fbf2d2a0b7db71e5`:

```sh
git clone https://github.com/damianoazzolini/pasta.git /tmp/pasta
python3 -m venv /tmp/pasta-venv
/tmp/pasta-venv/bin/pip install /tmp/pasta
/tmp/pasta-venv/bin/pastasolver \
  Examples/system_comparison/pasta_independent_support.lp --query=answer
/tmp/pasta-venv/bin/pastasolver \
  Examples/system_comparison/pasta_conjunctive_support.lp --query=answer
/tmp/pasta-venv/bin/pastasolver \
  Examples/system_comparison/pasta_nixon.lp --query='pacifist(nixon)'
/tmp/pasta-venv/bin/pastasolver \
  Examples/system_comparison/pasta_nixon.lp --query='nonpacifist(nixon)'
```

## I-DLV inputs

I-DLV can fully evaluate stratified Datalog programs and answer a supplied
query using Magic Sets. `idlv_birds.lp` is stratified and returns
`flies(tweety)`. It uses a separate `nonflies` predicate for the explicit
exception; in this example that predicate has the same blocker role as strong
negation because no rule can derive both conclusions.

The Nixon program is not stratified. I-DLV grounds it and clasp computes its
two stable models:

```text
quaker(nixon) republican(nixon) pacifist(nixon)
quaker(nixon) republican(nixon) nonpacifist(nixon)
```

The runs used I-DLV 1.1.6, whose Linux executable had SHA-256
`4fcf0dd01fae22b82e3b52a4421d3c5c0b2a377486450b6175d30b209ffec32a`:

```sh
curl -fL \
  https://github.com/DeMaCS-UNICAL/I-DLV/releases/download/1.1.6/idlv_1.1.6_linux_x86-64 \
  -o /tmp/idlv
chmod +x /tmp/idlv
/tmp/idlv --query --silent Examples/system_comparison/idlv_birds.lp
/tmp/idlv --silent Examples/system_comparison/idlv_nixon.lp | clasp 0
```

The larger query-focus measurements for I-DLV use the normalized workload in
[`../asp_comparison/`](../asp_comparison/README.md).
