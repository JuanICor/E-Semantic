#include <stdio.h>

int increment(int* x)
{
    return *x + 1;
}

int main()
{
    int y;

    do
    {
        printf("Enter a Number: ");
    }
    while (scanf("%d\n", &y) != 1);

    // Start Semantic Matching
    y = increment(&y);
    // End Semantic Matching
    
    printf("Return Value: %d\n", y);

    return 0;
}