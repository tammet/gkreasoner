# The recursive method's output

Since 1.2.0, gk answers a query with the recursive method by default. This
page describes what gk 1.2.5 prints: the `{"recursive": ...}` line with the
proofs of the answer, the dump that follows it, and the status facts in the
dump. What the four numbers of a
value mean is explained on examples in
[support_semantics.md](support_semantics.md).

## 1. The methods and the options

| command | method | output |
|---|---|---|
| `gk input` | the recursive method | the `{"recursive": ...}` line, then the dump |
| `gk input -recursive` | the same (an alias, kept for scripts) | the same |
| `gk input -direct` | the direct method of gk 1.1.2 | gk 1.1.2's result object, byte for byte |
| `gk input -audit` | the recursive method, and the direct method in a second process | the line, the dump, and an `{"audit": ...}` object with the direct method's result; each method gets half of `-seconds` |

- `-direct` cannot be combined with `-recursive` or `-audit`.
- These options keep the direct method, as in 1.1.2: `-plain`,
  `-rawproofs`, `-directed`, `-directiontrace` and `-dwdump`.
- An option that only the direct method reads also runs the direct method:
  `-legacy <mode>` (the older modes `olduncertainty`, `oldcumulate`,
  `oldposneg`, `envelope`, `stake=<f>`, `softblock`, `dwlegacy` and `dwopen`),
  `-detail`, `-outformat`, `-defworlds`, `-nocumulate`, `-nonegative`,
  `-nocheck`, `-blockerconfidence`, `-noconfsplit` and the `-dw` options
  (`-dwjoint`, `-dwjointcap`, `-dwcore`, `-dwsep`, `-dwnosep`, `-dwdirected`,
  `-dwproofs`). With `-recursive` or `-audit` the recursive method runs;
  `-audit` gives the option to its direct process.
- The options of the proof search apply to both methods: for example
  `-seconds`, `-strategy`, `-keepconfidence`, `-confidence`, `-maxproofs`,
  `-explore`, `-taxonomy` and `-defaults`.
- An input error gives the error object and exit 1 under both methods (for
  example a taxonomy priority without `-taxonomy`).
- These modes print something other than a query's result and do not run
  a method: `-clausify`, `-writejson`, `-dwcatalogue`,
  `-readkb`, `-deletekb`.
- With an attached knowledge base (`-usekb`) the recursive method runs as
  on one input file: its catalogue holds the knowledge base's
  clauses first, then the query's. `-readkb` keeps the written head of every
  rule and the catalogue fields of every clause for it. A knowledge base
  built by another gk version does not attach (`Existing segment header is
  incompatible`, exit 1): rebuild it with `-readkb`. A knowledge base
  without the written heads gives a `{"recursive": ...}` line with
  `"value": null` and writes `{"recursive_boundary":{"setting":"usekb",...}}`
  to stderr.
- `-fullproof` adds the sub-proofs of the nested searches to the proofs of
  the line (Section 3.1). Without it, a proof shows only its main structure.
- `-checkpoints DIR` writes the dump of every checkpoint into the folder
  DIR. The folder must exist: with a missing folder gk writes nothing and
  reports no error.
- Without `-outformat`, the recursive method prints JSON for every input
  language. The plain-text formats of GKP and TPTP input come with
  `-direct`, or with `-outformat`, which runs the direct method.
- The deadline is `-seconds` (default 10). The line's `budget_ms` is the
  recursive method's budget (9,000 ms at the default). A quarter of it is
  kept as a reserve for the evaluations; the nested searches stop when
  only the reserve is left (the fact `the budget`).

## 2. The method in short

1. gk's proof search runs on the query, as in 1.1.2, and keeps every
   derivation it finds.
2. Each derivation is replayed into applications: one per use of an input
   statement, with its conditions and its exceptions.
3. For every application, nested searches look for evidence of its
   conditions, for opposition to its conclusion and for its exceptions.
   Each nested search gets a smaller budget than the search that started
   it.
4. One evaluation over all applications gives four numbers for the
   question: (for, against, conflict, ignorance). They sum to 1. The
   evaluation computes them without sampling, by the rules of
   [support_semantics.md](support_semantics.md); Section 12 of that page
   says where gk's value can differ from the semantics.
5. The evaluation runs again at checkpoints, when the program has new
   applications. The line shows the value of the last completed
   evaluation.

