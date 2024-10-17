#include <stdio.h>
#include <stdlib.h>

int main()
{
    int x = rand() % 100,
        y = rand() % 100;
    
    // Start Semantic Matching
    if (x <= 50 || y > 50)
    {
        printf("Outside\n");
    }
    else if (x > 50 && y <= 50)
    {
        printf("Inside\n");
    }
    // End Semantic Matching
    
    return 0;
}