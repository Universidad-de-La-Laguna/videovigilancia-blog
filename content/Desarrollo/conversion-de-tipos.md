Title: Conversión de tipos en C++
Tags: typecast, c++, cpp, static_cast, dynamic_cast, const_cast, reinterpret_cast
Date: 2013-05-05

En C, cuando una conversión entre dos tipos no es realizada por el compilador de
forma automática —esto sólo ocurre cuando la conversión es segura, como ir de
`char` a `int` o de éste a `float`— se puede forzar utilizando una expresión de
_typecast_ de la forma `(type)object` —o `type(object)`— para convertir el
elemento `object` al tipo especificado por `type`.

En C++, aunque entre los programadores sigue siendo muy común la conversión de
_estilo C_, existen diversos operadores de _typecast_ cuyo uso es más adecuado y
menos peligroso.

# static_cast

El operador:

~~~.cpp
static_cast<type>(object)
~~~

es el primero que se debe intentar utilizar.

Puede hacer conversiones implícitas entre tipos —como de `int` a `float` o de
un puntero a `void*`— así como llamar a los métodos de conversión explícitos
definidos en las clases:

~~~.cpp
operator const char*()
{
    ...
}
~~~

**static_cast** convierte de clases bases a derivadas en una jerarquía de clases
—la conversión de clases derivadas a clases bases es automática— siempre que no
haya polimorfismo[^1]. En cualquier caso las conversiones **static_cast** se
resuelven en **tiempo de compilación** y no comprueban si el tipo al que se
convierte coincide con el tipo real del objeto. El estándar indica que queda
indefinido lo que pueda pasar si se convierte de un tipo base a uno derivado
cuando este último no es el tipo real del objeto.

# dynamic_cast

El operador:

~~~.cpp
dynamic_cast<type>(object)
~~~

se utiliza exclusivamente para manejar el polimorfismo ya que permite convertir
un puntero o referencia de un tipo polimórfico a cualquier otro tipo. Esto no
sólo permite convertir de clases base a derivadas, sino también desplazarnos
lateralmente e incluso movernos a una cadena de herencia diferente dentro de
una misma jerarquía de clases.

**dynamic_cast** busca **en tiempo de ejecución** el objeto del tipo deseado
en la jerarquía, devolviéndolo en caso de encontrarlo. Si los tipos no son
compatibles, devuelve `NULL` para punteros o lanza una excepción
`std::bad_cast` si lo que se convierten son referencias a objetos.

# const_cast

El operador:

~~~.cpp
const_cast<type>(object)
~~~

se usa exclusivamente para eliminar o añadir `const` a una variable, ya que esto
es algo que no pueden hacer los otros operadores de _typecast_.

Es importante destacar que su uso queda indefinido si la variable original
realmente es constante. Por ejemplo, algunos compiladores optimizan las constantes
reemplazándolas donde son utilizadas directamente por el valor que contienen. En
casos como ese, intentar modificar la variable tiene un resultado indefinido
según indica el estándar del lenguaje.

# reinterpret_cast

El operador:

~~~.cpp
reinterpret_cast<type>(object)
~~~

permite convertir un tipo directamente en otro, por lo que es el más peligroso
de los operadores de conversión. Por ejemplo permite convertir punteros de un
tipo a otro o convertir un puntero en un entero para su manipulación. Se utiliza
fundamentalmente para convertir un flujo de bytes en el tipo definitivo con
el que se van a manipular los datos.

La única garantía ofrecida por el estándar de C++ es que si se hace un
**reinterpret_cast** y posteriormente se realiza un conversión al tipo original,
se obtiene el mismo resultado si el tipo intermedio tiene el tamaño suficiente.

# Conversión estilo C

En C++ una conversión de _estilo C_ se define como la primera que tenga éxito
intentándolo en el siguiente orden:

 1. **const_cast**.
 2. **static_cast**.
 3. **static_cast** y después **const_cast**.
 4. **reinterpret_cast**
 5. **reinterpret_cast** y después **const_cast**.

Obviamente este tipo de _typecast_ es peligroso porque se puede convertir en un
**reinterpret_cast**, siendo preferible que si este tipo de conversión es
necesaria se indique de forma explícita, quedando como tal reflejada en el
código.

Además la conversión _estilo C_ ignora el control de acceso cuando realiza un
**static_cast** por lo que que este tipo de conversión permite hacer
operaciones que con las otras no se puede. Diversos ejemplos de esto se pueden encontrar en
[stackoverflow](http://stackoverflow.com/questions/8548667/static-cast- restricts-access-to-public-member-function).

# Referencias

 1. [When should static_cast, dynamic_cast and reinterpret_cast be used?](http://stackoverflow.com/questions/332030/when-should-static-cast-dynamic-cast-and-reinterpret-cast-be-used)
 2. [static_cast restricts access to public member function?](http://stackoverflow.com/questions/8548667/static-cast-restricts-access-to-public-member-function)

[^1]: Un tipo polimórfico es aquel que tiene al menos una función virtual, ya sea
declarada directamente en el o heredada de una clase base.