#include <stdio.h>

int main()
{
    int a = 5,
        b = 8,
        c = 3;

    // Start Semantic Matching
    if ((a == 5 && b > 10) || (a == 5 && c < 10))
    {
        printf("Inside\n");
    }
    else if ((a != 5 || b <= 10) && (a != 5 || c >= 10))
    {
        printf("Outside\n");
    }
    // End Semantic Matching
    
    return 0;
}