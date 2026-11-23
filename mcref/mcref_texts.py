"""mcref_texts: the texts of the field `interpretation` of mcref's output and of the variants of the exception
pass."""
BACKBONE_TEXT = {
  "judge": "in each world the applications without an exception literal that are not normal defaults are "
           "evaluated first, alone; an application with an exception literal that this evaluation establishes "
           "(its atom positive for a positive literal, negative for a negative one) is removed in that world; all "
           "atoms are then evaluated from the remaining applications, in groups formed from them; then every "
           "removed application none of whose exception literals established in the first evaluation is usable "
           "in that result is restored, and all atoms are evaluated again, until no application is restored; a "
           "restored application is never removed again; no state of the first evaluation is kept",
  "fix": "in each world the applications without an exception literal that are not normal defaults are evaluated "
         "first, alone; an atom positive, negative or in conflict there keeps that state; the other atoms are then "
         "evaluated from all applications, a kept atom read as a fact of its state, in groups formed without the "
         "dependencies of the kept atoms",
}
LAYERS_TEXT = ("the layers of signed literals; for each layer, lowest first, an evaluation without the applications "
               "of that layer and above and without those removed before, and the removal of the applications of "
               "the layer whose external exception literal is usable there; then an evaluation of all applications "
               "that are not removed, and the restore step, repeated until no application is restored "
               "(Doc/support_semantics.md, Section 11.9)")
CASES_TEXT = ("proofs by cases: the certain clauses without exception literals and the uncertain disjunctions "
              "without them prove a literal by cases over case hypotheses; a rule with a written head that is "
              "uncertain or has exception literals, and is not a normal default, is a leaf of a proof at its head "
              "only, not a clause to split on; a premise that is not a hypothesis, and the event of an uncertain "
              "clause used, stay requirements; the exception literals of every rule used are kept, and so is the "
              "identity of every uncertain rule used; a proof with no hypothesis left gives an application from "
              "its requirements with the kept exception literals; the strength of a side is the probability that "
              "at least one present application has all its uncertain rules, each rule counted once and different "
              "rules independent; above a limit the input is evaluated without them, with a reading; normal "
              "defaults take no part in proofs by cases")
PROOFS_TEXT = ("every minimal proof (L, G) of several statements, found by resolution on clauses with the set of "
               "statements they come from, gives an application: as body every single literal that G and the "
               "non-goal clauses imply; as listed clauses the non-goal clauses of several literals, which must not "
               "be contradicted in the world; the exception literals of every statement of L; the identities of its "
               "uncertain rules, each rule counted once in the strength of a side. A rule with a written head that "
               "is uncertain or has an exception takes part only in the proofs of its own head; a normal default "
               "takes part too, and a proof with normal defaults of the proved literal is a normal default of the "
               "smallest of their ranks. A proof whose application another application makes redundant is dropped. "
               "A listed clause inside a cycle is evaluated by the clause rule in a cycle "
               "(Doc/support_semantics.md, Sections 11.4 and 11.8)")
INTERPRETATION = {
  "semantics": "the support semantics of Doc/support_semantics.md; the reference definitions are in its Section 11",
  "exception pass": BACKBONE_TEXT["judge"],
  "rules with a written head": "a certain rule without exception literals is used in every direction; below "
                               "confidence 1 or with an exception literal, at its written head only "
                               "(Doc/support_semantics.md, Section 11.3)",
  "clauses": "one application per literal; one event per uncertain ground statement of several literals",
  "clauses without a written head": "with the proofs of several statements, such a clause takes part in proofs in "
                                    "every direction, also with a confidence or exception literals; a proof that "
                                    "uses it keeps its exception literals as external exceptions and, when it is "
                                    "uncertain, has its event as a premise",
  "no self-support": "an application with head L is left out when one of its body literals cannot be derived "
                     "without the applications that have head L (exceptions and opposition ignored); one pass, "
                     "before the applications whose body can never hold are left out (Doc/support_semantics.md, "
                     "Section 11.4)",
  "blocked-rule repair": "in every evaluation of the exception pass, the applications held out or removed are absent "
                         "from the whole preparation: no self-support, the rule for a body that can never hold, the "
                         "concluded literals and the groups are made again on the others; one preparation per set "
                         "of absent applications (Doc/support_semantics.md, Section 11.9)",
  "clause rule without a result": "when the clause rule in a cycle has no result, an atom of the group with the same "
                                  "state in every evaluation the rule made keeps it, and the others get no value; "
                                  "when the rule stops at a check that cannot be decided, one more evaluation with "
                                  "every listed clause whose check is open or contradicted counted as contradicted "
                                  "comes first (Doc/support_semantics.md, Section 11.8)",
  "head read from a default": "a statement whose consequent has several literals and which has exception literals "
                              "has the written head L when exactly one exception literal is the opposite of a "
                              "consequent literal L, and of exactly one; compared as written, before grounding "
                              "(Doc/support_semantics.md, Section 11.1); for .gkp input gk's converter reads it, "
                              "for JSON input this reader",
  "not represented": "a classical consequence that needs several input statements at once",
  "domain": "the constants of the input",
  "kind of a side": "decided in each world from the applications present in it (Doc/support_semantics.md, "
                    "Section 5.5)",
  "groups": "a sweep group (no cycle across signs, no exception literal in the group, no normal default for or "
            "against an atom of the group, no outside atom without a value) by sweeps, which settle; every other "
            "group by the narrowing, ordinary applications first when the group has normal defaults, an atom left "
            "open read as ignorance when the group has no cycle across signs and no outside atom without a value "
            "(Doc/support_semantics.md, Section 11.7)",
  "no value": "an atom of a cycle across signs left possible but not sure; a group that depends on an atom without a "
              "value runs the narrowing with that atom's two literals possible and neither sure, and an atom of it "
              "left possible but not sure has no value too (Doc/support_semantics.md, Section 11.7)",
  "rank contexts": "not covered; an input where they can matter is declined",
  "self exception": "an application whose exception literal is its own body literal never applies",
}
