# Default and exception examples

A default rule derives a candidate conclusion together with a blocker. GK then
searches for the blocking condition. Numeric or taxonomy priorities determine
which defaults may defeat other defaults.

Run commands from the repository root. `-detail` prints support, opposition,
conflict, ignorance, conflict sources, and report flags.

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

Both `a` and `b` are returned with confidence 1. Their proofs retain
`unless(-flies(a), 2)` and `unless(-flies(b), 2)`, recording the exceptions on
which the answers depend.

## Negative evidence against a default

[`bird_exception.gkp`](bird_exception.gkp) and
[`bird_exception.js`](bird_exception.js) add:

```prolog
0.9::-flies(a).
```

The exception does not have enough priority to eliminate the priority-2
default, but it
provides negative evidence against the answer:

```text
b  confidence 1.0
a  confidence 0.1, conflict 0.9
```

[`bird_hierarchy.js`](bird_hierarchy.js) uses an ordinary rule without a
blocker, providing a control case for the same confidence calculation.

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

The two defaults have equal priority. One supports `pacifist(n)` and the other
supports its negation. The candidate `dislikeswar(n)` is reported with a zero
margin and a `CONTESTED` flag; no rule-order tie breaker is used.
[`nixon_taxonomy.js`](nixon_taxonomy.js) asks the direct pacifism question with
taxonomy-style priorities.

## Numeric and taxonomy priorities

The `penguin*.js` files build a hierarchy from organism to bird, penguin, and
flying penguin, with opposing flight defaults at different priorities.
[`penguin2.js`](penguin2.js) uses numeric priorities.
[`penguin3.js`](penguin3.js) uses taxonomy priorities and therefore requires:

```sh
./bin/gk Examples/exceptions/penguin3.js \
  -defaults -datafolder Examples/exceptions
```

The auxiliary files in this directory map names to taxonomy nodes and store
the hierarchy. [`penguin4.js`](penguin4.js) applies the same pattern to nested
function terms.

[`penguin.gkp`](penguin.gkp) and [`penguin.js`](penguin.js) are compact cases
with a strict penguin exception and two opposed defaults. The stronger flight
default prevails for the ordinary bird; the penguin has full negative support.

## Classification from parts

[`classify.gkp`](classify.gkp) and [`classify.js`](classify.js) classify three
objects from observed parts. Several uncertain defaults may support the same
class, while strict engine evidence supports `-isa(X, organism)`.

```sh
./bin/gk Examples/exceptions/classify.gkp \
  -defaults -datafolder Examples/exceptions
```

Principal results:

```text
h1  accepted, confidence 0.44
b1  accepted through the bird path, confidence 0.5552
a1  rejected with negative confidence 1
```

The `b1` assessment also contains an opposed airplane path. The detailed proof
shows which classification defaults were pooled and which supplied negative
evidence.

## Persistence across situations

[`people_room.js`](people_room.js) represents entry and exit events across
three situations. Frame rules use blockers to carry `in` and `-in` forward
unless an event changes them. The example contains contested states; use
`-detail -confidence 0` to inspect the positive and negative event
paths:

```sh
./bin/gk Examples/exceptions/people_room.js \
  -detail -confidence 0
```

## Equivalent input notations

[`bird_penguin.gkp`](bird_penguin.gkp),
[`bird_penguin.js`](bird_penguin.js), and
[`bird_penguin.p`](bird_penguin.p) encode one problem in GKP,
JSON-LD-LOGIC, and TPTP. They are useful for inspecting conversion and output
format differences.

## Additional cases

| Files | Main feature |
|---|---|
| `hierarchy.js`, `taxonomy.js` | compact specificity and hierarchy cases |
| `gbirds.js` | bird/penguin default with an ASP comparison in comments |
| `gbirds_funsymbs.js` | the same pattern with function symbols |
| `trivial.js` | plain facts and one closed query, with no defaults |
| `gk_name_number.txt`, `gk_taxonomy_packed.txt` | data loaded by `-defaults` |

The blocker and confidence algorithms are described in
[`../../Doc/how_gk_works.md`](../../Doc/how_gk_works.md).
