# The recursive method's output

gk answers a query with one of three methods: **Exact**, the exhaustive
search (`gk -exact input`), **General**, the recursive method (`gk -general
input`), and **Auto**, the default (`gk input`, `gk -auto input`), which
combines them. This page describes what they print: the `{"recursive":
...}` line with the proofs of the answer, the dump that follows it with
`-dwdump`, and the status facts in the dump. Sections 2 to 6 describe General's line; Section 7
the keys of Exact and of Auto. What the four numbers of a
value mean is explained on examples in
[support_semantics.md](support_semantics.md).

## 1. The methods and the options

| command | method | output |
|---|---|---|
| `gk -exact input` | Exact, the exhaustive search (Section 7) | the line with the object `complete_mode`, then, with `-dwdump`, Exact's dump |
| `gk -exact -ground-first input` | an experiment: Exact over the full grounding (`GK_COMPLETE_GROUND=1`) | as Exact |
| `gk -exact -keyunified input` | experimental: Exact with general-prover assistance (Section 7.3) | as Exact, with `complete_mode.unified` |
| `gk -general input` | General, the recursive method | the `{"recursive": ...}` line, then, with `-dwdump`, the dump |
| `gk input`, `gk -auto input` | Auto: Exact first with half of `-seconds`, then General with the time left when Exact gives no answer (Section 7.5) | the line of the method that answered, with the field `policy`, then, with `-dwdump`, its dump |
| `gk input -audit` | General, and the direct method in a second process | the line, an `{"audit": ...}` object with the direct method's result, then, with `-dwdump`, General's dump; each method gets half of `-seconds` |
| `gk input -direct` | the legacy direct method of gk 1.1.2 ([direct_method.md](direct_method.md)) | gk 1.1.2's result object, byte for byte |

