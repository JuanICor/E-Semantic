#include <stdio.h>

int main()
{
    int x = 10,
        i = 0;

    // Start Semantic Matching
    while (i < 10)
    {
        if (i == 5)
            break;
        
        x--;
    }
    // End Semantic Matching
    
    printf("Final Value: %d\n", x);

    return 0;
}