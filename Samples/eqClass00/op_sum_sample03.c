#include <stdio.h>

int main()
{
    int x;

    do
    {
        printf("Enter a number: ");
    } while(scanf("%d\n", &x) != 1);

    ++x;

    printf("Your number plus 1: %d\n", x);

    return 0;
}