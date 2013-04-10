Title: Concurrencia
Tags: concurrencia, hilos, bucle de mensajes, multiproceso, multihilo, callbacks, qthreadpool
Date: 2013-04-06
PlusActivityId: z12rtbxb3vznxlg1z22egliyvmyrubrkf

La concurrencia tiene que ver con manejar múltiples eventos que se superponen
en el tiempo fuera del control del programa. Por lo tanto debe preocuparse de
manejar la creciente complejidad que surge de la necesidad de un control de
flujo no determinista. Los programas concurrentes vienen con frecuencia
_limitados por la E/S_, como por ejemplo es el caso de las arañas usadas por
los buscadores de Internet para explorar la web. Estos programas inician
varias peticiones HTTP para obtener diversas páginas y aceptan de forma
concurrente las respuestas con su contenido, acumulándolas en el conjunto de
páginas visitadas. El control del flujo es no determinista porque las respuestas
no se reciben necesariamente en el mismo orden en el que el programa hizo las
correspondientes peticiones.

En general existen aplicaciones que son fundamentalmente concurrentes, como
los servidores web, los de archivos, los de base de datos y otros programas
similares que deben manejar al mismo tiempo la conexión con diversos clientes.
También son concurrentes las [aplicaciones paralelas](|filename|/Overviews/paralelismo.md),
donde una tarea se descompone en otras más pequeñas que se ejecutan al mismo
tiempo para obtener el máximo rendimiento, porque en muchas ocasiones no se sabe
de antemano cuando van a terminar estas subtareas o van a intentar acceder a las
estructuras de datos compartidas. Así mismo son concurrentes las aplicaciones
para las GUI modernas, ya que peticiones tales como atender un click de ratón o
actualizar el contenido de una ventana pueden llegar en cualquier momento fuera
del control del programa.

Por su naturaleza no determinista, los programas concurrentes son difíciles de
depurar. 

## Manejar la concurrencia

Hasta el momento hemos dejado entrever las dos motivos más comunes por los que
necesitamos gestionar la concurrencia:

 * Si nuestro programa deben manejar eventos externos que escapan a su control,
como es el caso de un servidor que deben aceptar peticiones de múltiples
clientes o una aplicación interactiva que debe responder ante los eventos
notificados por el sistema a causa de las acciones del usuario, necesitamos
manejar la concurrencia.

     Las tareas de estos programas con frecuencia están _limitadas por la E/S_,
aunque no siempre es así. Por ejemplo, los recolectores de basura concurrentes
presentes en algunas plataformas (p. ej. Java y .NET) están enteramente
_limitados por la CPU_.

     Obviamente todo sería mucho más sencillo si optáramos por ignorar la
concurrencia, manejando en turno una solicitud cada vez. Pero entonces una
petición o un evento bloquearía a los otros hasta que hubiera terminado.

 * Si en nuestro programa queremos usar **programación paralela** para descomponer
ciertas tareas en otras más pequeñas que se puedan ejecutar al mismo tiempo con
el objeto de obtener el máximo rendimiento, también es necesario gestionar la
concurrencia. Sin embargo, por lo general, este tipo de tareas están
_limitadas por la CPU_.

En la actualidad existen diferentes maneras de tratar la concurrencia, que
pueden ser más o menos convenientes según el tipo de problemas a resolver.
Nosotros nos centraremos por el momento en el primer tipo, dejando los detalles
relacionados con la **programación paralela** para un
[artículo posterior](|filename|/Overviews/paralelismo.md).

## Multihilo

El uso de múltiples hilos dentro de un mismo programa es uno de los enfoques
más comunes cuando se plantea resolver un problema de concurrencia. En las
mayor parte de los sistemas modernos los hilos creados por la aplicación son
conocidos y gestionados por el núcleo ([modelo uno a
uno](http://en.wikipedia.org/wiki/Thread_(computing)#1:1_.28Kernel-
level_threading.29)), lo que les permite acceder simultáneamente al mismo y
ser planificados en diferentes procesadores, pudiendo así aprovechar el
paralelismo ofrecido por el hardware en los sistemas multiprocesador y/o
multinúcleo.

