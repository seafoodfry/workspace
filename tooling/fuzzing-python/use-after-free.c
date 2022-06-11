#include <stdlib.h>
#include <stdio.h>

int main() {
    char *x = (char*)malloc(10 * sizeof(char*));
    free(x);
    printf("Characters 0 through 5 of x[]: %.6s\n", x);
    printf("Characters 5 through 10 of x[]: %.6s\n", &x[5]);
    return x[5];
}
