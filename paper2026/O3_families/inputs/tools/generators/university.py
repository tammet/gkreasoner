"""Generation functions of the university base in the pattern of LUBM (family G),
copied unchanged from the trial's generator of 2026-11-04. usable_rules needs the list
RULES, read from univ_bench_rules.pl by generate.py."""
import random, re

RULES = []


def university(ndept, seed, scale=1.0):
  rnd = random.Random(seed)
  facts = []
  univ = 'univ0'
  facts.append(f'university({univ})')
  people = []
  for d in range(ndept):
    dept = f'dept{d}'
    facts += [f'department({dept})', f'subOrganizationOf({dept},{univ})']
    profs = []
    for kind, n in (('fullProfessor', int(8 * scale)), ('associateProfessor', int(10 * scale)), ('assistantProfessor', int(10 * scale)), ('lecturer', int(5 * scale))):
      for i in range(max(1, n)):
        p = f'{kind[:4]}{i}_d{d}'; profs.append(p)
        facts += [f'{kind}({p})', f'worksFor({p},{dept})', f'doctoralDegreeFrom({p},univ{rnd.randint(0,9)})',
                  f'emailAddress({p},mail_{p})', f'researchInterest({p},res{rnd.randint(0,19)})']
    facts.append(f'headOf({profs[0]},{dept})')
    courses = [f'course{i}_d{d}' for i in range(int(20 * scale))] + [f'gradCourse{i}_d{d}' for i in range(int(10 * scale))]
    for c in courses:
      facts.append(('graduateCourse' if c.startswith('grad') else 'course') + f'({c})')
      facts.append(f'teacherOf({rnd.choice(profs)},{c})')
    students = []
    for i in range(int(150 * scale)):
      s = f'ugrad{i}_d{d}'; students.append(s)
      facts += [f'undergraduateStudent({s})', f'memberOf({s},{dept})']
      for c in rnd.sample(courses[:len(courses) * 2 // 3], 2):
        facts.append(f'takesCourse({s},{c})')
      if rnd.random() < 0.2:
        facts.append(f'advisor({s},{rnd.choice(profs)})')
    for i in range(int(40 * scale)):
      s = f'grad{i}_d{d}'; students.append(s)
      facts += [f'graduateStudent({s})', f'memberOf({s},{dept})', f'undergraduateDegreeFrom({s},univ{rnd.randint(0,9)})',
                f'advisor({s},{rnd.choice(profs)})']
      for c in rnd.sample(courses[len(courses) * 2 // 3:], 2):
        facts.append(f'takesCourse({s},{c})')
      if rnd.random() < 0.3:
        facts.append(f'teachingAssistantOf({s},{rnd.choice(courses[:len(courses) * 2 // 3])})')
    for i in range(int(60 * scale)):
      pub = f'pub{i}_d{d}'
      facts.append(f'publication({pub})')
      facts.append(f'publicationAuthor({pub},{rnd.choice(profs)})')
      if rnd.random() < 0.5:
        facts.append(f'publicationAuthor({pub},{rnd.choice(students)})')
    people.append((profs[1], students[-1]))
  return facts, people


def usable_rules(facts):
  """keep the rules whose body predicates are defined by facts or by kept rule heads
  (ProbLog rejects a body predicate with no clauses)"""
  import re
  defined = set(re.match(r'(\w+)\(', f).group(1) for f in facts)
  rules = list(RULES); kept = []
  changed = True
  while changed:
    changed = False
    for r in rules:
      if r in kept: continue
      head, body = r[:-1].split(' :- ')
      preds = re.findall(r'(\w+)\(', body)
      if all(p in defined for p in preds):
        kept.append(r); defined.add(re.match(r'(\w+)\(', head).group(1)); changed = True
  return kept


