#include <stdio.h>

int main()
{
    int x, y, z;

    // Start Semantic Matching
    x = 6;
    y = 4;
    z = -(y - x);
    // End Semantic Matching

    printf("z = %d\n", z);

    return 0;
}
