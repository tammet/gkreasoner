#!/usr/bin/env python3
"""Rerun the gk and mcref runs of this folder and compare them with the
recorded results.

Every part folder (O1_tweety, O2_record, ...) has a file runs.tsv with one
row per run and a file results.tsv with one row per result; a result names
its run in the column run. This script reruns every gk run, and with
--mcref also every mcref run, and compares each new value with every
result that names the run, at the precision of the recorded number: .396
matches a new value from .3955 to .3965. In part O2 it also compares the
shares of every row of rows.tsv. It never writes into the folder.

Usage, from the repository root (the folder that holds bin/ and mcref/):

  python3 paper2026/check_gk.py                 all gk runs
  python3 paper2026/check_gk.py --part O1       the gk runs of part O1
  python3 paper2026/check_gk.py --mcref         the gk runs and the mcref runs
  python3 paper2026/check_gk.py --gk PATH       another gk binary
  python3 paper2026/check_gk.py --jobs 3        runs at the same time (default 3)

A run marked alone=yes in runs.tsv depends on gk's deadline or on the
machine load: its value or its time can change from run to run. Such runs
run one at a time after the others, and a difference is reported as
"alone" and not counted as a failure. Needs Python 3.9 or later and no
other package. Exit status 0 means that every other compared row matched.
"""
import argparse, os, shutil, sys, tempfile, threading

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "tools"))
import run_store as RS  # noqa: E402
import collect as C     # noqa: E402
import gkout as G       # noqa: E402


def rerun(r, paths, timeout, scratch):
  """run one row of runs.tsv; an entry like a stored run's"""
  outdir = None
  if "{outdir}" in (r.get("options") or ""):
    outdir = tempfile.mkdtemp(prefix="checkpoints_", dir=scratch)
  input_path = os.path.normpath(os.path.join(r["part_folder"], r["input"]))
  cmd, cwd, env = RS.command(r, input_path, paths, outdir)
  out, secs, timed_out, code = run(cmd, cwd, env, timeout)
  files = {}
  if outdir:
    for name in sorted(os.listdir(outdir)):
      files[name] = open(os.path.join(outdir, name), "rb").read()
    shutil.rmtree(outdir, ignore_errors=True)
  return {"stdout": out, "stderr": "", "out": files,
          "status": {"exit": code, "elapsed_s": secs, "timed_out": timed_out, "peak_rss_kb": 0}}


def run(cmd, cwd, env, timeout):
  import signal, subprocess, time
  t0 = time.time()
  p = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
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
  return out.decode("utf-8", "replace"), time.time() - t0, timed_out, p.returncode


def o2_rows(folder):
  path = os.path.join(folder, "rows.tsv")
  if not os.path.isfile(path):
    return {}
  _, rows = RS.read_tsv(path)
  by_run = {}
  for x in rows:
    for col in ("gk_run", "mcref_run"):
      by_run.setdefault(x[col], []).append((col, x))
  return by_run


def check_o2(entry, tool, rows):
  """the shares of the rows of rows.tsv against the new output"""
  ans = dict(G.gk_answers(entry["stdout"]) or []) if tool == "gk" else dict(G.mcref_answers(entry["stdout"]) or [])
  bad = []
  for col, x in rows:
    rec = x["gk"] if tool == "gk" else x["mcref"]
    if not rec:
      continue
    want = [float(v) for v in rec.strip("[]").split(",")]
    got = ans.get(x["answer"])
    if got is None and tool == "gk" and len(ans) == 1:
      got = list(ans.values())[0]      # a closed question: gk names the question, the tool the answer
    if got is None or any(abs(a - b) > 1e-6 for a, b in zip(want, got)):
      bad.append("%s %s: recorded %s, now %s" % (x["input"], x["answer"], rec,
                                                 G.shares_text(got) if got else "no value"))
  return bad


def main():
  ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
  ap.add_argument("--gk", default=os.path.join(ROOT, "bin", "gk"))
  ap.add_argument("--mcref", action="store_true")
  ap.add_argument("--part", default="")
  ap.add_argument("--jobs", type=int, default=3)
  ap.add_argument("--timeout", type=float, default=0, help="seconds per run; default the timeout_s of runs.tsv")
  a = ap.parse_args()
  if not os.access(a.gk, os.X_OK):
    sys.exit("gk binary not found or not executable: " + a.gk)
  paths = {"gk": os.path.abspath(a.gk), "mcref": os.path.join(ROOT, "mcref", "mcref.py")}
  tools = ("gk", "mcref") if a.mcref else ("gk",)
  work = []
  for folder in RS.part_folders([a.part] if a.part else []):
    part = os.path.basename(folder)
    _, results = RS.read_tsv(os.path.join(folder, "results.tsv")) if os.path.isfile(
      os.path.join(folder, "results.tsv")) else ([], [])
    by_run = {}
    for x in results:
      if x.get("run"):
        by_run.setdefault(x["run"], []).append(x)
    o2 = o2_rows(folder)
    for r in RS.run_list(folder):
      if r["tool"] in tools and (by_run.get(r["run_id"]) or o2.get(r["run_id"])):
        work.append(dict(r, part=part, part_folder=folder, results=by_run.get(r["run_id"], []),
                         o2=o2.get(r["run_id"], [])))
  scratch = tempfile.mkdtemp(prefix="check_gk_")
  lock = threading.Lock()
  tally = {"ok": 0, "DIFF": 0, "alone": 0}
  def one(r):
    timeout = a.timeout or float(r.get("timeout_s") or 600)
    e = rerun(r, paths, timeout, scratch)
    lines = []
    for x in r["results"]:
      text, values, declined = C.stored_value(r["tool"], e, r)
      v = C.compare(x, r["tool"], values, declined, e)
      if v == "not compared":
        continue
      lines.append((v, "%s/%s: recorded %s, now %s, %.1f s" % (r["part"], x["id"], x["result"], text,
                                                                 e["status"]["elapsed_s"])))
    if r["o2"]:
      bad = check_o2(e, r["tool"], r["o2"])
      lines.append(("DIFF" if bad else "ok", "%s/%s: %d rows of rows.tsv%s, %.1f s" % (
        r["part"], r["run_id"], len(r["o2"]), "; " + "; ".join(bad) if bad else "", e["status"]["elapsed_s"])))
    with lock:
      for v, line in lines:
        if v == "DIFF" and r.get("alone") == "yes":
          v = "alone"
          line += " (a run marked alone: its value can depend on the deadline or the machine load)"
        tally[v] = tally.get(v, 0) + 1
        print("%-5s %s" % (v, line), flush=True)
  shared = [r for r in work if r.get("alone") != "yes"]
  queue, qlock = list(shared), threading.Lock()
  def worker():
    while True:
      with qlock:
        if not queue:
          return
        r = queue.pop(0)
      one(r)
  threads = [threading.Thread(target=worker) for _ in range(max(1, min(a.jobs, len(queue))))]
  for t in threads:
    t.start()
  for t in threads:
    t.join()
  for r in work:
    if r.get("alone") == "yes":
      one(r)
  shutil.rmtree(scratch, ignore_errors=True)
  print("%d runs rerun; compared rows: %d match, %d differ, %d differ in runs marked alone" % (
    len(work), tally["ok"], tally["DIFF"], tally["alone"]))
  sys.exit(1 if tally["DIFF"] else 0)


if __name__ == "__main__":
  main()
