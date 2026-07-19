# First-order comparison candidates

These inputs were adapted from the
[GKC](https://github.com/tammet/gkc) example collection to identify
first-order problems that gk can solve before testing systems centered on
probabilistic or defeasible logic.

## Confirmed cases

`set.p` is a set-theory identity with union, intersection, difference,
extensional subset axioms, equality, and function terms used as witnesses.
GKC clausified the source `Examples/set.txt`; the original negated conjecture
was restored as the positive literal query required by gk.

```sh
./bin/gk Examples/fol_comparison/set.p -plain -nonegative -firstanswer \
  -seconds 30 -mbsize 1000 \
  -strategytext '{"strategy":["negative_pref","posunitpara"],"query_preference":1}'
```

gk reports `SZS status Theorem` and gives a 77-step resolution proof.

`blocks.gkp` is a blocks-world planning problem with situation terms, action
terms, frame axioms, explicit negative literals, and an unbounded query
variable. The source used `$ans(State)` directly. The adapted input derives
`goal(State)` and asks `query(goal(State))`, as required by gk's input
interface.

```sh
./bin/gk Examples/fol_comparison/blocks.gkp -plain -nonegative \
  -firstanswer -seconds 30 -mbsize 1000 \
  -strategytext '{"strategy":["hardness_pref"],"weight_select_ratio":100,"query_preference":0}'
```

gk returns this four-action situation term:

```text
do(putdown(c,b),do(pickup(c),do(putdown(b,a),do(pickup(b),s0))))
```

The set-theory and planning cases are the current candidates for comparison.
Both require unrestricted function terms and non-Horn clauses. The planning
case also asks the prover to construct a nested term rather than check a
finite list of proposed plans.

## Other inspected examples

GKC proves the original `nlp.txt`, `medicine.txt`, and `dreadbury.txt`
problems. Their conjectures were converted to gk queries and their FOF input
was clausified with GKC. The current gk binary did not complete these adapted
inputs: the quantified `nlp.txt` and `medicine.txt` conjectures need a fresh
literal wrapper because gk rejects explicit quantifiers in a question, and
the wrapped CNF inputs terminate with an internal `wg_decode_int` error.
The clausified Dreadbury query terminates with the same error. These three are
therefore not comparison candidates for the current gk binary.
