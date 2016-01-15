Quick Start
===========

Get GHC 7.10.2 ([MinGHC](https://www.haskell.org/downloads/windows) for Windows).
Make sure to take the 32 bit Version, to be able to link to the `raildriver.dll`.

Now run the following to install it. Make sure the `extra-lib-dirs` argument points to
the directory where the compiler can find the `raildriver.dll`:

```
$ cabal sandbox init
$ cabal configure --extra-lib-dirs="C:\Program Files (x86)\Steam\steamapps\common\RailWorks\plugins"
$ cabal build
$ cabal install
```

