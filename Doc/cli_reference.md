# Command-Line Reference

The examples below use `gk` as the executable name. In this repository the
Linux binary is `./bin/gk`; [`../bin/README.md`](../bin/README.md) lists the
other platforms.

## Invocation

```text
gk [options] file1 [file2 ...]
gk -jstext 'JSON-LD-LOGIC text' [options]
gk -readkb file [options]
gk -usekb [query-file] [options]
gk -deletekb [options]
```

With ordinary input files, GK reads all files as one problem and proves the
query they contain.

```sh
gk Examples/exceptions/bird_penguin.js
gk facts.js rules.js query.js
```

## Option syntax

An option is matched as a whole word: `-print 12` works, `-printx 12` is an
unknown keyword. Every option and command word also accepts a second
leading dash: `--seconds 5`, `--prove` and `--usekb` work like the one-dash
forms. Three leading dashes give an unknown keyword.

A numeric argument must be a number and nothing else: `-seconds 5x` is an
error. `-confidence`, `-keepconfidence` and `-blockerconfidence` take a
number from 0 to 1, or an integer from 2 to 100, which gk reads as a
percentage (`50` means 0.5). Any other value is an error, for example `1.5`
or `-0.1`. Every error of this kind prints one error object and exits with
code 1.

## Primary commands

These are mutually exclusive. When none is given, `-prove` is assumed.

### `-prove`

Prove the goals in the input. The default.

### `-help`, `-version`, `-licence`

Print the built-in option summary; the version, build date, word sizes, byte
order, compiler and database features; the licence embedded in the executable.
`--help`, `--version` and `-license` are also accepted.

The shared-memory commands `-readkb`, `-usekb`, `-writekb`, `-loadkb`,
`-readwritekb` and `-deletekb` are described under *Shared-memory knowledge
bases*; the conversion commands `-clausify` and `-writejson` under
*Conversion*.

## The method of a query

gk answers a question with one of three methods. They are the public choices:

| Command | Method | What the answer is |
|---|---|---|
| `gk -exact FILE` | **Exact**, the exhaustive search | With `"complete": true`, the value of the support semantics for the input as gk reads it. On an input outside its class: no value and the reason. Exact never switches to General. |
| `gk -general FILE` | **General**, the recursive method | A budgeted estimate. General covers the whole input language: function terms, equality, arithmetic, taxonomies, attached knowledge bases. |
| `gk FILE`, `gk -auto FILE` | **Auto**, the default | Exact's answer when Exact ends within half of the time limit; otherwise General's, with the time left. The line's field `policy` names the method that answered. |

Every method prints one line `{"recursive":{...}}` with the value and the
proofs. With `-dwdump` a dump follows the line.
[`recursive_output.md`](recursive_output.md) describes both; Section 7 there
describes the keys that Exact and Auto add.

The line's field `proof` gives the resolution proofs for and against the
answer, and the proofs of their guards (the exceptions left in them). A
default proof gives the main structure of the proof: the steps by which the
proof search derived the answer. The nested searches can also find sub-proofs
for or against these steps. The value counts the sub-proofs, but the default
proof does not show them; `-fullproof` adds them.

Two options that select different methods are an error, in either order:
`gk -general -exact FILE` and `gk -exact -general FILE` both stop with exit 1
and `{"error": "do not use -general together with -exact: ..."}`.

The help also lists the spellings of gk 1.2.5 (`-recursive`, `-keyfirst`,
`-complete`) and the options `-backbone` and `-narrowing`, which have no
effect. gk's source repository lists them with the forms to use now.

Copyable commands, from the repository root:

```sh
# blocks-world planning (function terms: Auto sends it to General)
gk Examples/fol_comparison/blocks.gkp -seconds 30 -maxanswers 1
# an exact comparison: the three methods on one input and one time limit
gk -exact   Examples/exceptions/penguin.gkp -seconds 10
gk -general Examples/exceptions/penguin.gkp -seconds 10
gk          Examples/exceptions/penguin.gkp -seconds 10
# the full-grounding experiment beside the usual Exact
gk -exact -ground-first Examples/exceptions/penguin.gkp -seconds 10
```

On `penguin.gkp`, Exact lists the three instances `flies(b)` (for),
`flies(p)` and `flies(o)` (against), each complete; General lists the
instances that a proof found, `flies(b)` and `flies(p)`, with the same
values; Auto answers with Exact.

### `-exact`

