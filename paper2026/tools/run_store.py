#!/usr/bin/env python3
"""Run every run of the run lists and keep each result in a run store.

Each part folder (O1_tweety, O2_record, ...) has a file runs.tsv with one
row per run. This script computes the store key of every row, skips every
key that the store already holds, and runs the rest. The store keeps every
finished run: the command, the standard output, the standard error and the
exit status. A run is never repeated: a later call runs only the rows whose
key is new, for example after an input changed or a row was added.

The key of a run is the SHA-256 of a JSON object with: the tool; the SHA-256
of the executable (for mcref: of mcref.py, mcref_read.py and the gk binary
it calls); the SHA-256 of the input and of every file the input includes or
reads, each with its path relative to the input's folder; the options; the
settings. The path of the input is not part of the key, so a part folder can
move without losing its runs.

Usage, from the folder that holds bin/, mcref/ and paper2026/:

  python3 paper2026/tools/run_store.py --store STORE            all parts
  python3 paper2026/tools/run_store.py --store STORE O1 O2      two parts
  python3 paper2026/tools/run_store.py --store STORE --dry-run  list only
  python3 paper2026/tools/run_store.py --store STORE --force KEY

STORE defaults to the environment variable PAPER2026_STORE. The script can
be stopped at any moment, also with kill -9, and restarted with the same
command: it then runs only what is missing.

Columns of runs.tsv: run_id, tool, input, options, settings, alone,
timeout_s, and optionally reads. The input is relative to the part folder.
The options are passed to the tool; a token {input} stands for the input
file, otherwise the input comes first; a token {outdir} stands for a
folder of the run's own (gk's -checkpoints writes its dumps there). The settings are key=value pairs:
for mcref "samples=20000 seed=1". A row with alone=yes runs with no other
run active. The column reads names further files that the run reads,
relative to the input's folder, separated by spaces.

The store, one directory per key:

  STORE/<key[0:2]>/<key>/run.json      key object, command, folder, times, load, host
  STORE/<key[0:2]>/<key>/stdout.gz
  STORE/<key[0:2]>/<key>/stderr.gz
  STORE/<key[0:2]>/<key>/status.json   exit code, wall time, peak RSS, timeout flag
  STORE/<key[0:2]>/<key>/out.tar.gz    the files written into {outdir}, if the options name it
  STORE/log.jsonl                      one line per finished run
  STORE/running/                       runs in progress; cleared at the next start

A directory in its final place is a finished run. The runner writes into
STORE/running/<key>.<pid>/ and renames the directory only after status.json is
written. Python 3.9 or later, standard library only. Linux.
"""
import argparse, fcntl, glob, gzip, hashlib, json, os, platform, re, shlex
import shutil, signal, socket, subprocess, sys, tarfile, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)                 # paper2026/
ROOT = os.path.dirname(FOLDER)                 # the folder with bin/ and mcref/
COLUMNS = ("run_id", "tool", "input", "options", "settings", "alone", "timeout_s")
STORE_FORMAT = 1


def sha256_file(path):
  h = hashlib.sha256()
  with open(path, "rb") as f:
    for block in iter(lambda: f.read(1 << 20), b""):
      h.update(block)
  return h.hexdigest()


# --- the tools ---------------------------------------------------------------

def tool_paths(args):
  """the executable of each tool. An external tool comes from --tool
  NAME=COMMAND, where COMMAND is a program, or a program and its first
  arguments ("venv/bin/python -m clingo"); otherwise from the program
  search path"""
  paths = {"gk": os.path.abspath(args.gk),
           "mcref": os.path.abspath(args.mcref)}
  for item in args.tool or []:
    name, _, cmd = item.partition("=")
    words = shlex.split(cmd)
    words[0] = os.path.abspath(words[0]) if os.sep in words[0] else (shutil.which(words[0]) or words[0])
    paths[name] = words
  return paths


class ToolMissing(Exception):
  pass


def external_prefix(tool, paths):
  words = paths.get(tool)
  if words:
    return list(words)
  exe = shutil.which(tool)
  if not exe:
    raise ToolMissing("no executable for the tool %s: give --tool %s=COMMAND" % (tool, tool))
  return [exe]


