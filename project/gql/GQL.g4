grammar GQL;

PRINT: 'print' ;
COMMA: ',' ;
QUOTE: '"' ;
LEFT_CURLY_BRACE: '{';
RIGHT_CURLY_BRACE: '}';
LEFT_PARENTHESIS: '(' ;
RIGHT_PARENTHESIS: ')' ;
LINE_END: ';' ;
EMPTY_SET: 'set()';
WS: ([ \t\n\r\f] | ('/*' ~[\r\n]* '*/')) -> skip;
NEWLINE : [\r\n]+ -> skip ;
IDENTIFIER_CHAR : '_' | [a-z] | [A-Z] ;
INT     : '-'? [1-9][0-9]* | '0' ;
BOOL    : 'true' | 'false'  ;

FUN : 'fun';
MAP : 'map';
FILTER: 'filter';
prog:	(stmt NEWLINE?)* EOF ;

stmt:   var '=' expr LINE_END
    |   PRINT expr LINE_END
    ;

lambda_expr: FUN LEFT_PARENTHESIS var RIGHT_PARENTHESIS LEFT_CURLY_BRACE expr RIGHT_CURLY_BRACE ;


var:    IDENTIFIER_CHAR string ;
string: (IDENTIFIER_CHAR | '/' | '.' | INT)* ;


expr:	LEFT_PARENTHESIS expr RIGHT_PARENTHESIS
    |   var
    |   val
    |   MAP LEFT_PARENTHESIS lambda_expr COMMA expr RIGHT_PARENTHESIS
    |   FILTER LEFT_PARENTHESIS lambda_expr COMMA expr RIGHT_PARENTHESIS
    |   intersect
    |   concat
    |   union
    |   star
    ;

val:    LEFT_PARENTHESIS val RIGHT_PARENTHESIS
    |   QUOTE string QUOTE
    |   INT
    |   BOOL
    |   graph
    |   vertices
    |   labels
    |   edges
    ;

graph:  'set_start' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
    |   'set_final' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
    |   'add_start' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
    |   'add_final' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
    |   'load_graph' LEFT_PARENTHESIS path RIGHT_PARENTHESIS
    |   var
    ;

path:   QUOTE string QUOTE
    |   var
    ;

vertices:   'get_start' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
        |   'get_final' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
        |   'get_reachable' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
        |   'get_vertices' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
        |   LEFT_CURLY_BRACE INT (COMMA INT)* RIGHT_CURLY_BRACE
        |   var
        |   EMPTY_SET
        ;

labels: 'get_labels' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
    |   LEFT_CURLY_BRACE (QUOTE string QUOTE | INT | var) (COMMA (QUOTE string QUOTE | INT | var))* RIGHT_CURLY_BRACE
    |   EMPTY_SET
    ;

edges:  'get_edges' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
    |   LEFT_CURLY_BRACE LEFT_PARENTHESIS INT COMMA (val | var) COMMA INT RIGHT_PARENTHESIS ( COMMA LEFT_PARENTHESIS INT COMMA (val | var) COMMA INT RIGHT_PARENTHESIS )* RIGHT_CURLY_BRACE
    |   EMPTY_SET
    ;




intersect   :  'intersect' LEFT_PARENTHESIS expr COMMA expr RIGHT_PARENTHESIS ;
concat      :   'concat' LEFT_PARENTHESIS expr COMMA expr RIGHT_PARENTHESIS ;
union       :   'union' LEFT_PARENTHESIS expr COMMA expr RIGHT_PARENTHESIS ;
star        :   LEFT_PARENTHESIS expr RIGHT_PARENTHESIS '*' ;
