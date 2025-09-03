#include <stdio.h>

int main()
{
    int x = 2,
        y = 6;

    // Start Semantic Matching
    if (x > 1)
    {
        if (y < 5)
        {
            printf("Inside\n");
        }
    }
    // End Semantic Matching

    return 0;
}
