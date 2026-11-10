# Systems: versions, installation and commands

This folder holds no code of the external systems. This page names the
version of each system that produced the results, where to get it, how it
was installed, and the command that ran it. Every command runs on one
input file of this folder.

The runs were made on one machine: an AMD Ryzen 5 3600 six-core processor
(12 threads), 64 GB of memory, Ubuntu 26.04.1 LTS with Linux 7.0.0-42,
Python 3.14.4 and PyPy 3.11. Times in the results are wall-clock times of
single runs. The gk runs of 2026-11-10 ran three at a time, and the mcref
1.1.2 runs four at a time, except the runs marked `alone` in `runs.tsv`,
which ran with no other run of the runner active; other processes of the machine were not controlled.
The run store records the load average before each run.

## gk and the reference tool (in this repository)

| system | version | where | command |
|---|---|---|---|
| gk | 1.2.5 | `bin/gk` (Linux x86-64); other platforms in [`../bin/README.md`](../bin/README.md) | `./bin/gk FILE` |
| mcref, the reference tool | 1.1.2 | `mcref/mcref.py`; Python 3, no other package; it calls `bin/gk` to read gk's input syntax | `python3 mcref/mcref.py FILE --samples N --seed 1` |

gk runs without options unless a result names options. Its default is the
recursive method with a deadline of 10 s and the automatic choice of
search strategy. Every gk and mcref value, time and note of this folder
comes from a run of gk 1.2.5 and mcref 1.1.2 on 2026-11-10. The earlier
runs of the paper's drafts used gk 1.2.3 and mcref 1.1.0. mcref 1.1.2
computes the cycle rule of 2026-11-10: sweeps only for a sweep group, the
narrowing for every other cycle group. It changed five values of part O3
(`O3_families/README.md`, the cyclic families); mcref 1.1.1 and 1.1.0 gave the same
counts on every run. `check_gk.py`
reruns every gk and mcref run with the versions in this repository.

| file | SHA-256 |
|---|---|
| `bin/gk` (Linux x86-64, 1.2.5) | `9744ade923bf10230acec4f4ee5b0b6460cfffde39f08d939a8c016683fa8e2d` |
| `mcref/mcref.py` (1.1.2) | `92465ad8d53878060d0fd1e03f314cc34fe486ced4a19ddc5d7d57e3eda7344d` |
| `mcref/mcref_read.py` | `36063563420653033406346a5ddb129e5440c61a337e3e97c027e6f7960c60a8` |

## Python packages

The Python packages ran in one virtual environment under Python 3.14:

```sh
python3 -m venv venv
venv/bin/pip install problog==2.3.0 plingo==1.1.0 clingo==5.8.3 pgmpy==1.1.2
```

| system | version | project page | command |
|---|---|---|---|
| ProbLog | 2.3.0 | <https://dtai.cs.kuleuven.be/problog/> | `problog FILE.pl` |
| plingo | 1.1.0 (libclingo 5.8.3) | <https://github.com/potassco/plingo> | `plingo --frontend=problog FILE.plp 0` |
| clingo | 5.8.3 | <https://potassco.org/clingo/> | `clingo FILE.lp 0`; also the Python module used by `tools/enumerate_answer_sets.py` |
| pgmpy | 1.1.2 | <https://pgmpy.org/> | variable elimination on the BIF files of part O3 |

## Systems installed from their source repositories

| system | version | source | installation | command |
|---|---|---|---|---|
| PASTA | 1.0.1, git `5687268` (2026-09-28) | <https://github.com/damianoazzolini/pasta> | `git clone` the repository, `git checkout 5687268`, then `python3 -m venv venv_pasta && venv_pasta/bin/pip install ./pasta` | `pastasolver FILE.lp --query="ATOM"`, with `--normalize` where a result says so |
| smProbLog | 2.1.0.42, git `bfbc542` (2022-11-28) | <https://github.com/PietroTotis/smProblog> | `git clone` the repository and `git checkout bfbc542`; set the execute bit of `problog/bin/linux/dsharp_with_unfounded`. The pip installation fails under Python 3.12 and later (the module `imp` is gone), so smProbLog runs from the clone under PyPy 3.11 | `SMPROBLOG_SRC=<clone> pypy3 tools/run_smproblog.py -k ddnnf FILE.pl` |

