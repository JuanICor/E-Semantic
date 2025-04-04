import argparse

from Classes.process_file import FileProcessor
from Classes.process_egraph import (
    HandlerInvoker, EgraphProcessor, LoadHandler, SubHandler, AddHandler,
    StoreHandler, CallHandler, GreaterThanHandler, LessEqualHandler,
    TruncHandler, LabelHandler, ExtractionHandler, BranchHandler)
from Classes.ssa_graph import SSA_basic_ruleset


handlers = [("add", AddHandler()), ("sub", SubHandler()),
            ("load", LoadHandler()), ("store", StoreHandler()),
            ("call", CallHandler()), ("icmp_sgt", GreaterThanHandler()),
            ("icmp_sle", LessEqualHandler()), ("labels", LabelHandler()),
            ("br_cond", BranchHandler()), ("trunc", TruncHandler()),
            ("extract", ExtractionHandler())]


def main(files: list[str], variable: str) -> None:
    invoker = HandlerInvoker()

    values = []

    invoker.register_handler_list(handlers)

    for filepath in files:
        processor = EgraphProcessor(SSA_basic_ruleset)
        invoker.set_handlers_processor(processor)

        file_processor = FileProcessor(filepath)
        invoker.set_handlers_extension(filepath)
        invoker.set_variables_mapping(file_processor.create_var_map())

        parsed_llvm = file_processor.process_file()

        for function in parsed_llvm["functions"]:
            if (func_instr := function.get("instructions")) is None:
                continue

            for instruction in func_instr:
                invoker.upload_instruction_data(instruction)

        values.append(invoker.get_variable_value(variable))

    if values[0] == values[1]:
        print("The expressions matched!")

    else:
        print(f"Expressions didn't match.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Matches programs semantically.")
    parser.add_argument("file1",
                        type=str,
                        help="Path to the first file")
    parser.add_argument("file2",
                        type=str,
                        help="Path to the second file")
    parser.add_argument("--variable",
                        type=str,
                        help="Variable to inspect")

    args = parser.parse_args()

    main(files=[args.file1, args.file2], variable=args.variable)
