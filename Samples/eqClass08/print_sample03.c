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
    printf("%s", (a == 'a') ? "A" :
                   (a == 'b') ? "B" :
                   (a == 'c') ? "C" :
                   "Wrong Letter."
          );
    // End Semantic Matching

    printf("\n");

    return 0;
}