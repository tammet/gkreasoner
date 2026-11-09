# Default and exception examples

A default rule has an exception condition, written `unless(...)` in GKP and
as a `$block` literal in JSON-LD-LOGIC. The default applies only where its
exception does not hold. gk's default method, the recursive method, starts
from a proof that uses the default. It then searches for the exception, and
for evidence for and against it, in nested searches with smaller time
allowances. All the evidence goes into one calculation of the four shares:
for, against, conflict, and ignorance. Ranks, numeric or from a taxonomy,
decide which defaults may defeat other defaults.

Run commands from the repository root. The values below are gk 1.2.4's,
shortened. [`../../Doc/support_semantics.md`](../../Doc/support_semantics.md)
explains the four shares on examples.

## An unopposed default

[`bird_default.gkp`](bird_default.gkp) and [`bird_default.js`](bird_default.js)
contain:

```prolog
bird(a).
bird(b).
flies(X) :- bird(X), unless(-flies(X), 2).
query(flies(X)).
```

```sh
./bin/gk Examples/exceptions/bird_default.gkp
```

Each answer depends on its exception, `-flies(a)` or `-flies(b)`. gk finds no
evidence for either exception, so `flies(a)` and `flies(b)` are both
(1, 0, 0, 0).

## Uncertain support for an exception condition

[`bird_exception.gkp`](bird_exception.gkp) and
[`bird_exception.js`](bird_exception.js) add:

```prolog
0.9::-flies(a).
```

```text
"answers":[{"answer":"flies(a)","value":[0.1,0.9,0,0]},
           {"answer":"flies(b)","value":[1,0,0,0]}]
```

Where the fact of confidence .9 is present, it is the exception: the
default does not apply, and `-flies(a)` holds. That gives .9 against.
Elsewhere the default applies: .1 for. The default yields to the fact, so
there is no conflict.

[`bird_hierarchy.js`](bird_hierarchy.js) uses an ordinary rule without an
exception as a control case. The certain rule and the fact meet head on, so
`flies(a)` is (.1, 0, .9, 0): conflict .9 instead of against .9.

## Evidence against an exception

Evidence against an exception may be a fact or may be derived by a rule;
both count. In [`bird_counter.gkp`](bird_counter.gkp) a rule with confidence
.58 derives evidence against the exception:

```prolog
bird(a).
0.6::injured(a).
vet(a).
0.58::-injured(X) :- vet(X).
flies(X) :- bird(X), unless(injured(X), 2).
query(flies(a)).
```

The exception `injured(a)` has .6 for it and .58 against it. The two are
tested against one shared number of the atom, so `injured(a)` holds without
conflict only in a share of .6 − .58 = .02. Only there does the exception
block the default. gk answers `flies(a)` with (.98, 0, 0, .02).

[`bird_counter_premise.gkp`](bird_counter_premise.gkp) moves the .58 from
the rule to its premise (`0.58::vet(a)` with a certain rule). The answer is
(.748, 0, 0, .252). The two placements mean different things. A rule
confidence of .58 gives `-injured(a)` .58 against, as above. A premise
confidence of .58 means that the premise is present in .58 of the worlds.
There the certain rule derives `-injured(a)`, and the exception never holds
alone. In the other .42 of the worlds, the exception holds with .6. The
default is blocked in .42 × .6 = .252 of the worlds, so the share for is
1 − .252 = .748. The line also has one `cycle cut` reading; the reference
tool gives .7556 for, within its sampling error of ±.0113.

Evidence against an exception is itself checked: if its own derivation is
blocked by a certain exception, it contributes nothing.

## Equal defaults

[`nixon.gkp`](nixon.gkp) and [`nixon.js`](nixon.js) encode the Nixon diamond:

```prolog
quaker(n).
republican(n).
pacifist(X)  :- quaker(X),     unless(-pacifist(X), 2).
-pacifist(X) :- republican(X), unless(pacifist(X), 2).
dislikeswar(X) :- pacifist(X).
query(dislikeswar(X)).
```

The two defaults have equal rank and block each other, so neither side is
usable. gk answers `dislikeswar(n)` with (0, 0, 0, 1): ignorance, not
conflict. No rule-order tie breaker is used.
[`nixon_taxonomy.js`](nixon_taxonomy.js) asks the pacifism question itself
with taxonomy ranks and gets `pacifist(n)` (0, 0, 0, 1).

## Numeric and taxonomy ranks

The `penguin*.js` files build a hierarchy from organism to bird, penguin, and
flying penguin, with opposing flight defaults at different ranks.
[`penguin2.js`](penguin2.js) uses numeric ranks.
[`penguin3.js`](penguin3.js) uses taxonomy ranks and therefore requires:

```sh
./bin/gk Examples/exceptions/penguin3.js \
  -taxonomy -datafolder data
```

