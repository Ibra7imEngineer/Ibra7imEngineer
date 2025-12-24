#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    do
    {
        height = get_int("Enter thr height of thr pyramid: ");
    }
    while (height < 1);
    for (int d = 1; d <= height; d++)
    {
        for (int s = 0; s < (height - d); s++)
        {
            printf(" ");
        }

        for (int a = 0; a < d; a++)
        {
            printf("#");
        }

        printf("\n");
    }
    return 0;
}
