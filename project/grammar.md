## Описание абстрактного синтаксиса языка

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | // а здесь пространство для творчества

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход

lambda =
    // а здесь пространство для творчества
```
### Конкретный синтаксис

```
prog --> (stmt)*

stmt -->
    var '=' expr LINE_END
  | 'print 'LEFT_PARENTHESIS expr RIGHT_PARENTHESIS 

var --> initial_letter string
initial_letter --> IDENTIFIER_CHAR
string --> (initial_letter | '/' | '.' | INT)*

expr -->
     LEFT_PARENTHESIS expr RIGHT_PARENTHESIS
  | var
  | val
  | map
  | filter
  | intersect
  | concat
  | union
  | star

val -->
    LEFT_PARENTHESIS val RIGHT_PARENTHESIS
  | QUOTE string QUOTE
  | INT
  | BOOL
  | graph
  | labels
  | vertices
  | edges

graph -->
    'set_start' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
  | 'set_final' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
  | 'add_start' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
  | 'add_final' LEFT_PARENTHESIS vertices COMMA graph RIGHT_PARENTHESIS
  | 'load_graph' LEFT_PARENTHESIS path RIGHT_PARENTHESIS
  | var

path -->  QUOTE string QUOTE | var

vertices -->
    'get_start' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
  | 'get_final' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
  | 'get_reachable' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
  | 'get_vertices' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS
  | set
  | var

labels --> 'get_labels' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS | set

edges --> 'get_edges' LEFT_PARENTHESIS graph RIGHT_PARENTHESIS | set

set --> LEFT_CURLY_BRACE expr (COMMA expr)* RIGHT_CURLY_BRACE
  | 'set()'
  | LEFT_CURLY_BRACE ( LEFT_PARENTHESIS INT COMMA (val | var) COMMA INT RIGHT_PARENTHESIS )* RIGHT_CURLY_BRACE

lambda --> 'fun' LEFT_PARENTHESIS var RIGHT_PARENTHESIS LEFT_CURLY_BRACE expr RIGHT_CURLY_BRACE

map --> 'map' LEFT_PARENTHESIS lambda COMMA expr RIGHT_PARENTHESIS

filter --> 'filter' LEFT_PARENTHESIS lambda COMMA expr RIGHT_PARENTHESIS

intersert --> 'intersect' LEFT_PARENTHESIS expr COMMA expr RIGHT_PARENTHESIS

concat --> 'concat' LEFT_PARENTHESIS expr COMMA expr RIGHT_PARENTHESIS

union --> 'union' LEFT_PARENTHESIS expr COMMA expr RIGHT_PARENTHESIS

star --> LEFT_PARENTHESIS expr RIGHT_PARENTHESIS '*'

COMMA --> ','
QUOTE --> '"'
LEFT_CURLY_BRACE --> '{'
RIGHT_CURLY_BRACE --> '}'
LEFT_PARENTHESIS --> '('
RIGHT_PARENTHESIS --> ')'
LINE_END --> ';'
IDENTIFIER_CHAR --> '_' | [a-z] | [A-Z]
INT --> [1-9][0-9]* | '0'
BOOL --> 'true' | 'false'
```
### Пример скриптов
1. Загрузка графа
2. Получение финальных вершин в переменную `vertices`
3. Назначение стартовыми всех вершин
4. Печать `vertices`
5. Печать меток обновленного графа
```
graph = load_graph("p/a/t/h");
vertices = get_final(graph);
graph_upd = set_start(get_vertices(graph), graph);
print (vertices);
print (get_labels(graph_upd));
```
1. Загрузка графа
2. Получение всех ребер графа
3. Назначение финальными вершинами стартовые
4. Печать финальных вершин
5. Печать ребер
```
graph = load_graph("skos");
edges = get_edges(graph);
graph_upd = set_final(get_start(graph), graph);
print (get_final(graph_upd));
print (edges);
```
1. Регулярный запрос
2. Регулярный запрос, использующий предыдущий
3. печать конкатенации используемых регулярных запросов
```
a = union ("A", "a");
b_a = (union ("b", a))*;
print (concat (a, b_a));
```