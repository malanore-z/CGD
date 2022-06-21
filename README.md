# CGD

*Compile-Generate-Diff*  
*A auxiliary tool for algorithm competition questioner.*  

+ Usage:
```text
usage: cgd [-h] {compile,generate,diff,template} ...

cgd

optional arguments:
  -h, --help            show this help message and exit

cgd subparsers:
  {compile,generate,diff,template}
```
  
## Compile

```text
usage: cgd compile [-h] [--timeout TIMEOUT]
                   [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [--tmp-dir TMP_DIR] [--lang {c,cpp,java,py}] [--args ARGS]
                   [--output OUTPUT] [--output-name OUTPUT_NAME]
                   source [source ...]

positional arguments:
  source                source files

optional arguments:
  -h, --help            show this help message and exit
  --timeout TIMEOUT     command execute time limit(ms)
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        log level
  --tmp-dir TMP_DIR     temp dir
  --lang {c,cpp,java,py}
                        source language
  --args ARGS           compile args
  --output OUTPUT, -o OUTPUT
                        output file directory
  --output-name OUTPUT_NAME
                        output file name
```

## Generate

```text
usage: cgd generate [-h] [--timeout TIMEOUT]
                    [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [--tmp-dir TMP_DIR] [--mode {std,stdout,rand}] --output
                    OUTPUT [--gen-path GEN_PATH] [--gen-cls GEN_CLS]
                    [--std-src STD_SRC] [--std-lang STD_LANG]
                    [--std-args STD_ARGS] [--std-bin STD_BIN]

optional arguments:
  -h, --help            show this help message and exit
  --timeout TIMEOUT     command execute time limit(ms)
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        log level
  --tmp-dir TMP_DIR     temp dir
  --mode {std,stdout,rand}
                        mode
  --output OUTPUT, -o OUTPUT
                        output file path.
  --gen-path GEN_PATH   the path of python script
  --gen-cls GEN_CLS     generate fully qualified class name
  --std-src STD_SRC     std source code path
  --std-lang STD_LANG   std source code language
  --std-args STD_ARGS   std source code compile args
  --std-bin STD_BIN     std executable binary
```

## Diff

```text
usage: cgd diff [-h] [--timeout TIMEOUT]
                [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                [--tmp-dir TMP_DIR] [--mode {std,rand}] [--data DATA]
                [--gen-path GEN_PATH] [--gen-cls GEN_CLS] [--std-src STD_SRC]
                [--std-lang STD_LANG] [--std-args STD_ARGS]
                [--std-bin STD_BIN] [--fc-path FC_PATH] [--fc-cls FC_CLS]
                [--rand-round RAND_ROUND] [--use-stdout] [--fail-fast]
                source [source ...]

positional arguments:
  source                source files

optional arguments:
  -h, --help            show this help message and exit
  --timeout TIMEOUT     command execute time limit(ms)
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        log level
  --tmp-dir TMP_DIR     temp dir
  --mode {std,rand}     mode
  --data DATA           the data path
  --gen-path GEN_PATH   generator path
  --gen-cls GEN_CLS     generator class name
  --std-src STD_SRC     std source code path
  --std-lang STD_LANG   std source code language
  --std-args STD_ARGS   std source code compile args
  --std-bin STD_BIN     std executable binary
  --fc-path FC_PATH     file comparator path
  --fc-cls FC_CLS       file comparator class name
  --rand-round RAND_ROUND
                        round in rand mode
  --use-stdout          diff output with std out
  --fail-fast           whether exit when fc failed.
```

## Template

```text
usage: cgd template [-h] [--timeout TIMEOUT]
                    [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [--tmp-dir TMP_DIR] --path PATH [--clean]

optional arguments:
  -h, --help            show this help message and exit
  --timeout TIMEOUT     command execute time limit(ms)
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        log level
  --tmp-dir TMP_DIR     temp dir
  --path PATH           generate template directory
  --clean               whether clean the directory before generating template
```
