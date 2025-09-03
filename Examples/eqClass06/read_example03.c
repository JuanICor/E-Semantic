#include <stdio.h>

int increment(int* x)
{
    return *x + 1;
}

int main()
{
    int y;
    int* ptr = &y;

    do
    {
        printf("Enter a Number: ");
    }
    while (scanf("%d\n", &y) != 1);

    // Start Semantic Matching
    y = increment(ptr);
    printf("Return Value: %d\n", y);

    return 0;
}
