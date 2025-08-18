#include <stdio.h>
#include <stdlib.h>

int main()
{
    int x = 53,
        y = 35;

    // Start Semantic Matching
    if (x > 50 && y <= 50)
    {
        printf("Inside\n");
    }
    else if (!(x > 50 && y <= 50))
    {
        printf("Outside\n");
    }
    // End Semantic Matching

    return 0;
}
