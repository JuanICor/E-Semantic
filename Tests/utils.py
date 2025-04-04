from typing import TypeAlias, Any
from unittest.mock import Mock

MethodName: TypeAlias = str
ReturnValue: TypeAlias = Any
SideEffect: TypeAlias = Any

def create_mock_object(
        mock_class: type[object],
        mock_name: str,
        mock_returns: list[tuple[MethodName, ReturnValue]] | None = None,
        mock_side_effects: list[tuple[MethodName, SideEffect]] | None = None) -> Mock:
    mock_object = Mock(name=mock_name, spec_set=mock_class)

    if mock_returns is None: mock_returns = []
    if mock_side_effects is None: mock_side_effects = []

    for method, ret_val in mock_returns:
        mock_method = getattr(mock_object, method)
        mock_method.return_value = ret_val

    for method, side_eff in mock_side_effects:
        mock_method = getattr(mock_object, method)
        mock_method.side_effect = side_eff

    return mock_object
