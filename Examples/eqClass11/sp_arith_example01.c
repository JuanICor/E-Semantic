#include <stdio.h>

int main()
{
    int x;
    int x1 = 1, x2 = 8, x3 = 9;

    // Start Semantic Matching
    x = ((x1 + x2) - 6) + x3;
    // End Semantic Matching
    
    printf("z = %d\n", x);

    return 0;
}
