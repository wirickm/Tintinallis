"""Command line entry point for the pipeline."""

import argparse


def cmd_extract(args):
    from tintinallis.extract import extract_to_file
    print(extract_to_file(args.pdf, args.section))


def cmd_summarize(args):
    from tintinallis.config import RAW_DIR
    from tintinallis.sections import slug
    from tintinallis.summarize import summarize_file
    print(summarize_file(RAW_DIR / f"{slug(args.section)}.txt"))


def cmd_index(args):
    from tintinallis.index import build_index
    store = build_index()
    print(f"Vectorstore created with {store._collection.count()} documents")


def cmd_app(args):
    from tintinallis.app import main
    main()


def cmd_all(args):
    from tintinallis.extract import extract_to_file
    from tintinallis.summarize import summarize_file
    for section in args.sections:
        summarize_file(extract_to_file(args.pdf, section))
    cmd_index(args)


def build_parser():
    """Build the argparse parser with all subcommands."""
    parser = argparse.ArgumentParser(prog="tintinallis")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("extract", help="Extract a section's text from the PDF")
    p.add_argument("--pdf", required=True)
    p.add_argument("--section", required=True)
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser("summarize", help="Summarize an extracted section")
    p.add_argument("--section", required=True)
    p.set_defaults(func=cmd_summarize)

    p = sub.add_parser("index", help="Build the vector database")
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("app", help="Launch the Gradio app")
    p.set_defaults(func=cmd_app)

    p = sub.add_parser("all", help="Extract, summarize and index sections")
    p.add_argument("--pdf", required=True)
    p.add_argument("--sections", nargs="+", required=True)
    p.set_defaults(func=cmd_all)
    return parser


def main(argv=None):
    """Parse arguments and run the chosen subcommand."""
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