## 3. The `{"recursive": ...}` line

One JSON object on one line, under the key `recursive`.

| key | meaning |
|---|---|
| `method` | `"recursive"` |
| `question` | the question literal in gk's JSON form, for example `["smokes","sam"]` or `["-flies","tweety"]`; left out for a question with variables |
| `value` | the four numbers (for, against, conflict, ignorance), rounded to 6 decimals; left out for a question with variables |
| `signed_confidence` | the for share minus the against share, rounded to 6 decimals; left out with `value` |
| `proof` | the proofs for and against the question and the proofs of their guards (Section 3.1); left out when there is none |
| `answers` | for a question with variables: one object per ground answer, with `answer` (the literal in JSON form), `value`, `signed_confidence`, `value_from` and `proof` |
| `value_from` | the checkpoint the value comes from, as `"checkpoint N"` |
| `value_model_version` | the model version that was evaluated for the value |
| `model_version`, `report_revision` | the last model version, and the revisions of the report since it |
| `evaluation` | present when the newest model version's evaluation did not complete: its state and the reason |
| `readings` | the evaluator's approximations applied to the value (Section 5) |
| `steps_not_represented` | the number of proof applications in the program (Section 4), when above 0 |
| `rounds` | the rounds of nested searches |
| `budget_ms`, `budget_used_ms` | the deadline and the time used |
| `tasks`, `tasks_cut`, `tasks_queued`, `tasks_that_cannot_run` | the nested searches: all, cut by their allowance, waiting, and those that cannot run |
| `applications` | the applications in the program |
| `pending_steps` | proof steps that are not yet applications |
| `loop_marks` | cycle marks (0 unless the strategy turns loop marks on) |
| `switches` | the settings of the recursive method that apply |
| `stop` | why the nested searches stopped |
| `search` | what the last search of the question reported |

A key whose value would be `null` is left out. Example
(`Examples/confidences/net_premise.js`), shortened:

```
{"recursive":{"method":"recursive","question":["flies","a"],"rounds":2,"tasks":4,
 "applications":3,"value":[0.27,0,0,0.73],"signed_confidence":0.27,
 "value_from":"checkpoint 2","proof":{"for":[...]},
 "stop":"no task can become runnable under a later allowance",
 "search":"no further proof found within the budget",...}}
```

### 3.1 The proofs

The field `proof` explains the value with classical resolution proofs. It
has up to three lists, and an empty list is left out:

- `for`: the proofs of the question, or of the answer;
- `against`: the proofs of its complement;
- `guards`: the proofs of the guards of the listed proofs. A guard is the
  literal of an exception, `unless(L, k)` (stored as a `$block` literal),
  that is left in the last clause of a proof for or against. The proof's
  `guard_of` names the listed proofs with that guard, for example
  `[["for",1]]`.

Each list holds each distinct proof once. A proof object has these keys:

| key | meaning |
|---|---|
| `proves` | the proved literal |
| `search` | the literal of the search that found the proof; present only when it differs from `proves` |
| `confidence` | the proof's confidence: the confidence of its last clause, rounded to 6 significant digits |
| `in_value` | `false` when gk made no application from the proof, so the value does not use it (for example a case analysis through a default); left out otherwise |
| `steps` | the resolution steps |
| `guard_of` | in `guards` only: the listed proofs that have the guard |
| `subproofs` | with `-fullproof` only: the proofs that the nested searches found |

