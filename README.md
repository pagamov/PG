# PG

;; coment ;;

<table>
    <tr><th>Исходный код</th><th>Итоговый</th></tr>
    <tr><td>def int a ;</td><td>int a;</td></tr>
    <tr><td>def int a = 10 ;</td><td>int a = 10;</td></tr>
</table>

<table>
    <tr><th>Исходный код</th><th>Итоговый</th></tr>
    <tr><td>in int a ;</td>scanf("%d", &a);<td></td></tr>
    <tr><td>out int a ;</td>printf("%d", a);<td></td></tr>
</table>

<table>
    <tr><th>Исходный код</th><th>Итоговый</th></tr>
    <tr><td>a += 4 ;</td><td>a += 4;</td></tr>
    <tr><td>a -= 5 ;</td><td></td></tr>
    <tr><td>a *= 10 ;</td><td></td></tr>
    <tr><td>a /= 2 ;</td><td></td></tr>
</table>

<table>
    <tr><th>Исходный код</th><th>Итоговый</th></tr>
    <tr><td></td><td></td></tr>
    <tr><td></td><td></td></tr>
</table>

          -> 
         -> 

            -> 
            -> a -= 5;
           -> a *= 10;
            -> a /= 2;

a += b ;            -> a += b;
a -= b ;            -> a -= b;
a *= b ;            -> a *= b;
a /= b ;            -> a /= b;

a ++ ;              -> a = a + 1;
a -- ;              -> a = a - 1;
++ a ;              -> a = a + 1;
-- a ;              -> a = a - 1;

a == b ;            -> (a == b)  \
a > b ;             -> (a >  b)   \
a < b ;             -> (a <  b)    \
a >= b ;            -> (a >= b)     \
a <= b ;            -> (a <= b)      \
                                      [not pushed from stack]
a == 10 ;           -> (a == 10)     /
a > 10 ;            -> (a >  10)    /
a < 10 ;            -> (a <  10)   /
a >= 10 ;           -> (a >= 10)  /
a <= 10 ;           -> (a <= 10) /

def string b size_t ;   -> char b[size_t];

def string b 'some text' ; -> char * b = (char *)malloc(size_t);
                              b = "some text";

in string b ;       -> scanf("%s", b);
out string b ;      -> printf("%s", b);









    

    