Run Exact, the exhaustive search, with the whole time limit. Exact follows
the dependencies of the question with resumable tasks, one per signed
literal: the question's two literals, then every literal that a task needs
(body literals, exceptions, opposites). The tasks run in rounds; each task
gets the same work allowance in a round, 2,000 units at first
(`GK_KEY_ALLOWANCE`), four times more in each later round. The search is
resolution first, with variables; with a function symbol, a round runs the
tasks with the shallowest terms first, up to a depth limit. When every task
has ended and the evaluation gave a value, the line says `"complete": true`;
the value is then the value of the support semantics for the input as gk
reads it (`recursive_output.md` Section 7, with its numerical precision in
Section 7.4). Otherwise it says `"complete": false` and lists the limits,
each a kind and a sentence (`recursive_output.md` Section 7): for example
`tasks`, `memory of the collection`, `task limit`, `binding by data`,
`clause rule across groups` or `recursion depth`.

The class of Exact excludes an equality that the question reaches, an
exception with a rank above 0 that is not the opposite of its rule's head, a
taxonomy priority, an attached knowledge base and a few further forms
(`recursive_output.md` Section 7). On such an input Exact prints no value,
`"covered": false` and the reason with the statement and its line, and
points to `gk -general FILE` or `gk -auto FILE` for a budgeted estimate.
Exact never switches to General. An option that only General or the direct
method uses (`-checkpoints`, `-audit`, `-direct`, `-plain`, ...) is an error
under Exact.

### `-general`

Run General, the recursive method, with the whole time limit. The searches
use a direction table: a default and an uncertain rule only at their head, a
certain rule and a disjunction on any literal. The base
search for the question is followed by the task registry's rounds: nested
searches for signed literals in contexts, with allowances `L0 * 2^k * r^d` in
round k at dependency depth d, so a deeper search gets a smaller time slot.
Every proof is imported as applications, and gk evaluates them once. gk's own
blocker checks and negative-evidence phases do not run. The strategy JSON can
set `recursive_L0` (ms, 50), `recursive_r` (.5), `recursive_share0` (.25),
`recursive_reserve` (.25), `recursive_a0` (4), `recursive_d0` (4),
`recursive_m0` (256) and `recursive_base_answers`. A strategy text with only
these keys leaves gk's automatic ladder in place. With `-usekb` the method
reads the attached knowledge base too (*Shared-memory knowledge bases*
below). General keeps the recursive method when an option of the direct
method is also given.

### `-auto`

Run Auto, the two-phase policy. It is the default of a query, so `gk FILE`
and `gk -auto FILE` give the same routing, deadline and output. With the
time limit T of `-seconds` (10 s by default) and N = T/2 (the share is the
environment switch `GK_KEY_FIRST_SHARE`, 0.5):

1. **The first test**, before any search. An input with a function symbol
   with arguments or an equality anywhere, an attached knowledge base
   (`-usekb`), or another input that Exact does not cover goes to General at
   once, with the whole time limit. The line's `policy` says
   `"branch":"direct"` and gives the reason with the statement and its line.
2. **Phase 1.** Exact alone within N: its collection until 0.6 N, then its
   evaluation until N. When the collection ended and the evaluation gave a
   value, that answer is printed with its own status: complete, or not
   complete with the named approximation of the evaluator (`limits`). A
   complete answer of ignorance, (0, 0, 0, 1), is an answer.
3. **A switch.** When the collection did not end by 0.6 N, a task or the
   collection met a limit, or the evaluation gave no value, phase 1 prints
   nothing. General starts afresh with the time left until T. The line's
   `policy` says `"branch":"switch"` with the reason and the moment.

`policy.answer_from` names the method that answered: `"the exhaustive
search"` is Exact, `"ordinary gk"` is General. Auto needs a positive time
limit: `gk FILE -seconds 0` and `gk -auto FILE -seconds 0` stop with exit 1
and a message that names `-general` for a run without a limit. Auto accepts
General's options; phase 1 does not use them.

### Advanced and experimental choices

These options stay out of the three public choices.

`gk -exact -ground-first FILE` is the full-grounding experiment: Exact
collects its evidence over the full grounding of the input first, in place of
the resolution-first search. The environment switch `GK_COMPLETE_GROUND=1`
has the same effect. `-ground-first` without `-exact` is an error. Compare it with
`gk -exact FILE` on the same input and time limit.

`gk -exact -keyunified FILE` is **experimental: Exact with general-prover
assistance.** On an input that Exact accepts, Exact's search and gk's
general prover take turns in one thread. The prover's attempts get a time
slot that doubles each round and halves with each step of distance from the
question; Exact's tasks keep their own work allowances. A proof of the prover
that passes the import check becomes an application of the one evaluation.
Only Exact's own search can establish that the collection is complete, and
the evaluation's checks apply as usual. Exact's coverage test is kept: when
an equation that the question reaches makes the input unsupported, the run
names the reason, gives no value and points to `-general` or `-auto`.
Equality reasoning stays in General, which Auto selects for such an input.
`-keyschedule single` names the only schedule of this build (one process and
one thread, also in WebAssembly). `-keyunified` without `-exact` is an error.

### `-eval125`

