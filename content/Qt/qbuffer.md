Title: Uso de la memoria como un dispositivo de E/S
Tags: qt, qbuffer, qiodevice, qimagewriter, qimagereader
Date: 2013-03-13

Algunas libreras se diseñan específicamente para leer y/o escribir datos en
dispositivos de entrada/salida. Por ejemplo, una librería desarrollada en C++ para
codificar y decodificar archivos MP3 recibiría objetos [std::istream] o
[std::ostream] para indicar el flujo del que leer o en el que escribir los datos
respectivamente:

[std::istream]
: Clase de flujo de entrada. Los objetos de esta clase pueden leer e interpretar
la entrada de datos a partir de secuencias de caracteres.

[std::ostream]
: Clase de flujo de salida. Los objetos de esta clase pueden escribir secuencias
de caracteres y representar como cadenas otras clases de datos.

Por lo tanto, si deseáramos guardar o recuperar audio codificado en MP3 en un
medio de almacenamiento concreto, necesitaríamos disponer de una clase que nos
ofrezca el acceso al mismo a través de la interfaz de flujos de C++ de
entrada/salida descrita por las clases anteriores.

Objetos como [std::cin] y [std::cout] son instancias de estas clases, lo que
permitiría que nuestra aplicación codificara y decodificara audio hacia y
desde la entrada/salida estándar del proceso. Lo mismo ocurre con
[std::ifstream], [std::ofstream] y [std::fstream]; que heredan de las clases
anteriores e implementan la interfaz de flujos de C++ para los archivos. De
esta manera nuestra hipotética librería de MP3 podría codificar y decodificar
datos en este formato hacia y desde dichos archivos.

En este punto la cuestión que se nos plantea es ¿qué podríamos hacer si,
por ejemplo, quisiéramos codificar el audio para posteriormente transmitirlo
a otro ordenador a través de una red? Teniendo en cuenta lo comentado hasta
ahora, una opción sería codificarlo almacenándolo en un archivo y posteriormente
leer del mismo para transmitir los datos por la red. Obviamente esto dista
de ser ideal ya que sería preferible disponer de una clase que implementara
la interfaz de [std::ostream] para almacenar los datos codificados directamente
en la memoria, evitando tener que dar pasos intermedios como guardarlos y
leerlos de un archivo temporal.

Por fortuna la librería estándar de C++ nos provee de las clases:

[std::istringstream]
: Flujo de entrada para operar sobre cadenas. Los objetos de esta clase
permiten leer los caracteres del flujo de entrada a partir del contenido
de un objeto `std::string`.

[std::ostringstream]
: Flujo de salida para operar sobre cadenas. Los objetos de esta clase
permiten escribir los caracteres del flujo de salida en un objeto `std::string`.

[std::stringstream]
: Flujo para operar sobre cadenas. Los objetos de esta clase permiten leer
y escribir en un objeto `std::string`.

ofreciéndonos una forma sencilla de almacenar o leer de la memoria del proceso
los datos codificados en MP3, lo que facilitaría cuaĺquier tarea que quisiéramos
realizar con ellos posteriormente.

## QIODevice

En el _framework_ [Qt] ocurre algo muy parecido. Todas las clases diseñadas
para acceder a dispositivos de entrada/salida reciben un objeto de la clase
[QIODevice]. Por ejemplo:

[QTextStream]
: Proporciona una interfaz adecuada para leer y escribir datos en
formato texto desde un [QIODevice].

[QDataStream]
: Proporciona una interfaz adecuada para leer y escribir datos binarios
desde un [QIODevice].

[QImageReader]
: Proporciona una interfaz independiente del formato para leer archivos de
imágenes desde un dispositivo [QIODevice].

[QImageWriter]
: Proporciona una interfaz independiente del formato para escribir archivos de
imágenes desde un dispositivo [QIODevice].

[QMovie]
: Es una clase diseñada para reproducir películas leidas con [QImageReader]
desde un [QIODevice].

La clase [QIODevice] no se instancia directamente para crear objetos, sino que
su función es definir una interfaz genérica válida para todo tipo de
dispositivos de entrada/salida. En el _framework_ [Qt] diversas clases
heredan de esta, implementando la interfaz [QIODevice] para un dispositivo
concreto:

[QTcpSocket]
: Es una clase heredera de [QIODevice] que permite establecer una conexión
TCP y transferir flujos de datos a través de ella.

