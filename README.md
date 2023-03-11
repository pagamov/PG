# PG

;; coment ;;

def int a ;         -> int a;
def int a = 10 ;    -> int a = 10;

in int a ;          -> scanf("%d", &a);
out int a ;         -> printf("%d", a);

a += 4 ;            -> a += 4;
a -= 5 ;            -> a -= 5;
a *= 10 ;           -> a *= 10;
a /= 2 ;            -> a /= 2;

a += b ;            -> a += b;
a -= b ;            -> a -= b;
a *= b ;            -> a *= b;
a /= b ;            -> a /= b;

a ++ ;              -> a = a + 1;
a -- ;              -> a = a - 1;
++ a ;              -> a = a + 1;
-- a ;              -> a = a - 1;

def string b size_t ;   -> char b[size_t];
def string b 'some text' ; -> char * b = (char *)malloc(size_t);
                              b = "some text";

in string b ;       -> scanf("%s", b);
out string b ;      -> printf("%s", b);







    

    
