from typing import TypeAlias

Opcode: TypeAlias = str
VarType: TypeAlias = str
HandlerName: TypeAlias = str

instructions_handlers_path: dict[Opcode, HandlerName] = {
    "alloca": "AllocHandler",
    "load": "LoadHandler",
    "store": "StoreHandler",
    "add": "AddHandler",
    "sub": "SubHandler",
    "mul": "MultHandler",
    "trunc": "TruncHandler",
    "call": "CallHandler",
    "br": "BranchHandler",
    "gamma": "GammaHandler",
    "icmp": "CompareHandler",
    "ret": "ReturnHandler",
}

global_variables_handlers_path: dict[VarType, HandlerName] = {
    "string": "GlobalStringHandler",
    "struct": "GlobalStructHandler",
}