def executable_hashes(tool, paths):
  """the files of a tool whose content enters the key"""
  if tool == "gk":
    return {"gk": sha256_file(paths["gk"])}
  if tool == "mcref":
    d = os.path.dirname(paths["mcref"])
    return {"mcref.py": sha256_file(paths["mcref"]),
            "mcref_read.py": sha256_file(os.path.join(d, "mcref_read.py")),
            "gk": sha256_file(paths["gk"])}
  words = external_prefix(tool, paths)
  # the program file and the arguments that select the tool: a file by its
  # SHA-256 (a driver script), another path as a placeholder (a class path);
  # the version of an external tool belongs in the settings column
  args = []
  for w in words[1:]:
    if os.path.isfile(w):
      args.append("file " + sha256_file(w))
    elif "/" in w or ":" in w:
      args.append("path")
    else:
      args.append(w)
  return {tool: sha256_file(words[0]), "arguments": args}


INCLUDE = re.compile(r"""(?:^|[\s:(])include\s*\(\s*["']([^"']+)["']\s*\)|"@include"\s*:\s*"([^"]+)\"""", re.M)


def read_files(row, input_path):
  """the files besides the input that the run reads, relative to the input's
  folder: the included files (GKP, GKS, TPTP and JSON-LD-LOGIC syntax, also
  nested), gk_similarity.txt under -similarities, every option that names an
  existing file, and the files of the column reads"""
  base = os.path.dirname(input_path)
  found, todo = [], [input_path]
  while todo:
    f = todo.pop()
    try:
      text = open(f, encoding="utf-8", errors="replace").read()
    except OSError:
      continue
    for m in INCLUDE.finditer(text):
      name = m.group(1) or m.group(2)
      p = os.path.normpath(os.path.join(os.path.dirname(f), name))
      if os.path.isfile(p) and p not in found:
        found.append(p)
        todo.append(p)
  opts = shlex.split(row.get("options") or "")
  if row["tool"] == "gk" and "-similarities" in opts:
    found.append(os.path.join(base, "gk_similarity.txt"))
  for tok in opts:
    tok = tok.split("=", 1)[-1]
    p = os.path.normpath(os.path.join(base, tok))
    if tok not in ("{input}", "{outdir}") and not tok.startswith("-") and os.path.isfile(p) and \
       os.path.abspath(p) != os.path.abspath(input_path):
      found.append(p)
  for name in (row.get("reads") or "").split():
    found.append(os.path.normpath(os.path.join(base, name)))
  out = {}
  for p in found:
    if not os.path.isfile(p):
      raise SystemExit("%s reads %s, which does not exist" % (input_path, p))
    out[os.path.relpath(p, base)] = sha256_file(p)
  return out


def settings_of(row):
  return dict(x.split("=", 1) for x in (row.get("settings") or "").split())


def command(row, input_path, paths, outdir=None):
  """the command, its working folder and its environment; the token
  {outdir} stands for a folder of the run's own, kept in its store entry"""
  name = os.path.basename(input_path)
  opts = shlex.split(row.get("options") or "")
  if outdir:
    opts = [outdir if t == "{outdir}" else t for t in opts]
  if "{input}" in opts:
    opts = [name if t == "{input}" else t for t in opts]
  else:
    opts = [name] + opts
  env = dict(os.environ)
  tool = row["tool"]
  if tool == "gk":
    cmd = [paths["gk"]] + opts
  elif tool == "mcref":
    s = settings_of(row)
    cmd = [sys.executable, "-I", paths["mcref"]] + opts
    for k in ("samples", "seed"):
      if k in s:
        cmd += ["--" + k, s[k]]
    env["MCREF_GK"] = paths["gk"]
  else:
    cmd = external_prefix(tool, paths) + opts
  return cmd, os.path.dirname(input_path), env


def key_object(row, part_folder, paths):
  input_path = os.path.normpath(os.path.join(part_folder, row["input"]))
  if not os.path.isfile(input_path):
    raise SystemExit("%s: input %s does not exist" % (row["run_id"], input_path))
  return {"store_format": STORE_FORMAT,
          "tool": row["tool"],
          "executable": executable_hashes(row["tool"], paths),
          "input": sha256_file(input_path),
          "reads": read_files(row, input_path),
          "options": row.get("options") or "",
          "settings": settings_of(row)}