Select the evaluation of gk 1.2.5, for comparison: the cycle cut in place of
the narrowing, no exception pass and no field `unresolved`. The additions to
General's proof search after gk 1.2.5 are off: proof applications with listed
clauses, the check that a directed rule (a rule with a written head that is
uncertain or has an exception) enters a proof only towards that head, nested
proof applications, rule identities and the further searches. On its own, `gk FILE -eval125` runs General with this
evaluation, never Auto. With `-dwevaluate` it replays a dump with this
evaluation. The strategy key `recursive_eval125` 1 does the same.

### `-audit`

Run General, and the direct method in a second process beside it. gk prints
the recursive line and an `{"audit":{...}}` object with the direct method's
result, labelled as a comparison. Each method gets half of `-seconds`. An
option of the direct method goes to the second process.

### `-fullproof`

With every method: print the full proofs, with all their details.
Every proof in the line's field `proof` also gets `subproofs`: the proofs
that the nested searches of its input steps found, nested to every depth that
the searches reached. A subproof names the step whose search found it
(`step`) and the roles of that search (`opposition`, `further proofs`). A
subproof that is already listed at the top prints as a reference, for
example `"listed_as":["against",1]`. The lists `for`, `against` and `guards`
and the value are the same as without `-fullproof`.
[`recursive_output.md`](recursive_output.md) Section 3.1 describes the keys.

    ./bin/gk Examples/semantics/tweety_3a_gull_rule.gkp -fullproof

### `-checkpoints <dir>`

With General: write every checkpoint as a dump into `dir`
(`checkpoint_000_v0_r0.json` for the empty version 0, then one file per
checkpoint with its model version and report revision). The files are
written with or without `-dwdump`. The folder must exist: with a missing
folder gk writes nothing and reports no error.

### `-keyenv NAME=VALUE`

