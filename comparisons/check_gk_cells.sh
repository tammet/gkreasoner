#!/bin/sh
# Rerun the 18 gk cells of the comparison table with gk's default method,
# the recursive method, and compare each output with its capture in
# results/raw/. Uses only the gk binary; no external system is involved.
# Exit status 0 means every cell reproduced.
#
# The comparison reads the first output line, {"recursive": ...}, of the
# new run and of the capture. It compares these fields: question, value,
# answers (answer and value of each), readings and stop. Numbers are
# rounded to 6 decimals first. It ignores the other fields of the line,
# which include the times budget_used_ms and switches, and the dump that
# follows the line. python3 reads the JSON line.
#
# Since gk 1.2.5 the line writes the question and the answers as JSON
# literals, ["q","a"], where gk 1.2.4 and earlier wrote the text "q(a)". The
# script turns a JSON literal into that text before it compares, so the
# captures of gk 1.2.3 and the output of a newer gk compare alike.
#
# Usage, from the repository root or from comparisons/:
#   comparisons/check_gk_cells.sh
#   GK=<path> comparisons/check_gk_cells.sh    (another gk binary)
cd "$(dirname "$0")" || exit 1
GK=${GK:-../bin/gk}
RAW=results/raw
if [ ! -x "$GK" ]; then
  echo "gk binary not found or not executable: $GK" >&2
  exit 1
fi
if ! command -v python3 > /dev/null 2>&1; then
  echo "python3 not found; it reads the JSON line" >&2
  exit 1
fi
STABLE='
import json, sys
text = open(sys.argv[1]).read()
if "\n[stdout]\n" in text:
  text = text.split("\n[stdout]\n", 1)[1]
line = text.split("\n", 1)[0]
try:
  r = json.loads(line)["recursive"]
except Exception:
  print("no {\"recursive\": ...} line")
  sys.exit(0)
def term_text(t):
  # a term or literal of the JSON form as the text of gk 1.2.4
  if isinstance(t, bool):
    return "true" if t else "false"
  if isinstance(t, int):
    return str(t)
  if isinstance(t, float):
    for p in range(1, 18):
      s = "%.*g" % (p, t)
      if float(s) == t:
        break
    return s if any(c in s for c in ".eni") else s + ".0"
  if isinstance(t, str):
    if t.startswith("?:X"):
      return "_V" + t[3:]
    if t.startswith(":"):
      return t[1:]
    return t
  if isinstance(t, list) and t:
    if len(t) == 1:
      return term_text(t[0])
    return term_text(t[0]) + "(" + ",".join(term_text(a) for a in t[1:]) + ")"
  return str(t)
def lit_text(x):
  # text and None stay as they are
  return x if x is None or isinstance(x, str) else term_text(x)
def rnd(x):
  if isinstance(x, float):
    return round(x, 6)
  if isinstance(x, list):
    return [rnd(y) for y in x]
  if isinstance(x, dict):
    return {k: rnd(v) for k, v in x.items()}
  return x
answers = sorted(([lit_text(a.get("answer")), rnd(a.get("value"))] for a in r.get("answers", [])), key=str)
keep = {"question": lit_text(r.get("question")), "value": rnd(r.get("value")),
        "answers": answers, "readings": rnd(r.get("readings")), "stop": r.get("stop")}
print(json.dumps(keep, sort_keys=True))
'
tmp=$(mktemp -d) || exit 1
trap 'rm -rf "$tmp"' EXIT
fail=0
for pair in \
  c1:gk_c1 c2:gk_c2 d1:gk_d1 d2:gk_d2 d3:gk_d3 d4:gk_d4 \
  d4sm_pos:gk_d4sm_pos d4sm_neg:gk_d4sm_neg d5:gk_d5 \
  d6_undercut:gk_d6_undercut d6_rebut:gk_d6_rebut d7:gk_d7 \
  e1:gk_e1 x1:gk_x1 f1:gk_f1 dj1:gk_dj1 \
  n1_study4:gk_n1 n2_study10:gk_n2
do
  input=${pair%%:*}
  run=${pair#*:}
  if [ ! -f "$RAW/$run.txt" ]; then
    echo "FAIL: $run has no capture $RAW/$run.txt"
    fail=1
    continue
  fi
  "$GK" "inputs/gk/$input.gkp" > "$tmp/out" 2> /dev/null
  python3 -c "$STABLE" "$tmp/out" > "$tmp/new"
  python3 -c "$STABLE" "$RAW/$run.txt" > "$tmp/recorded"
  if diff -q "$tmp/new" "$tmp/recorded" > /dev/null; then
    echo "pass: $run"
  else
    echo "FAIL: $run differs from $RAW/$run.txt"
    echo "  new:      $(cat "$tmp/new")"
    echo "  recorded: $(cat "$tmp/recorded")"
    fail=1
  fi
done
exit $fail
