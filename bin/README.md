# Binaries

Prebuilt GK executables, one per platform, all from the same source revision:
gk 1.3.2 (2026-11-23), commit `34dacd3` of the gk source repository. The
section *Checksums* below lists the SHA-256 of each file.

| File | Platform |
|---|---|
| `gk` | Linux x86-64, statically linked |
| `gk-macos-arm64` | macOS on Apple silicon |
| `gk-windows-x64.exe` | 64-bit Windows |
| `gkjs.js` + `gkjs.wasm` | WebAssembly, for a browser page |

Every binary takes the same command-line arguments and produces the same
answers. `-version` prints the build version, `-help` the option summary; the
options themselves are in [`../Doc/cli_reference.md`](../Doc/cli_reference.md).

By default a binary runs Auto: the exact method within half of the time
limit, then the general method when the exact method gives no answer.
`-exact` and `-general` select one method. Every method prints one line
that starts with `{"recursive":`; `-dwdump` adds a dump of the evidence
([`../Doc/recursive_output.md`](../Doc/recursive_output.md)). `-direct` runs
the legacy direct method of gk 1.1.2
([`../Doc/direct_method.md`](../Doc/direct_method.md)).

## Running

Linux:

```sh
chmod +x bin/gk
./bin/gk Examples/exceptions/penguin.gkp
```

macOS:

```sh
chmod +x bin/gk-macos-arm64
./bin/gk-macos-arm64 Examples/exceptions/penguin.gkp
```

macOS marks a downloaded binary as quarantined. If it is refused, clear the
attribute with `xattr -d com.apple.quarantine bin/gk-macos-arm64`.

Windows:

```text
bin\gk-windows-x64.exe Examples\exceptions\penguin.gkp
```

Run the commands from the repository root, so that the example paths resolve.

## WebAssembly

`gkjs.js` is the loader and `gkjs.wasm` the compiled reasoner. A browser page
includes `gkjs.js`, which fetches `gkjs.wasm` from the same directory.

The browser has no host filesystem. The page writes the problem into the
in-memory filesystem before starting the reasoner:

```js
Module.onRuntimeInitialized = function () {
  Module.FS.writeFile("input", problemText);
};
Module.postRun = [function () { Module.callMain(["input", "-seconds", "5"]); }];
```

`callMain` adds the program name to the front of the array it is given. A
page that calls the reasoner several times in one instance passes a new
array, or a copy (`args.slice()`), to each call.

The same applies to the auxiliary data files of `-taxonomy` (synonym
`-defaults`): `gk_name_number.txt` and `gk_taxonomy_packed.txt`, whose
canonical copies are in [`../data/`](../data/README.md), must be written
with `FS.writeFile` before the flag is used.

Two further limits of the WebAssembly build: it is single-process, so
`-parallel` must not be passed, and its memory is fixed at build time. The
build here was made with Emscripten 6.0.13 and is set to 2000 MB, which
Chrome accepts; a page that has to work in
browsers refusing that size is served a build compiled with a smaller
`TOTAL_MEMORY`.

Reasoning that needs the host filesystem, shared-memory knowledge bases, or
parallel search belongs to the native binaries above.

## Building from source

The binaries are built from the GK source repository, which is separate from
this distribution repository. Its build scripts are, per platform: `compile.sh`
(Linux, GCC), `compile_osx.sh` (macOS, Clang), `compile.bat` (Windows, MSVC in
an x64 developer prompt), and `compile_wasm.sh` (WebAssembly, Emscripten). The
macOS and Windows binaries here are produced by the GitHub Actions workflows of
that repository and are checked in after their smoke tests pass.

## Checksums

| File | SHA-256 | Built by |
|---|---|---|
| `gk` | `f73e9f2e9aac47bb8aaa20fa37db6e79042c0ffff441ed1ed4f5e0b05a1fb642` | `make` (GCC, static), Linux x86-64 |
| `gk-macos-arm64` | `46913031a9e01b31458eb835aace3370936dbf61c81400e9ce911b069a7b3dc4` | the workflow *macOS build*, run 45194740477 |
| `gk-windows-x64.exe` | `8b17ef460225184462b0b3d3ccd260693f3f4417a06bd9144abff188516ea39c` | the workflow *Windows build (exploratory)*, run 45194740442 |
| `gkjs.js` | `0c6dc538f868cd8013dc8c08fafce2d41def1bb9ff547f62aecb8d8c90b87118` | `compile_wasm.sh`, Emscripten 6.0.13 |
| `gkjs.wasm` | `4dc293b274a0231906745a0c9689424a89ee14df38d91a91ed3946ce198f9819` | `compile_wasm.sh`, Emscripten 6.0.13 |

Check a file on Linux with `sha256sum bin/gk`, on macOS with
`shasum -a 256 bin/gk-macos-arm64`.
