import pytest
from unittest.mock import patch
from egglog import EGraph, Ruleset

from Classes.process_egraph import *
from Tests.utils import create_mock_object


def test_handler_execution():
    mock_processor = create_mock_object(EgraphProcessor,
                                        "ProcessorMock",
                                        mock_returns=[("write_load_or_store",
                                                       None)])

    handler = LoadHandler()
    handler.set_processor(mock_processor)
    handler.set_extension("test")

    assert handler._extension == "test"

    handler.execute({"res_reg": "%5", "arg_1": "%3"})

    mock_processor.write_load_or_store.assert_called_once_with(
        "%5.test", "%3.test")

    with pytest.raises(ValueError):
        handler.execute({"res_reg": "%9", "arg": "%1"})


def test_invoker():
    mock_add_handler = create_mock_object(AddHandler,
                                          "AddMock",
                                          mock_returns=[("execute", None)])
    mock_store_handler = create_mock_object(StoreHandler,
                                            "StoreMock",
                                            mock_returns=[("execute", None)])

    invoker = HandlerInvoker()

    invoker.register_handler("add", mock_add_handler)

    assert invoker._handlers == {"add": mock_add_handler}

    invoker.register_handler_list([("add", mock_add_handler),
                                   ("store", mock_store_handler)])

    assert invoker._handlers == {
        "add": mock_add_handler,
        "store": mock_store_handler
    }

    invoker.set_handlers_extension("test")

    mock_add_handler.set_extension.assert_called_once_with("test")
    mock_store_handler.set_extension.assert_called_once_with("test")

    invoker.upload_instruction_data(
        {"add": {
            "res_reg": "%6",
            "arg_1": "%2",
            "arg_2": 3
        }})

    mock_add_handler.execute.assert_called_once_with({
        "res_reg": "%6",
        "arg_1": "%2",
        "arg_2": 3
    })


@patch("Classes.process_egraph.processor.EGraph")
def test_integration(mock_egraph_class):
    mock_ruleset = create_mock_object(Ruleset,
                                      "RulesetMock")
    mock_egraph_instance = create_mock_object(
        EGraph,
        "EgraphMock",
        mock_side_effects=[("let", lambda id, ssa: ssa)])

    mock_egraph_class.return_value = mock_egraph_instance

    # Set Up
    invoker = HandlerInvoker()
    processor = EgraphProcessor(mock_ruleset)
    handlers = [("sub", SubHandler()), ("call", CallHandler()),
                ("store", StoreHandler()), ("load", LoadHandler())]

    invoker.register_handler_list(handlers)
    invoker.set_handlers_processor(processor)
    invoker.set_handlers_extension("test")

    # Execution
    invoker.upload_instruction_data({"store": {"res_reg": "%2", "arg_1": 0}})

    assert processor._egraph_id == 1
    assert list(processor._regs_mapping.keys()) == ["%2.test"]
    assert list(map(str, processor._regs_mapping.values())) == ["SSA(0)"]

    mock_egraph_instance.let.assert_called

    invoker.upload_instruction_data({"store": {"res_reg": "%3", "arg_1": 5}})
    invoker.upload_instruction_data({"sub": {"res_reg": "%4", "arg_1": "%2", "arg_2": "%3"}})

    assert processor._egraph_id == 3
    assert list(processor._regs_mapping.keys()) == ["%2.test", "%3.test", "%4.test"]
    assert list(map(str, processor._regs_mapping.values())) == ["SSA(0)", "SSA(5)", "SSA(0) - SSA(5)"]
