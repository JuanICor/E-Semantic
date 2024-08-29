#include <stdio.h>

int main()
{
    int x = 0,
        i = 0;

    // Start Semantic Matching
    do
    {
        x += i;
        i++;
    }
    while (i < 20);
    // End Semantic Matching
    
    printf("Final value: %d\n", x);

    return 0;
}