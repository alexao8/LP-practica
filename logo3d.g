grammar logo3d;



// Funcio que es crida a l'inici
root : bloc EOF ;

// Un bloc es un conjunt de sentencies
bloc : sentence* ;

// Una sentencia pot ser dels seguents tipus
sentence
    : f_declaration_sent
    | f_sent
    | turtle_sent
    | assig_sent
    | write_sent
    | read_sent
    | if_sent
    | while_sent
    | for_sent
    | coment
    | ENTER
    ;




// Formes que pot tenir una expresio
expr
    : OPEN_PAR expr CLOSE_PAR
    | expr MULT expr
    | expr DIV expr 
    | expr MES expr
    | expr MENYS expr
    | expr GT expr
    | expr LT expr
    | expr GEQ expr
    | expr LEQ expr
    | expr EQ expr
    | expr NEQ expr
    | INT
    | FLOAT
    | ID
    ;




// Sentencia per declarar una funcio amb parametres
f_declaration_sent : PROC ID OPEN_PAR p_decl CLOSE_PAR IS bloc END ;
p_decl : ID? (COMA ID)* ;

// Sentencia que fa una crida a una funcio
f_sent : ID OPEN_PAR p_exec CLOSE_PAR ;
p_exec : expr? (COMA expr)* ;




// Sentencies d'assignacio i d'E/S
assig_sent : ID ASSIGN expr ;
read_sent : READ ID ;
write_sent : WRITE expr ;




// Sentecies condicional i dels bucles
if_sent : IF expr THEN bloc (ELSE bloc)? END ;
while_sent : WHILE expr DO bloc END ;
for_sent : FOR ID FROM expr TO expr DO bloc END ;




// Funcions del Turtle
turtle_sent
    :
        ( FORWARD
        | BACKWARD
        | RIGHT
        | LEFT
        | UP
        | DOWN
        | COLOR
        | SHOW
        | HIDE
        | HOME
        )
    OPEN_PAR p_exec CLOSE_PAR
    ;




// Comentaris
coment : COM (expr)* ENTER ;






// Operadors Aritmetics
    MES : '+' ;
    MENYS: '-' ;
    MULT: '*' ;
    DIV: '/' ;


// Operadors Logics
    GT: '>';
    LT: '<';
    GEQ: '>=';
    LEQ: '<=';
    EQ: '=';
    NEQ: '!=';


// Operador d'assignacio

    ASSIGN: ':=';


// Operadors d'E/S
    READ: '>>';
    WRITE: '<<';


// Sentencia Condicional
    IF: 'IF';
    THEN: 'THEN';
    ELSE: 'ELSE';


// Bucles
    WHILE: 'WHILE';
    FOR: 'FOR';
    FROM: 'FROM';
    TO: 'TO';
    DO: 'DO';


// Comentaris

    COM: '//' ;


// Funcions
    PROC: 'PROC' ;
    IS: 'IS' ;
    COMA: ',' ;


// Funcio main

    MAIN: 'MAIN' ;


// Funcions Tortuga
    FORWARD: 'forward' ;
    BACKWARD: 'backward' ;
    RIGHT: 'right' ;
    LEFT: 'left' ;
    UP: 'up' ;
    DOWN: 'down' ;
    COLOR: 'color' ;
    SHOW: 'show' ;
    HIDE: 'hide' ;
    HOME: 'home' ;


// Parentesis
    OPEN_PAR: '(' ;
    CLOSE_PAR: ')' ;


// Final de sentencia

    END: 'END';





// Tipus de valors
    INT: [0-9]+ ;
    FLOAT: [0-9]+ '.' [0-9]* ;
    ID: [a-zA-Z][a-zA-Z_0-9]* ;
    ENTER : [\n\r];
    WS : [ \t]+ -> skip;