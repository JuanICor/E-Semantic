#include <stdbool.h>

int main()
{
    volatile int condition = 0;
    
    // Start Semantic Matching
    if (condition)
    {
        return 0;
    }

    int x = -1000;
    // End Semantic Matching
    
    return 0;
}
