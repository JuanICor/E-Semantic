# handler_config.py

# Use full import paths as strings
handler_class_path = {
    "add": "Classes.process_egraph.handlers.AddHandler",
    "sub": "Classes.process_egraph.handlers.SubHandler",
    "load": "Classes.process_egraph.handlers.LoadHandler",
    "store": "Classes.process_egraph.handlers.StoreHandler",
    "call": "Classes.process_egraph.handlers.CallHandler",
    "icmp_sgt": "Classes.process_egraph.handlers.GreaterThanHandler",
    "icmp_sle": "Classes.process_egraph.handlers.LessEqualHandler",
    "trunc": "Classes.process_egraph.handlers.TruncHandler",
    "trace": "Classes.process_egraph.handlers.TraceHandler",
    "extract": "Classes.process_egraph.handlers.ExtractionHandler"
}


# [("add", AddHandler()), ("sub", SubHandler()),
#             ("load", LoadHandler()), ("store", StoreHandler()),
#             ("call", CallHandler()), ("icmp_sgt", GreaterThanHandler()),
#             ("icmp_sle", LessEqualHandler()), ("labels", LabelHandler()),
#             ("br_cond", BranchHandler()), ("trunc", TruncHandler()),
#             ("extract", ExtractionHandler())]
