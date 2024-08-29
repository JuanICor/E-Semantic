#include <stdbool.h>

int main()
{
    int x;

    // Start Semantic Matching
    if (false)
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