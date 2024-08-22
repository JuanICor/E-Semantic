#include <stdio.h>

int main()
{
    int x = 1,
        y = 16;

    y = (x > 5) ? y + x : y - x;

    return 0;
}