The steps have the form of the direct method's proofs: `[n, label,
clause]`.

- `["in", name, role, confidence]` is an input clause. The role is `axiom`
  or `goal`. The goal named `taskgoal` is the goal of a nested search.
- `["mp", p1, p2, ..., "fromgoal", confidence]` is a resolution step
  (`"fromaxiom"` when no goal clause is among its ancestors). A parent
  `[3,1]` means literal 1 of step 3, counted from 0. `simp`, `=`,
  `arithinst` and `merge` are other steps.
- The clause is a list of literals in JSON form. `false` is the empty
  clause.
- An input step has a fourth element `{"head": k}` when the rule was written
  with literal k as its head and the usual reading picks another head. The
  usual reading takes the positive literals as the head, or the first
  negative literal when the clause has none. For example,
  `-flies(X) :- penguin(X), unless(flies(X), 3)` is stored as
  `[["$block",3,["flies","?:X"]],["-penguin","?:X"],["-flies","?:X"]]`,
  with `{"head":2}`.

**The default proof and `-fullproof`.** A default proof gives the main
structure of the reasoning: the steps by which gk's proof search derived the
literal. The nested searches can find sub-proofs for or against these steps:
evidence for a condition, opposition to a premise, or an exception. The value
counts the sub-proofs, but the default proof does not show them. `-fullproof`
adds them. Each proof gets `subproofs`: the proofs that the nested searches
of its input steps found, at every depth that the searches reached. The lists
`for`, `against` and `guards` are the same with and without `-fullproof`. A
subproof has the keys of a proof and these:

| key | meaning |
|---|---|
| `step` | the input step of the parent proof whose search found the subproof |
| `roles` | the roles of that search: `"opposition"`, a search for the complement of the step's literal, and `"further proofs"`, a search for more proofs of it |
| `listed_as` | for example `["against",1]`: the subproof is the first proof of the list `against`, so it is not repeated |
| `no_new_instances` | `true` when the subproof uses no input instance beyond the proofs above it |

Example: the Tweety input of the tutorial
(`Examples/semantics/tweety_3a_gull_rule.gkp`) has the value
(.6984, .224, 0, .0776). Its default proof against `flies(tweety)` has the
confidence .56: tweety is a penguin, because it is a seabird (.8) and not a
gull (.7). The against share is lower than .56 because a nested search found
a proof of `gull(tweety)` from the yellow bill (.432), which opposes the
not-gull premise. Only `-fullproof` shows that proof. The subproofs of
`proof.against[0]`, with their keys `step`, `roles`, `proves` and
`confidence`:

```
against #1: -flies(tweety), confidence 0.56, 9 steps
  step 1, further proofs: penguin(tweety), 0.56
    step 1, further proofs: seabird(tweety), 0.8
    step 1, opposition: gull(tweety), 0.432
      step 1, opposition and further proofs: -gull(tweety), 0.7
      step 1, further proofs: yellow_bill(tweety), 0.6
```

## 4. Proof applications

Some proof steps cannot be turned into applications: an arithmetic
instance, a case analysis through a default, a literal that was not
decoded. A proof of the question with such a step still enters the
program:

- a source event with the proof's confidence (gk's score of the proof);
- a certain application of the proved literal that has the source event
  as its condition and the proof's `$block` literals as its exceptions.

Its origin in the dump is `"proof not represented"`. Two proofs that use
the same uncertain input instances give one application; the more
confident proof gives its confidence. A proof whose evidence the program
already holds gives none. A case analysis whose exceptions include one of
its own case literals gives none, because one of its exceptions holds in
every case.

## 5. The status facts

The dump's `status_facts` object has two lists.

**`unfinished`: what the value does not include.**

| kind | meaning |
|---|---|
| `a cut task` | a nested search stopped at its allowance |
| `a queued task not run` | a nested search that the deadline did not reach |
| `a task that cannot run` | a nested search that cannot be made (`why` says why) |
| `a pending step` | a proof step that is not an application yet |
| `a step not represented` | a step of a proof that entered as a proof application; `application` names it, or is `null` when the proof gave no application |
| `an interrupted evaluation` | the newest model's evaluation did not complete; the value is an older model's |
| `the budget` | the budget above the evaluation reserve is spent |
| `a cap` | the limit on applications stopped a round |
| `a conditional form without a connection` | a conditional question with no route from its definition |
| `a conditional form's groundings capped` | not all groundings of a conditional question were read |
| `a refutation not read in a declared context` | a refutation of a conditional question with several antecedent sets |
| `the question's form was read from the clause heads` | the question's definition has several antecedent sets |
| `a variable class of the definition is ambiguous` | the definition's variables could not be matched to one class |
| `the question's form is not supported` | the question is not a literal or a supported definition |
| `a nested definition not supported` | a definition inside a definition |
| `an assumption conflict` | a literal assumed by a task and its complement assumed by a refutation; `count` says how often |
| `fresh constant prefix` | the input has constants of the form of gk's fresh constants, so a fresh constant can equal an input constant |

**`approximation`: what the value counts in a simplified way.** Each item
has `reading` and `by`.