<img src="https://docs.google.com/drawings/d/1oViFjM7lI5jCoWx4uM9xD_8DRz9d2mOETWQuzjf3AU4/pub?w=606&amp;h=534" alt="Modelo de hilo 1:1" class="centered">

Obviamente la manera en la que se utilizan los hilos dependen del tipo de problema.
Si lo que se pretende es gestionar eventos o peticiones externas, lo más habitual
es crear un hilo por cliente conectado. Así cada hilo funcionará de manera
independiente procesando y atendiendo las peticiones de su cliente.

### Características

Las principales características de la programación multihilo son:

 * Es muy sencilla, ya que permite gestionar diferentes hilos de ejecución
dentro del espacio de direcciones virtual de un mismo proceso, lo que facilita
la compartición de datos y otros recursos comunes.

 * Se puede volver muy compleja, debido al cuidadoso control que es necesario
hacer sobre el acceso a los recursos compartidos, a poco que el problema crezca.

### Modelos basados en paso de mensajes

Debido a que muchos de los problemas de la programación multihilo provienen de
la compartición de recursos, se ha extendido el uso de modelos basados en paso
de mensajes para resolver problemas concurrentes complejos.

En estos modelos los hilos no acceden directamente a los datos sino que se los
transfieren entre si por medio de mensajes. Así se evita compartir recursos y,
por tanto, el uso de [cerrojos, semáforos y variables de condición](|filename|/Qt/hilos-en-qt.md).
Lamentablemente así se pierde sencillez.

