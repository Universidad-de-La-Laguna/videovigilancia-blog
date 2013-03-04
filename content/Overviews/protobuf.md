Title: Protocol Buffers
Tags: protobuf, serialización
Date: 2013-03-02

[Protocol Buffers] es una herramienta para la serialización[^1] de estructuras de
datos.

Básicamente provee una manera sencilla de definir la estructura de los datos,
pudieron entonces generar código capaz de leer y escribir dichos datos de
manera eficiente, desde diferentes lenguajes y en una variedad de distintos
tipos de flujos de datos.

[Protocol Buffers] fue desarrollado internamente por Google para almacenar
e intercambiar todo tipo de información estructurada. Hasta el punto de que
sirve de base para un sistema de [llamada a procedimiento remoto](http://es.wikipedia.org/wiki/Remote_Procedure_Call)
o [RPC] (Remote Procedure Call) propio que es usado prácticamente para
todas las comunicaciones entre equipos en Google.

En su momento Google hizo generadores de código de [Protocol Buffers] para
C++, Java y Python y liberó la herramienta con una licencia
[BSD](http://es.wikipedia.org/wiki/Licencia_BSD)

La idea detrás de [Protocol Buffers] es muy similar a la que dio origen a
[XML], solo que en este caso el formato es binario, compacto y pone énfasis
en la velocidad a la hora de serializar[^1] y deserializar los datos. Además
es muy similar a [Apache Thrift] (creado y usado internamente por Facebook)
o [Apache Avro], excepto porque [Protocol Buffers] no define un protocolo
[RPC] concreto, sino sólo como deben empaquetarse los datos.

Si se quiere definir un servicio [RPC] que haga uso de un protocolo que se
apoye sobre [Protocol Buffers] para el intercambio de datos, existen
[diversas implementaciones RPC](http://code.google.com/p/protobuf/wiki/ThirdPartyAddOns#RPC_Implementations)
para distintos lenguajes de programación.

## Referencias

 1. [protobuf - Protocol Buffers - Google's data interchange format](http://code.google.com/p/protobuf/).
 1. [Protocol Buffers - Google Developers](https://developers.google.com/protocol-buffers/)
 1. [Wikipedia](http://en.wikipedia.org/wiki/Protocol_Buffers).

[Protocol Buffers]: http://code.google.com/p/protobuf/ "Protocol buffers - Google's data interchange format"
[XML]: http://en.wikipedia.org/wiki/XML "XML"
[Apache Thrift]: http://en.wikipedia.org/wiki/Apache_Thrift "Apache Thrift"
[Apache Avro]: http://en.wikipedia.org/wiki/Apache_Avro "Apache Avro"
[RPC]: http://es.wikipedia.org/wiki/Remote_Procedure_Call "Llamada a Procedimiento Remoto"


[^1]: La serialización es un proceso de codificación de un objeto en un medio
de almacenamiento (como puede ser una archivo o un buffer en memoria), en
ocasiones para transmitirlo a través de una conexión de red o para preservarlo
entre ejecuciones de un programa. La serie de bytes que codifican el estado
del objeto tras la serialización puede ser usada para crear un nuevo objeto,
idéntico al original, tras aplicar el proceso inverso de deserialización.