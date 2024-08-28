#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main()
{
    int x = rand() % 50,
        y = rand() % 50,
        z = rand() % 50;

    bool b = (x < 10 && y > 45);

    if (b && z >= 20 && z < 40)
    {
        printf("Inside\n");
    }
    else if (!b && z < 20 && z >= 40)
    {
        printf("Outside\n");
    }

    return 0;
}