Para estos lenguajes como Scala o Erlang implementan el modelo [Actor], mientras
que Go se basa en en el modelo [CSP]. Ambos casos, pese a [sus diferencias](http://www.informit.com/articles/article.aspx?p=1768317),
fundamentalmente operan tal y como hemos descrito. También entraría dentro de
este tipo de modelos el [mecanismo de comunicación entre hilos](|filename|/Qt/hilos-usando-senales-y-slots.md) que implementa [Qt] a través del uso de señales y _slots_.

## Multiproceso

En los sistemas operativos que implementan una llamada al sistema tipo
[fork]() se pueden crear de forma sencilla múltiples procesos, en lugar de
hilos, para manejar la concurrencia. La forma de hacerlo no difiere mucho de
la programación multihilo, aunque es necesario tener en cuenta los siguientes
aspectos:

 * Escala peor, ya que soportar cientos de clientes implica la creación de
cientos de procesos y estos son más costosos que los hilos, en lo que respecta
al consumo de recursos del sistema.

 * No es tan sencilla como la programación multihilo, porque hay que
indicar explícitamente que regiones de la memoria se desea compartir entre
procesos. Además, normalmente sólo se puede establecer que recursos van a
ser compartidos durante la creación de cada proceso, no pudiendo compartir
otros recursos posteriormente.

 * Los procesos ofrecen mejor aislamiento que los hilos y por tanto mayor
robustez y seguridad.

Respecto a esto último debemos de tener en cuenta que un acceso indebido a la
memoria en uno de los procesos, quizás ocasionada por una petición de un
cliente mal formateada, no tiene por qué provocar la caída de toda la aplicación;
a diferencia de lo que pasaría en una aplicación multihilo. De igual manera,
si un atacante tomara el control de uno de los procesos tendría más difícil tener
acceso a los otros. Además, los procesos tienen características interesantes de
las que carecen los hilos, como la posibilidad de ejecutarse como un usuario
concreto del sistema o en un jaula [chroot].

## Agrupamiento de hilos

Aunque más baratos que los procesos, los hilos tienen un coste que llegado el
momento puede hacer que nuestra aplicación no pueda escalar ya que no se puedan
crear más hilos.

Para evitarlo se puede hacer uso del patrón [agrupamiento de hilos](http://en.wikipedia.org/wiki/Thread_pool_pattern)
(o _thread pool_) que básicamente consiste en:

 1. Crear un grupo de hilos, una cola con las tareas que deben ser ejecutadas en
dichos hilos y otra cola donde almacenar los resultados de las tareas ejecutadas.
<a href="http://commons.wikimedia.org/wiki/File:Thread_pool.svg"><img src="http://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Thread_pool.svg/500px-Thread_pool.svg.png" alt="Sencillo esquema de un agrupamiento de hilos" class="right-float"></a>

 2. Cada vez que un hilo del agrupamiento queda libre, toma la siguiente tarea
de la cola y la ejecuta hasta que es completada, insertando los resultados en
la cola correspondiente.

 3. Cuando la cola de tareas está vacía, los hilos pueden morir o dormir hasta
que hayan más tareas.


### Número de hilos

Obviamente el número concreto de hilos del agrupamiento se debe ajustar con
el objeto de conseguir el mayor rendimiento posible. Con tareas _limitadas por
la E/S_ el número generalmente depende de la capacidad del sistema y del tipo de
tarea, por lo que suele ser necesario determinarlo experimentalmente.

Además, en ocasiones el número de hilos en el agrupamiento puede ser ajustado
por el programa dinámicamente, en base al número de tareas pendientes de ser
ejecutadas. Así la aplicación podría incorporar hilos al agrupamiento sólo si la
cantidad de tareas a la espera supera cierto umbral, y únicamente hasta el
máximo por encima del cual hemos determinado que el rendimiento se vería penalizado.

### Soporte

Debido a la proliferación de los procesadores multinúcleo, es cada vez más
común que los diferentes lenguajes dispongan de alguna implementación del
patrón _agrupamiento de hilos_, ya sea en la librería que lo acompaña o a
través de librerías de terceros, con el fin de facilitar la programación
paralela.

Plataformas como Java y .NET lo incorporan, así como el sistema operativo Mac
OS X bajo el nombre de [Grand Central Dispatch](http://en.wikipedia.org/wiki/Grand_Central_Dispatch) (GCD).
En el caso de C++ existen múltiples librerías, como por ejemplo Intel [TBB], diseñada
específicamente para facilitar que los programas aprovechen las ventajas de
los sistemas multinúcleo, o [Qt], que incorpora su propia implementación del
patrón a través de la clase [QThreadPool]:

~~~~.cpp
class HelloWorldTask : public QRunnable
 {
     void run()
     {
         qDebug() << "Hello world from thread" << QThread::currentThread();
     }
 }

 HelloWorldTask *hello = new HelloWorldTask();
 // QThreadPool takes ownership and deletes 'hello' automatically
 QThreadPool::globalInstance()->start(hello);
~~~~

## Ejecución basada en eventos

Como ya hemos comentado, los hilos tienen un coste que no se puede despreciar
cuando el número que necesitamos es alto. Además, en muchos problemas de
concurrencia las tareas están muy _limitadas por la E/S_, por lo que a penas se
obtiene beneficio alguno de la posibilidad de ejecutarlas en paralelo. En esos
casos la forma de gestionar la concurrencia que se ha demostrado más eficaz es
la ejecución basada en eventos.

Simplificando, sus principales características son:

 * Generalmente sólo se usa un hilo de ejecución. Por tanto no es posible la
ejecución paralela de código, lo que implica que si se ejecutan tareas _limitadas
por la CPU_ se podría estar bloqueando las peticiones de otros clientes al
ocupar el hilo de ejecución.

 * Toda la E/S es asíncrona, para evitar el bloqueo de las peticiones de los
clientes y que las operaciones de E/S se ejecuten en paralelo, tanto entre sí
como respecto al código en el hilo de ejecución.

 * Hace uso de un bucle de mensajes a donde llegan los eventos de E/S
notificados por el sistema operativo. Desde este bucle se llama a las rutinas
de _callback_ correspondientes, donde la aplicación tiene el código que da
respuesta a dichos eventos.

<img src="https://docs.google.com/drawings/d/1vr_1x_UQAW905hjxALQE0hGB6ii55dIiKOsqFD9lw_M/pub?w=809&amp;h=367" alt="Ejecución basada en eventos" class="centered">

Estas rutinas de _callback_ pueden tener nombres predefinidos, como es el caso
del sistema de señales de [Qt], o especificarse a través de un argumento
adicional indicado cuando se solicitó la E/S.

Por lo general los programas que gestionan la concurrencia de esta manera
tiene muchos menos requerimientos de memoria que los que usan múltiples hilos
o procesos, lo que les permite escalar mejor. Este es por ejemplo el caso del
servidor web Nginx o el servidor de aplicaciones en Javascript Node.js cuando
se los compara con Apache, un servidor web que según la configuración utiliza
un hilo o un proceso por conexión.

## Corrutinas

Aunque eficiente, la ejecución basada en eventos puede ser más compleja de
implementar ya que el control del flujo de ejecución se invierte. Es decir, en
un patrón procedural normal la interacción se expresa de forma imperativa,
haciendo llamadas a procedimientos, funciones o métodos. En su lugar, en la
ejecución basada en eventos se especifican las respuestas deseadas a los
eventos notificados, siendo imposible desarrollar una función que contenga
todo el código implicado en una tarea concreta.

Esto se puede resolver incorporando el uso de [corrutinas](http://en.wikipedia.org/wiki/Coroutine).
Estas son una generalización de los procedimientos o subrutinas convencionales
de las que se puede salir por diversos puntos para posteriormente volver y
reiniciar la ejecución desde el último punto de retorno.

<img src="https://docs.google.com/drawings/d/1CiGFeo02uYTWL3Y31u-RpIKBjlLUDrIEaXj8e1_geLw/pub?w=851&amp;h=330" alt="Ejemplo de corrutina" class="centered">

En el contexto de la ejecución basada en eventos, las distintas tareas que deben
ser ejecutadas pueden programarse como corrutinas, mientras que las operaciones
de E/S, a parte de solicitar la operación correspondiente de manera asíncrona,
forzarían la salida de la corrutina. Así el bucle de mensajes, en lugar de
invocar el _callback_ de una operación completada, sólo tiene que restablecer
la ejecución de la corrutina allí donde fue interrumpida.

Los corrutinas son soportadas por algunos lenguajes de alto nivel como Ruby,
Lua o Go. Este último incluso permite planificar su ejecución en paralelo
dentro de un agrupamiento de hilos, dando lugar a lo que sus desarrolladores
ha denominado _goroutines_. Otro ejemplo destacable es Python, que si bien no
las soporta en el intérprete estándar, si lo hacen a través de [Stackless
Python]. Este intérprete es usado en productos como Eve Online o Second Live,
donde el número de conexiones simultáneas es muy alto. Por lo demás la mayor
parte de los lenguajes más populares no lo soportan, ni en el propio lenguaje
ni a través de su librería estándar, con la excepción de C++ a través de la
librería [Boost.Coroutine].

# Referencias

 2. [Concurrency pattern](http://en.wikipedia.org/wiki/Concurrency_pattern)
 3. [Java SE 6 - The Concurrent Collector](http://www.oracle.com/technetwork/java/javase/gc-tuning-6-140523.html#cms)
 4. [A Tale of Two Concurrency Models: Comparing the Go and Erlang Programming Languages](http://www.informit.com/articles/article.aspx?p=1768317)
 5. [Thread pool pattern](http://en.wikipedia.org/wiki/Thread_pool_pattern)
 6. [Understanding the node.js event loop](http://blog.mixu.net/2011/02/01/understanding-the-node-js-event-loop/)
 7. Wikipedia - [Corutine](http://en.wikipedia.org/wiki/Coroutine)

[Qt]: |filename|/Overviews/proyecto-qt.md "Proyecto Qt"
[Actor]: http://en.wikipedia.org/wiki/Actor_model "Actor model"
[CSP]: http://en.wikipedia.org/wiki/Communicating_sequential_processes "Communicating sequential processes"
[fork]: http://es.wikipedia.org/wiki/Bifurcaci%C3%B3n_(sistema_operativo) "Bifurcación (sistema operativo)"
[chroot]: http://es.wikipedia.org/wiki/Chroot "chroot"
[QThreadPool]: http://qt-project.org/doc/qt-5.0/qtcore/qthreadpool.html "QThreadPool"
[TBB]: http://es.wikipedia.org/wiki/Intel_Threading_Building_Blocks "Intel Threading Building Blocks" 
[Stackless Python]: http://en.wikipedia.org/wiki/Stackless_Python "Stackless Python"
[Boost.Coroutine]: http://www.boost.org/doc/libs/1_53_0/libs/coroutine/doc/html/index.html "Boost.Coroutine"
