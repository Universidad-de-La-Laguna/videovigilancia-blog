Title: Servicios y demonios en Linux
Tags: demonio, servicio, init, syslog, FHS, getopt, daemon, umask, Qxt, setsid, LSB, runlevel, nivel de ejecución, /etc/init.d, /var/run
Date: 2013-05-18

Un [demonio][^1] o servicio es un programa que se ejecuta en segundo plano,
fuera del control interactivo de los usuarios del sistema ya que carecen de
interfaz con estos.

El sistema generalmente inicia los demonios durante el arranque, siendo las
funciones más comunes de estos las de ofrecer servicios a otros programas, ya
sea respondiendo a las peticiones que llegan a través de la red o atendiendo a
procesos que se ejecutan en el mismo sistema, así como responder ante cierta
actividad del hardware —por ejemplo `acpid`[^2] maneja el apagado del sistema
cuando el usuario pulsa el botón de encendido del equipo—. Algunos demonios
sirven para configurar hardware —como es el caso de `udevd` en algunos sistemas
GNU/Linux— ejecutar tareas planificadas —como hace `cron`— o realizar otras
funciones similares.

# Crear demonios del sistema

En Linux, cuando ejecutamos un comando cualquiera, como `ls`:

~~~~.sh
$ ls
~~~~

el nuevo proceso `ls` es hijo del proceso de la _shell_ desde la que lo hemos
ejecutado. Dicha _shell_ conoce su PID y puede bloquearse esperando a que el
comando termine, antes de volver a mostrar el _prompt_[^3] para indicar al
usuario que puede introducir un nuevo comando. Incluso si la _shell_ decide no
esperar a que el comando termine —por ejemplo cuando en `bash` el usuario lo
indica utilizando el caracter `&`— permitiendo la ejecución en segundo plano,
esta será notificada cuando el proceso hijo termine mediante una señal,
pudiendo así controlar el estado de los distintos comandos en ejecución.
Además la _shell_ tiene acceso al motivo por el que el proceso hijo terminó,
así como al código de estado devuelto por este a través de la llamada al
sistema [exit][]().

