#include <stdio.h>

int main()
{
    int x = 1,
        y = 16;

    // Start Semantic Matching
    y = (x > 5) ? y + x : y - x;
    // End Semantic Matching

    return 0;
}
