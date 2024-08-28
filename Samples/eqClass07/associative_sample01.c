#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main()
{
    int x = rand() % 50,
        y = rand() % 50,
        z = rand() % 50;

    bool b = (y > 45 && z >= 20 && z < 40);

    if (x < 10 && b)
    {
        printf("Inside\n");
    }
    else if (x >= 10 && !b)
    {
        printf("Outside\n");
    }

    return 0;
}