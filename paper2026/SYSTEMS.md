# Systems: versions, installation and commands

This folder holds no code of the external systems. This page names the version of each system that produced the
results, where to get it, how it was installed, and the command that ran it.

The runs were made on one machine: an AMD Ryzen 5 3600 processor (six cores, 12 threads) with 64 GB of memory,
Ubuntu 26.04.1 LTS with Linux 7.0, Python 3.14.4, PyPy 3.11 and OpenJDK 25.0.5.

## gk and the tool

| system | version | where | command |
|---|---|---|---|
| gk | 1.3.2 | `bin/gk` of the gkreasoner repository (Linux x86-64); in the full dataset `bin/gk` | `gk FILE` (the default), `gk FILE -exact`, `gk FILE -general` |
| gk | 1.3.2 | in the full dataset `bin/gk-macos-arm64` (macOS ARM64), built by the macOS workflow of GitHub Actions from gk commit 34dacd3 (run 45194740477); no run of this folder used it | `gk FILE` (the default), `gk FILE -exact`, `gk FILE -general` |
| gk | 1.3.2 | in the full dataset `bin/gk-windows-x64.exe` (Windows x64), built by the Windows workflow of GitHub Actions from gk commit 34dacd3 (run 45194740442); no run of this folder used it | `gk FILE` (the default), `gk FILE -exact`, `gk FILE -general` |
| mcref, the tool | 1.3.1 | `mcref/` of the gkreasoner repository; in the full dataset `mcref/`; Python 3, no other package; it calls gk to read gk's input syntax | `MCREF_GK=PATH/TO/gk python3 mcref.py FILE` (exact evaluation up to 300,000 cells, else 100,000 sampled worlds with seed 1); `--all-atoms` where a part compares atoms |

| file | SHA-256 |
|---|---|
| `bin/gk` (Linux x86-64, 1.3.2) | `f73e9f2e9aac47bb8aaa20fa37db6e79042c0ffff441ed1ed4f5e0b05a1fb642` |
| `bin/gk-macos-arm64` of the full dataset (macOS ARM64, 1.3.2) | `46913031a9e01b31458eb835aace3370936dbf61c81400e9ce911b069a7b3dc4` |
| `bin/gk-windows-x64.exe` of the full dataset (Windows x64, 1.3.2) | `8b17ef460225184462b0b3d3ccd260693f3f4417a06bd9144abff188516ea39c` |
| `mcref/mcref.py` (1.3.1) | `e7489ee3ef14ebcc506099236ec4dd6962ff8880faa7ab7f09a2a6653179ec13` |
| `mcref/mcref_apps.py` (1.3.1) | `d09fab3251c3593631df4d8ef5aed90041585823fc5f092710dac32b86826243` |
| `mcref/mcref_compare.py` (1.3.1) | `8a45209618a0d0d15f1a359f98753954f4809a473d2ffaa2c1302cd4b1b6f32a` |
| `mcref/mcref_exact.py` (1.3.1) | `03607c422b7b390dab4e70d44c1f06b3ebc9a535c9a1e43067cc5774710b8aa8` |
| `mcref/mcref_graph.py` (1.3.1) | `700bfb415412cef811e2569a6f7af2063520cca3027a875e23fc98225d3f97c9` |
| `mcref/mcref_proofs.py` (1.3.1) | `1cd62b63a39eab23fda5e2630b648e706d555f8781bf6fae4e68385befd74072` |
| `mcref/mcref_read.py` (1.3.1) | `6cddd6a4bf0da459eb2944d0b3a15996733841281f75f47796fbb42a2a5f5206` |
| `mcref/mcref_tables.py` (1.3.1) | `5f465268830d11e8662971eec4aecc8086bfa72315395e67afe8caf9ab145427` |
| `mcref/mcref_texts.py` (1.3.1) | `42ed23d1615a7885ed389efec63877fb7d4a091d72a265070ec726029e3607b8` |

## Python packages

ProbLog, plingo, clingo and pgmpy ran in one virtual environment:

```sh
python3 -m venv venv
venv/bin/pip install problog==2.3.0 plingo==1.1.0 clingo==5.8.3 pgmpy==1.1.2
```

