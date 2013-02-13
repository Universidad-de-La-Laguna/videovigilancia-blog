Title: Acerca de...

# Sistema de videovigilancia _from scratch_

Esta es la web del proyecto de preparación de la práctica "Sistema de
Videovigilancia from Scratch"
para la asignatura de Sistemas Operativos Avanzados de 3º de Grado de
Ingeniería Informática
([ETSII-ULL](http://www.etsii.ull.es/))

Como su propio nombre indica, la idea es desarrollar un sistema de
videoconferencia completo, incluyendo una serie de cámaras inteligentes, un
servidor de almacenamiento para las imágenes y un frontal para el puesto del
operador del sistema. El objetivo es que los estudiantes, al enfrentarse a los
retos de esta práctica, adquieran todas las [competencias](#antecedentes) recogidas
en la memoria académica del grado para la asignatura de Sistemas Operativos
Avanzados.

Este sitio recoge, a modo de blog, todo el material que consideramos
interesante desde el punto de vista del desarrollo de la práctica. Sin embargo es muy
posible que sea también una referencia a tener en cuenta para quienes tienen pensado
desarrollar proyectos similares.

## Arquitectura del sistema
Básicamente el sistema consta de 3 elementos:

 * Una o más cámaras de videovigilancia inteligentes, encargadas de la captura
de las imágenes, procesamiento y envío de las mismas al servidor de
videovigilancia.
 * Un servidor de videovigilancia, donde se recogen y clasifican las imágenes
capturadas por las cámaras.
 * Un frontal para la configuración y monitorización del sistema, así como
para consultar los datos almacenados en el mismo.

En la siguiente figura la interconexión de estos elementos se ilustra en un
esquema general:

<img
src="https://docs.google.com/drawings/d/1M_yEQ_BTL66j23hB6gXWwF31HtpmgNTq-SgMXo6eoj8/pub?w=901&amp;h=420">

Como se puede observar, en principio el frontal puede ir tanto integrado en el
servidor de videovigilancia como correr en un equipo a parte.

## Cámaras inteligentes
Una cámara inteligente es un sistema de visión que posee, a parte de la
electrónica de captura de la imagen, un procesador para tratar los datos
capturados y, generalmente, algún tipo de conexión externa: puerto ethernet o
serie, E/S digital, líneas de control, etc. La idea es poder realizar pequeñas
tareas de procesamiento dentro del propio dispositivo y/o facilitar el acceso
a los datos a través de algún tipo red.

Las cámaras inteligentes son dispositivos relativamente baratos si las
comparamos con un sistema basado en PC al que se conectan cámaras
convencionales. Sin embargo su potencia y flexibilidad, en cuanto a las tareas
que podemos realizar con ellas, son bastante limitadas en relación a su
precio.

Por eso diseñaremos nuestra propia cámara inteligente de bajo coste. Cada
cámara está compuesta por:

 * Una placa computadora [Raspberry Pi](|filename|/Hardware/sbc-rpi.md). Esta
placa ofrece más recursos hardware que la mayor parte de las cámaras
inteligentes disponibles en el mercado. Además dispone de un puerto [GPIO] a
través del que se exponen al exterior diversos buses de interconexión y
recursos de la placa (E/S digital, [I2C], [SPI], RS232, etc).
 * Una cámara [CF7670C-V2] controlable por [I2C].
 * Una [pantalla LCD de 1.8"](|filename|/Hardware/lcd-1.8spi.md) [SPI].

A continuación se muestra un esquema de los diferentes componentes de la
cámara y su interconexión:

<img
src="https://docs.google.com/drawings/d/1FJZdS7dX56nrNA55Y1fnkK1ZlUFSoE24Mr4Qxrkfapk/pub?w=624&amp;h=366">

### Tareas previstas

Obviamente las primeras tareas en el desarrollo de nuestro sistema de
videovigilancia estarán relacionadas con la puesta en marcha de las cámaras
inteligentes:

 * Hacer uso del proyecto [Yocto] para desarrollar una distribución empotrada
de Linux para las cámaras.
 * Familiarizarse con el entorno de desarrollo de aplicaciones de [Yocto] y
las herramientas que provee y con conceptos tales como la compilación cruzada,
la depuración cruzada y la emulación del hardware mediante [QEMU].
 * Desarrollar un controlador para el núcleo que exponga al espacio de usuario
una interfaz de acceso a las funcionalidades de la cámara [CF7670C-V2]. En lo
posible la interfaz expuesta al espacio de usuario debe ser compatible con [V4L],
como cualquier otro dispositivo de vídeo; aunque cualquier tipo de interfaz
básica a medida también serviría.
 * Incluir en la distribución el controlador necesario para hacer accesible
la pantalla LCD SPI de forma transparente como un [framebuffer].
 * Desarrollar una aplicación multihilo que capture las imágenes de la cámara
y las muestre en la pantalla LCD, así como otra información relevante, como por
ejemplo la dirección IP del dispositivo. Para el desarrollo de esta aplicación
se utilizaría [Qt for Embedded Linux] como framework ya que puede funcionar sobre
el dispositivo [framebuffer] de la pantalla LCD.

## Servidor de videovigilancia
En un buen sistema de videovigilancia las imágenes recogidas desde las
diferentes cámaras deben archivarse en un servidor centralizado (que se
ejecutará en un PC) donde puedan ser revisadas, tanto en el momento actual
como en uno posterior.

En este sentido lo primero será diseñar un protocolo de comunicación entre las
cámaras y el servidor adecuado a la tarea que se va a realizar. Con el
objeto de aprovechar el trabajo que otros ya han hecho, los mensajes de dicho
protocolo se serializarán y formatearan para su transmisión con
[Protocol Buffers]. Mientras que en la capa de transporte, para la
transmisión de los mensajes propiamente dicha, se utilizará TCP através de la
interfaz que sobre la del sistema operativo provee [Boost.Asio].

Obviamente no nos olvidamos de otras alternativas a la solución propuesta, como:
[Apache Thrift](http://en.wikipedia.org/wiki/Apache_Thrift) o
[Apache Avro](http://en.wikipedia.org/wiki/Apache_Avro). Sin embargo [Protocol Buffers]
parece ser una librería más sencilla, robusta, mejor documentada y eficiente
en el tamaño de los mensajes serializados. Además de permitirnos escoger la
tecnología de transporte que más nos interese.

En concreto las tareas a realizar serán las siguientes:

### Tareas previstas en las cámaras inteligentes

 * Añadir a la aplicación de captura soporte para procesar las imágenes y
detectar cambios en las mismas.
 * Implementar el protocolo de comunicación comentado anteriormente para
transferir dichas imágenes, y otros datos que puedan ser relevantes, al servidor
de videovigilancia.
 * Hacer algunas pruebas de rendimiento de la aplicación utilizando distintos criterios:
    * Ajustando las prioridades y el tipo de planificación de los hilos y de la E/S.
    * Probando prioridades de tiempo real y un núcleo Linux con el
[parche de tiempo real](https://rt.wiki.kernel.org).
    * Probando el bloqueo de páginas en memoria.

### Tareas previstas en el servidor de videovigilancia

 * Desarrollar un servicio o demonio capaz de escuchar el protocolo
comentado anteriormente, con las características comunes a este tipo de aplicaciones:
    * Soporte para funcionar tanto en modo demonio como en primer plano.
    * Script de arranque estándar en el inicio del sistema.
    * Manejo adecuado de las señales.
    * Salida mediante el uso del [gestor de registro](http://es.wikipedia.org/wiki/Syslog) del sistema.
 * Implementar diversas soluciones para manejar la concurrencia en las comunicaciones
y comparar sus ventajas e inconvenientes: multiproceso con memoria compartida,
comunicación asíncrona y/o multihilo.
 * Implementar el almacenamiento de las imágenes recibidas:
   * Empleando archivos mapeados en memoria para el almacenamiento de las
imágenes en disco, de los metadatos asociados y de los índices para las búsquedas.
   * Utilizando bloqueos para manejar la concurrencia en el acceso a los
archivos cuando sea necesario.
 * **(Opcional)** Implementar la capa de transporte con [0MQ](http://www.zeromq.org/).

## Frontal del operador

Para que las imágenes archivadas puedan tener alguna utilidad es necesario
disponer de un frontal desde el que poder hacer consultas para recuperarlas y
para monitorizar el estado de todo el sistema.

Este es el aspecto menos definido del proyecto, ya que se pueden adoptar diversas
soluciones, todas ellas muy interesantes:

Aplicación de escritorio
: Se puede extender el protocolo de comunicación entre las cámaras y el
servidor para incluir consultas e información de estado. Este protocolo se
utilizaría para comunicar el servidor con una aplicación de escritorio que se
ejecutaría en el puesto de mando. Lo más interesante de esta solución es poder
tener la experiencia de desarrollar una aplicación de escritorio real.

Aplicación web en servidor convencional
: Se puede desplegar en el servidor de videoconferencia un servidor web o
servidor de aplicaciones, según el caso, para el que desarrollar una
aplicación capaz de consultar las imágenes archivadas y sus metadatos. Al
estar la apliación web y el servidor de videovigilancia en procesos diferentes,
sería necesario controlar el acceso a los archivos compartidos mediante el uso
de bloqueos. Además el desarrollo se pude realizar en un lenguaje de programación
diferente a C++.

Aplicación web en servidor empotrado
: Se puede empotrar un servidor web, como [Mongoose](http://code.google.com/p/mongoose/),
en el propio proceso del servidor de videovigilancia. Esta sería la solución más
compacta, aunque tal vez también la menos interesante al incorporar menos novedades.

Sea cual sea la solución finalmente elegida el frontal debe soportar que el
usuario pueda realizar las siguientes acciones:

 * Consultar el estado de las cámaras. Por ejemplo, si están en
funcionamiento, fecha y hora de la última captura, etc.
 * Localizar secuencias de imágenes por cámara y/o fecha y hora y reproducirlas.

## <a id="metodología"></a>Metodología de trabajo

A parte del trabajo concreto a realizar, es necesario destacar algunos
aspectos de la metodología de trabajo que son fundamentales para complementar
la formación de los estudiantes:

 * Los equipos de trabajo se organizarán en grupos de 2 personas, 3 como
máximo.
 * Todo el desarrollo se realizará en GitHub, dentro de una organización
creada al efecto, con los equipos de trabajo correspondientes.
 * Se promoverá el uso de todos los recursos propios de la plataforma:
elaboración de un README, uso de las incidencias y tareas, fork del proyecto
base de la práctica, branching, uso del Wiki para documentar, creación de una
página para el proyecto, etc.
 * Para el protocolo de comunicación entre las cámaras y el servidor de
videovigilancia se acordará una estructura básica y después cada equipo implementará
el suyo para su cámara como considere más conveniente. Para esto seguramente
sólo sea necesario acordar el nombre de un campo con el **ID** de la versión concreta
del protocolo, siendo este **ID** diferente para cada equipo de trabajo. A la
hora de implementar el servidor, cada equipo tendrá que hacerlo funcionar con 1 o 2
cámaras de otros grupos a parte de la suya. Eso significa que tendrán que dar
soporte a otros protocolos y/o proponer parches a otros equipos, según el caso.
 * Todo el trabajo realizado y el resultado final deberá ser presentado y defendido
ante la clase para su evaluación.

## <a id="antecedentes"></a>Antecedentes

Las competencias específicas de la asignatura, tal y como aparecen en la
memoria de grado, son las siguientes:

 * E11. Capacidad de diseñar Software de Sistemas Operativos.
 * E12. Capacidad para verificar y analizar sistemas de tiempo real sencillos.
 * E13. Comprender las ventajas e inconvenientes de distintos planificadores
para Sistemas Operativos.
 * E14. Capacidad para evaluar requerimientos de tiempo real en aplicaciones.

La cuestión era desarrollar contenidos y actividades que permitiera cubrir
estas competencias, manteniendo al mismo tiempo la idea original de que la
asignatura fuera eminentemente práctica, recurriendo a las clases magistrales
sólo para introducir conceptos y líneas de trabajo y dejando de lado la
realización de exámenes para la evaluación.

Tomando en consideración las actividades prácticas, esta podría ser una lista
de deseos a considerar para su diseño:

 * Cubrir todas las competencias.
 * Motivar la creatividad, la innovación, el desarrollo de espíritu
emprendedor, etc.
 * Enfrentar a los estudiantes a problemas de diseño y desarrollo reales.
 * Tener una dificultad controlada, aunque al mismo tiempo deben permitir que
aquellos estudiantes que quieran esforzarse más puedan hacerlo.
 * Ser pocas en cantidad, porque lo contrario difícilmente sería compatible
con plantear problemas de diseño reales.
 * Se debe evitar en lo posible los cambios tecnológicos para intentar
maximizar el aprovechamiento de los conocimientos adquiridos en actividades
prácticas o asignaturas previas.

Con idea de cubrir algunos de los puntos anteriores, una primera aproximación
fue plantear el desarrollo de un servidor de juegos. Es decir, tomar algún
videojuego libre multijugador y desarrollar desde cero un servidor de juego
online. En este sentido tengo que dar las gracias a [Noel Diaz](https://plus.google.com/u/0/107625531464190540689/)
por prestarse a dejarme su versión de **PACMAN**. Creo que hacer una versión
multijugador hubiera sido de lo más interesante.

Lamentablemente esta opción hubiera obligado a preparar al menos una segunda
práctica, ya que por sí misma no cubría el desarrollo de un tipo de software
de sistema muy concreto, los controladores de dispositivo.

Al pensar en esta segunda práctica surgió la idea de desarrollar un sistema de
videovigilancia completo, como práctica única de la asignatura de Sistemas
Operativos Avanzados. Esta solución permite cubrir todas las competencias, al
tiempo que parece encajar perfectamente con nuestra lista de deseos.

## <a id="autor"></a>Sobre el autor y contacto

Mi nombre es [Jesús Torres](https://github.com/aplatanado). Si tienes cualquier
cuestión no dudes en ponerse en contacto [conmigo](jmtorres@ull.es).

[GPIO]: http://en.wikipedia.org/wiki/General_Purpose_Input/Output "General-Purpose Input/Output"
[I2C]: http://es.wikipedia.org/wiki/I2C "I²C (Inter-Integrated Circuit)"
[SPI]: http://es.wikipedia.org/wiki/SPI "Serial Peripheral Interface"
[Protocol Buffers]: |filename|/Overviews/protobufs.md "Google Protocol Buffers"
[Yocto]: |filename|/Overviews/yocto-poky-y-bitbake.md "Yocto, Poky y BitBake"
[Raspberry Pi]: |filename|/Hardware/sbc-rpi.md "Raspberry Pi"
[QEMU]: http://wiki.qemu.org/ "QEMU"
[CF7670C-V2]: |filename|/Hardware/camara-cf7670c.md "CF7670C-V2 (OV7670+AL422)"
[V4L]: http://en.wikipedia.org/wiki/Video4Linux "Video for Linux"
[Qt for Embedded Linux]: http://doc.qt.digia.com/qt/qt-embedded-linux.html "Qt for Embedded Linux"
[framebuffer]: http://es.wikipedia.org/wiki/Framebuffer "Framebuffer"
[Boost.Asio]: http://www.boost.org/doc/libs/1_52_0/doc/html/boost_asio/overview.html "Boost.Asio"