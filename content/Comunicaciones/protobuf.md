Title: Implementando un protocolo con Protocol Buffers
Tags: protobuf, serialización
Date: 2013-03-5
PlusActivityId: z13si3rxdnejjlhvf22egliyvmyrubrkf

[Protocol Buffers] es un mecanismo sencillo para serializar estructuras de
datos, de tal forma que los datos así codificados pueden ser almacenados
o enviados a través de una red de comunicaciones. Esto nos ofrece una forma
sencilla de crear nuestro propio protocolo de comunicaciones, adaptado a las
necesidades de un problema concreto.  

Los pasos concretos para usar [Protocol Buffers] son lo siguientes:

 1. Especificar la estructura de datos del mensaje del nuevo protocolo en un
 archivo `.proto`. Estos archivos se escriben utilizando un [lenguaje de
 descripción de interfaz](https://developers.google.com/protocol-buffers/docs/proto)
 que es propio de [Protocol Buffers].
 
 2. Ejecutar el compilador de [Protocol Buffers], para el lenguaje de la
 aplicación, sobre el archivo `.proto` con el objeto de generar las clases
 de acceso a los datos. Estas proporcionan _accesores_ para cada campo, así
 como métodos para serializar y deserializar los mensajes a y desde
 una secuencia de bytes. 
 
 3. Incluir las clases generadas en nuestra aplicación y usarlas para generar
 instancias del mensaje, serializarlas y enviar los mensajes codificados o
 leer dichos mensajes, deserializarlos y reconstruir las instancias de los
 mensajes para acceder a sus campos.
 
## Definir la estructura del mensaje

Supongamos que conectados a una red tenemos un conjunto de [Arduinos] equipados
con varios sensores de diferente tipo: temperatura, humedad, luminosidad,
movimiento, etc. Cada [Arduino] tiene un nombre que lo identifica y su función
es leer el estado de dichos sensores, a intervalos regulares, y enviar mensajes
con los datos de los mismos a un servidor.

Teniendo esto presente, el archivo `.proto` podría ser el siguiente:

~~~~
// sensorsreport.proto - Protocolo de comunicaciones con Arduino
//
message SensorsReport {
    required string deviceName = 1;     // Nombre del Arduino
    required uint64 timestamp = 2;      // Seg. desde 1/1/1970

    enum SensorType {
        HUMIDITY = 0;
        LUMINOSITY = 1;
        MOTION = 2;
        TEMPERATURE = 3;
    }

    message SensorStatus {
        required SensorType type = 1;
        required int32 value = 2;
    }

    repeated SensorStatus sensors = 3;  // Vector de estados de los
                                        // sensores
}
~~~~

Como se puede observar el lenguaje usado en los archivos `.proto` es muy
sencillo. Solamente hay que indicar el nombre y el tipo de cada campo,
así como si es opcional (_optional_), requerido (_required_) o se repite
(_repeated_).

En [Protocol Buffers] los campos se etiquetan de manera única con un entero
que después es utilizado en la codificación binaria para identificarlos.

## Clases de acceso a los datos

Una vez tenemos la definición de la estructura del mensaje, podemos invocar
al compilador de [Protocol Buffers] para generar las clases de acceso a los
datos.

### Desde línea de comandos

Desde línea de comandos generar las clases es tan sencillo como:

 1. Invocar el compilador de la siguiente manera:

        $ protoc --cpp_out=. sensorsreport.proto

    que genera los archivos `sensorsreport.pb.cc` y `sensorsreport.pb.h` en el
    directorio actual.

 2. Incluir el archivo de cabecera en nuestro código fuente allí donde vaya a
    ser utilizado:

        #include "sensorsreport.pb.h"

 3. Compilar el ejecutable junto con el archivo `sensorsreport.pb.cc` y enlazar
    con la librería `protobuf`.
    
### Con qmake

Si estamos usando `qmake` para construir nuestro proyecto (como es el caso cuando
desarrollamos con el IDE Qt Creator) lo más cómodo es que este se encargue de
invocar al compilador [Protocol Buffers] para generar las clases de acceso
de forma automática.

En este sentido el archivo [protobuf.pri](http://code.google.com/p/ostinato/source/browse/protobuf.pri) del proyecto
[ostinato](http://code.google.com/p/ostinato) puede ser de gran ayuda.

~~~~
#
# Qt qmake integration with Google Protocol Buffers compiler protoc
#
# To compile protocol buffers with qt qmake, specify PROTOS variable and
# include this file
#
# Example:
# PROTOS = a.proto b.proto
# include(protobuf.pri)
#
# By default protoc looks for .proto files (including the imported ones) in
# the current directory where protoc is run. If you need to include additional
# paths specify the PROTOPATH variable
#

PROTOPATH += .
PROTOPATHS =
for(p, PROTOPATH):PROTOPATHS += --proto_path=$${p}

protobuf_decl.name  = protobuf header
protobuf_decl.input = PROTOS
protobuf_decl.output  = ${QMAKE_FILE_BASE}.pb.h
protobuf_decl.commands = protoc --cpp_out="." $${PROTOPATHS} ${QMAKE_FILE_NAME}
protobuf_decl.variable_out = GENERATED_FILES
QMAKE_EXTRA_COMPILERS += protobuf_decl

protobuf_impl.name  = protobuf implementation
protobuf_impl.input = PROTOS
protobuf_impl.output  = ${QMAKE_FILE_BASE}.pb.cc
protobuf_impl.depends  = ${QMAKE_FILE_BASE}.pb.h
protobuf_impl.commands = $$escape_expand(\n)
protobuf_impl.variable_out = GENERATED_SOURCES
QMAKE_EXTRA_COMPILERS += protobuf_impl
~~~~

Para usarlo sólo tenemos que:

 1. Descargarlo al directorio del proyecto con el nombre `protobuf.pri`.
 2. Abrir el archivo `.pro` del proyecto y añadir las líneas:

        PROTOS = sensorsreport.proto
        include(protobuf.pri)

 3. Incorporar la librería `protobuf` al proyecto. El procedimiento sería similar
 al que [comentamos](/deteccion-de-movimiento.html#incorporar_libreria_manualmente)
 para añadir manualmente la librería OpenCV con el objeto de implementar la
 [detección de movimiento](/deteccion-de-movimiento.html)

## Interfaz de Protocol Buffers

Si abrimos el archivo `sensorsreport.proto` veremos que la clase `SensorsReport`
nos ofrece los siguientes _accesores_:

~~~~.cpp
// required string deviceName = 1;
inline bool has_devicename() const;
inline void clear_devicename();
inline const ::std::string& devicename() const;
inline void set_devicename(const ::std::string& value);
inline void set_devicename(const char* value);
inline void set_devicename(const char* value, size_t size);
inline ::std::string* mutable_devicename();
inline ::std::string* release_devicename();

// required uint64 timestamp = 2;
inline bool has_timestamp() const;
inline void clear_timestamp();
inline ::google::protobuf::uint64 timestamp() const;
inline void set_timestamp(::google::protobuf::uint64 value);

// repeated .SensorsReport.SensorStatus sensors = 3;
inline int sensors_size() const;
inline void clear_sensors();
inline const ::SensorsReport_SensorStatus& sensors(int index) const;
inline ::SensorsReport_SensorStatus* mutable_sensors(int index);
inline ::SensorsReport_SensorStatus* add_sensors();
inline const ::google::protobuf::RepeatedPtrField< ::SensorsReport_SensorStatus >&
    sensors() const;
inline ::google::protobuf::RepeatedPtrField< ::SensorsReport_SensorStatus >*
    mutable_sensors();
~~~~

a los campos del mensaje. Además  se define el `enum` `SensorsReport::SensorStatus`
y la clase `SensorsReport::SensorStatus`.

Todos los detalles sobre el código generado por el compilador están documentados
en la [referencia del código generado en C++](https://developers.google.com/protocol-buffers/docs/reference/cpp-generated).
Eso incluye [los accesores creados](https://developers.google.com/protocol-buffers/docs/reference/cpp-generated#fields)
según el tipo de definición de los campos.

### Campos individuales

Por ejemplo, para definiciones de este tipo:

~~~~
optional int32 foo = 1;
required int32 foo = 1;
~~~~

el compilador genera los siguientes _accesores_:

`bool has_foo() const`
: Devuelve `true` si el campo `foo` tiene un valor.

`int32 foo() const`
: Devuelve el valor del campo `foo`. Si el campo no tiene valor, devuelve el
valor por defecto.

`void set_foo(int32 value)`
: Fija el valor del campo. Después de llamar a este método, llamar a `has_foo()`
devolvería `true`.

`void clear_foo()`
: Limpia el valor del campo. Después de llamar a este método, llamar a `has_foo()`
devolvería `false`.

que nos permiten hacer cosas tales como:

~~~~.cpp
SensorsReport report;

report.set_devicename("ARDUINO01");
report.set_timestamp(1362507283);

cout << "Device name: " << report.devicename() << endl;
cout << "Timestamp: " << report.timestamp() << endl;
~~~~

### Campos con repeticiones

Mientras que para definiciones de este tipo:

~~~~
repeated int32 foo = 1;
~~~~

El compilador genera los siguientes _accesores_:

`int foo_size() const`
: Devuelve el número de elementos en el campo.

`int32 foo(int index) const`
: Devuelve el elemento en el índice indicado.

`void set_foo(int index, int32 value)`
: Fija el valor del elemento en el índice indicado.

`void add_foo(int32 value)`
: Añade un nuevo elemento con el valor indicado.

`void clear_foo()`
: Elimina todos los elementos del campo.

`const RepeatedField<int32>& foo() const`
: Devuelve el objeto `RepeatedField`que almacena todos los elementos. Este
contenedor proporciona iteradores al estilo de otros contenedores de la STL.

## Serialización y deserialización

Cada clase de un mensaje ofrece un conjunto de métodos para codificar
(serializar) y decodificar (deserializar) los mensajes:

`bool SerializeToString(string* output) const`
: Serializa el mensaje y almacena los bytes en la cadena especificada en el
argumento `output`. Nótese que estos bytes son binarios, no texto, y que la
clase `std::string` se usa como un mero contenedor.

`bool ParseFromString(const string& data)`
: Deserializa un mensaje codificado en la cadena especificada en el argumento
`data`.

`bool SerializeToOstream(ostream* output) const`
: Escribe el mensaje serializado en el flujo `ostream` indicado.

`bool ParseFromIstream(istream* input)`
: Deserializa un mensaje leido del flujo `istream` indicado.

## Almacenamiento y transmisión por red de múltiples mensajes

El formato de codificación de [Protocol Buffers] no está auto-limitado. Es decir,
no incluye marcas que permitan identificar el principio y fin de los mensajes.
Esto es un problema si se quieren almacenar o enviar varios mensajes en un mismo
flujo de datos.

La forma más sencilla de resolverlo es:

 1. Escribir el tamaño del mensaje codificado y después escribir el mensaje en
 si mismo.

        // Serializar el mensaje
        std::string buffer;
        report.SerializeToString(&buffer);
        uint32 bufferSize = buffer.size();

        // Abrir el archivo de destino y escribir el mensaje
        //
        // std::ofstream ofs(...);
        //
        ofs.write(&bufferSize, sizeof(bufferSize));
        ofs.write(buffer.c_str(), bufferSize);

 2. Al leer, leer primero el tamaño del mensaje, después leer los bytes
 indicados en un  _buffer_ independiente y finalmente deserializar el mensaje
 desde dicho _buffer_.

        // Abrir el archivo de origen y leer el tamaño del mensaje
        //
        // std::ifstream ifs(...);
        //
        uint32 bufferSize;
        ifs.read(&bufferSize, sizeof(bufferSize));

        // Leer el mensaje
        std::string buffer;
        buffer.resize(bufferSize);
        ifs.read(const_cast<char*>(buffer.c_str()), bufferSize);

        // Deserializar
        report.ParseFromString(buffer);

En la misma documentación de la librería se nos sugiere una solución más
conveniente usando las clases `CodedInputStream` y `CodedOutputStream`:

> [Streaming Multiple Messages](https://developers.google.com/protocol-buffers/docs/techniques#streaming)
>
> If you want to avoid copying bytes to a separate buffer, check out the
> CodedInputStream class (in both C++ and Java) which can be told to limit
> reads to a certain number of bytes.

## Referencias

 1. [Protocol Buffers - Google Developers](https://developers.google.com/protocol-buffers/)
 1. [Language Guide](https://developers.google.com/protocol-buffers/docs/proto)
 1. [C++ Generated Code](https://developers.google.com/protocol-buffers/docs/reference/cpp-generated)
 1. [protobuf - Protocol Buffers - Google's data interchange format](http://code.google.com/p/protobuf/)
 1. [Streaming Multiple Messages](https://developers.google.com/protocol-buffers/docs/techniques#streaming)
     * [Protocol Buffers - coded_stream.h](https://developers.google.com/protocol-buffers/docs/reference/cpp/google.protobuf.io.coded_stream)
     * [Stackoverflow - Are there C++ equivalents for the Protocol Buffers delimited I/O functions in Java?](http://stackoverflow.com/questions/2340730/are-there-c-equivalents-for-the-protocol-buffers-delimited-i-o-functions-in-ja)
     * [Stackoverflow - Length prefix for protobuf messages in C++](http://stackoverflow.com/questions/11640864/length-prefix-for-protobuf-messages-in-c)

[Protocol Buffers]: |filename|/Overviews/protobuf.md "Protocol Buffers"
[Arduino]: http://www.arduino.cc/ "Arduino"
[Arduinos]: http://www.arduino.cc/ "Arduino"
