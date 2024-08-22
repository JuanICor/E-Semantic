#include <stdio.h>

int main()
{
    char a;

    printf("Insert a letter: ");
    while(scanf("%c\n", &a) != 1)
    {
        printf("Insert a letter: ");
    }

    if (a == 'a')
    {
        printf("A");
    }
    else if (a == 'b')
    {
        printf("B");
    }
    else if (a == 'c')
    {
        printf("C");
    }
    else
    {
        printf("Wrong Letter.");
    }

    printf("\n");

    return 0;
}