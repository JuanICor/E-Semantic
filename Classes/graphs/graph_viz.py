import graphviz
from typing import Protocol


class GraphVisualization(Protocol):
    """
    Protocol for graph visualization.
    Classes don't need to explicitly inherit - just implement the method.
    """

    def to_dot(self) -> str:
        """Generate DOT representation of the graph"""
        ...


def save_dot(graph_obj: GraphVisualization, filename: str) -> None:
    """
    Save the DOT representation to a file.
    Works with any object that implements GraphVisualization protocol.

    Args:
        graph_obj: Object with a to_dot() method
        filename: Path to the output file
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(graph_obj.to_dot())


def visualize_graph(graph_obj: GraphVisualization,
                    filename: str,
                    extension: str = 'png') -> None:
    """
    Generate a visual representation of any graph.
    Works with any object that implements GraphVisualization protocol.

    Args:
        graph_obj: Object with a to_dot() method (must implement GraphVisualization)
        filename: Base name for output file (without extension)
        extension: Output format (png, pdf, svg, etc.)
        default_prefix: Prefix for default filename
    """
    dot_source = graph_obj.to_dot()
    name = filename.rsplit('.', 1)[0]

    graph = graphviz.Source(dot_source)
    graph.render(filename=name, format=extension, cleanup=True)
    print(f"Graph visualization saved as {name}.{extension}")
