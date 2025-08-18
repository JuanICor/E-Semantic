#include <stdbool.h>

int main()
{
    volatile bool cond = false;
    // Start Semantic Matching
    if (cond)
    {
        return 0;
    }

    int x = -1000;
    // End Semantic Matching
    
    return x;
}
