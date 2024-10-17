#include <stdio.h>
#include <stdlib.h>

int main()
{
    int x = rand() % 200;

    // Start Semantic Matching
    if (x < 50 && x < 50)
    {
        printf("Outside\n");
    }
    else if (x >= 50 || x >= 50)
    {
        printf("Inside\n");
    }
    // End Semantic Matching
    
    return 0;
}