#include <stdio.h>

int main()
{
    int x = 0,
        i = 0;

    // Start Semantic Matching
    while (i < 20)
    {
        x += i;
        i++;
    }
    // End Semantic Matching
    
    printf("Final value: %d\n", x);

    return 0;
}