Por lo tanto los procesos que quieren convertirse en un [demonio] deben
asegurarse que siempre se ejecutan en segundo plano, desvinculándose del
proceso de la _shell_ que los invocó y de la [terminal del
sistema](http://en.wikipedia.org/wiki/POSIX_terminal_interface) desde la que
esta se ejecutaba.

## Crear un proceso hijo

El primer paso para que un proceso se convierta en un [demonio] es crear un
proceso hijo y a continuación terminar el proceso padre:

~~~~.cpp
pid_t pid;

// Nos clonamos a nosotros mismos creando un proceso hijo
pid = fork();

// Si pid es < 0, fork() falló
if (pid < 0) {
    // Mostrar la descripción del error y terminar
    std::cerr << strerror(errono) << std::endl;
    exit(10);
}

// Si pid es > 0, estamos en el proceso padre
if (pid > 0) {
    // Terminar el proceso
    exit(0);
}

// Si la ejecución llega a este punto, estamos en el hijo
~~~~

Al finalizar el proceso padre el proceso hijo es adoptado por `init`[^4]. El
resultado es que la _shell_ piensa que el comando terminó con éxito,
permitiendo que el proceso hijo se ejecute de manera independiente en segundo
plano.

## Cambiar umask

Todos los procesos tiene una máscara que indica que permisos no deben
establecerse al crear nuevos archivos. Así cuando se utilizan llamadas al
sistema como [open][]() los permisos especificados se comparan con esta
máscara, desactivando de manera efectiva los que en ella se indiquen.

La máscara —denominada [umask][]()— es heredada de padres a hijos por los
procesos, por lo que su valor por defecto será el mismo que el que tenía
configurada la _shell_ que lanzó el demonio. Esto significa que el [demonio]
no sabe que permisos acabarán tenido los archivos que intente crear. Para
evitarlo simplemente podemos autorizar todos los permisos:

~~~~.cpp
umask(0)
~~~~

o establecer específicamente para [umask][]() otro valor más seguro según nuestra
conveniencia. Incluso algunos desarrolladores permiten que los administradores
del sistema especifiquen la máscara deseada a través del archivo de
configuración del [demonio].

## Abrir conexión con el registro de eventos

Puesto que un demonio se ejecuta en segundo plano no debe estar conectado a
ninguna terminal. Sin embargo esto plantea la cuestión de cómo indicar
condiciones de error, advertencias u otro tipo de sucesos del programa.

Algunos demonios almacenan estos mensajes en archivos específicos o en su
propia base de datos de sucesos. Sin embargo en muchos sistemas existe un
servicio especifico para registrar estos eventos. En lo sistemas basados en
UNIX este servicio lo ofrece el demonio [Syslog], al que otros procesos
pueden enviar mensajes a través de la función [syslog][]().

~~~~.cpp
// Abrir una conexión al demonio syslog
openlog(argv[0], LOG_NOWAIT | LOG_PID, LOG_USER);

...

// Enviar un mensaje al demonio syslog
syslog(LOG_NOTICE, "Demonio iniciado con éxito\n");

...

// Cuando el demonio termine, cerrar la conexión con
// el servicio syslog
closelog();
~~~~

Al crear la conexión se especifica un código de recurso —en el ejemplo
anterior `LOG_USER` indica mensajes genéricos de nivel de usuario— que indica
el tipo de software que genera los mensajes. Además cada mensaje se envía
acompañado de un nivel de severidad —`LOG_NOTICE` especifica que nuestro
mensaje no es más que una aviso—. El administrador del sistema puede configurar
[Syslog] para que haga cosas diferentes con los mensajes según el código de
recurso y el nivel de severidad. Por ejemplo pueden ser escritos a un archivo
concreto en disco, mostrados por una consola, enviados por red a registro de
eventos centralizados o filtrados.

### Registro de eventos en aplicaciones Qt

Cuando se desarrolla con [Qt] puede ser interesante echar un vistazo a las
funcionalidades de la librería [LibQxt]. Este proyecto proporciona un conjunto
de clases que añaden funcionalidades multiplataforma que no están disponibles
en el _framework_ [Qt].

Entre dichas funcionalidades adicionales está la clase [QxtLogger], que facilita
que el demonio registre los eventos en sus propios archivos de sucesos
[QxtLogger] —por ejemplo `/var/log/midemonio/info.log`,
`/var/log/midemonio/debug.log`, etc.— de forma más apropiada para una aplicación
en C++.

~~~~.cpp
#include <QxtBasicFileLoggerEngine>
#include <QxtLogger>

...

// Configurar QtLogger para usar dos archivos de registro. Uno para
// los niveles de severidad de INFO en adelante y otro para los
// niveles de DEBUG en adelante.

// Primero se crea un engine por archivo de registro
QxtBasicFileLoggerEngine *debug =
    new QxtBasicFileLoggerEngine("debug.log");
QxtBasicFileLoggerEngine *info =
    new QxtBasicFileLoggerEngine("info.log");

// Cada engine se registra en el objeto QtLogger asignándole
// un nombre diferente
qxtLog->addLoggerEngine("dbg", debug);
qxtLog->addLoggerEngine("app", info);

// Finalmente se indica que niveles de severidad se envían a cada
// engine y, por tanto, a cada archivo de registro
qxtLog->disableAllLogLevels();

qxtLog->enableLogLevels("dbg", QxtLogger::AllLevels);
qxtLog->enableLogLevels("app",  QxtLogger::InfoLevel |
                                QxtLogger::WarningLevel |
                                QxtLogger::ErrorLevel |
                                QxtLogger::CriticalLevel |
                                QxtLogger::FatalLevel |
                                QxtLogger::WriteLevel );

...

// Y ya podemos registar los distintos sucesos.
qxtLog->info("Demonio iniciado con éxito");

...

qxtLog->info(QTime::currentTime(), "Algo ha ocurrido", 3.14);
~~~~

En teoría el mecanismo usado por [QxtLogger] es lo bastante flexible como para
que sea posible extenderlo con el objeto de usar el registro del sistema
—a través de la función [syslog][]()— en lugar de nuestros propios archivos,
si estuviéramos interesados en ello.

## Crear una nueva sesión

Cada proceso es miembro de un grupo y estos a su vez se reúnen en sesiones. En
cada una de estas hay un proceso que hace las veces de líder, de tal forma que
si muere todos los procesos de la sesión reciben una señal `SIGHUP`. La idea
es que el líder muere cuando se quiere dar la sesión por terminada, por lo que
mediante `SIGHUP` se notifica al resto de procesos esta circunstancia para que
puedan terminar ordenadamente.

Obviamente no estamos interesados en que el [demonio] termine cuando la sesión
desde la que fue creado finalice, por lo que necesitamos crear nuestra propia
sesión de la que dicho [demonio] será el lider:

~~~~.cpp
pid_t sid;

// Intentar crear una nueva sesión
sid = setsid();
if (sid < 0) {
    syslog(LOG_ERR, "No fue posible crear una nueva sesión\n");
    exit(11);
}
~~~~

## Cambiar el directorio de trabajo

Hasta el momento el directorio de trabajo del proceso es el mismo que el de la
_shell_ en el momento en el que se ejecutó el comando. Este podría estar
dentro de un punto de montaje cualquiera del sistema, por lo que no tenemos
garantías de que vaya a seguir estando disponible durante la ejecución del
proceso.

Por eso es probable que prefiramos cambiar el directorio de trabajo al
directorio raiz, ya que podemos estar seguros de que siempre existirá:

~~~~.cpp
// Cambiar el directorio de trabajo de proceso
if ((chdir("/")) < 0) {
    syslog(LOG_ERR, "No fue posible cambiar el directorio de "
                    "trabajo a /\n");
    exit(12);
}
~~~~

Otra opción es cambiar el directorio de trabajo a donde se almacenan los datos
de nuestra aplicación o a algún otro directorio similar, siempre según el
[Filesystem Hierarchy Standard].

## Reabrir los descriptores estándar

Como ya hemos comentado, un [demonio] no interactúa directamente con los
usuarios, por lo que no necesita usar la E/S estándar, así que podemos cerrar
sus descriptores:

~~~~.cpp
// Cerrar los descriptores de la E/S estándar
close(STDIN_FILENO);            // fd 0
close(STDOUT_FILENO);           // fd 1
close(STDERR_FILENO);           // fd 2
~~~~

Sin embargo esto puede no ser lo más conveniente porque los siguientes
archivos que se abran —archivos de registro, _sockets_, etc— reusarán esos
mismos descriptores, lo que puede ser un problema si se utiliza alguna
librería que pueda intentar hacer uso de la E/S estándar. En su lugar puede ser
preferible mantenerlos abiertos pero conectados al archivo `/dev/null`:

~~~~.cpp
// Cerrar los descriptores de la E/S estándar
close(STDIN_FILENO);                    // fd 0
close(STDOUT_FILENO);                   // fd 1
close(STDERR_FILENO);                   // fd 2

int fd0 = open("/dev/null", O_RDONLY);  // fd0 == 0
int fd1 = open("/dev/null", O_WRONLY);  // fd0 == 1
int fd2 = open("/dev/null", O_WRONLY);  // fd0 == 2
~~~~

# Usar daemon()

Algunos de los pasos comentados anteriormente se pueden hacer de una sola vez
mediante la función [daemon][]():

   1. Hace el [fork][]() y termina el proceso padre.
   2. Opcionalmente puede cambiar el directorio de trabajo pero sólo al directorio raíz.
   3. No ajusta [umask][]().
   4. Opcionalmente reabre los descriptores de archivo estándar a `/dev/null`.

En todo caso el principal inconveniente es que no es una función del estándar
POSIX, por lo que en algunas plataformas puede no existir o tener un
comportamiento diferente.

# Cambiar la personalidad del proceso

Los demonios son generalmente lanzados por el usuario `root`, lo que les da
acceso a todos los recursos del sistema. Esto puede ser muy peligroso si un
atacante se saltara las medidas de seguridad incorporadas en el programa y
fuera capaz de hacer que ejecutara código arbitrario.

Para evitarlo es muy común que los demonios cambien su personalidad a un
usuario y grupo convencional del sistema:

~~~~.cpp
// Cambiar el usuario efectivo del proceso a 'midemonio'
passwd* user = getpwnam("midemonio");
seteuid(user->pw_uid);

// Cambiar el grupo efectivo del proceso a 'midemonio'
group* group = getgrnam("midemonio");
setegid(group->gr_gid);
~~~~

# Señales

Una vez el demonio está en ejecución las señales ser convierten en un
mecanismo muy potente para comunicarnos con él:

 * Debe atender la señal `SIGTERM` para terminar en condiciones de seguridad.
 * Es muy común que intercepte la señal `SIGHUP` ya que así se le suele indicar
 que recargue los archivos de configuración sin tener que reiniciarlo.

Si estamos desarrollando nuestra aplicación con [Qt], lo más conveniente es
echar un vistazo al final del artículo [Aplicaciones de consola con
Qt](|filename|/Qt/aplicaciones-de-consola.md) ya que allí se explican las
particularidades del uso de señales POSIX en este tipo de aplicaciones.

# Arranque del servicio

Los demonios `init` de muchos sistemas operativos operan en base a _niveles de
ejecución_. Cada [nivel de ejecución] define un estado de la máquina después
del arranque, estableciendo que demonios deben ser iniciados y/o detenidos
para alcanzarlo. Por lo tanto en cada momento sólo puede haber un [nivel de
ejecución] activo.

Por lo general existen 7 niveles —del 0 al 6— alguno de los cuales suelen ser
para:

 * Entrar en modo monousuario (generalmente el 1 o S).
 * Entrar en modo multiusuario sin soporte de red.
 * Entrar en modo multiusuario con soporte de red.
 * Apagar el sistema (generalmente el 0).
 * Reiniciar el sistema (generalmente el 6).

Para iniciar o detener los demonios según el nivel de ejecución, estos suelen
ir acompañados de un _script_ de inicio que por lo general se almacena en el
directorio `/etc/init.d`. En aquellas distribuciones de Linux que siguen el
estándar LSB[^5] la estructura de este _script_ suele ser muy similar a la
siguiente:

~~~~.sh
#!/bin/sh
#
# midemoniod    /etc/init.d initscript para MiDemonio
#

### BEGIN INIT INFO
# Provides:          midemonio
# Required-Start:    $network $local_fs $remote_fs
# Required-Stop:     $network $local_fs $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: inicia y detiene midemonio
# Description:       MiDemonio es el mejor demonio. Y este archivo
#                    es un ejemplo de como crear un script de
#                    inicio.
### END INIT INFO

# Salir inmediatamente si un comando falla
# http://www.gnu.org/software/bash/manual/bashref.html#The-Set-Builtin
set -e

# Importar funciones LSB:
# start_daemon, killproc, status_of_proc, log_*, etc.
. /lib/lsb/init-functions

NAME=midemoniod
PIDFILE=/var/run/$NAME.pid
DAEMON=/usr/sbin/$NAME
DAEMON_OPTS="--daemon"

# Si el demonio no existe, salir.
test -x $DAEMON || exit 5

start()
{
    log_daemon_msg "Starting the $NAME process"
    start_daemon -p $PIDFILE -- $DAEMON $DAEMON_OPTS
    log_end_msg $?
}

stop()
{
    log_daemon_msg "Stoppping the $NAME process"
    killproc -p $PIDFILE
    log_end_msg $?
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        if [ -e $PIDFILE ]; then
            status_of_proc -p $PIDFILE $DAEMON "$NAME process"
        else
            log_failure_msg "$NAME process is not running"
            log_end_msg 0
        fi
        ;;
    restart)
        stop
        start
        ;;
    reload|force-reload)
        if [ -e $PIDFILE ]; then
            killproc -p $PIDFILE -SIGHUP
            log_success_msg "$NAME process reloaded successfully"
        else
            log_failure_msg "$NAME process is not running"
            log_end_msg 0
        fi
        ;;
    *)
        echo "Usage:  $0 {start|stop|status|reload|force-reload|restart}"
        exit 2
        ;;
