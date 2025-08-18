from Classes.egraph_elements import graph_ruleset, Instruction, Trace
from Classes.process_egraph import EgraphProcessor, HandlerInvoker
from Classes.trace_calculator import Tracer


class SAMEProcessor:

    def __init__(self) -> None:
        self.invoker = HandlerInvoker(EgraphProcessor(graph_ruleset))

    def construct_egraph_from_llvm(self, llvm_ast) -> None:
        ...

    def _process_function(self, function_data) -> None:
        tracer = Tracer()
        trace_references: list[Trace] = []

        for trace in tracer.get_function_traces(function_data):
            trace_references.append(self._process_trace(trace))

        self.invoker.upload_function(function_data["name"], trace_references)

    def _process_trace(self, trace: list[str]) -> Trace:
        instructions_references: list[Instruction] = []

        for instruction in trace:
            instructions_references.append(
                self._process_instruction(instruction))

        return self.invoker.upload_trace(instructions_references)

    def _process_instruction(self,
                             instruction: dict[str, str | int]) -> Instruction:
        return self.invoker.upload_instruction(instruction, self._egraph)
