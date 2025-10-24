import rustworkx as rx


class ECallGraph:

    def __init__(self):
        self._graph: rx.PyDiGraph[str, None] = rx.PyDiGraph(multigraph=False)