Both answer `fly(b)` (1, 0, 0, 0), `fly(p)` (0, 1, 0, 0) and `fly(fp)`
(1, 0, 0, 0). Here the taxonomy supplies the order: `penguin` is below
`bird` and `organism` in the loaded hierarchy, so the penguin defaults
defeat the bird and organism defaults without hand-assigned numbers.

The taxonomy data files are in [`../../data/`](../../data/README.md); a
taxonomy-form rank without `-taxonomy` (synonym `-defaults`) is an
input error. [`penguin4.js`](penguin4.js) applies the same pattern to nested
function terms; it answers `fly(father(father(p)))` (0, 1, 0, 0) and uses its
whole time budget, about 7 seconds. [`taxonomy.js`](taxonomy.js) is a compact
taxonomy-rank case:

```sh
./bin/gk Examples/exceptions/taxonomy.js -taxonomy -datafolder data
```

It asks `bird(os)` for an ostrich, and no rule makes an ostrich a bird:
(0, 0, 0, 1).

[`penguin.gkp`](penguin.gkp) and [`penguin.js`](penguin.js) are compact cases
with a certain penguin exception and two opposed defaults. The stronger
flight default prevails for the ordinary bird, `flies(b)` (1, 0, 0, 0); the
penguin gets `flies(p)` (0, 1, 0, 0).

## Classification from parts

[`classify.gkp`](classify.gkp) and [`classify.js`](classify.js) classify three
objects from observed parts: `h1` (legs), `b1` (legs, wings and feathers)
and `a1` (an engine and wings). Several uncertain defaults may support the
same class, while a certain engine rule supports `-isa(X, organism)`.

```sh
./bin/gk Examples/exceptions/classify.gkp \
  -taxonomy -datafolder data
```

```text
"answers":[{"answer":"isa(b1,organism)","value":[0.5731,0.0179,0.3821,0.0269]},
           {"answer":"isa(a1,organism)","value":[0,0.4,0.6,0]}]
```

`b1` has a bird path for it and an opposed airplane path against it. The
line has two `cycle cut` readings. With the default search, gk does not
list `h1`. With the strategy file
[`../strategy/query_focus.json`](../strategy/query_focus.json) it lists
`isa(h1,organism)` with (.44, 0, 0, .56): the human default .3 and the bird
default .2 combine by noisy-or. That search does not list `a1`. Which
answers the recursive method lists depends on the search: a measured limit
of gk 1.2.4.

## Persistence across situations

[`people_room.js`](people_room.js) represents entry and exit events across
three situations. Frame rules use exceptions to carry `in` and `-in` forward
unless an event changes them:

```sh
./bin/gk Examples/exceptions/people_room.js \
  -taxonomy -datafolder data
```

gk answers `in(man1,room1,sit2)` (1, 0, 0, 0) and `in(man1,room1,sit3)`
(0, 1, 0, 0). It uses its whole time budget, about 7 seconds, and reports
8 nested searches cut by their allowances. The named markers in its frame
rules are taxonomy-form ranks, so the tables must be loaded; they do not
change this example's result.

## Equivalent input notations

[`bird_penguin.gkp`](bird_penguin.gkp),
[`bird_penguin.js`](bird_penguin.js), and
[`bird_penguin.p`](bird_penguin.p) encode one problem in GKP,
JSON-LD-LOGIC, and TPTP:

```prolog
bird(b).
0.8::penguin(p).
bird(X) :- penguin(X).
0.9::-flies(X) :- penguin(X).
flies(X) :- bird(X), unless(-flies(X), 2).
query(-flies(X)).
```

The notations differ in one respect that the recursive method uses. A GKP
rule keeps its written head. The `.js` and `.p` files state flat clauses,
which gk uses in every direction. The values therefore differ:

| File | gk 1.2.4 for `-flies(p)` |
|---|---|
| `bird_penguin.gkp` | (.72, .08, 0, .2) |
| `bird_penguin.js`, `bird_penguin.p` | (.72, 0, 0, .28), with three `cycle cut` readings |

The reference tool gives (.722, .077, 0, .201) for both forms, within its
sampling error. The GKP value is the semantics value. The penguin rule
derives `-flies(p)` in .8 × .9 = .72 of the worlds: the share for. Where
`penguin(p)` holds but that rule does not (.08), the bird default derives
`flies(p)`: the share against. With the flat clauses gk cuts a cycle
across signs, and the .08 against goes to ignorance.

## Additional cases

| Files | Main feature |
|---|---|
| `hierarchy.js`, `taxonomy.js` | compact specificity and hierarchy cases (`taxonomy.js` needs `-taxonomy`) |
| `gbirds.js` | bird/penguin default with an ASP comparison in comments |
| `gbirds_funsymbs.js` | the same pattern with function symbols |
| `trivial.js` | plain facts and one closed query, with no defaults |

How gk reaches an answer is described in
[`../../Doc/how_gk_works.md`](../../Doc/how_gk_works.md).
