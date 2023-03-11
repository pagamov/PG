#include <stdio.h>

int main(int argc, char *argv[]) {

// coment 
// def int a ; 
int a = 10;
char b[10];
scanf("%d", &a);
a += 4;
a -= 5;
a *= 10;
a /= 2;
printf("%d", a);
a = a + 1;
a = a - 1;
a = a + 1;
a = a - 1;
int c = 10;
a += c;
a -= c;
a *= c;
a /= c;
return 0;
}