[QFile]
: Es una clase heredera de [QIODevice] para leer y escribir archivos de texto
y binarios, así como [recursos de la aplicación](http://qt-project.org/doc/qt-5.0/qtcore/resources.html).

[QProcess]
: Es una clase heredera de [QIODevice] que permite ejecutar un programa externo
y comunicarnos con él.

[QBuffer]
: Es una clase heredera de [QIODevice] que implementa dicha interfaz de
dispositivos sobre un [QByteArray]. Ésta es una clase que provee una interfaz
para manipular un _array_ de bytes en la memoria.

## Ejemplos con imágenes

Para ilustrar lo comentado vamos a codificar y decodificar una imagen [QImage]
directamente desde la memoria.

### Codificando una imagen en la memoria

Supongamos que `image` es un objeto [QImage] que queremos codificar en formato
PNG, guardando el resultado en un _array_ en la memoria para su procesamiento
posterior (p. ej. para transmitirlo a través de una red de comunicaciones).

Hacerlo es tan sencillo como incorporar las siguientes líneas al programa:

~~~~.cpp
QBuffer buffer;
image.save(&buffer, "png");
~~~~

Como hemos comentado, [QBuffer] es un clase heredada de [QIODevice], por lo
que podemos usarla allí donde se requiera un dispositivo de entrada/salida.
Por defecto los objetos de [QBuffer] se crean con un _buffer_ interno de tipo
[QByteArray], al que podemos acceder directamente invocando el método
[QBuffer]::[buffer][](). Por ejemplo:

~~~~.cpp
QByteArray bytes = buffer.buffer();

// Guardamos en un string los primeros 6 bytes de la imagen en PNG
string pngHeader(bytes.constData(), 6);
std::cout << pngHeader << std::endl;
~~~~

lo que mostraría por la salida estándar algo como lo siguiente:

~~~~
�PNG
~~~~

Esta forma de guardar los datos es adecuada cuando no necesitamos más control
sobre las opciones del formato en cuestión. Si por el contrario queremos
controlar el nivel de compresión, el de gamma o algunos otros parámetros
específicos del formato, tendremos que emplear un objeto [QImageWriter]:

~~~~.cpp
QBuffer buffer;
QImageWriter writer(&buffer);
writer.setFormat("jpeg");
writer.setCompression(70);
writer.write(&image):
~~~~

### Decodificando una imagen almacenada en la memoria

Ahora hagámoslo en sentido inverso. Si tenemos un puntero `const char *bytes`
a una zona de memoria con `size` bytes donde se almacena una imagen en formato
PNG y queremos cargarla en un objeto `QImage`, sólo tenemos que asignar los
datos a un objeto `QBuffer` y leer desde el:

~~~~.cpp
QBuffer buffer;
buffer.setData(bytes, size);
QImage image();
image.setDevice(&buffer);
image.setFormat("png");
image.read();
~~~~

o lo que es equivalente y mucho más simple:

~~~~.cpp
QBuffer buffer;
buffer.setData(bytes, size);
image(&buffer, "png");
~~~~

## Referencias

 1. [QBuffer].
 1. [QByteArray].
 1. [QImage].
 1. [QImageReader].
 1. [QImageWriter].


[Qt]: |filename|/Overviews/proyecto-qt.md "Proyecto Qt"
[QIODevice]: http://qt-project.org/doc/qt-5.0/qtcore/qiodevice.html "QIODevice"
[QTextStream]: http://qt-project.org/doc/qt-5.0/qtcore/qtextstream.html "QTextStream"
[QDataStream]: http://qt-project.org/doc/qt-5.0/qtcore/qdatastream.html "QDataStream"
[QMovie]: |filename|/Qt/qmovie.md "QMovie"
[QImageReader]: http://qt-project.org/doc/qt-5.0/qtgui/qimagereader.html "QImageReader"
[QImageWriter]: http://qt-project.org/doc/qt-5.0/qtgui/qimagewriter.html "QImageWriter"
[QTcpSocket]: http://qt-project.org/doc/qt-5.0/qtnetwork/qtcpsocket.html "QTcpSocket"
[QFile]: http://qt-project.org/doc/qt-5.0/qtcore/qfile.html "QFile"
[QProcess]: http://qt-project.org/doc/qt-5.0/qtcore/qprocess.html "QProcess"
[QBuffer]: http://qt-project.org/doc/qt-5.0/qtcore/qbuffer.html "QBuffer"
[QByteArray]: http://qt-project.org/doc/qt-5.0/qtcore/qbytearray.html "QByteArray"
[QImage]: http://qt-project.org/doc/qt-5.0/qtgui/qimage.html "QImage"
[std::istream]: http://www.cplusplus.com/reference/istream/istream/ "std::istream"
[std::ostream]: http://www.cplusplus.com/reference/ostream/ostream/ "std::ostream"
[std::cin]: http://www.cplusplus.com/reference/iostream/cin/ "std::cin"
[std::cout]: http://www.cplusplus.com/reference/iostream/cout/ "std::cout"
[std::ifstream]: http://www.cplusplus.com/reference/fstream/ifstream/ "std::ifstream"
[std::ofstream]: http://www.cplusplus.com/reference/fstream/ofstream/ "std::ofstream"
[std::fstream]: http://www.cplusplus.com/reference/fstream/fstream/ "std::fstream"
[std::istringstream]: http://www.cplusplus.com/reference/sstream/istringstream/ "std::istringstream"
[std::ostringstream]: http://www.cplusplus.com/reference/sstream/ostringstream/ "std::ostringstream"
[std::stringstream]: http://www.cplusplus.com/reference/sstream/stringstream/ "std::stringstream"
[buffer]: http://qt-project.org/doc/qt-5.0/qtcore/qbuffer.html#buffer "QBuffer::buffer()"