Set the environment switch `NAME` of gk to `VALUE` for this run. `NAME`
starts with `GK_`, for example `-keyenv GK_KEY_FIRST_SHARE=0.25` (the share
of Auto's phase 1). The option is for a caller that cannot set the
environment, such as a WebAssembly page. The next call of main removes the
switches that the previous call set. A value without `=`, or a name without
`GK_`, stops gk with exit 1 and `{"error": "-keyenv needs NAME=VALUE with a
NAME that starts with GK_"}`. [`recursive_output.md`](recursive_output.md)
Section 7.3 lists the switches.

### `-direct`

Run the direct method, the legacy method of gk 1.1.2, instead.
[`direct_method.md`](direct_method.md) describes it. gk prints the direct
method's result object, as gk 1.1.2 prints it. `-direct` cannot be combined with
`-auto`, `-general`, `-exact` or `-audit`.

These options also run the direct method: `-plain`, `-rawproofs`,
`-directed`, `-directiontrace`, and every option that only the
direct method reads. Those options are `-legacy` (every mode), `-detail`,
`-outformat`, `-defworlds`, `-nocumulate`, `-nonegative`, `-nocheck`,
`-blockerconfidence`, `-noconfsplit` and the `-dw` options. With
`-general` or `-audit`, General runs anyway. General ignores `-directed`, in
either order of the options; the direct method's part of `-audit` uses it.

## Input and output formats

### `-informat <json|prolog|tptp|simple>`

Read every input file in this language, whatever it looks like: `json`,
`prolog` (GKP), `tptp` (GKTPTP CNF) or `simple` (GKS, the
"premise => consequence" surface). This key is the authority.

Without it GK detects the language itself. The file **contents** decide when
they settle it — a leading `[` or `{` is JSON; a leading `cnf(`/`fof(`, or an
`include(` naming its file in single quotes, is TPTP CNF; a `:-` is GKP; a
`=>` is GKS — and the file-name **suffix** is the hint used when they do not
(`.js*` JSON, `.gkp`/`.pl`/`.pro`/`.prolog` GKP, `.p`/`.ax`/`.tptp`/`.cnf`
TPTP CNF, `.gks` GKS; anything else JSON). Contents outrank the suffix.

GK's own uncertainty vocabulary — `::`, `query(`, `unless(` — is shared by GKP
and GKS and decides neither: it narrows the file to those two, the first `:-`
or `=>` picks, and failing that the suffix does (`.gks` GKS, otherwise GKP).
Comments and quoted text are skipped throughout the scan, so a `=>` written in
a comment decides nothing.

### `-outformat <json|prolog|tptp>`

Format of the result. The default follows the input language: JSON for JSON
input, the plain-text key:value format for GKP input, SZS comments plus TSTP
`cnf()` records for TPTP input. This option runs the direct method; the
recursive method prints JSON for every input language.

### `-jstext '<json>'`

Read JSON-LD-LOGIC directly from the command line:

```sh
gk -jstext '[["bird","tweety"],{"@question":["bird","tweety"]}]'
```

### `-writejson`

Parse the input, print its JSON-LD-LOGIC representation, and exit without
proving it. GKP and TPTP input is converted; JSON input is passed through
unchanged and named in a comment.

### `-detail`

Add a `detail` block to each answer: `support_for`, `support_against`,
`conflict`, `ignorance`, the `calculation`, `coverage_status` and
`polarity_status` fields, conflict sources, flags and `recursive_checks`. The
field values are defined in the report-status tables of
[`direct_method.md`](direct_method.md) Section 5. `coverage_status: complete` means that no covered
operational failure was detected; it does not establish that the query lies in
the exact-correspondence fragment (the `DIRECTED_CORE` flag reports that
run-time check; see "Core selection" below). Implied by the `-legacy` modes
`envelope`, `stake` and `oldposneg`.

### `-print <n>`

Set output verbosity. The default is 10. The levels below describe the
output of the direct method. Auto, General and Exact print the same line at
every level; at level 12 and higher gk also prints the converted input and a
trace of the search before the line. Each band includes everything from
the bands below it; levels 0-11 print one valid JSON document, 12 and up
interleave a human-readable trace with the reports.

| Level | Content |
|---|---|
| 0-9 | answers with confidences and blockers; no proofs |
| 10 | default: answers with positive and negative proofs |
| 11 | adds the `detail` block and proof-step provenance |
| 12 | adds the high-level search trace: positive/negative searches, blocker checks with depth and time budget, brief sub-search results |
| 13-15 | adds full intermediate reports, the given-clause trace, and input statistics |
| 16-20 | adds kept derived clauses with clause metadata |
| 21-30 | adds subsumed and pre-cut derived clauses and the initial clause lists |
| 31-50 | adds given candidates with resolvability, active clauses, partial derivations, and parser dumps |
| 51+ | adds literal/term selection and datastructure dumps |

Note that a strategy file's own `print_level` defaults to 15, not to the
CLI default of 10; see `strategy_reference.md`.

### `-derived`

Print all derived clauses independently of `-print`.

## Time and memory

### `-seconds <n>`

Set the total time limit in seconds. The default is 10. Auto needs a positive
limit; `-seconds 0` (no limit) is for `-general` and the direct method.

### `-mbsize <n>`

Set the initially allocated database size in megabytes. The default is 5000,
the minimum 10. The WebAssembly build uses 100 by default. `-readkb` requires at least 1000 MB on Linux and macOS and at
least 100 MB on Windows; `-readwritekb` has the same requirement. When the
search fills the database, gk stops with exit 1 and the error `the database
of N MB is full (the option -mbsize sets its size in MB)`. The general
method can fill the default database on a long chain of certain rules: on a
chain of 10,000 rules it can stop with this error after about 9 s of the
default time limit of 10 s.

### `-parallel <n>`

Run automatic search strategies in up to `n` concurrent processes (1 to 8;
default 1, meaning no parallel search). Linux and macOS only: the option is
ignored on Windows and in the WebAssembly build.

Effective only when the automatic strategy ladder is used, that is without
`-strategy` / `-strategytext`. The ladder's alternative strategies run as
separate probe processes alongside the in-process champion, and when the
champion gives up, the first strategy a probe proved (in ladder order) is
replayed in the main process. Answer selection stays deterministic; only the
wall-clock latency of hard queries changes. Works with `-usekb`. Raw-proof
mode remains single-process. See `strategy_reference.md`.

## Answer and proof limits

### `-confidence <n>`

Set the minimum verdict confidence for an accepted or rejected answer of
the direct method. Auto, General and Exact do not read it: on a chain with
the value (.72, 0, 0, .28), `-confidence 0.8` gives the same line. The
underlying signed confidence is `support_for - support_against`; the routed
verdict uses its absolute value. The default is 0.1. The value may be a
decimal from 0 to 1 or an integer percentage from 2 to 100; any other value
is an error.

The effect is mode-specific. In the default shared-threshold mode the
threshold is compared against the legacy-compatible `confidence` field; when
no answer clears it the run's result string becomes `evidence below limit`,
but every found answer still prints with its full four-component report —
nothing is hidden. Under `-legacy olduncertainty` answers below the threshold are
dropped from the output entirely.

### `-keepconfidence <n>`

Discard derived clauses below this confidence during search. The value uses
the same decimal or percentage forms as `-confidence`. The default is 0,
which keeps all derived clauses.

### `-blockerconfidence <n>`

Acceptance threshold for an exception proof in the direct method's blocker check;
same decimal or percentage forms as `-confidence`, default 0.5. The
threshold applies only to answers outside the directed core: an answer
reported with `DIRECTED_CORE` carries the evaluator's value, which grades every
exception (a .4686 exception against a certain default gives .5314 at any
threshold). Outside the core, and for every answer under `-legacy dwlegacy`, an
exception proof below the threshold is ignored entirely, so the reported
confidence can jump when the combined evidence for an exception crosses it.
There, lower the threshold, or use `-legacy softblock`, for graded behavior below
0.5.

### `-firstanswer`

Stop after the first answer and its first retained proof.

### `-maxanswers <n>`

The A limit: stop the search when `n` distinct answers have been found; if
`-maxproofs` is also set, when each of them holds that many proofs.
Default: off. Combined by OR with the total-proofs stop (strategy key
`max_answers`, default 10 — raise it if it fires first). Strategy-file
equivalent: `max_distinct_answers`.

### `-maxproofs <n>`

The P limit: retain at most `n` proofs for each distinct answer, enforced at
proof registration. The option never stops the search by itself. Default: off
in normal mode, 16 in raw-proof mode. Strategy-file equivalent: `max_proofs`.

## Defaults and auxiliary data

### `-nocheck`

Do not run blocker checks. Default rules then fire without testing their
exception conditions.

### `-taxonomy`

Load the taxonomy data used by taxonomy-form blocker priorities such as
`tax(name)` and `tax(name, nr)`. GK reads two files, from the `-datafolder`
path or the current working directory:

```text
gk_name_number.txt
gk_taxonomy_packed.txt
```

The two files form one generated pair and are validated together; a missing or
mismatched file is an error with a nonzero exit. An input that uses
taxonomy-form priorities without this flag is an error; numeric priorities
never need it. `-defaults` is an accepted synonym. The comparison rule — a
more specific class defeats a more general one — is described in
`direct_method.md` Section 6. General compares taxonomy ranks by
specificity too (`how_gk_works.md` Section 10). Exact does not cover a
taxonomy rank, so Auto sends such an input to General.

### `-relatedwords`

Load `gk_relatedwords.txt`.

### `-similarities`

Load the word-similarity file `gk_similarity.txt` and enable similarity
derivation. `-similarity` is an accepted synonym.

### `-nosimilarities`

Disable similarity derivation even when a similarity file has been loaded.
Useful with `-usekb` when the shared base contains the file.

### `-datafolder <path>`

Read auxiliary `gk_...` files from `path` rather than the current directory.

```sh
gk Examples/exceptions/classify.js -taxonomy -datafolder Examples/exceptions
```

### `-task <name>`

Select a build-specific auxiliary task. Task names are not part of the stable
proof-search interface; an ordinary reasoning command does not use this option.

## Search strategies

### `-strategy <file>`

Use a JSON strategy file:

```sh
gk problem.js -strategy Examples/strategy/query_focus.txt
```

### `-strategytext '<json>'`

Supply the strategy object directly:

```sh
gk problem.js -strategytext '{"strategy":["query_focus"],"query_preference":1}'
```

Without either option, GK constructs a strategy automatically: a short ordered
ladder with initial proof-finding time limits, described in
`strategy_reference.md`, where the strategy keys are listed as well.

### `-explore`

Exploratory-first automatic selection (mode B): every ladder entry gets an
equal short give-up time for its first proof, and the first strategy that
proves something continues with the remaining budget and is adopted for the
rest of the query. GK enables this mode automatically when `-seconds` exceeds
30.

## Shared-memory knowledge bases

A parsed knowledge base can be held in shared memory for repeated queries.
Database number 1000 is used by default.

### `-readkb <file>`

Parse a question-free file into shared memory. Requires at least 1000 MB via
`-mbsize` on Linux and macOS, 100 MB on Windows. The loaded axioms must not
contain a question: questions belong in the per-query input, and one stored in
the KB is rejected. Options that load auxiliary data, such as
`-taxonomy -datafolder DIR`, belong on this command so that `-usekb` queries
need not repeat them.

The knowledge base also keeps the written head of every directed
rule and the statement number, `@sourcetype` and `@provenance` of every
clause. The recursive method of a `-usekb` query reads them; the direct
method does not. A knowledge base, or a dump, made by another gk version
does not attach: gk prints `Existing segment header is incompatible` and
exits with 1. Rebuild it with `-readkb`.

### `-usekb`

Use the shared knowledge base together with any query file on the command
line; that file carries the question. Auxiliary data loaded with `-taxonomy`,
`-datafolder`, `-similarities` or `-relatedwords` comes from the shared base,
so those options must not be repeated here. With one of them, gk prints
`{"error": "if you give -usekb, do not use -datafolder, -taxonomy/-defaults,
-similarities or -relatedwords: these come from the shared database"}` and
exits with 1.

Both General and the direct method run on an attached knowledge base. Exact
does not read one, so Auto sends a `-usekb` query to General at once (the
reason "an attached knowledge base"). General reads the knowledge base's
clauses together with the query's; its value equals the value of one run on both inputs, up to the
search order (the automatic ladder differs, see below).

The automatic strategy ladder, `-parallel`, `-confidence`, `-keepconfidence`,
`-outformat` and the report flags all apply per query. One limitation: a sine
strategy does no relevance filtering over a shared KB, because its per-symbol
data cannot live in the read-only segment. The automatic ladder therefore
omits sine under `-usekb`, and an explicit sine strategy runs without it.

### `-deletekb`

Delete the selected shared-memory database. Linux and macOS only.

### `-mbnr <n>`

Select a shared-memory database number. The default is 1000, the minimum 1.
Separate numbers allow several databases to coexist.

### `-writekb <file>`

Write the selected shared-memory database to a dump file.

### `-loadkb <file>`

Load a dump file into shared memory.

### `-readwritekb <logic-file> <dump-file>`

Parse a logic file and write the resulting database directly to a dump file.
Requires at least 1000 MB via `-mbsize` on Linux and macOS, 100 MB on
Windows.

Typical sequence:

```sh
gk -readkb axioms.js -mbsize 2000 -taxonomy -datafolder DIR
gk query.js -usekb -parallel 3
gk -deletekb
```

Shared-memory databases are host resources. Delete an unused database before
reusing its number with a different size or configuration.

## Conversion

### `-clausify`

Print the clausified problem instead of proving it. Cannot be combined with
`-usekb`. Plain `-clausify` emits the classic clause representation;
`-defworlds -clausify` emits the confidence-aware representation.

Combined with `-defworlds`, the JSON output follows the versioned
`gk_clauses_v1` exchange convention, consumed by the shared-threshold
reference implementation: a leading meta object

```json
{"format":"gk_clauses_v1","confsplit":1}
```

with `confsplit` 1 unless `-noconfsplit`, then per clause the effective
clause-level fields:

- `@confidence` — stored per-clause confidence with the root split already
  applied, at full float precision (0 becomes 1.0);
- `@head` — literal index carrying the parse-time head marker
  (`ATOM_META_HEAD`); a fact is trivially 0, a rule clause with no marker −1;
- `@role` — `"goal"` on the negated-conjecture clauses.

Plain `-clausify` output carries none of these extra fields.

## Auxiliary data files

When using `-taxonomy` (synonym `-defaults`), `-similarities` or
`-relatedwords`, GK looks for these files in the current directory or the
`-datafolder` path.

| File | Contents |
|---|---|
| `gk_name_number.txt` | words mapped to taxonomy class numbers; in [`../data/`](../data/README.md) |
| `gk_taxonomy_packed.txt` | the packed WordNet taxonomy hierarchy; in [`../data/`](../data/README.md) |
| `gk_similarity.txt` | word similarity scores, one `word1 word2 score` per line, score 0.0 to 1.0 |
| `gk_relatedwords.txt` | related-word associations |

## Usage examples

Basic proof search:

```sh
./bin/gk problem.js
./bin/gk problem.js -seconds 30 -print 15
```

With confidences and defaults:

```sh
./bin/gk problem.js -taxonomy -confidence 0.2
```

Shared-memory knowledge base:

```sh
./bin/gk -readkb axioms.js -mbsize 2000 -taxonomy -datafolder DIR
./bin/gk query.js -usekb
./bin/gk query.js -usekb -parallel 3       # automatic ladder, probes in parallel
./bin/gk query.js -usekb -mbnr 1001
./bin/gk -deletekb
```

Strategy file, direct input, and several input files:

```sh
./bin/gk problem.js -strategy mystrategy.json -seconds 60
./bin/gk -jstext '[["bird","tweety"], {"@question": ["bird","tweety"]}]'
./bin/gk facts.js rules.js query.js
```

## Confidence and support assessment

The options of this section belong to the direct method (`-direct`). The
older modes of that method are selected with `-legacy` (below). Its
default report gives a compact verdict `confidence` equal to
`abs(support_for - support_against)` and, with `-detail`, the four components
from which it is derived. Accepted and rejected answer lists carry the sign.
The algorithms and interpretation are described in
[`direct_method.md`](direct_method.md).

### `-nocumulate`

Do not combine alternative proofs of the same answer.

### `-nonegative`

Do not search for support for the explicit negation.

### `-legacy <mode>[,<mode>...]`

Select one or more older modes of the direct method. Give several modes as
a comma list, or repeat the option: `-legacy envelope,oldposneg` and
`-legacy envelope -legacy oldposneg` are the same. gk applies the modes in
the order given. Each mode runs the direct method, unless `-general` or
`-audit` is also given. An unknown mode, or `stake` without a value, is an
error.

#### `olduncertainty`

Restore the legacy single-number pipeline, the default of the direct method
before the four-component report: one signed positive-minus-negative
`confidence` per answer, with low answers dropped under `evidence below
limit`. The output is byte-identical to the output of that pipeline.

#### `oldcumulate`

Combine two proofs by noisy-or with the weaker contribution scaled by a
dependency ratio estimated from the proof histories and by the `independence`
strategy percentage, instead of the default per-ground-instance combination
(post-search proof replay producing one event per ground clause instance,
combined by bounded inclusion-exclusion). Without this mode GK measures the
overlap from the proofs' activation-event sets.

The default and this mode give different answer confidences wherever several
proofs of one answer share supporting clauses; this mode gives the numbers of
the older cumulation exactly. Per-proof confidences are also affected: the
exact default reports each proof as the product over its distinct used instances of uncertain clauses — one
independent event per ground clause instance, the ProbLog reading, in which an
axiom used twice at the same instance counts once and at two different
instances twice — reconstructed from the proof after the search. When that
reconstruction fails the proof keeps the stepwise per-use product, the
conservative floor. The old mode keeps the stepwise product throughout.

undefining it removes the exact machinery entirely.

#### `oldposneg`

Additionally print the legacy signed positive-minus-negative `legacy_posneg`
number alongside the four-component report.

#### `envelope`

Compute minimum and maximum support when identified conflicts are resolved in
each direction, plus a `brittle` flag. The bounds are support values; they
have no probability reading. Implies detailed output.

#### `stake=<F>`

Set a decision threshold `F`, from 0 to 1, and report `ACCEPT`, `DEFER` or
`REJECT`, read from the `support_for` envelope: `ACCEPT` if the lower end
clears the threshold, `REJECT` if the upper end fails it, otherwise `DEFER`.
Without the mode `envelope` it is a point comparison with a printed caveat.
A value outside 0..1 is an error.

#### `softblock`

A legacy-report mode between `olduncertainty` and the shared-threshold
default: the single-number report, but with graded blockers. The raw firing
blocker confidences pool by noisy-or into a discount factor `1 - pb` on the
blocked answer, instead of the hardwired all-or-nothing 0.5 threshold. The
mode selects the single-number calculation pipeline unless `-defworlds` is
given; the four-component report does not use this discounting.

#### `dwlegacy`

Restore the report routes of 1.1.1: no core selection, no flag, the upstream
conditioning rule alone (see `-dwnosep`), no instance enumeration. Its output
equals the 1.1.1 default output. See "Core selection" below.

#### `dwopen`

Opt-in, experimental and diagnostic. Two of its acceptance cases disagree
with the current binary, and the mode is planned for retirement.

It grounds the free variables of a matched clause and evaluates each ground
instance as a separate weighted instance instead of abstaining. The
instances come from a bounded forward-closure witness join over concludable
ground literals, so compound Skolem witnesses are reachable. Every cap overflow makes the
dependency-aware attempt incomplete: the final report falls back to the
proof-derived components with `OPEN_PREMISE` + `PROOF_FALLBACK` flags, never
silently.

Without this mode, non-ground premises make the dependency-aware attempt
abstain with `OPEN_PREMISE`, and the fallback still reports the
proof-derived components, so answers are not lost either way.

### `-defworlds`

Select the four-component report: per answer, `support_for`,
`support_against`, `conflict` and `ignorance` (the four sum to 1) plus the
legacy-compatible single `confidence`, conflict sources and flags. Only
`confidence` is top-level; the components and everything derived from them
print under `detail` with `-detail`.

Exact by enumeration up to 6 shared elements; above that the dependency-aware
attempt is discarded and the report falls back to the proof-derived components
with `JOINT_CAP` + `PROOF_FALLBACK` flags. Recognises the load-time
declarations `@report` and `@marginal` (see [`json_ld_logic.md`](json_ld_logic.md)).

This is the default of the direct method, so giving the flag is a no-op
except with `-clausify`, where an explicit `-defworlds` selects the
`gk_clauses_v1` export while plain `-clausify` keeps the classic one. `-plain`
implies the legacy pipeline, having no confidences to report.

### `-rawproofs`

Return the retained positive and negative proofs without cumulation or
positive-negative arithmetic: proofs are collected per distinct answer (up to
`-maxproofs` each), and the negative-evidence search runs once per distinct
answer. Output is a JSON document with the format marker
`gk_raw_proofs_v1`, carrying per answer the lists `positive` and `negative` of
proof objects; downstream scripts do the combining (see `gkraw.py` in the
csrtools confidence project). `-confidence` does not filter this mode.


### `-plain`

Ignore input confidences: any `@confidence` values are dropped, and unless
blocker literals are present in the input the default machinery is also
skipped. Intended for boolean per-world runs of the clause-activation
sampler ([`../montecarlo/`](../montecarlo/README.md)), typically combined
with `-nonegative`.

### `-noconfsplit`

Disable the confidence root split. By default a statement whose formula
flattens into N clauses — an equivalence, or a conjunction of implications —
has its confidence P distributed as P^(1/N) to each clause, so the conjunction
of the clauses, that is the formula, holds at exactly P. With `-noconfsplit`
each produced clause keeps the full P.
Statements with N=1, such as facts and plain implications, are unaffected
either way. The split runs only under the four-component report, so
flag-off output is byte-identical regardless.

### Core selection: the default, `-dwcore` and `-legacy dwlegacy`

The report route of an answer is chosen by core selection. For an answer that
the routes of 1.1.1 (`-legacy dwlegacy`) report `flat` or `blocked_flat`, gk also runs the
dependency-aware evaluation of the question atom. It reports that evaluation
(`calculation: canonical_atom`) when all of these hold:

* the retained proofs of both rails are inside the evaluator's inference
  fragment;
* the evaluation completed: no cap, cutoff, open premise or sampling;
* every rule the evaluation used is one directed application of the finite
  core: one reading of the clause, no `$` or equality predicate, and either
  at most one exception with positive content on a distinct atom and an
  integer rank (an ordinary veto), or a normal default whose exception is
  its own conclusion's complement (`flies(X) :- bird(X) unless -flies(X)`),
  with an integer rank and its written head on that conclusion;
* at every atom, each sign of support is of one kind: ordinary (facts, rules,
  ordinary vetoes) or normal defaults; a normal side does not mix rank 0 with
  positive ranks; when both sides are normal, every rank is positive (equal
  maximal ranks block each other, a higher rank wins); the evaluator applies
  the matching local calculation;
* no atom cycle, no context-restricted check, no self-defeating or paired
  exception, no clause whose written head is not the conclusion that gk
  reads; no equality literal in the KB; the question is not reached through
  an alias or definition hop; the KB is not an attached shared-memory KB
  (`-usekb`: the evaluator's clause scans read only the local clause list);
* the coverage check of the proof fallback holds: the evaluation does not
  zero a side that has a retained proof and no conflict source, unless that
  side's retained answer has a `$block` literal (a default proof can be
  defeated without conflict).

A rule whose body has a variable outside its head (`q(X) :- p(X,Y)`) is one
application per ground instance. The evaluator finds the instances among the
ground literals that some clause can conclude: a forward closure, to a
fixpoint, over the predicates that the open body literals depend on. More than
16 instances give the flag `INSTANCE_CAP`; a universal fact or a source that
stays non-ground, an unbounded function term and an exception with a free
variable leave the premise open (`OPEN_PREMISE`). Both are flagged fallbacks.
Built-in predicates and a KB with an equality literal keep the open premise.

Every `canonical_atom` report that meets these conditions has the flag
`DIRECTED_CORE`, including one that the routes of 1.1.1 already chose. The
flag states that the reported tuple is the support-state distribution of the
question atom for the evaluated directed program; it is a run-time check of
the rules met, not a proof that the KB has no other relevant derivation. Any
other answer keeps its report of 1.1.1, without the flag.

In the core, core selection replaces two behaviours of 1.1.1: the flat
netting of the reported answer's retained proofs, which misses the
derivations of other answers (`.2::b`, `.2::q unless b`, `.5::q :- b` gives
`.20` flat and `.26` exactly), and the `-blockerconfidence` threshold, which
the evaluator does not apply (an exception below 0.5 is graded).

`-legacy dwlegacy` restores the report routes of 1.1.1 (see the mode
`dwlegacy` below). `-dwcore` is accepted and changes nothing.

### `-dwjoint`, `-dwproofs`

Diagnostic and test-only switches of the direct method's evaluator.
`-dwjoint` forces the joint enumeration. `-dwproofs` prints the retained
proofs and the separator trace (*Separators* above). Each option runs the
direct method.

## Result strings

These are the result strings of the direct method (`-direct`). The
recursive method's line reports the fields `stop` and `search` instead
([`recursive_output.md`](recursive_output.md) Section 3).

These are the `result` strings of the direct method. Auto, General and
Exact print the `{"recursive": ...}` line instead. One exception: when the
time limit of the process ends General's run under Auto, the line is
`{"result": "time limit, proof not found", "policy": {...}}`
([`recursive_output.md`](recursive_output.md) Section 7.5).

| Result | Meaning |
|---|---|
| `answer found` | at least one answer met the acceptance threshold |
| `evidence below limit` | a proof was found but its assessed margin was below `-confidence` |
| `no answers found` | no substitution was found for an open query |
| `no information` | neither polarity of a ground query was proved |
| `generic assumptions contradicted` | the assumptions of the question lead to a contradiction |
| `time limit, proof not found` | the search limit expired before a proof was found |

An output may also contain rejected answers when negative support dominates.
Use `-detail` to distinguish negative support, conflict and ignorance.