esac
~~~~

Como se puede observar, la mayor parte de las opciones del _script_ necesitan poner
comunicarse con el demonio en ejecución:

**start**
: Necesita poder determinar si el demonio ya ha sido iniciado para no hacerlo
por segunda vez

**status**
: También necesita poder determinar si el demonio ya ha sido iniciado o no.

**stop**
: Necesita poder enviar la señal `SIGTERM` al proceso.

**reload**
: Necesita poder enviar la señal `SIGHUP` al proceso.

Para que todo esto sea posible el demonio suele crear una archivo con extensión
`.pid` en el directorio `/var/run`. En el almacena únicamente su propio
identificador de proceso, del tal forma que las funciones LSB `start_daemon`,
`killproc`, `pidofproc` y `status_of_proc` asumen que:

 1. Si el archivo no existe, el demonio no se está ejecutando.
 2. En otro caso y si contiene uno o más valores numéricos separados por
espacios en la primera línea, estos valores son considerados los PID de los
procesos del demonio.

Las funciones anteriores considerarán que el demonio está en ejecución si
existen procesos con esos PID y enviarán las señales que correspondan.
 
# Opciones de línea de comandos

Los demonios, igual que cualquier otro programa, pueden recibir opciones de
línea de comandos para configurarlos o alterar su comportamiento. Por ejemplo
es muy común que ofrezcan opciones para sobrescribir los parámetros indicados
en el archivo de configuración. También es habitual que un proceso de un programa
diseñado para ejecutarse como un demonio no se convierta en tal si no es
especificada en la línea de comandos una opción del estilo de `-d` o `--daemon`.
Esto es así, por ejemplo, porque es más sencillo depurar el programa y comprobar
su funcionamiento cuando éste no se ejecuta en segundo plano.

