from Classes.process_file import ProcessFile, create_vars_mapping
from Classes.process_egraph import (HandlerInvoker, EgraphProcessor,
                                    LoadHandler, SubHandler, AddHandler,
                                    StoreHandler, CallHandler,
                                    ExtractionHandler)
from Classes.ssa_graph import SSA_basic_ruleset


def get_file_path(number: int):
    return f"Examples/eqClass00/simple_example0{number}.c"


handlers = [("add", AddHandler()), ("sub", SubHandler()),
            ("load", LoadHandler()), ("store", StoreHandler()),
            ("call", CallHandler()), ("extract", ExtractionHandler())]


def main() -> None:
    invoker = HandlerInvoker()
    processor = EgraphProcessor(SSA_basic_ruleset)

    for id, handler in handlers:
        invoker.register_handler(id, handler)

    invoker.set_handlers_processor(processor)

    for num in range(1, 3):
        filepath = get_file_path(num)
        file_processor = ProcessFile(filepath)
        invoker.set_handlers_extension(filepath)
        invoker.set_variables_mapping(create_vars_mapping(filepath))

        for name in file_processor.get_functions().keys():
            blocks = file_processor.get_function_blocks(name)

            if blocks is None:
                continue

            for _, instructions in blocks.items():
                for instr in instructions:
                    instr_info = file_processor.get_instruction_info(instr)
                    if instr_info != None:
                        invoker.upload_instruction_data(instr_info)

    invoker.display_variables_value("z")

    processor._saturate_graph()
    processor.egraph.display()


if __name__ == "__main__":
    main()
