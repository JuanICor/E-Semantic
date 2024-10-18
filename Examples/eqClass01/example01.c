#include <stdbool.h>

int main()
{
    int x;
    volatile bool cond = true;
    // Start Semantic Matching
    if (cond)
    {
        x = -1000;
    }
    else
    {
        x = 1000;
    }
    // End Semantic Matching
    
    return 0;
}
