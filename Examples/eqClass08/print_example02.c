#include <stdio.h>

int main()
{
    char a;

    printf("Insert a letter: ");
    while (scanf("%c\n", &a) != 1)
    {
        printf("Insert a letter: ");
    }

    // Start Semantic Matching
    switch (a)
    {
    case 'a':
        printf("A");
        break;
    case 'b':
        printf("B");
        break;
    case 'c':
        printf("C");
        break;
    default:
        printf("Wrong Letter.");
        break;
    }
    // End Semantic Matching

    printf("\n");

    return 0;
}
