#include <stdbool.h>

int main()
{
    int x;
    volatile int condition = 0;

    // Start Semantic Matching
    if (condition)
    {
        x = 1000;
    }
    else
    {
        x = -1000;
    }
    // End Semantic Matching
    
    return 0;
}