En el código del proyecto [rifftree](http://github.com/aplatanado/rifftree),
que ya comentamos en el artículo [Resource Interchange File
Format](|filename|/Overviews/riff.md), se puede observar como se utiliza la
familia de funciones [getopt] para procesar adecuadamente la línea de
comandos de un programa cualquiera.

# Referencias

 1. Wikipedia - [Demonio](http://es.wikipedia.org/wiki/Demonio_(inform%C3%A1tica)).
 1. [Writing a Daemon in C](http://www.danielhall.me/2010/01/writing-a-daemon-in-c/)
 2. [What's the difference between calling daemon() and calling fork(), setsid(), fork(), etc.?](http://stackoverflow.com/questions/7645378/whats-the-difference-between-calling-daemon-and-calling-fork-setsid-for)
 1. Proyecto [LibQxt](http://libqxt.org).
 4. The GNU C Library - [Users and Groups](http://www.gnu.org/software/libc/manual/html_node/Users-and-Groups.html#Users-and-Groups)
 5. Wikipedia - [Runlevel](http://en.wikipedia.org/wiki/Runlevel)
 6. Linux Standard Base Core Specification 3.2 - [System Initialization](http://refspecs.linuxfoundation.org/LSB_3.2.0/LSB-Core-generic/LSB-Core-generic/tocsysinit.html)

[Qt]: |filename|/Overviews/proyecto-qt.md "Proyecto Qt"
[demonio]: http://es.wikipedia.org/wiki/Demonio_(inform%C3%A1tica) "Demonio (informática)"
[Filesystem Hierarchy Standard]: http://es.wikipedia.org/wiki/Filesystem_Hierarchy_Standard "Filesystem Hierarchy Standard"
[Syslog]: http://en.wikipedia.org/wiki/Syslog "Syslog"
[syslog]: http://linux.die.net/man/3/syslog "syslog(3)"
[daemon]: http://linux.die.net/man/3/daemon "daemon(3)"
[exit]: http://linux.die.net/man/3/exit "exit(3)"
[open]: http://linux.die.net/man/2/open "open(2)"
[umask]: http://linux.die.net/man/2/umask "umask(2)"
[QxtLogger]: http://libqxt.bitbucket.org/doc/tip/qxtlogger.html "QxtLogger"
[nivel de ejecución]: http://es.wikipedia.org/wiki/Nivel_de_ejecuci%C3%B3n "Nivel de ejecución"
[LibQxt]: http://libqxt.org "LibQxt"
[setsid]: http://linux.die.net/man/2/setsid "setsid(2)"
[getopt]: http://linux.die.net/man/3/getopt "getopt(3)"

[^1]: El término [demonio] se usa fundamentalmente en sistemas UNIX y basados
en UNIX, como GNU/Linux o Mac OS X. En Windows y otros sistemas operativos se
denominan servicios porque fundamentalmente son programas que ofrecen
servicios al resto del sistema.
[^2]: Tradicionalmente los nombres de los demonios terminan con la letra _d_.
Por ejemplo `syslogd` es el demonio que implementa el registro de eventos del
sistema, mientras que `sshd` es el que sirve a las conexiones SSH entrantes.
[^3]: Se denomina _prompt_ al carácter o conjunto de caracteres que la _shell_
muestra en la línea de comandos para indicar que está a la espera de nuevos
comandos.
[^4]: `init` es el [demonio] antepasado de todos los procesos del sistema. Es
el primer proceso que se inicia durante el arranque del sistema y su función
principal es lanzar el resto de demonios necesarios para el funcionamiento del
sistema. Generalmente también lanza los procesos encargados de solicitar el
inicio de sesión a los usuarios.
[^5]: LSB o Linux System Standard es una iniciativa de la Linux Foundation para
reducir las diferencias entre las distintas distribuciones de Linux, limitando
así los costes derivados de portar las aplicaciones de unas distribuciones a otras.
