#include <stdio.h>

int main()
{
    int x;

    do
    {
        printf("Enter a number: ");
    } while(scanf("%d\n", &x) != 1);

    x *= 2;

    printf("Your number times 2 is: %d\n", x);

    return 0;
}