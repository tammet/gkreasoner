#!/usr/bin/env python3
"""check_gk.py: rerun the gk and tool runs of one or more parts of this folder and compare every value with the
recorded one in the part's results.csv.

  python3 check_gk.py --part O1_tweety --gk PATH/TO/gk --mcref PATH/TO/mcref.py
  python3 check_gk.py --part O18_lifschitz --part O14_routes --gk ... --mcref ... --jobs 2
  python3 check_gk.py --all --gk ... --mcref ...          every part (several hours)

Options:
  --part NAME    a part folder (repeatable)
  --all          every part with gk or tool runs
  --gk PATH      the gk binary for every gk run; or, repeated, VERSION=PATH (for example 1.3.2=PATH): the binary
                 of one build, used for the runs that this build made (the column system of runs.tsv). A run
                 whose build has no binary of its own uses the plain PATH
  --mcref PATH   the tool's mcref.py (mcref 1.3.1); without it the tool runs are skipped
  --jobs N       runs at the same time (default 1). Runs whose time is reported ran one at a time.
  --out FILE     write one line per compared value (tab-separated) to FILE

Every run of runs.tsv whose system is gk or the tool runs in its folder (the column cwd) with its command; $GK
and $MCREF are replaced by the given paths, and the tool gets MCREF_GK=PATH/TO/gk. A part whose inputs are
packed in inputs/*.tar.xz is unpacked into a temporary folder first; the check never writes into this folder.

A value equals the recorded one within 1.5e-6 (gk prints six decimals). The mark complete and the method that
answered are compared too. A run that did not end by itself (column ended_by_itself = no) used its time limit,
so its value can change from run to run; a difference on such a run is reported apart and is no failure. The
same holds when the rerun reports cut or queued searches (gk's search state "searches were cut or not run"):
its value then depends on the time budget and on the load of the machine.
Exit status 0 means that every other compared value is equal. Python 3.9 or later, no other package.
"""
import argparse
import csv
import gzip
import os
import shlex
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import threading
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gkline as GL  # noqa: E402

csv.field_size_limit(1 << 30)
SYSTEMS = ("gk ", "mcref")


def read(path, delim=","):
  """a CSV or TSV file; a large file is stored compressed as NAME.gz"""
  if not os.path.exists(path) and os.path.exists(path + ".gz"):
    f = gzip.open(path + ".gz", "rt", newline="")
  else:
    f = open(path, newline="")
  with f:
    return list(csv.DictReader(f, delimiter=delim))


def unpack(part, tmp):
  """the packed inputs of a part, unpacked into tmp; returns {folder prefix: unpacked folder}"""
  out = {}
  d = os.path.join(ROOT, part, "inputs")
  if not os.path.isdir(d):
    return out
  for fn in sorted(os.listdir(d)):
    if fn.endswith(".tar.xz"):
      dst = os.path.join(tmp, part)
      os.makedirs(dst, exist_ok=True)
      with tarfile.open(os.path.join(d, fn)) as tf:
        tf.extractall(dst)
      out[os.path.join(part, "inputs")] = dst
  return out


def place(cwd, part, packs):
  """the folder in which a run starts: the folder itself, or the unpacked copy of a packed input folder"""
  p = os.path.normpath(os.path.join(ROOT, cwd))
  if os.path.isdir(p):
    return p
  for pre, dst in packs.items():
    if cwd == pre or cwd.startswith(pre + "/"):
      q = os.path.join(dst, os.path.relpath(cwd, os.path.dirname(pre)))
      if os.path.isdir(q):
        return q
  return None


def command(run, gk, mcref):
  words = shlex.split(run["command"])
  env = dict(os.environ)
  while words and "=" in words[0] and not words[0].startswith("-") and words[0].split("=")[0].isupper():
    k, v = words.pop(0).split("=", 1)
    env[k] = v.replace("$GK", gk)
  words = [w.replace("$GK", gk).replace("$MCREF", mcref or "") for w in words]
  env["MCREF_GK"] = gk
  return words, env


def execute(words, cwd, env, timeout):
  t0 = time.time()
  p = subprocess.Popen(words, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL, start_new_session=True)
  try:
    out, _ = p.communicate(timeout=timeout)
    timed_out = False
  except subprocess.TimeoutExpired:
    os.killpg(p.pid, signal.SIGKILL)
    out, _ = p.communicate()
    timed_out = True
  try:
    os.killpg(p.pid, signal.SIGKILL)
  except ProcessLookupError:
    pass
  return out.decode("utf-8", "replace"), time.time() - t0, timed_out


def rerun_cut(parsed):
  """True when a gk rerun reports cut or queued searches: its value depends on the time budget"""
  if (parsed.get("tasks_cut") or 0) > 0 or (parsed.get("tasks_queued") or 0) > 0:
    return True
  return "cut or not run" in str(parsed.get("search") or "")


