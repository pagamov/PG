#include <stdio.h>                   
#include <string.h>                   
#include <stdlib.h>

int main(int argc, char *argv[]) {

// coment 
// def int a ; 
int a = 10;
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
// def string b 10 ; 
// b = some text and more; 
char * b = (char *)malloc(10);
b = "some text";
// b = some new text ; 
scanf("%s", b);
// free section
free(b);
return 0;
}