- Two options that select different methods are an error in either order.
- The `{"audit": ...}` object of `-audit` has the keys `method`
  (`"direct"`), `label` (the comparison label), `seconds` (the direct
  method's time limit), `deadline` (a sentence on that limit),
  `exit_status` (the direct process's exit status) and `direct` (the
  direct method's result as it printed it, as one string).
- `-eval125` alone runs General with the evaluation of gk 1.2.5, never Auto
  (`cli_reference.md`).
- `-direct` cannot be combined with `-auto`, `-general`, `-exact` or
  `-audit`.
- These options run the direct method: `-plain`,
  `-rawproofs`, `-directed` and `-directiontrace`.
- A General run (`-general`, `-recursive`, the General part of `-audit`, and
  Auto when it hands the query to General) ignores `-directed`, in either
  order of the options. The direct method's part of `-audit` uses it.
- `-dwdump` prints the dump of the method that answers after its line:
  `gk_dump_v1` for General (Section 6), `gk_key_dump_v1` for Exact
  (Section 7.2). Without `-dwdump` no dump is printed. `-dwdump` does not
  choose a method: `gk -dwdump input` runs Auto. The direct method has no
  dump: `-dwdump` with `-direct`, or with an option that runs the direct
  method, is an input error with exit 1.
- An option that only the direct method reads also runs the direct method:
  `-legacy <mode>` (the older modes `olduncertainty`, `oldcumulate`,
  `oldposneg`, `envelope`, `stake=<f>`, `softblock`, `dwlegacy` and `dwopen`),
  `-detail`, `-outformat`, `-defworlds`, `-nocumulate`, `-nonegative`,
  `-nocheck`, `-blockerconfidence`, `-noconfsplit` and the `-dw` options
  (`-dwjoint`, `-dwjointcap`, `-dwcore`, `-dwsep`, `-dwnosep`, `-dwdirected`,
  `-dwproofs`). With `-general` or `-audit` General runs;
  `-audit` gives the option to its direct process.
- The options of the proof search apply to General and the direct method: for example
  `-seconds`, `-strategy`, `-keepconfidence`, `-maxproofs`, `-explore`,
  `-taxonomy` and `-defaults`. `-confidence` filters only the answers of the
  direct method's report; the line of Auto, General and Exact does not
  change with it.
- An input error gives the error object and exit 1 under both methods (for
  example a taxonomy priority without `-taxonomy`).
- These modes print something other than a query's result and do not run
  a method: `-clausify`, `-writejson`, `-dwcatalogue`,
  `-readkb`, `-deletekb`.
- With an attached knowledge base (`-usekb`) General runs as on one input
  file (Auto sends such a query to General at once): its catalogue holds the knowledge base's
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
  DIR, with or without `-dwdump`. The folder must exist: with a missing
  folder gk writes nothing and reports no error.
- Without `-outformat`, every method prints JSON for every input
  language. The plain-text formats of GKP and TPTP input come with
  `-direct`, or with `-outformat`, which runs the direct method.
- The deadline is `-seconds` (default 10). The line's `budget_ms` is
  General's budget (9,000 ms at the default). A quarter of it is
  kept as a reserve for the evaluations; the nested searches stop when
  only the reserve is left (the fact `the budget`).

## 2. The methods in short

General, the recursive method:

1. gk's proof search runs on the query, as in the direct method, and keeps
   every derivation it finds.
2. Each derivation is replayed into applications: one per use of an input
   statement, with its conditions and its exceptions.
3. For every application, nested searches look for evidence of its
   conditions, for opposition to its conclusion and for its exceptions.
   Each nested search gets a smaller budget than the search that started
   it.
4. One evaluation over all applications gives four numbers for the
   question: (for, against, conflict, ignorance). They sum to 1, less the
   share `unresolved` that the narrowing leaves undecided (Section 3). The
   evaluation computes them without sampling, by the rules of
   [support_semantics.md](support_semantics.md); Section 10.5 of that page
   says where gk's value can differ from the semantics.
5. The evaluation runs again at checkpoints, when the program has new
   applications. The line shows the value of the last completed
   evaluation.

The schedules of the methods differ:

- **Exact** follows the dependencies of the question with resumable tasks,
  one per signed literal. In each round every open task continues with the
  same work allowance, 2,000 units at first and four times more each round.
  A task keeps its state between rounds. The aim is that every task ends;
  the allowances order the work. When every task ended and the evaluation
  gave a value, the answer is complete, and a larger time limit would not
  change it.
- **The full grounding** (`-exact -ground-first`) is a separate, experimental
  way for Exact to collect the evidence: it grounds every statement first and
  then searches the ground statements. Count limits bound it (500,000 ground
  statements, `GK_KEY_GROUND`).
- **The interleaved experiment** (`-exact -keyunified`) runs Exact's tasks and
  gk's general prover in turns. Each search keeps its own schedule: Exact's
  tasks their work allowances, the prover a time slot that doubles each
  round and halves with each step of distance from the question.
- **General** gives each nested search a time slot `L0 * 2^k * r^d` in round
  k at dependency depth d (50 ms, doubling each round, halving with each
  level of depth by default). A deeper search gets less time; the run stops
  when the budget above the reserve is spent.
- **Auto** runs Exact within half of the time limit (its collection until 0.6
  of that half), then General with the time left (Section 7.5).

## 3. The `{"recursive": ...}` line

One JSON object on one line, under the key `recursive`.

| key | meaning |
|---|---|
| `method` | `"recursive"` |
| `question` | the question literal in gk's JSON form, for example `["smokes","sam"]` or `["-flies","tweety"]`; left out for a question with variables |
| `value` | the four numbers (for, against, conflict, ignorance), rounded to 6 decimals; left out for a question with variables |
| `signed_confidence` | the for share minus the against share, rounded to 6 decimals; left out with `value` |
| `unresolved` | the share that the narrowing leaves undecided (Section 5, the reading `narrowing`); the four numbers of `value` sum to 1 − `unresolved`; also in each answer |
| `proof` | the proofs for and against the question and the proofs of their guards (Section 3.1); left out when there is none |
| `answers` | for a question with variables: one object per ground answer, with `answer` (the literal in JSON form), `value`, `signed_confidence`, `unresolved`, `value_from` and `proof` |
| `value_from` | the checkpoint the value comes from, as `"checkpoint N"` |
| `value_model_version` | the model version that was evaluated for the value |
| `model_version`, `report_revision` | the last model version, and the revisions of the report since it |
| `evaluation` | present when the newest model version's evaluation did not complete: `model_version`, `state` (`interrupted`), `why` (the kind of stop, for example `block allowance`) and `detail` (the stop as a sentence) |
| `readings` | the evaluator's approximations applied to the value (Section 5) |
| `steps_not_represented` | the number of proof applications in the program (Section 4), when above 0 |
| `rounds` | the rounds of nested searches |
| `budget_ms`, `budget_used_ms` | the deadline and the time used |
| `tasks`, `tasks_cut`, `tasks_queued`, `tasks_that_cannot_run` | the nested searches: all, cut by their allowance, waiting, and those that cannot run |
| `applications` | the applications in the program |
| `pending_steps` | proof steps that are not yet applications |
| `loop_marks` | always 0; gk keeps the key for the format of the line |
| `switches` | the settings of the recursive method that apply |
| `stop` | why the nested searches stopped |
| `search` | what the last search of the question reported |
| `unfinished`, `approximation` | only when the recursion did not run, for example for a question with variables without a proof: the status facts of Section 5 (`["a question with variables: the recursion did not run"]`) |

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

The dump's `status_facts` object has three lists: `unfinished`,
`approximation` and `searches`.

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
| `direction` | `count` proofs used an uncertain rule, or a rule with an exception, for a literal other than its head; such a rule enters a proof only towards its written head, so such a proof gives no proof application, and that literal is decided at its own atom |

**`approximation`: what the value counts in a simplified way.** Each item
has `reading` and `by`.

| reading | meaning |
|---|---|
| `cycle cut` | a cycle across signs or through exception literals was cut to evaluate it: walking depth-first from the question atom, gk removes an application whose body literal leads back to an atom on the current path and drops such an exception literal; gk does this only for a cyclic group too large for the narrowing, which the semantics uses ([support_semantics.md](support_semantics.md) §7.2, §10.5), and the two can differ |
| `context copies` | an atom read in several contexts got a copy per context |
| `taxonomy ignored` | a taxonomy rank is read as rank 0, where the evaluator cannot decide whether the rank is allowed in the context of an exception check; elsewhere the evaluator compares taxonomy ranks by specificity |
| `rank zero as equal rank` | priority 0 is read as an equal rank |
| `an inconsistent antecedent context` | an antecedent context makes an atom certain in both signs (kind `the antecedent context is inconsistent`) |
| `a proof application with shared evidence` | a proof application shares input instances with the program or with another proof application, so they count twice (kind `a proof application shares input instances with the program`) |
| `residual variable represented by a fresh constant` | a variable that a proof left unbound is represented by a fresh constant (`by` is `importer`; `constants` names them); the semantics, which grounds over the input's constants, has no such instance |
| `no self-support` | applications that no self-support left out of the evaluation: a body literal of such an application can be derived only through applications with the application's own head literal; `detail` gives the count |
| `narrowing` | a group of atoms in a cycle was evaluated by the narrowing ([support_semantics.md](support_semantics.md) §7.2); `atoms` lists the group's atoms as JSON literals. With a cycle across signs, an atom that the narrowing leaves undecided is unresolved (the share `unresolved` of the line); without one, it is in ignorance |
| `backbone` | in the group named by `detail`, the exception pass removed an application with an exception literal in some cells of the evaluation, and restored it in some |
| `backbone approximation` | in the exception pass of a group, an atom outside the group was read in its final state in the first pass, where the semantics reads its first-pass state; the two can differ when that atom's evidence holds an application with an exception literal or a normal default; `detail` names the group and the atom. The exact method marks such an answer not complete ([support_semantics.md](support_semantics.md) §10.5) |
| `blocked-rule repair` | in the group named by `detail`, applications that rest on held-out or removed applications were left out in some cells: no self-support and the rule for a body that can never hold were applied again without them |
| `clause rule in a circle` | in some cells of a group that holds a listed clause of a proof, the listed clause is contradicted only while its own proof applies, or a check cannot be decided; the group's atoms whose state differs between the evaluations get no value there |
| `self exception` | an application whose exception literal is one of its own body literals is not registered: it never applies; `applications` lists them. An exception that matches a body literal by binding only variables of the exception counts too; an exception that follows from the body through other rules does not. The `{"recursive": ...}` line lists the same applications in `readings` |

**`searches`: the searches that gk made beyond the proof search and the
nested searches.** The value does not lack them.

| kind | meaning |
|---|---|
| `further searches` | a found proof used contested statements, and gk searched its literal again without them; `count` is the number of such searches and `left_out_clauses` the clauses left out of them. With an attached knowledge base no further search is made, and `why` says so |

The line's `readings` lists the readings of the evaluation as pairs
`[reading, detail]`. The reading `search again` is in the line
only: the limit of further searches of a literal (the strategy key
`recursive_search_again`) was reached.

## 6. The dump

With `-dwdump`, gk prints the dump of the last checkpoint after the line
(format `gk_dump_v1`). Without `-dwdump` no dump is printed. It holds the applications, the derivations, the nested
searches (`tasks`), the checkpoints, the status facts and the evaluation
(`value_c`). The format is described in gk's source documentation, which
this repository does not hold.

## 7. Exact (`-exact`)

With `-exact`, gk computes the value of the support semantics without a
budget of nested searches: a search of the applications by first-order
resolution, or with `-ground-first` by a ground search, then one evaluation
of all applications. The line has the form of Section 3. Exact's own fields
are in one object, `complete_mode`.

| key | meaning |
|---|---|
| `question`, `value`, `signed_confidence`, `unresolved`, `readings`, `proof` | as in Section 3; `value` is the value of the question's literal; a key without a value is left out |
| `reading_atoms` | the atoms that a reading names, `[{"reading": i, "atoms": [literals]}]`, beside `readings` |
| `answers` | for a question with variables: per answer `answer`, `value`, `signed_confidence`, `unresolved`, `complete`, `limits` (when there are some), `readings`, `reading_atoms`, `proof`; no top-level `question` and `value` |
| `applications`, `budget_ms`, `budget_used_ms` | as in Section 3 |
| `complete_mode` | `version`, `covered`, `not_covered`, `complete`, `limits`, `join_limit`, `search` (`first-order resolution`, `class 1, binding by data`, `class 2, binding by data` or `ground`), `class`, how the tasks of the search ended (`tasks`, `tasks_ended`, `tasks_at_limit`, `tasks_closed`, `tasks_by_ground_search`, `tasks_single_applications_only`), the counts of the search and of the input, `collection_ms`, `evaluation_ms`, and `proofs` (below) |

**An input that Exact does not cover** gets no value and no proof.
`complete_mode.not_covered` names the cause and the statement:
`{"reason": "an equality between terms", "statement": "frm_3", "line": 4,
"file": "ex/cs13.gkp", "text": "an equality between terms, in the
statement frm_3 on line 4 of ex/cs13.gkp. Exact gives no value for it; gk
-general FILE (or gk -auto FILE, the default) gives a budgeted estimate."}`.
Under Exact gk never prints a value of another method. A run that ended its own evaluation and is not complete keeps its
value, with `"complete": false` and the limits.

**The limits.** Each entry of `complete_mode.limits` (and of an answer's
`limits`) is a pair [kind, sentence]. The kinds:

| kind | meaning |
|---|---|
| `tasks` | the time budget of the collection ended, or some tasks did not end |
| `memory of the collection` | the collection passed its limit (`GK_KEY_MEMORY_MB`, 1,000 MB), and the tasks that did not end are not complete |
| `task limit` | a task stopped at a count limit; the sentence names it (for example `GK_KEY_GROUND`, `GK_KEY_RESOLVENTS`) |
| `no self-support` | the pass that leaves out self-supporting applications did not end in the time budget |
| `binding by data` | the search that binds the variables of the rules by the facts stopped after 100,000 rounds while it still derived new atoms; the atoms of later rounds are missing |
| `function terms`, `term depth` | with function symbols: a variable ran through the ground terms written in the input, or terms deeper than the depth limit were cut |
| `clause rule across groups` | the clause rule in a cycle ran on atoms of more than one group of the definition: a proof outside a cycle lists a clause of that cycle; gk evaluated its conclusion inside the cycle, and the semantics evaluates it after the cycle ([support_semantics.md](support_semantics.md) §11.8) |
| `complete mode`, `cycle cut`, `backbone approximation`, `context copies`, `taxonomy ignored` | a reading of the evaluator that names an approximation ([support_semantics.md](support_semantics.md) §10.5) |
| `recursion depth` | the evaluation stopped without a value: a chain of the dependency is longer than the evaluator's recursion allows (40,000 levels natively, 20,000 in WebAssembly, or less where the stack is smaller) |
| `block allowance`, `evaluation budget`, `memory`, ... | the evaluation stopped without a value at another limit of the evaluator |
| `test switch` | a test switch withheld proof candidates |

**Errors.** The input errors are those of the other modes, with exit 1. An
option that Exact does not use (`-direct`, `-audit`,
`-checkpoints`, `-plain`, `-rawproofs`, `-directiontrace`, an option of the
direct method such as `-outformat`) gives `{"error": "do not use -audit
together with -exact: Exact does not use it"}` and exit 1.

### 7.1 The proofs under Exact

A printed proof of a literal H is one derivation of H from input
statements, built from the applications that the run collected and that
no self-support did not leave out (the reading `no self-support`). Its `confidence` is the confidence of this
derivation: the product of the confidences of the uncertain ground
statements that it uses, each once. The `value` comes from the evaluation of
all applications.

- The steps have the form of Section 3.1: `["in", name, "axiom", c]` for an
  input statement (its literals as written, then its exceptions as `$block`
  literals, with its variables), `["in", name, "goal", 1]` for the
  complement of H, `["mp", [s, i], [t, j], "fromaxiom" or "fromgoal", c]`
  for a binary resolution step. The last step resolves with the goal and
  leaves the exception literals, the guards.
- Each literal is derived once in a proof; later steps refer to its step.
  The application of each body literal is chosen in the order of
  derivation: from the applications without a body, an application is
  usable when every body literal has a derivation, and among the usable
  applications of a literal the most confident is taken. So a proof is
  never in a circle.
- An application of several statements (a proof found by the search) is
  derived again by ground resolution on its statements and printed with
  their resolution steps. When that does not succeed, the application is
  one step `["proof", parents..., "fromaxiom", c]` that names its
  statements; `complete_mode.proofs` counts both cases.
- `for` holds one proof per application of the answer's literal, `against`
  one per application of its opposite, `guards` the proofs of the other
  exception literals of their last clauses (with `guard_of`), most
  confident first, at most `GK_KEY_PROOFS` (10) each.
- `-fullproof` adds `subproofs` under the input step of each application of
  a proof: the proofs of the opposite of its head (`"opposition"`) and of
  each body literal (`"further proofs"`), with the keys of Section 3.1
  (`step`, `roles`, `listed_as`, `no_new_instances`). The subproofs of a
  literal are shown once per answer.
- An answer has at most `GK_KEY_PROOF_STEPS` (2,000) steps in all its
  proofs. The proof object's `left_out` counts the proofs and subproofs
  that the two limits, or the time limit of the printing (a quarter of the
  budget, at least 1 s), left out. `complete_mode.proofs` gives the limits
  and the totals.

### 7.2 The dump under Exact

With `-dwdump`, Exact prints its dump after the line. The dump is named
`gk_key_dump_v1`. It holds the evaluated
applications in the format of `gk_dump_v1`, with confidences as the
shortest text that reads back as the same number, and with
`exceptions_written`: the exception literals as the proofs show them,
together with the opposite of the head of a normal default, which
`exceptions` leaves out. `-dwevaluatenodes` reads it as it reads a
`gk_dump_v1` dump.

### 7.3 Exact, the experiment with general-prover assistance and the switches

`gk -exact -keyunified FILE` is **experimental: Exact with general-prover
assistance** (it is not among the public choices). Exact and this experiment
run in one process and one thread, in
the native program and in one WebAssembly instance. Their name is **the
single-thread schedule**: gk's general prover and Exact's search
take turns at the question and at the inner tasks, with slots that grow
with the round and shrink with the distance from the question, and both
feed one evaluation. The general prover's time in a run stays at most the
time of Exact's turns plus one first slot at the question
(`GK_KEY_GP_FAIR`, on; 0 turns this limit off). A parallel
schedule would be a second value of `-keyschedule` beside `single`; this
build has none.

| what | a native caller | a WebAssembly caller (`callMain(args)`) |
|---|---|---|
| Exact | `-exact` | the same arguments |
| Exact over the full grounding | `-exact -ground-first` (or `GK_COMPLETE_GROUND=1`) | `-exact -ground-first` |
| Exact with general-prover assistance | `-exact -keyunified`, or the environment switch `GK_KEY_UNIFIED=1` with `-exact` | `-exact -keyunified` |
| the schedule | `-keyschedule single` (the default), or `GK_KEY_SCHEDULE=single` | `-keyschedule single` |
| the budget | `-seconds N` | `-seconds N` |
| any other switch `GK_...` (Exact's limits, `GK_KEY_FUNCS`, `GK_KEY_PROVENANCE`, `GK_EVAL_MEMORY_MB`, the test switches) | the environment, or `-keyenv NAME=VALUE` | `-keyenv NAME=VALUE` |

A WebAssembly module cannot read the caller's environment, so every switch
has the command-line form `-keyenv NAME=VALUE`; NAME starts with `GK_`.
In WebAssembly a switch value must be below 2,147,483,648 (a `long` has 32
bits there). gk's data files (`gk_similarity.txt` of `-similarities`, the
data of `-defaults`) must be written into the module's file system by the
caller. `-keyunified`, `-keyschedule` and `-keyenv` hold for one call of main: the
next call removes the switches that the previous one set. `-keyunified`
and `-keyschedule` without `-exact` are an error with
exit 1, and so is a schedule other than `single`.

**Many runs in one instance.** Exact keeps its state
in static variables that one run fills. Every call of main frees that
state first and gives each variable its initial value, as in a new process:
Exact's tables, the state of the general prover's collection under Exact with general-prover assistance, the
parser's table of clause records, the converter's table of the lines of the
statements and the object of the field `policy`. So Exact, Exact with
general-prover assistance, Auto and General can follow each other in any order in one process or
WebAssembly instance, and each run gives the output of a run in an instance
of its own. An Exact run in WebAssembly also frees its database of 100 MB at
the end, as the other exits of main do. The times differ: the first run in
a new instance runs slower in WebAssembly (the runtime compiles the module's
code again while it runs), so an attempt of General with a short
allowance can end in a later round.

**The limits of the runtime.** The deadlines read a monotonic clock in
both targets (`clock_gettime(CLOCK_MONOTONIC)`; in WebAssembly the
runtime's `performance.now`). The memory of the collection is the
resident memory gained since the Exact run started (natively
`/proc/self/statm`); in WebAssembly it is the top of the heap, and the
collection also stops, as "memory of the collection", when less than
400 MB of the module's memory is left. gk tests it between the steps of a
task, and every 8 MB while a task builds the pool of its ground search,
which grows with the square of the number of its statements. The evaluation stops as an
interrupted evaluation before a new block would leave less than 64 MB.
Either stop makes the run not complete; it never ends the module. The
module of `compile_wasm.sh` has 2,000 MB of memory, which does not grow,
and a database of 100 MB for gk's general prover.

### 7.4 Confidences under Exact

gk reads a written confidence c in three steps: the reader keeps the
number as text with six decimals (`"%f"`), reads that text as a float, and
stores round(f × 10^7) as a whole number of the scale 10,000,000. The
three readers (`.gkp`, `.gks`, TPTP) write the number with all its digits
into the JSON form, so every input format takes the same steps, in both
targets. In effect:

- c ≥ 0.9999995 (and c < 1) is read as 1: the statement is certain. For a
  rule with a written head this makes a certain clause, used in every
  direction.
- 0 < c ≤ 0.0000005 is read as 0: the statement is left out.
- Any other c is stored within 6 × 10^-7 of c; a confidence with at most
  six decimals is stored within 10^-7, and exactly for most values (0.66
  is stored as 0.6600001, 0.72 as 0.7200001).

Under Exact, `complete_mode.confidence_readings` names every statement
whose stored number differs from its written confidence, for example
`"the confidence 0.99999999 of frm_1 was read as 1"` or `"the confidence
1e-08 of frm_2 was read as 0, and the statement was left out"`. The field
is there only when a statement has such a reading. The value is then the
definition's value for the input as gk reads it. Exact does not
cover an input with a knowledge base (`-usekb`), so no reading is missing
there.

### 7.5 Auto, the two-phase policy: Exact first, then General

Auto is the default of a query: `gk input` and `gk -auto input` select it. It
runs in native gk and in one WebAssembly instance, in one process and one
thread. Bare `gk input` and `gk -auto input` give the same routing, deadline
and output. Auto does not run for a query with `-eval125`, `-audit`,
`-direct` or an option of the direct method; those keep their own method. Let T be the time
limit of `-seconds` in wall-clock time (it must be positive), and N = s × T
with the share s of `GK_KEY_FIRST_SHARE` (0.5; a WebAssembly caller writes
`-keyenv GK_KEY_FIRST_SHARE=0.25`).

1. **The direct branch.** While the input is read, before any search: if a
   function symbol with arguments or an equality occurs anywhere in the input
   or the question, or Exact does not cover the input for another
   reason (Section 7), General answers with the time left until T.
2. **Phase 1.** Otherwise the exhaustive search (Exact alone, without
   the general prover) runs within N: its collection until 0.6 × N, then no
   self-support and the evaluation until N, and the printing of the proofs within N with
   at least 200 ms.
3. **Its answer** is printed when every task ended by its own search, no task
   and no collection stopped at a limit, no self-support ended, and the evaluator gave a
   value. The answer says complete, or not complete with the limits of the
   evaluator's named approximations.
4. **A switch** in every other case, at the moment the reason appears: tasks
   still open at 0.6 × N; a task or the collection at a limit of counts, time
   or memory; no self-support stopped at the deadline; the evaluator without a value (an interrupted
   evaluation); no time of N left for the evaluation. Phase 1 prints nothing.
   Its memory is freed. General runs as a separate run started with the
   time left until T, with the run's own options; nothing of phase 1 enters it.
5. **The line** is the line of the method that answered, in its usual form,
   with one more field `"policy"`:

| key | meaning |
|---|---|
| `name`, `share` | `"keyfirst"` and s |
| `answer_from` | `"the exhaustive search"` (Exact) or `"ordinary gk"` (General) |
| `branch` | `"phase 1"`, `"direct"` or `"switch"` |
| `reason` | on the direct branch and on a switch: why, with the statement and its line when one statement is the cause |
| `switch_at_ms` | on a switch: the moment, ms from the start of gk |
| `T_ms`, `N_ms` | T and N |
| `phase_1_ms` | the time phase 1 used (on the direct branch, the time of the first test) |
| `phase_2_ms` | the time General got (0 when phase 1 answered) |

**Only an answer with `"answer_from": "the exhaustive search"` and
`"complete": true` has the claim of exactness** (Section 7). An answer of General is a budgeted estimate.

`reason` is there only on the direct branch and on a switch, and
`switch_at_ms` only on a switch.

`-auto` together with `-exact`, `-keyunified`, `-direct`, `-plain`,
`-rawproofs` or `-directiontrace`, or with `-seconds 0`, is an error with
exit 1. General's other options are accepted; phase 1 does not use them.
Every Auto run in one instance starts with phase 1 as the first one does.

When the time limit of gk's process ends General's run under Auto
(natively, the alarm of `-seconds`), the line is `{"result": "time
limit, proof not found", "policy": {...}}` with the same object.

### 7.6 Every key of Exact's line

The line of Exact (`-exact`, also with `-ground-first` and with
`-keyunified`, and phase 1 of Auto) has the
keys of Section 3 (`method`, `question`, `answers`, `value`,
`signed_confidence`, `unresolved`, `proof`, `readings`, `reading_atoms`,
`applications`, `budget_ms`, `budget_used_ms`) and the object
`complete_mode`. A key with no value is left out; no key holds `null`.

| key of `complete_mode` | meaning |
|---|---|
| `version` | the version of gk, `1.3.2` |
| `covered` | true when Exact covers the input; false with `not_covered` |
| `not_covered` | `reason`, `statement`, `line`, `file` and `text`: the first cause that Exact does not cover, as a sentence that names the statement and its line |
| `complete` | true when the value is the definition's value for the input as gk reads it (Section 7) |
| `confidence_readings` | the statements whose stored confidence differs from the written one (Section 7.4); only when there is one |
| `limits` | pairs [kind, sentence]: every limit or approximation that makes the run not complete |
| `join_limit` | true when a group of the exception pass was evaluated on its own above the size limit of a join |
| `search` | `first-order resolution`, `ground`, or a class of the binding search (`class 1, binding by data`, `class 1, matched downward`, `class 2, ...`) |
| `class` | the class of the input that the search saw (0, 1 or 2) |
| `tasks`, `tasks_ended`, `tasks_at_limit`, `tasks_closed` | the tasks of the search: all, those that ended by their own search, those that stopped at a limit, those closed with every application of their literal |
| `tasks_by_ground_search`, `tasks_single_applications_only` | the tasks that the ground search answered, and those whose applications are single statements |
| `symbolic_states`, `ground_pairs` | the states of the symbolic search and the ground pairs it formed |
| `pairs_not_implying_the_head` | the pairs that the symbolic search turned away because their clauses and premises do not imply the head; only when there are some |
| `rounds` | the rounds of the collection |
| `resolvents` | the resolvents that the search formed |
| `proof_applications` | the applications of several statements (proofs found by the search) |
| `left_out_by_no_self_support` | the applications that no self-support left out (a body literal derived only through the application's own head) |
| `statements`, `ground_statements`, `ground_full` | the statements of the input, the ground statements formed, and the size of the full grounding |
| `constants` | the constants of the input and the question |
| `function_terms` | with function symbols: `ground_terms` (the ground terms made), `deepest_written_term` (the depth of the deepest term written in the input), `depth_limit` (the depth beyond which a term is not made), `tasks_cut_by_depth`, `terms_cut_by_depth` |
| `collection_ms`, `evaluation_ms` | the time of the collection and of the evaluation |
| `proofs` | the printing of proofs: `listed_at_most` (`GK_KEY_PROOFS`, 10 per list), `steps_at_most` (`GK_KEY_PROOF_STEPS`, 2,000 per answer), `bytes_at_most` (`GK_KEY_PROOF_BYTES`, 1,000,000 per answer), `several_statements_with_steps` and `several_statements_in_one_step` (the applications of several statements printed with their resolution steps, or as one step `proof`), `left_out` and `subproofs_left_out` (what the limits left out), `a_limit_reached`, and `causes`: per cause the sentence `cause`, the `proofs` and `subproofs` it left out, and `sides_with_a_share_and_no_proof` (sides with a share of the value and no printed proof) |
| `checkpoints` | under `GK_KEY_CHECKPOINTS`: the value at each test point |
| `no_self_support_check` | under `GK_KEY_RULE1_CHECK` (a test): the fast and the full form of no self-support, with their results |
| `unified` | with `-keyunified` only: `prover_ready` (the general prover started), `schedule` (`single`), `gp_fair` (`GK_KEY_GP_FAIR`), `attempts` and `attempts_ms` (the general prover's attempts and their time), `key_turns_ms` (Exact's turns), `derivations`, `repeated_derivations`, `candidates`, `applications_first_by_the_general_prover`, `derivations_not_imported` (the derivations that Exact could not read, with the cause) |

Under Auto, the line has also `policy` (Section 7.5).

The proof object of an answer has `for`, `against` and `guards`, and
`left_out` when a limit left proofs out (with the counts and causes of
`complete_mode.proofs`). A proof has `proves`, `confidence`, `steps`, and
with `-fullproof` `subproofs`; a subproof has `step` (the step of the
application it belongs to), `roles` (`opposition` or `further proofs`),
`proves`, `confidence`, `steps`, and `listed_as` (a proof printed earlier
in the answer, given by its place) or `no_new_instances` instead of its
steps. A step is `[n, rule, clause]`; Section 7.1 gives the rules. An
input step can have a fourth element `{"head": i}`, in every mode: the
place of the statement's written head among its literals, counted from 0. General's rules are `in`, `mp`, `simp` (a
clause simplified by unit clauses), `=` (an equality step) and `arithinst`
(an instance of an arithmetic literal).

General's line has `switches`, the settings of the recursive method
that apply: `keep_equal_goals` and `loop_marks` (always 0; gk keeps them
for the format of the line), `floor_ms` (the allowance floor,
`recursive_floor`), `floor_adaptive` (`recursive_floor_adaptive`: the floor
follows the shortest measured attempt) and `floor_last_ms` (the floor in
use at the end).
