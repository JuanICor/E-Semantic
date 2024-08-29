#include <stdio.h>

int main()
{
    int a = 25,
        b = 16;

    // Start Semantic Matching
    if (a == 5 * 5)
    {
        if (b == 4 * 4)
        {
            printf("Inside\n");
        }

    }
    // End Semantic Matching
    
    return 0;
}