def compare(run, rows, out):
  """one line per recorded value: (status, run_id, question, recorded, new, detail)"""
  res = []
  is_tool = run["system"].startswith("mcref")
  parsed = GL.parse_tool(out) if is_tool else GL.parse_gk(out)
  cut = not is_tool and rerun_cut(parsed)
  for r in rows:
    if not r.get("value") or GL.read_value(r["value"]) is None:
      continue
    rec = GL.read_value(r["value"])
    if is_tool:
      new, _ = GL.tool_value(parsed, r["question"])
    else:
      new, _ = GL.gk_value(parsed, r["question"])
    detail = []
    ok = GL.close(rec, new, 1.5e-6)
    if not is_tool and ok:
      c = None
      for a in parsed.get("answers") or []:
        if GL.norm(a["lit"]) in (GL.norm(r["question"]), GL.negate(r["question"])):
          c = a.get("complete")
      mark = "" if parsed.get("answered_by") != "exact" else ("yes" if c is True else "no")
      if parsed.get("answered_by") == "exact" and parsed.get("covered") is False:
        mark = "no"
      if r.get("answered_by") and parsed.get("answered_by") != r["answered_by"]:
        ok = False
        detail.append("answered by %s, recorded %s" % (parsed.get("answered_by"), r["answered_by"]))
      if (r.get("complete") or "") != mark:
        ok = False
        detail.append("complete %r, recorded %r" % (mark, r.get("complete")))
    if ok:
      status = "equal"
    elif r.get("ended_by_itself") == "no":
      status = "differs, the run used its time limit"
    elif cut:
      status = "differs, the run used its time limit"
      detail.append("the rerun reports cut or queued searches")
    else:
      status = "differs"
    res.append((status, r["run_id"], r["question"], r["value"], GL.fmt(new), "; ".join(detail)))
  return res


def main():
  ap = argparse.ArgumentParser(
    description="Rerun the gk and tool runs of one or more parts of this folder and compare every value with the "
                "recorded one in the part's results.csv. Exit status 0 means that every compared value is equal, "
                "apart from the runs whose value depends on the time limit.",
    epilog="Example, from this folder: python3 check_gk.py --part O18_lifschitz --gk $GK --mcref $MCREF")
  ap.add_argument("--part", action="append", default=[], metavar="NAME",
                  help="a part folder, for example O1_tweety; repeat it for several parts")
  ap.add_argument("--all", action="store_true", help="every part with gk or tool runs (many hours)")
  ap.add_argument("--gk", required=True, action="append", metavar="PATH",
                  help="the gk binary for every gk run; or, repeated, VERSION=PATH: the binary of one build, used "
                       "for the runs of that build (column system of runs.tsv)")
  ap.add_argument("--mcref", metavar="PATH",
                  help="the tool's mcref.py (mcref 1.3.1); without it the tool runs are skipped")
  ap.add_argument("--jobs", type=int, default=1, metavar="N",
                  help="runs at the same time (default 1); the runs whose time is reported run one at a time")
  ap.add_argument("--out", metavar="FILE", help="write one tab-separated line per compared value to FILE")
  a = ap.parse_args()
  per_build, plain = {}, None
  for x in a.gk:
    if "=" in x and not os.path.exists(x):
      ver, path = x.split("=", 1)
      per_build["gk " + ver] = os.path.abspath(path)
    else:
      plain = os.path.abspath(x)
  gk = plain or sorted(per_build.items())[-1][1]

  def gk_of(run):
    """the binary for a run: the one of its build, else the plain one"""
    return per_build.get(run["system"], gk) if run["system"].startswith("gk ") else gk
  mcref = os.path.abspath(a.mcref) if a.mcref else None
  parts = a.part
  if a.all:
    parts = sorted(d for d in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT, d, "runs.tsv"))
                   or os.path.isfile(os.path.join(ROOT, d, "runs.tsv.gz")))
  if not parts:
    ap.error("name a part with --part, or give --all")
  tmp = tempfile.mkdtemp(prefix="check_gk_")
  jobs = []
  for part in parts:
    runs = read(os.path.join(ROOT, part, "runs.tsv"), "\t")
    results = read(os.path.join(ROOT, part, "results.csv"))
    by_run = {}
    for r in results:
      by_run.setdefault(r["run_id"], []).append(r)
    packs = unpack(part, tmp)
    for run in runs:
      if not run["system"].startswith(SYSTEMS) or run["run_id"] not in by_run:
        continue
      if run["system"].startswith("mcref") and not mcref:
        continue
      jobs.append((part, run, by_run[run["run_id"]], packs))
  lines, lock = [], threading.Lock()
  counts = {"equal": 0, "differs": 0, "differs, the run used its time limit": 0, "not run": 0}

  def one(job):
    part, run, rows, packs = job
    cwd = place(run["cwd"], part, packs)
    if cwd is None:
      with lock:
        counts["not run"] += 1
        print("not run: %s (folder %s missing)" % (run["run_id"], run["cwd"]))
      return
    words, env = command(run, gk_of(run), mcref)
    limit = float(run["limit_s"] or 10)
    timeout = 900 if run["system"].startswith("mcref") else limit + 60
    out, secs, timed_out = execute(words, cwd, env, timeout)
    res = compare(run, rows, out)
    with lock:
      for x in res:
        counts[x[0]] += 1
        lines.append((part,) + x)
        if x[0] != "equal":
          print("%s: %s %s: recorded %s, now %s %s" % (x[0], x[1], x[2], x[3], x[4], x[5]))

  timed = [j for j in jobs if j[1].get("timed_alone") == "yes"]
  rest = [j for j in jobs if j[1].get("timed_alone") != "yes"]
  threads = []
  for j in rest:
    while len([t for t in threads if t.is_alive()]) >= max(1, a.jobs):
      time.sleep(0.05)
    t = threading.Thread(target=one, args=(j,))
    t.start()
    threads.append(t)
  for t in threads:
    t.join()
  for j in timed:
    one(j)
  shutil.rmtree(tmp, ignore_errors=True)
  if a.out:
    with open(a.out, "w") as f:
      f.write("part\tstatus\trun_id\tquestion\trecorded\tnow\tdetail\n")
      for x in sorted(lines):
        f.write("\t".join(x) + "\n")
  print("%d runs; values compared: %d equal, %d differ, %d differ on runs that used their time limit; "
        "%d runs not run" % (len(jobs), counts["equal"], counts["differs"],
                             counts["differs, the run used its time limit"], counts["not run"]))
  sys.exit(1 if counts["differs"] or counts["not run"] else 0)


if __name__ == "__main__":
  main()
