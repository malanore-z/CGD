import argparse
import logging

from cgd import utils
from cgd.compile import Compiler
from cgd.diff import Diff
from cgd.generate import Generator
from cgd.template import Template
from cgd.log import set_level


logger = logging.getLogger("cgd")


def add_common_argument(parser: argparse.ArgumentParser):
    parser.add_argument("--timeout",
                        type=int, default=3000,
                        help="command execute time limit(ms)")
    parser.add_argument("--log-level",
                        type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="log level")
    parser.add_argument("--tmp-dir",
                        type=str, default="tmp",
                        help="temp dir")
    return parser


def parse_args(args):
    parser = argparse.ArgumentParser(prog="cgd", description="cgd")
    subparsers = parser.add_subparsers(dest="action", title="cgd subparsers")

    compile = add_common_argument(subparsers.add_parser("compile"))
    compile.add_argument("sources",
                         type=str,
                         metavar="source", nargs="+",
                         help="source files")
    compile.add_argument("--lang",
                         type=str, default=None,
                         choices=["c", "cpp", "java", "py"],
                         help="source language")
    compile.add_argument("--args",
                         type=str, default=None,
                         help="compile args")
    compile.add_argument("--output", "-o",
                         type=str, default=None,
                         help="output file directory")
    compile.add_argument("--output-name",
                         type=str, default=None,
                         help="output file name")

    generate = add_common_argument(subparsers.add_parser("generate"))
    generate.add_argument("--mode",
                          type=str, default="std",
                          choices=["std", "stdout", "rand"],
                          help="mode")
    generate.add_argument("--output", "-o",
                          type=str, required=True,
                          help="output file path.")
    generate.add_argument("--gen-path",
                          type=str, default=None,
                          help="the path of python script")
    generate.add_argument("--gen-cls",
                          type=str, default="gen.Generator",
                          help="generate fully qualified class name")
    generate.add_argument("--std-src",
                          type=str, default=None,
                          help="std source code path")
    generate.add_argument("--std-lang",
                          type=str, default=None,
                          help="std source code language")
    generate.add_argument("--std-args",
                          type=str, default=None,
                          help="std source code compile args")
    generate.add_argument("--std-bin",
                          type=str, default=None,
                          help="std executable binary")

    diff = add_common_argument(subparsers.add_parser("diff"))
    diff.add_argument("sources",
                      type=str,
                      metavar="source", nargs="+",
                      help="source files")
    diff.add_argument("--mode",
                      type=str, default="std",
                      choices=["std", "rand"],
                      help="mode")
    diff.add_argument("--data",
                      type=str, default="data",
                      help="the data path")

    diff.add_argument("--gen-path",
                      type=str, default=None,
                      help="generator path")
    diff.add_argument("--gen-cls",
                      type=str, default="gen.Generator",
                      help="generator class name")
    diff.add_argument("--std-src",
                      type=str, default=None,
                      help="std source code path")
    diff.add_argument("--std-lang",
                      type=str, default=None,
                      help="std source code language")
    diff.add_argument("--std-args",
                      type=str, default=None,
                      help="std source code compile args")
    diff.add_argument("--std-bin",
                      type=str, default=None,
                      help="std executable binary")

    diff.add_argument("--fc-path",
                      type=str, default=None,
                      help="file comparator path")
    diff.add_argument("--fc-cls",
                      type=str, default="cgd.fc.IgnoreBEBlankLineFC",
                      help="file comparator class name")
    diff.add_argument("--rand-round",
                      type=int, default=50,
                      help="round in rand mode")
    diff.add_argument("--use-stdout",
                      action="store_true",
                      help="diff output with std out")
    diff.add_argument("--fail-fast",
                      action="store_true",
                      help="whether exit when fc failed.")

    template = add_common_argument(subparsers.add_parser("template"))
    template.add_argument("--path",
                          type=str, required=True,
                          help="generate template directory")
    template.add_argument("--clean",
                          action="store_true",
                          help="whether clean the directory before generating template")

    return parser.parse_args(args)


def cgd(args=None):
    args = parse_args(args)
    utils.Global.timeout = args.timeout
    utils.Global.tmp_dir = args.tmp_dir
    set_level(args.log_level)
    if args.action == "compile":
        for src in args.sources:
            compiler = Compiler(src, dst=args.output, dst_name=args.output_name, lang=args.lang, args=args.args,
                                timeout=args.timeout)
            compiler.compile()
    elif args.action == "generate":
        generator = Generator(mode=args.mode, output=args.output,
                              gen_path=args.gen_path, gen_cls=args.gen_cls,
                              std_src=args.std_src, std_lang=args.std_lang, std_args=args.std_args, std_bin=args.std_bin,
                              timeout=args.timeout)
        generator.generate()
    elif args.action == "diff":
        diff = Diff(sources=args.sources, mode=args.mode, data=args.data,
                    gen_path=args.gen_path, gen_cls=args.gen_cls,
                    std_src=args.std_src, std_lang=args.std_lang, std_args=args.std_args, std_bin=args.std_bin,
                    fc_path=args.fc_path, fc_cls=args.fc_cls, rand_round=args.rand_round,
                    use_stdout=args.use_stdout, fail_fast=args.fail_fast, timeout=args.timeout)
        diff.diff()
    elif args.action == "template":
        template = Template(path=args.path, clean=args.clean)
        template.generate()
    else:
        logger.error(f"Unsupported action {args.action}")
