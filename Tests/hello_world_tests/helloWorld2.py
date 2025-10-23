from egglog import *
from helloWorld import CompMath

egraph = EGraph()

a, b = vars_("a b", CompMath)
x, y = vars_("x y", i64)

egraph.register(
    rewrite(CompMath(x) > CompMath(y)).to(
        CompMath(1),
        eq(x.bool_gt(y)).to(Bool(True))
    ),
    rewrite(CompMath(x) > CompMath(y)).to(
        CompMath(0),
        ne(x.bool_gt(y)).to(Bool(True))
    ),
    rewrite(CompMath(x) + CompMath(y)).to(CompMath(x + y)),
    rewrite(CompMath(x) * CompMath(y)).to(CompMath(x * y))    
)


if __name__ == "__main__":
    expr1 = egraph.let("E1", CompMath(3) * CompMath(9) > CompMath(10))
    expr2 = egraph.let("E2", CompMath(5) + CompMath(-4) > CompMath(10))
    egraph.run(10)

    try:
        egraph.check(eq(expr1).to(expr2))
        print("The Expressions are equal.")
    except Exception:
        print("The Expression are not equal.")