| reading | meaning |
|---|---|
| `cycle cut` | a cycle across signs or through exception literals was cut to evaluate it: walking depth-first from the question atom, gk removes an application whose body literal leads back to an atom on the current path and drops such an exception literal; the semantics evaluates the cycle by the narrowing instead ([support_semantics.md](support_semantics.md) §9), and the two can differ |
| `context copies` | an atom read in several contexts got a copy per context |
| `taxonomy ignored` | a taxonomy rank is read as rank 0 |
| `rank zero as equal rank (decision 62)` | priority 0 is read as an equal rank |
| `an inconsistent antecedent context` | an antecedent context makes an atom certain in both signs (kind `the antecedent context is inconsistent`) |
| `a proof application with shared evidence` | a proof application shares input instances with the program or with another proof application, so they count twice (kind `a proof application shares input instances with the program`) |
| `residual variable represented by a fresh constant` | a variable that a proof left unbound is represented by a fresh constant (`by` is `importer`; `constants` names them); the semantics, which grounds over the input's constants, has no such instance |
| `self exception` | an application whose exception literal is one of its own body literals is not registered: it never applies (decision 68, gk 1.2.2); `applications` lists them. An exception that matches a body literal by binding only variables of the exception counts too; an exception that follows from the body through other rules does not. The `{"recursive": ...}` line lists the same applications in `readings` |

## 6. Version notes

- **1.2.5.** The line gives the proofs of the answer: the field `proof`
  (Section 3.1), and with `-fullproof` the nested sub-proofs. The
  question, the answers and the proved literals are literals in gk's JSON
  form: `["smokes","sam"]`, where 1.2.4 wrote the text `"smokes(sam)"`. The
  new key `signed_confidence` is the for share minus the against share.
  `value` and `signed_confidence` are rounded to 6 decimals. A key whose
  value would be `null` is left out: until 1.2.4 a question with variables
  had `"question":null` and `"value":null`. The values are unchanged.
- **1.2.4.** The recursive method runs on a shared-memory knowledge base
  (`-readkb`, then `-usekb`; Section 1). Until 1.2.3 such a query gave a
  line with `"value": null`. The other outputs of 1.2.3 are unchanged.
- **1.2.3.** The kind of a side (normal or ordinary) is decided in each
  world from the applications present in it: a side is normal when every
  present application is a normal default, ordinary when at least one is
  not ([support_semantics.md](support_semantics.md) §8). Until
  1.2.2 a side whose candidates mixed the two kinds was read as ordinary
  once, over the candidates (the reading `mixed kinds as ordinary`, now
  gone). On `bird(t). 0.3::-flies(t). 0.9::flies(X) :- bird(X),
  unless(-flies(X), 2). x(t). -x(t). 0.8::flies(t) :- x(t).` the rule
  through x(t) is present in no world, so the side stays normal and
  flies(t) is (.63, .3, 0, .07); 1.2.2 gave (.6, 0, .3, .1).
- **1.2.3.** An application with an exception literal on its own atom
  with the head's sign, `p :- b, unless(p, 0)`, never applies
  ([support_semantics.md](support_semantics.md) §8 and §9: a one-atom cycle
  through an exception literal, which the narrowing leaves undecided; the
  atom keeps only its other evidence). Until
  1.2.2 the exception was read as a veto by a copy of the atom (the reading
  `same-atom exception`, now gone): `0.5::b. p :- b, unless(p, 0).` gave
  (.5, 0, 0, .5) and now gives (0, 0, 0, 1). Decision 68 (an exception that
  is one of the application's own body literals) is unchanged.
- **1.2.2.** An application whose exception literal is one of its own body
  literals never applies (decision 68): for example, the orientation
  `-bird(o) <- -flies(o)` of the flat clause
  `[-bird(X), flies(X), $block(3, -flies(X))]` in
  `Examples/exceptions/penguin.js` is dropped, so "who is not a bird"
  gives ignorance for o; the reading `self exception` names the dropped
  applications.
- **1.2.2.** A signed exception literal inside `$block` (JSON input writes
  `-flies(X)` there without `$not`) is no longer registered as the record
  of its atom; before, the nested searches for that atom asked a doubly
  signed goal and found nothing, so a question with a variable could miss
  the opposition that the ground question finds.

## 7. The dump

After the line, gk prints the dump of the last checkpoint (format
`gk_dump_v1`). It holds the applications, the derivations, the nested
searches (`tasks`), the checkpoints, the status facts and the evaluation
(`value_c`). The format is described in gk's source documentation, which
this repository does not hold.
