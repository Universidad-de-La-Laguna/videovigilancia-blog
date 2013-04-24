Title: Resource Interchange File Format
Tags: RIFF, AVI, WAV
Date: 2013-04-24

El [Resource Interchange File Format](http://en.wikipedia.org/wiki/Resource_Interchange_File_Format) o [RIFF] es un formato contenedor genérico diseñado para almacenar datos en forma
de fragmentos etiquetados o [chunks]. Siendo usado en la actualidad como formato
contenedor de los conocidos formatos de archivo AVI, ANI y WAV de Microsoft, es
indudable que resulta especialmente útil para almacenar contenidos multimedia,
aunque realmente puede almacenar cualquier tipo de información.

# Tipos de fragmentos

Hay dos tipos de fragmentos en un archivo [RIFF]. El más básico son los
[chunks] o fragmentos de datos propiamente dichos:

~~~~.cpp
struct Chunk
{
    uint32_t type;
    uint32_t size;
    uint8_t  data[size];        // contiene datos en general
};
~~~~

donde `type` sirve para identificar el tipo y el formato de los datos que
almacena el fragmento y `size` para especificar su tamaño —sin incluir ni el
tamaño del campo `type` ni el de `size`—.

El otro tipo de fragmento son las listas:

~~~~.cpp
struct List
{
    uint32_t type;
    uint32_t size;
    uint32_t listType;
    uint8_t  data[size-4];      // contiene otros Chunk o List
};
~~~~

que son aquellos que contienen una colección de otros fragmentos o listas:
    
 * Las listas se identifican y distinguen de otros fragmentos porque su campo
`type` contiene o los 4 caracteres de `RIFF` o de `LIST`[^1]
 * Para este tipo de fragmentos el tamaño en el campo `size` incluye tanto el
 de los datos almacenados dentro del fragmento como el del campo `listType`.
 * Dentro de la lista los fragmentos que contiene se disponen unos detrás de
otros, pero siempre asegurando que cada fragmento comienza en una dirección
par —es decir, que se alinean a 16 bits—.

El archivo contenedor en si mismo es una gran fragmento de lista tipo `RIFF` que
contiene otros fragmentos. Estos pueden ser _chunks_ o listas de tipo `LIST`.
Por lo tanto en una archivo RIFF sólo existe una lista de este tipo, que hace
las veces de contenedor de todos los fragmentos del archivo. El valor del campo
`listType` del fragmento `RIFF` es una secuencia de 4 bytes que identifica el
formato del archivo y se lo conoce como el [FourCC] del mismo.

# Estructura general

Para hacernos una idea del formato este sería el esquema de un archivo AVI
convencional:

~~~.sh
RIFF ('AVI '
      LIST ('hdr1'
            AVIH (<cabecera principal del AVI>)
            LIST ('str1'
                  STRH (<cabecera del flujo>)
                  STRF (<formato del flujo>)
                  ...
                 )
            ...
           )
      LIST ('movi'
            {Chunk | LIST ('rec '
                           Chunk1
                           Chunk2
                           ...
                          )
             ...
            }
            ...
           )
      [IDX1 (<índice AVI>)]
     )
~~~

Donde los identificadores en mayúsculas denotan el valor del campo `type` al
comienzo de un fragmento. Este siempre es seguido por el campo `size`, que no se
muestra en el esquema anterior. Por otro lado el valor de los campos `listType`
de los fragmentos de tipo lista se indica entre comillas simples.

Para observar una estructura real de archivo RIFF se puede utilizar el
programa [rifftree] del paquete `gigtools` con cualquier archivo `.avi` o
`.wav` que tengamos a mano.

# Referencias

 1. Wikipedia - [Resource Interchange File Format](http://en.wikipedia.org/wiki/Resource_Interchange_File_Format)
 2. MSDN - [AVI RIFF File Reference](http://msdn.microsoft.com/en-us/library/ms779636(VS.85).aspx)
 3. [AVI File Format](http://www.alexander-noe.com/video/documentation/avi.pdf)
 2. [FourCC]

[RIFF]: http://en.wikipedia.org/wiki/Resource_Interchange_File_Format "Resource Interchange File Format"
[chunks]: http://en.wikipedia.org/wiki/Chunk_(information) "Chunk (information)"
[FourCC]: http://www.fourcc.org/codecs.php "FourCC"
[rifftree]: http://manpages.ubuntu.com/manpages/lucid/man1/rifftree.1.html "Ubuntu Manpage: rifftree"
[little-endian]: http://es.wikipedia.org/wiki/Endianness "Endianness"

[^1]: Si bien en el archivo se almacenan los caracteres `'R'`, `'R'`, `'I'`, `'F'`
en ese orden, hay que tener en cuenta que al interpretarlo como `uint32_t` en
una máquina _little-endian_ no veremos el número 0x52494646 sino 0x46464952.