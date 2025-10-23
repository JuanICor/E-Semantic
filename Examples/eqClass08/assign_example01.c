#include <stdio.h>

int main()
{
    int x = 1,
        y = 16;

    // Start Semantic Matching
    if (x > 5)
    {
        y = y + x;
    }
    else
    {
        y = y - x;
    }
    // End Semantic Matching

    return 0;
}
