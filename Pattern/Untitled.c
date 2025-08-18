#include "same_rules.h"

void pattern_main(void)
{
    int x;
    OR_pattern
    {
        for(_;_;_)
        {
            _;
            x = x + 1;
            _;
        }
    }
    OR
    {
        x *= 3;
    }
}
