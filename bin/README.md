# Binaries

Prebuilt GK executables, one per platform, all from the same source revision.

| File | Platform |
|---|---|
| `gk` | Linux x86-64, statically linked |
| `gk-macos-arm64` | macOS on Apple silicon |
| `gk-windows-x64.exe` | 64-bit Windows |
| `gkjs.js` + `gkjs.wasm` | WebAssembly, for a browser page |

Every binary takes the same command-line arguments and produces the same
answers. `-version` prints the build version, `-help` the option summary; the
options themselves are in [`../Doc/cli_reference.md`](../Doc/cli_reference.md).

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

The same applies to the auxiliary data files of `-defaults`
(`gk_name_number.txt`, `gk_taxonomy_packed.txt`): they must be written with
`FS.writeFile` before `-defaults` is used.

Two further limits of the WebAssembly build: it is single-process, so
`-parallel` must not be passed, and its memory is fixed at build time. The
build here is set to 2000 MB, which Chrome accepts; a page that has to work in
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