def key_of(obj):
  text = json.dumps(obj, sort_keys=True, separators=(",", ":"))
  return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --- the run lists -------------------------------------------------------------

def part_folders(names):
  out = []
  for d in sorted(glob.glob(os.path.join(FOLDER, "O*"))):
    if os.path.isfile(os.path.join(d, "runs.tsv")):
      b = os.path.basename(d)
      if not names or any(b == n or b.startswith(n + "_") for n in names):
        out.append(d)
  return out


def read_tsv(path):
  lines = open(path, encoding="utf-8").read().rstrip("\n").split("\n")
  cols = lines[0].split("\t")
  rows = []
  for n, line in enumerate(lines[1:], 2):
    if not line.strip():
      continue
    vals = line.split("\t")
    if len(vals) > len(cols):
      raise SystemExit("%s line %d: %d fields, %d columns" % (path, n, len(vals), len(cols)))
    rows.append(dict(zip(cols, vals + [""] * (len(cols) - len(vals)))))
  return cols, rows


def run_list(part_folder):
  cols, rows = read_tsv(os.path.join(part_folder, "runs.tsv"))
  missing = [c for c in COLUMNS if c not in cols]
  if missing:
    raise SystemExit("%s/runs.tsv lacks the columns %s" % (part_folder, missing))
  seen = set()
  for r in rows:
    if r["run_id"] in seen:
      raise SystemExit("%s/runs.tsv: run_id %s twice" % (part_folder, r["run_id"]))
    seen.add(r["run_id"])
  return rows


def all_runs(names, paths, quiet=False):
  """every run of the named parts, with its key; a run of an external tool
  that is not installed gets no key and a field "missing" """
  out, missing = [], {}
  for d in part_folders(names):
    for r in run_list(d):
      r = dict(r, part=os.path.basename(d), part_folder=d)
      try:
        obj = key_object(r, d, paths)
        r.update(key_object=obj, key=key_of(obj))
      except ToolMissing as e:
        r.update(key=None, missing=str(e))
        missing[r["tool"]] = missing.get(r["tool"], 0) + 1
      out.append(r)
  if not quiet:
    for tool, n in sorted(missing.items()):
      print("skipped %d runs of %s: no executable (give --tool %s=COMMAND)" % (n, tool, tool))
  return out


# --- the store -----------------------------------------------------------------

def entry_dir(store, key):
  return os.path.join(store, key[:2], key)


def is_stored(store, key):
  return os.path.isfile(os.path.join(entry_dir(store, key), "status.json"))


def read_entry(store, key):
  """run.json, stdout, stderr and status.json of a stored run, or None"""
  d = entry_dir(store, key)
  if not os.path.isfile(os.path.join(d, "status.json")):
    return None
  def text(name):
    with gzip.open(os.path.join(d, name), "rt", encoding="utf-8", errors="replace") as f:
      return f.read()
  return {"run": json.load(open(os.path.join(d, "run.json"))),
          "status": json.load(open(os.path.join(d, "status.json"))),
          "stdout": text("stdout.gz"), "stderr": text("stderr.gz"), "out": read_out(d)}


def read_out(d):
  """the files that a run wrote into {outdir}: {name: bytes}"""
  p = os.path.join(d, "out.tar.gz")
  if not os.path.isfile(p):
    return {}
  with tarfile.open(p, "r:gz") as tf:
    return {m.name: tf.extractfile(m).read() for m in tf.getmembers() if m.isfile()}


def proc_start(pid):
  try:
    return open("/proc/%d/stat" % pid).read().rsplit(")", 1)[1].split()[19]
  except (OSError, IndexError):
    return None


def clear_tmp(store):
  """kill the process groups of runs that an earlier runner left behind and
  delete their partial directories"""
  tmp = os.path.join(store, "running")
  os.makedirs(tmp, exist_ok=True)
  for d in sorted(glob.glob(os.path.join(tmp, "*"))):
    try:
      child = json.load(open(os.path.join(d, "child.json")))
      if proc_start(child["pgid"]) == child["start"]:
        os.killpg(child["pgid"], signal.SIGKILL)
        print("killed the process group %d of an interrupted run" % child["pgid"])
    except (OSError, ValueError, KeyError):
      pass
    shutil.rmtree(d, ignore_errors=True)


