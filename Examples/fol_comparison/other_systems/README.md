# First-order runs in other reasoners

These runs use the three classical clause problems without probabilities,
defaults, finite-domain bounds, or function-depth bounds.

## Translation

[`../tptp_cnf_to_asp.py`](../tptp_cnf_to_asp.py) maps an equality-free clause

```text
P1 | P2 | ~N1 | ~N2
```

to the disjunctive rule

```prolog
P1 | P2 :- N1, N2.
```

It also generates `term/1` rules for the complete Herbrand universe so that
ASP safety does not impose a finite set of terms. This produces
[`set_asp.lp`](set_asp.lp). Its recursive term rules are unbounded because the
source uses the witness functions `g/3`, `h/3`, `k/3`, and
`member_of_1_not_of_2/2`.

The converter stops on `nlp_query.p` and `dreadbury_safe_query.p`. Both use
first-order equality as a literal in non-Horn clauses. ASP equality is an
assignment or comparison operation; it cannot occur as a derived disjunct and
does not provide equality resolution or paramodulation. The two inputs are
therefore not translated to ASP.

[`../tptp_cnf_to_fof.py`](../tptp_cnf_to_fof.py) converts the clauses to
explicitly quantified FOF for the [TweetyProject](https://tweetyproject.org/)
parser. It applies only bijective symbol renamings. Signature comments let the
test harness declare the source arities before parsing nested function terms;
the comments do not add formulas to the problem.

## [ProbLog](https://dtai.cs.kuleuven.be/problog/editor.html)

ProbLog 2.2.10 accepted the surface syntax of `set_asp.lp` and returned:

```text
union(cDa,cDb,cD_aIb):  0
```

Its `ground` mode reduces the query to `union(cDa,cDb,cD_aIb) :- fail`.
This is not a countermodel to the set theorem. ProbLog models contain Prolog
clauses and probabilistic or annotated-disjunction choices; an unannotated
multi-atom classical clause is not a ProbLog rule head. There is consequently
no semantics-preserving ProbLog input for these non-Horn clause theories.

Command:

```sh
/tmp/gkreasoner-language-tools/problog-venv/bin/problog \
  Examples/fol_comparison/other_systems/set_asp.lp
```

## [PASTA](https://github.com/damianoazzolini/pasta)

PASTA 1.0.1 accepts ASP programs with probabilistic facts. It was run on
`set_asp.lp` without probabilistic
facts, asking for cautious support of the set-theory query. Grounding the
unbounded `term/1` closure reached the eight-second limit after using about
950 MiB resident memory; no probability interval was produced.

```sh
OPENBLAS_NUM_THREADS=1 timeout 8s bash -c 'ulimit -v 1572864
exec /tmp/gkreasoner-language-tools/pasta-venv/bin/pastasolver \
  Examples/fol_comparison/other_systems/set_asp.lp \
  --query="union(cDa,cDb,cD_aIb)"'
```

The NLP and Dreadbury equality clauses have no corresponding PASTA/ASP input,
for the reason given in the translation section.

## TweetyProject

`TweetyFolComparison.java` runs TweetyProject's TPTP parser and
`SimpleFolReasoner` on the generated `*_tweety.p` files.

With the 1.31 FOL library, the equality-free set input parses and
`SimpleFolReasoner` then reports that its Herbrand base is defined only for
signatures without functors. The NLP and Dreadbury inputs stop earlier:
`TPTPParser` treats a function occurring inside an equality literal as an
undeclared constant. Thus none of the three inputs reaches an entailment
result from the bundled reasoner.

```sh
javac -cp /tmp/gkreasoner-language-tools/tweety-fol.jar \
  -d /tmp/gkreasoner-language-tools/tweety-fol-classes \
  Examples/fol_comparison/other_systems/TweetyFolComparison.java

timeout 5s java -Xmx512m \
  -cp /tmp/gkreasoner-language-tools/tweety-fol.jar:/tmp/gkreasoner-language-tools/tweety-fol-classes \
  TweetyFolComparison Examples/fol_comparison/other_systems/set_tweety.p
```

## ASP systems

The same set translation was tried with
[clingo](https://potassco.org/clingo/) 5.6.2,
[DLV](https://www.dlvsystem.it/dlvsite/dlv/),
[I-DLV](https://github.com/DeMaCS-UNICAL/I-DLV) 1.1.6, and
[s(CASP)](https://github.com/JanWielemaker/sCASP) 1.1.4:

The DLV executable was the official legacy x86-64 static download. It does
not report a semantic version and had SHA-256
`e26fe0c89c329e68c5cfa7c719e25ad6adab7d07082461a8b47cd3400ee00c11`.
The I-DLV executable had SHA-256
`4fcf0dd01fae22b82e3b52a4421d3c5c0b2a377486450b6175d30b209ffec32a`.

| System | Result |
|---|---|
| clingo | grounding reached a 512 MiB address-space bound and reported `bad_alloc`; no model was produced |
| DLV | rejected the program because the recursive `term/1` rule does not guarantee termination |
| I-DLV | grounding reached the 512 MiB bound; no ground program was produced |
| s(CASP) | accepted the query but produced no answer within five seconds |

The clingo, DLV, and I-DLV results follow from full grounding of an infinite
Herbrand universe. s(CASP) does not ground the complete program, but
query-directed execution did not complete this clause encoding within the
bound.

Representative commands:

```sh
timeout 5s bash -c 'ulimit -v 524288
exec clingo Examples/fol_comparison/other_systems/set_clingo.lp \
  0 --enum-mode=cautious'

/tmp/gkreasoner-language-tools/dlv -n=1 -filter=union \
  Examples/fol_comparison/other_systems/set_asp.lp

timeout 5s bash -c 'ulimit -v 524288
exec /tmp/gkreasoner-language-tools/idlv --silent --filter=union/3 \
  Examples/fol_comparison/other_systems/set_asp.lp'

timeout 5s scasp -s 1 \
  Examples/fol_comparison/other_systems/set_scasp.pl
```

## Summary

NLP and Dreadbury did not reach proof search in the tested systems because of
their equality clauses. The set translation has an infinite Herbrand universe:
the grounders reached their limits, s(CASP) reached its time limit, ProbLog
used different clause semantics, and TweetyProject rejected function symbols.
