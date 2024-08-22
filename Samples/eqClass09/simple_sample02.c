#include <stdio.h>

int main()
{
    int x, y;

    printf("Insert two numbers: ");
    while(scanf("%d %d\n", &x, &y) != 2)
    {
        printf("Insert two numbers: ");
    }

    if (x + y > 20)
    {
        return 1;
    } 
    else
    {
        return 0;
    }
}