def load_average():
  try:
    return open("/proc/loadavg").read().split()[:3]
  except OSError:
    return None


def execute(r, store, paths, log_lock):
  """run one row and store it; returns its status"""
  key = r["key"]
  input_path = os.path.normpath(os.path.join(r["part_folder"], r["input"]))
  work = os.path.join(store, "running", "%s.%d" % (key, os.getpid()))
  shutil.rmtree(work, ignore_errors=True)
  os.makedirs(work)
  outdir = None
  if "{outdir}" in (r.get("options") or ""):
    outdir = os.path.join(work, "out")
    os.makedirs(outdir)
  cmd, cwd, env = command(r, input_path, paths, outdir)
  timeout = float(r.get("timeout_s") or 600)
  info = {"key": r["key_object"], "key_sha256": key, "command": cmd, "cwd_relative_to_folder":
          os.path.relpath(cwd, FOLDER), "cwd": cwd, "part": r["part"], "run_id": r["run_id"],
          "input": r["input"], "alone": r.get("alone") == "yes", "timeout_s": timeout,
          "host": socket.gethostname(), "platform": platform.platform(),
          "python": sys.version.split()[0], "load_before": load_average(),
          "started": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
  out_path, err_path = os.path.join(work, "stdout"), os.path.join(work, "stderr")
  t0 = time.time()
  with open(out_path, "wb") as fo, open(err_path, "wb") as fe:
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=fo, stderr=fe,
                         start_new_session=True)
    with open(os.path.join(work, "child.json"), "w") as f:
      json.dump({"pgid": p.pid, "start": proc_start(p.pid)}, f)
    flag = {"timed_out": False}
    def kill():
      flag["timed_out"] = True
      try:
        os.killpg(p.pid, signal.SIGKILL)
      except ProcessLookupError:
        pass
    timer = threading.Timer(timeout, kill)
    timer.start()
    _, wstatus, ru = os.wait4(p.pid, 0)
    timer.cancel()
    p.returncode = os.waitstatus_to_exitcode(wstatus)
    try:
      os.killpg(p.pid, signal.SIGKILL)      # forked strategies left behind
    except ProcessLookupError:
      pass
  elapsed = time.time() - t0
  info["ended"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
  for name in ("stdout", "stderr"):
    with open(os.path.join(work, name), "rb") as f, gzip.open(os.path.join(work, name + ".gz"), "wb") as g:
      shutil.copyfileobj(f, g)
    os.remove(os.path.join(work, name))
  os.remove(os.path.join(work, "child.json"))
  if outdir:
    with tarfile.open(os.path.join(work, "out.tar.gz"), "w:gz") as tf:
      for name in sorted(os.listdir(outdir)):
        tf.add(os.path.join(outdir, name), arcname=name)
    shutil.rmtree(outdir)
  status = {"exit": p.returncode, "elapsed_s": round(elapsed, 3), "peak_rss_kb": ru.ru_maxrss,
            "user_s": round(ru.ru_utime, 3), "system_s": round(ru.ru_stime, 3),
            "timed_out": flag["timed_out"]}
  with open(os.path.join(work, "run.json"), "w") as f:
    json.dump(info, f, indent=1)
  with open(os.path.join(work, "status.json"), "w") as f:
    json.dump(status, f, indent=1)
  final = entry_dir(store, key)
  os.makedirs(os.path.dirname(final), exist_ok=True)
  os.rename(work, final)
  with log_lock:
    with open(os.path.join(store, "log.jsonl"), "a") as f:
      f.write(json.dumps({"key": key, "part": r["part"], "run_id": r["run_id"], "tool": r["tool"],
                          "input": r["input"], "ended": info["ended"], **status}) + "\n")
  return status


def estimate(r, store):
  """seconds, from a stored run of the same tool on the same input"""
  return r.get("_estimate") or float(r.get("timeout_s") or 600)


def estimates(runs, store):
  path = os.path.join(store, "log.jsonl")
  by_input, by_tool = {}, {}
  if os.path.isfile(path):
    for line in open(path):
      try:
        x = json.loads(line)
      except ValueError:
        continue
      by_tool.setdefault(x["tool"], []).append(x["elapsed_s"])
  for d in glob.glob(os.path.join(store, "??", "*", "run.json")):
    try:
      info = json.load(open(d))
      st = json.load(open(os.path.join(os.path.dirname(d), "status.json")))
    except (OSError, ValueError):
      continue
    by_input[(info["key"]["tool"], info["key"]["input"])] = st["elapsed_s"]
  for r in runs:
    k = (r["tool"], r["key_object"]["input"])
    if k in by_input:
      r["_estimate"] = by_input[k]
    elif by_tool.get(r["tool"]):
      xs = sorted(by_tool[r["tool"]])
      r["_estimate"] = xs[len(xs) // 2]


def main():
  ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
  ap.add_argument("parts", nargs="*", help="part names such as O1 or O2_record; default all")
  ap.add_argument("--store", default=os.environ.get("PAPER2026_STORE"))
  ap.add_argument("--jobs", type=int, default=3)
  ap.add_argument("--gk", default=os.path.join(ROOT, "bin", "gk"))
  ap.add_argument("--mcref", default=os.path.join(ROOT, "mcref", "mcref.py"))
  ap.add_argument("--tool", action="append", help="NAME=PATH of an external tool")
  ap.add_argument("--dry-run", action="store_true")
  ap.add_argument("--force", metavar="KEY", help="run this key again; the old entry stays as KEY.old.N")
  a = ap.parse_args()
  if not a.store:
    sys.exit("give --store DIR or set PAPER2026_STORE")
  if a.jobs > 4:
    sys.exit("at most 4 jobs: gk runs several strategies in parallel")
  store = os.path.abspath(a.store)
  os.makedirs(store, exist_ok=True)
  paths = tool_paths(a)
  runs = [r for r in all_runs(a.parts, paths) if r["key"]]
  if a.force:
    runs = [r for r in runs if r["key"] == a.force][:1]
    if not runs:
      sys.exit("no run of the run lists has the key " + a.force)
  todo = [r for r in runs if a.force or not is_stored(store, r["key"])]
  estimates(todo, store)
  print("%d runs in the lists, %d stored, %d to run" % (len(runs), len(runs) - len(todo) if not a.force else 0, len(todo)))
  if a.dry_run:
    total = 0.0
    for r in todo:
      s = estimate(r, store)
      total += s
      print("%s %-12s %-20s %-6s %s %s%s" % (r["key"][:12], r["part"], r["run_id"], r["tool"], r["input"],
                                            r.get("options") or "", "  (alone)" if r.get("alone") == "yes" else ""))
    print("estimated %.0f s of run time, about %.0f s with %d jobs" % (total, total / max(1, a.jobs), a.jobs))
    return
  lock = open(os.path.join(store, "lock"), "w")
  try:
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
  except OSError:
    sys.exit("another runner uses this store")
  clear_tmp(store)
  if a.force:
    old = entry_dir(store, a.force)
    if os.path.isdir(old):
      n = 1
      while os.path.exists("%s.old.%d" % (old, n)):
        n += 1
      os.rename(old, "%s.old.%d" % (old, n))
  # one run per key: two rows with the same key share the run
  unique, seen = [], set()
  for r in todo:
    if r["key"] not in seen:
      seen.add(r["key"])
      unique.append(r)
  shared = [r for r in unique if r.get("alone") != "yes"]
  alone = [r for r in unique if r.get("alone") == "yes"]
  log_lock = threading.Lock()
  done = [0]
  t_start = time.time()
  def report(r, st):
    done[0] += 1
    print("[%d/%d] %s/%s %s: exit %s, %.1f s%s" % (done[0], len(unique), r["part"], r["run_id"], r["tool"],
                                                  st["exit"], st["elapsed_s"], ", timed out" if st["timed_out"] else ""),
          flush=True)
  queue = list(shared)
  qlock = threading.Lock()
  def worker():
    while True:
      with qlock:
        if not queue:
          return
        r = queue.pop(0)
      report(r, execute(r, store, paths, log_lock))
  threads = [threading.Thread(target=worker) for _ in range(min(a.jobs, len(queue)))]
  for t in threads:
    t.start()
  for t in threads:
    t.join()
  for r in alone:
    report(r, execute(r, store, paths, log_lock))
  print("%d runs in %.0f s" % (len(unique), time.time() - t_start))


if __name__ == "__main__":
  main()
