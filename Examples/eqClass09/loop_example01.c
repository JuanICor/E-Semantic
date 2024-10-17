#include <stdio.h>

int main()
{
    int x = 0;

    // Start Semantic Matching
    for (int i = 0; i < 20; ++i)
    {
        x += i;
    }
    // End Semantic Matching
    
    printf("Final value: %d\n", x);

    return 0;
}