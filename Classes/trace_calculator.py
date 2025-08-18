from collections import Counter
from typing import Generator, TypeAlias

Node: TypeAlias = str
Instruction: TypeAlias = dict[str, int | str | list[str]]
Cfg: TypeAlias = dict[str, list[str] | list[Instruction]]
Trace: TypeAlias = list[Instruction]
FunctionInfo: TypeAlias = dict[str, str | list[str] | dict[str, Cfg]]


class Tracer:

    @staticmethod
    def _get_block_trace(cfg: Cfg,
                         curr_node: Node,
                         trace: list[str] | None = None) -> list[str]:
        found_traces = []
        curr_trace = trace + [curr_node] if trace is not None else [curr_node]
        next_blocks = cfg[curr_node]['succ']

        visit_counts = Counter(curr_trace)

        if not next_blocks:
            return [curr_trace]

        for node in next_blocks:
            if visit_counts.get(node, 0) < 2:
                found_traces.extend(
                    Tracer._get_block_trace(cfg, node, curr_trace))

        return found_traces

    def _generate_instruction_trace(
            cfg: Cfg, block_trace: list[str]) -> Generator[Trace, None, None]:

        for trace in block_trace:
            curr_trace: Trace = []

            for block in trace:
                curr_trace.extend(cfg[block]['instructions'])

            yield curr_trace

    def get_function_traces(self, function_info: FunctionInfo) -> list[Trace]:
        if not (cfg := function_info['blocks']):
            return []

        block_trace = self._get_block_trace(cfg, next(iter(cfg.keys())))

        return list(self._generate_instruction_trace(cfg, block_trace))
