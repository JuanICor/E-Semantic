#include <stdio.h>

int main()
{
    int x;
    int a[10];

    for(int i = 0; i < 10; ++i)
    {
        a[i] = i+1;
    }

    printf("Insert a number: ");
    int result = scanf("%d\n", &x);

    while (result != 1)
        result = scanf("%d\n", &x);

    // Start Semantic Matching
    for(int i = 0; i < 15; ++i)
    {
        if (i > 10)
        {
            break;
        }
    }
    // End Semantic Matching
    
    return 0;
}