| system | version | project page | command |
|---|---|---|---|
| ProbLog | 2.3.0 | <https://dtai.cs.kuleuven.be/problog/> | `problog FILE.pl` |
| plingo | 1.1.0 (libclingo 5.8.3) | <https://github.com/potassco/plingo> | `plingo FILE.plp --frontend=problog --quiet=2` |
| clingo | 5.8.3 | <https://potassco.org/clingo/> | the grounder: `python3 -m clingo --mode=gringo --text FILE.lp`; also the module that `tools/enumerate_answer_sets.py` uses |
| pgmpy | 1.1.2 | <https://pgmpy.org/> | variable elimination on the networks of part O3 (`O3_families/inputs/tools/bn_marginals.py`) |

## Systems installed from their source repositories

| system | version | source | installation | command |
|---|---|---|---|---|
| PASTA | 1.0.1, git `5687268` | <https://github.com/damianoazzolini/pasta> | `git clone`, `git checkout 5687268`, then `python3 -m venv venv_pasta && venv_pasta/bin/pip install ./pasta` | `pastasolver FILE.lp --query=ATOM`, with `--normalize` where a result says so |
| smProbLog | 2.1.0.42, git `bfbc542` | <https://github.com/PietroTotis/smProblog> | `git clone`, `git checkout bfbc542`; set the execute bit of `problog/bin/linux/dsharp_with_unfounded`. It runs from the clone under PyPy 3.11 | `SMPROBLOG_SRC=<clone> pypy3 tools/run_smproblog.py -k ddnnf FILE.pl` |
| SPINdle | 2.2.4 | the SourceForge project `spindle`, <https://sourceforge.net/projects/spindle/>, distribution `SPINdle_2.2.4` (jar `dist/spindle_2.2.4.jar`, SHA-256 `eaca354be02adc817ea55df8aa0e0f5e45faf72bf4fd263a9dcd06e2a42fddc9`) | unzip; Java | `java -Xmx8g -jar spindle_2.2.4.jar FILE.dfl` (`$SPINDLE_JAR` in `runs.tsv`) |
| s(CASP) | 1.1.4, git `ebfa170`, on SWI-Prolog 10.0.0 | <https://github.com/SWI-Prolog/sCASP> | SWI-Prolog 10.0.0 from conda-forge; `git clone`, `git checkout ebfa170`, then built in the clone | `scasp --query=QUERY FILE.pl`; `-n 0` prints every model (part O1) |
| DEFT | 1.0.0, git `7f3757d` | <https://github.com/hamhec/DEFT> | `mvn package` (jar SHA-256 `b82b1b2f3e9ed30b4428c4c764c183a50474b5ee4cdfa5dea55f576889a0ef7b`), then `mvn dependency:build-classpath -Dmdep.outputFile=cp.txt` | `java -Xmx8g -cp "DEFT-1.0.0.jar:$(cat cp.txt)" O19_defeasible_logic/tools/DeftRun.java FILE.dlgp ATOM...` (`$DEFT_CP` in `runs.tsv` is the class path) |

`tools/run_smproblog.py` is a starter written for this folder: it restores three names that newer Python versions
removed and leaves smProbLog's code unchanged. `O19_defeasible_logic/tools/DeftRun.java` loads one DEFT theory and
prints the status of each query.

The other systems ran with a time limit of 60 s and a memory limit of 8 GB, except where `runs.tsv` names
another; SPINdle and DEFT had 10 GB for the process and `-Xmx8g` for Java.

## The recorded runs of the earlier comparison

Some cells of the other systems are recorded runs of the earlier comparison, made with the versions below; the
parts that use them say so. The 16-case table of part O5 used ProbLog 2.2.10, PASTA 1.0.1, plingo 1.1.0,
smProbLog 2.1.0.42, TweetyProject 1.31, clingo 5.6.2, DLV 2.1.1, I-DLV 1.1.6 and s(CASP) 1.1.4. Parts O1, O3, O4
and O7 used ProbLog 2.3.0, plingo 1.1.0, clingo 5.8.3, PASTA 1.0.1, smProbLog 2.1.0.42, DEFT 1.0.0 and
TweetyProject DeLP 1.27 (Maven Central, `org.tweetyproject.arg:delp:1.27`).

## The translation pipeline of part O7

The English cases of part O7 were translated into logic by the pipeline llmpipe of
<https://github.com/tammet/nlpsolver>. The language-model calls were not repeated: part O7 holds the texts, the
extractions and the translations.
