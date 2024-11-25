#include <stdio.h>

int main()
{
    int x;

    do
    {
        printf("Enter a number: ");
    }
    while(scanf("%d", &x) != 1);

    // Start Semantic Matching
    ++x;
    // End Semantic Matching
    
    printf("Your number plus 1: %d\n", x);

    return 0;
}
