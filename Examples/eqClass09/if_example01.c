#include <stdio.h>

int main()
{
    int x, y;

    printf("Insert two numbers: ");
    while (scanf("%d %d\n", &x, &y) != 2)
    {
        printf("Insert two numbers: ");
    }

    // Start Semantic Matching
    if (x + y > 20)
    {
        return 1;
    } 

    return 0;
    // End Semantic Matching
}