`tools/run_smproblog.py` is a starter written for this folder. It restores
three names that newer Python versions removed and leaves smProbLog's code
unchanged; its docstring lists each step.

Each PASTA and smProbLog run of part O1 had a deadline of 60 s and an
address-space limit of 8 GB (`ulimit -v 8388608`).

## Defeasible reasoners of parts O3 and O7

| system | version | source | installation | command |
|---|---|---|---|---|
| SPINdle | 2.2.4 | SourceForge project `spindle`, <https://sourceforge.net/projects/spindle/>, distribution `SPINdle_2.2.4` (zip SHA-256 `d18d3b723d1f96bda6f001828dd2e96ddaffeda12dfb86d93c68b7b8c4db7e47`; jar `dist/spindle_2.2.4.jar`, SHA-256 `eaca354be02adc817ea55df8aa0e0f5e45faf72bf4fd263a9dcd06e2a42fddc9`) | unzip; Java | `java -Xmx8g -jar spindle_2.2.4.jar FILE.dfl` |
| DEFT | 1.0.0, git `7f3757d` (2018-04-12) | <https://github.com/hamhec/DEFT> | `mvn package` (jar SHA-256 `b82b1b2f3e9ed30b4428c4c764c183a50474b5ee4cdfa5dea55f576889a0ef7b`), then `mvn dependency:build-classpath -Dmdep.outputFile=cp.txt`; the exact Maven commands of the runs were not saved | `java -Xmx8g -cp "target/DEFT-1.0.0.jar:$(cat cp.txt)" O3_families/tools/DeftRun.java FILE.dlgp ATOM...` |
| TweetyProject DeLP | 1.27 | Maven Central, `org.tweetyproject.arg:delp:1.27` with `logics:commons` and `logics:fol` 1.27 | `mvn -f O3_families/tools/delp_pom.xml dependency:copy-dependencies -DoutputDirectory=libs` | `java -cp 'libs/*' O3_families/tools/DelpRun.java FILE.delp QUERY...` |

The runs used OpenJDK 25.0.5. The drivers `DeftRun.java` and `DelpRun.java`
in `O3_families/tools/` were written for these runs: each loads one file
and prints the answer to each query. The DeLP driver uses generalized
specificity. DEFT ran the theories of parts O3 and O7, DeLP those of
part O7. The DEFT and DeLP runs of part O7 had no saved output and were
run again on 2026-11-10 through the run store.

pgmpy 1.1.2 (installed with the Python packages above) computed the
marginals of the five bnlearn networks of part O3 by variable
elimination: `python3 O3_families/tools/bn_marginals.py BIF_FOLDER`. The
BIF files are not included; part O3 gives their addresses and SHA-256.

## The translation pipeline of part O7

The English cases of part O7 were translated into logic by llmpipe of
<https://github.com/tammet/nlpsolver>. N3 and N4 come from tag
`core-2026-06-03` (commit `585e8b0`, claude-sonnet-4-6). N1v1 and N2v2
were translated on 2026-11-04 at commit `b1a7298` with claude-sonnet-4-6,
deepseek-v4-flash and gemini-2.5-flash; the gpt-5.1 calls failed with
HTTP 429. The language-model calls were not repeated: part O7 holds the
texts, the extractions and the transcripts.

## Systems of the earlier comparison table

ProbLog 2.2.10, PASTA 1.0.1, plingo 1.1.0, smProbLog 2.1.0.42,
TweetyProject 1.31, clingo 5.6.2, DLV 2.1.1, I-DLV 1.1.6 and s(CASP) 1.1.4
produced the cells of [`../comparisons/`](../comparisons/README.md). Its
README lists the versions and project pages, and its `manifest.json`
records every command.
