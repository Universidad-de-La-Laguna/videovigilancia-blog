Title: BSD sockets
Tags: sockets, POSIX, comunicaciones
Date: 2013-03-02
PlusActivityId: z12qzhgakye0iduyy04cddm5vvifuzcyy1g

_POSIX sockets_ es una parte de la especificación POSIX[^1] que define un API
(Application Programming Interface) para la comunicación entre procesos,
fundamentalmente entre equipos conectados a través de Internet
(_socket_ de Internet), aunque también soporta la conexión local entre procesos
que se ejecutan en el mismo sistema ([socket de dominio UNIX](http://es.wikipedia.org/wiki/Socket_Unix)
o [socket UNIX](http://es.wikipedia.org/wiki/Socket_Unix)).

## Historia

La primera implementación ampliamente distribuida de la pila de protocolos
TCP/IP lo fue con el UNIX 4.2BSD, que incluía _BSD sockets_ (o _Berkeley sockets_)
como API para las comunicaciones entre procesos usando estos protocolos.

Las distintas versiones de BSD incorporaban código del UNIX original de AT&T,
por lo que estaban sujetas a la licencia de software de esta empresa. La
licencias de código fuente se estaban volviendo muy costosas, por lo que muchas
empresas y organizaciones comenzaron a interesarse en la liberación independiente
del código de red, que había sido desarrollado enteramente al margen de AT&T,
por lo que no tenía que estar sujeto a los requerimientos de su licencia.

En junio de 1989 este código fue liberado bajo los términos de la licencia
[BSD](http://es.wikipedia.org/wiki/Licencia_BSD). Muchos fabricantes incluyeron
este código directamente en sus propios sistemas, incluso aunque tuvieran sus
propios protocolos propietarios con los que competían entre ellos. Y algunas
compañías comenzaron a usarlo para vender pilas de protocolo TCP/IP para
Windows, hasta que Microsoft incluyó la suya propia en Windows 95, también
derivada del código de BSD.

Todo esto alimentó el despegue de TCP/IP como protocolo dominante e impuso
los _BSD sockets_ como API de acceso a la red, de tal forma que hoy en día
todos los sistemas operativos modernos tienen una implementación de _BSD
sockets_.

El API _BSD sockets_ evolucionó y finalmente fue adoptado en el estándar
POSIX[^1], donde algunas funciones fueron deprecadas y eliminadas y
reemplazadas por otras. Aun así el API _POSIX sockets_ es básicamente el
_BSD sockets_.

De la misma manera los sistemas Windows incluyen [Winsock], un API de acceso a
la red derivado de _BSD sockets_ que sólo difiere de éste en unos
[pocos detalles](http://tangentsoft.net/wskfaq/articles/bsd-compatibility.html)

## Funciones del API

Este es un resumen de las funciones proporcionadas por _POSIX sockets_:

`socket()`
: Crea un nuevo _socket_, identificado por un número entero, de cierto tipo y
reserva recursos del sistema para él.

`bind()`
: Se usa generalmente en el lado del servidor para asociar un _socket_ con una
dirección de red, por ejemplo una dirección IP y un puerto concretos.

`listen()`
: Se usa en el lado del servidor para hacer que un _socket_ TCP entre en modo
de escucha a la espera de nuevas conexiones entrantes.

`connect()`
: Se usa en el lado del cliente para asignar un número de puerto libre al
_socket_. En el caso de _sockets_ TCP, intenta establecer una nueva conexión TCP
con un _socket_ a la escucha en otro puerto y dirección IP.

`accept()`
: Se usa en el lado del servidor para aceptar una conexión entrante e intentar
crear una nueva conexión TCP con el cliente remoto. Si tiene éxito, crea un
nuevo socket asociado con esta pareja concreta de direcciones en ambos
extremos de la conexión.

`send()` y `recv()`, `write()` y `read()` o `sendto()` y `recvfrom()`
: Se usan para enviar y recibir datos hacia y desde el otro extremo de la conexión.

`close()`
: Hace que el sistema libere los recursos asignados al _socket_. En el caso
de conexiones TCP, ésta es finalizada.

`getaddrinfo()` y `getnameinfo()`
: Se usan para resolver nombres de máquina y direcciones IP ([DNS]).

`select()`
: Se usa para esperar a que uno o más _sockets_ de una lista estén listos
para leer, escribir o tengan algún error.

`poll()`
: Se usa para comprobar el estado de un _socket_ en un conjunto de _sockets_.
Puede comprobar si están listos para escribir, leer o si ha ocurrido algún error.

`getsockopt()`
: Se usa para recuperar el valor actual de una opción concreta de configuración
del _socket_ especificado.

`setsockopt()`
: Se usa para cambiar el actual de una opción concreta de configuración del
_socket_ especificado.

## POSIX API en Boost.Asio

[Boost.Asio] es una librería de C++ para programadores de software de sistema
donde el acceso a funcionalidades del sistema operativo; como la red, los archivos,
un puerto serie, etc.; se requiere con cierta frecuencia. El acceso a estos recursos
suele implicar operaciones de E/S que normalmente consumen mucho tiempo antes
de completarse, por lo que [Boost.Asio] provee de herramientas para gestionar
estas conexiones de manera asíncrona, sin necesitar modelos de concurrencia
basados en hilos o en múltiples procesos y memoria compartida.

Debido a que uno de los usos principales de esta librería son las comunicaciones
por red, [Boost.Asio] incluye una interfaz multiplataforma de _sockets_ de bajo nivel,
basada en el API _BSD sockets_, e implementada sobre la que proporciona el propio
sistema operativo.

A diferencia de esta última, la implementación proporcionada por [Boost.Asio] no incluye
algunos aspectos del API original que no son seguros o que son propensos a provocar
errores de programación. Por ejemplo, el uso de `int` para identificar a los _sockets_
por parte del API _BSD sockets_ carece de la seguridad que nos ofrecería tener un
tipo específico para ellos. Por eso la representación de un _socket_ en [Boost.Asio] usa
un tipo distinto para cada protocolo. Es decir, para TCP el tipo de un socket es
`ip::tcp::socket` mientras para UDP el tipo es `ip::udp::socket`.

En la documentación de [Boost.Asio] se incluye una [tabla](http://www.boost.org/doc/html/boost_asio/overview/networking/bsd_sockets.html)
que muestra la relación entre el API _BSD socket_ y el API de acceso a red de [Boost.Asio]:

## Referencias

 1. Wikipedia - [Berkeley sockets](http://en.wikipedia.org/wiki/Berkeley_sockets).
 1. [Wnsock - Windows Sockets API](http://msdn.microsoft.com/es-es/library/windows/desktop/ms740673(v=vs.85).aspx).
 1. [Winsock Programmer's FAQ - BSD Sockets Compatibility](http://tangentsoft.net/wskfaq/articles/bsd-compatibility.html).
 1. [Boost.Asio].
  
[Winsock]: http://msdn.microsoft.com/es-es/library/windows/desktop/ms740673(v=vs.85).aspx "Windows Sockets API"
[DNS]: http://es.wikipedia.org/wiki/Domain_Name_System "DNS - Domain Name System"
[Boost.Asio]: http://www.boost.org/libs/asio/ "Boost.Asio"
 
[^1]: POSIX son las siglas de Portable Operating System Interface, una familia
de estándares especificados por el [IEEE](http://www.ieee.org/) para mantener
la compatibilidad entre sistemas operativos. POSIX define un API, tomando del
de los sistemas UNIX, para asegurar la compatibilidad entre las distintas
variantes de UNIX y otros sistemas operativos.