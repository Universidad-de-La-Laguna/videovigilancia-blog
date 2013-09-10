Title: Aplicaciones de consola con Qt
Tags: qt, qcoreapplication, consola, terminal, señales, hilos, signal, sigaction, qsocketnotifier, volatile
Date: 2013-04-11

[Qt] es un _framework_ utilizado fundamentalmente para desarrollar aplicaciones
con interfaz gráfica. Sin embargo nada impide que también sea utilizado para crear
aplicaciones de linea de comandos.

# QCoreApplication

Al crear un proyecto de aplicación para consola, el asistente de Qt Creator
crea un archivo `main.cpp` con un contenido similar al siguiente:

~~~~.cpp
#include <QCoreApplication>

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    return a.exec();
}
~~~~

[QCoreApplication] es una clase que provee un bucle de mensaje para aplicaciones
de consola, mientras que para aplicaciones gráficas lo adecuado es usar [QApplication].
El bucle de mensajes es iniciado con la invocación del método
[QCoreApplication]::[exec][](), que no retorna hasta que la aplicación finaliza.
Por ejemplo cuando el método [QCoreApplication]::[quit][]() es llamado.

Si la aplicación no necesita de un bucle de mensajes, no es necesario instanciar
[QCoreApplication], pudiendo desarrollarla como cualquier programa convencional
en C++, sólo que beneficiándonos de las facilidades ofrecidas por las clases de [Qt].

Las clases de [Qt] que requieren disponer de un bucle de mensajes son:

 * **Controles, ventanas y en general todas las relacionadas con el GUI**.
 * **Temporizadores**.
 * **Comunicación entre hilos mediante señales**.
 * **Red**. Si se usan los métodos síncronos `waitFor*` se puede evitar el uso
del bucle de mensajes, pero hay que tener en cuenta que las clases de comunicaciones
de alto nivel (`QHttp`, `QFtp`, etc.) no ofrecen dicho API.

# Entrada estándar

Muchas aplicaciones de consola interactúan con el usuario a través de la
_entrada estándar_, para lo cual se pueden usar tanto las clases de la librería
estándar de C++:

~~~~.cpp
std::string line;
std::getline(std::cint, line)
~~~~

como los flujos de [Qt]:

~~~~.cpp
QTextStream qtin(stdin);
QString line = qtin.readLine();
~~~~

Sin embargo es necesario tener presente que en ambos casos el hilo principal
se puede bloquear durante la lectura (hasta que hayan datos que leer) lo que
impediría la ejecución del bucle de mensajes.

Para evitarlo se puede delegar la lectura de la _entrada estándar_ a otro hilo,
que se comunicaría con el principal para informar de las acciones del usuario
a través del mecanismo de señales y _slots_ de [Qt]. El procedimiento sería muy
similar al que comentamos en
[una entrada anterior](|filename|/Qt/hilos-usando-senales-y-slots.md), sólo que
para leer la _entrada estándar_ en lugar de para ordenar un vector de enteros.

# Manejo de señales

Los sistemas operativos compatibles POSIX implementan un tipo de interrupción
por software conocido como _señales POSIX_. Estas son enviadas a los procesos
para informar de situaciones excepcionales durante la ejecución del programa, como
por ejemplo:

**SIGSEGV**
: Acceso a una dirección de memoria no válida.

**SIGFPE**
: Intento de ejecutar una operación aritmética inválida, como por ejemplo una
división por cero.

**SIGILL**
: Intento de ejecutar una instrucción ilegal.

**SIGCHLD**
: Notificación de terminación de algún proceso hijo.

**SIGTERM**
: Notificación de que se ha solicitado la terminación del proceso.

**SIGINT**
: Notificación de que el proceso está controlado por una terminal y el usuario
quiere interrumpirlo. Generalmente esta señal es motivada por la pulsación de
la combinación de teclas `Ctrl-C` en la terminal desde la que se controla el
proceso.

Todas éstas sólo son una pequeña muestra de una [lista](http://en.wikipedia.org/wiki/Unix_signal#POSIX_signals)
mucho más larga.

Para cada tipo de señal el proceso puede especificar una [acción] diferente:

**SIG_DFL**
: Ejecutar la acción por defecto, lo que en ocasiones implica terminar el proceso.

**SIG_IGN**
: Ignorar la señal, lo que no es posible para todos los tipos de señales.

**Invocar un manejador de señal**
: Invocar una función concreta del programa que actua como _manejador de la señal_
para realizar las acciones que el programador considere oportunas.

Esto último es interesante porque permite realizar las acciones necesarias para
que el programa termine en condiciones seguras. Por ejemplo: borrar archivos
temporales, asegurar que los datos se escriben en disco y su estructura es
consistente, terminar procesos hijo a los que se les haya delegado parte del
trabajo, etc.

~~~~.cpp
void signalHandler(int signum)
{
    std::cout << "Señal (" << signum << ") recibida." << std::endl;

    // Terminar el programa
    exit(signum);
}
~~~~

## Seguridad respecto a las señales

Sin embargo debemos de tener presente que las _señales POSIX_ pueden llegar en
cualquier momento, interrumpiendo la secuencia normal de instrucciones del
proceso. Por lo tanto los _manejadores de señal_ son invocados de forma asíncrona
respecto a la ejecución del proceso, lo que introduce problemas de concurrencia
debido al posible acceso del manejador a datos que estén siendo manipulados por
el programa.

Por ello:

 * El estándar POSIX establece que desde una manejador de señal sólo se pueden
invocar funciones seguras respecto a la asincronicidad de las señales:
    * Estas funciones son aquellas que o son _reentrantes_[^1] o no interrumpibles[^2]
respecto a las señales.
    * Sólo [unas pocas](http://en.wikipedia.org/wiki/Unix_signal#POSIX_signals)
funciones de la librería del sistema cumplen con dicho requisito.
 * Incluso si se usan variables como banderas para notificar desde el manejador
al programa principal que ha ocurrido una señal, con el objeto de que éste último
ejecute las acciones necesarias, debemos especificar al compilador que no
utilice con esas variables optimizaciones que puedan dar problemas de la
concurrencia.

        // volatile informa al compilador que no optimice el acceso a la
        // variable porque su valor puede cambiar en cualquier momento.
        volatile sig_atomic_t waitingForQuit;

        void signalHandler(int signum)
        {
            // Indicar al programa principal que debe terminar
            waitingForQuit = 1;
        }

        int main()
        {
            ...
            waitingForQuit = 0;
            ...
            // Configurar el manejador de señal
            signal(SIGINT, signalHandler);
            signal(SIGTERM, signalHandler);
            ...
            while (1) {
                ...
                if (waitingForQuit == 1) {
                    // Terminar el proceso en condiciones seguras
                    ...
                    exit(0);
                }
            }
        }


 * En programas multihilo cualquier hilo en el que no se haya bloqueado una
señal puede ser utilizado para atenderla. Eso introduce problemas adicionales
de concurrencia que obligan al uso de [cerrojos, semáforos y otros elementos
de sincronización](|filename|/Qt/hilos-en-qt.md).

Obviamente no hay seguridad de que las funciones del API de [Qt] cumplan con
los requisitos comentados anteriormente, por lo que no podemos invocarlas
directamente desde los _manejadores de señal_.

Además [Qt] no integra ninguna solución que encapsule y simplifique la gestión
de _señales POSIX_, puesto que éstas no están disponibles en sistemas operativos
que no soporten dicha especificación.

## Usando manejadores de señales POSIX con Qt

Aun así en la documentación de [Qt] se describe una forma de usar manejadores de
señales POSIX. Realmente basta con que el _manejador de señal_ haga algo
que provoque que [Qt] emita una señal y después retorne. Al volver a la
secuencia normal de ejecución del programa, se emitiría la señal de [Qt]
invocando el _slot_ al que está conectada, desde donde se ejecutarían de forma
segura las operaciones que fueran necesarias.

Concretamente en el artículo
[Calling Qt Functions From Unix Signal Handlers](http://doc.qt.digia.com/4.7/unix-signals.html)
se propone lo siguiente:

 1. Declarar una clase que contenga los _manejadores de señal_, los _slots_ y
otros elementos que comentaremos a continuación.

        class MyDaemon : public QObject
        {
            Q_OBJECT

            public:
                MyDaemon(QObject *parent = 0);
                ~MyDaemon();

                // Manejadores de señal POSIX
                static void hupSignalHandler(int unused);
                static void termSignalHandler(int unused);

            public slots:
                // Slots Qt donde atender las señales POSIX
                void handleSigHup();
                void handleSigTerm();

            private:
                // Pares de sockets. Un par por señal a manejar
                static int sigHupSd[2];
                static int sigTermSd[2];

                // Objetos para monitorizar los pares de sockets
                QSocketNotifier *sigHupNotifier;
                QSocketNotifier *sigTermNotifier;
        };

 2. En el constructor, para cada señal que se quiere manejar, se usa la llamada
al sistema [socketpair][]() para crear una pareja de
[sockets de dominio UNIX](http://es.wikipedia.org/wiki/Socket_Unix) anónimos
conectados entre sí. Al estar conectados desde el principio, lo que se escribe
en uno de los _sockets_ de la pareja se puede leer en el otro. Además se crea un
objeto [QSocketNotifier] para uno de los sockets de cada pareja, con el objeto de
monitorizar cuando hay datos disponibles para ser leidos, en cuyo caso envía
la señal [QSocketNotifier]::[activated][]().

        MyDaemon::MyDaemon(QObject *parent) : QObject(parent)
        {
            // Crear las parejas de sockets UNIX
            if (::socketpair(AF_UNIX, SOCK_STREAM, 0, sigHupSd))
                qFatal("Couldn't create HUP socketpair");
            if (::socketpair(AF_UNIX, SOCK_STREAM, 0, sigTermSd))
                qFatal("Couldn't create TERM socketpair");

            // Crear los objetos para monitorizar uno de los socket
            // de cada pareja.
            sigHupNotifier = new QSocketNotifier(sigHupFd[1],
                QSocketNotifier::Read, this);
            sigTermNotifier = new QSocketNotifier(sigTermSd[1],
                QSocketNotifier::Read, this);

            // Conectar la señal activated() de cada objeto
            // QSocketNotifier con el slot correspondiente. Esta señal
            // será emitida cuando hayan datos para ser leidos en el
            // socket monitorizado.
            connect(sigHupNotifier, SIGNAL(activated(int)), this,
                SLOT(handleSigHup()));
            connect(sigTermNotifier, SIGNAL(activated(int)), this,
                SLOT(handleSigTerm()));

            ...
        }

 3. Entonces los manejadores de señal lo único que tienen que hacer cuando son
invocados es escribir _algo_ en el _socket_ correspondiente. Nótese que los
métodos de los manejadores se declaran como `static` para que puedan ser pasados
como un puntero de función de C a la llamada al sistema [sigaction][](), cuando
va a ser establecido el manejador de cada señal concreta:

        //
        // Manejador de la señal SIGHUP
        //
        void MyDaemon::hupSignalHandler(int)
        {
            char a = 1;
            ::write(sigHupSd[0], &a, sizeof(a));
        }

        //
        // Manejador de la señal SIGTERM
        //
        void MyDaemon::termSignalHandler(int)
        {

            char a = 1;
            ::write(sigTermSd[0], &a, sizeof(a));
        }

        //
        // Configurar los manejadores de señal
        //
        int setupUnixSignalHandlers()
        {
            struct ::sigaction hup, term;

            hup.sa_handler = &MyDaemon::hupSignalHandler;
            ::sigemptyset(&hup.sa_mask);
            hup.sa_flags = SA_RESTART;

            // Establecer manejador de la señal SIGHUP
            if (::sigaction(SIGHUP, &hup, 0) > 0)
            return 1;

            term.sa_handler = &MyDaemon::termSignalHandler;
            ::sigemptyset(&term.sa_mask);
            term.sa_flags = SA_RESTART;

            // Establecer manejador de la señal SIGTERM
            if (::sigaction(SIGTERM, &term, 0) > 0)
            return 2;

            return 0;
        }

 4. Finalmente en los _slots_ a los que conectamos la señal [QSocketNotifier]::[activated][]()
se lee _lo escrito_ desde el _manejador de señal_, para después hacer todo
aquello que no se puede hacer desde dicho manejador de señal POSIX.

        void MyDaemon::handleSigHup()
        {
            hupNotifier->setEnabled(false);
            char tmp;
            ::read(sigHupSd[1], &tmp, sizeof(tmp));

            // ...tu código aquí...

            hupNotifier->setEnabled(true);
        }

        void MyDaemon::handleSigTerm()
        {
            termNotifier->setEnabled(false);
            char tmp;
            ::read(sigTermSd[1], &tmp, sizeof(tmp));

            // ...tu código aquí...

            termNotifier->setEnabled(true);
        }

# Referencias

 1. [QCoreApplication].
 4. [QSocketNotifier].
 3. [Calling Qt Functions From Unix Signal Handlers](http://doc.qt.digia.com/4.7/unix-signals.html)
 2. Wikipedia - [Unix signal](http://en.wikipedia.org/wiki/Unix_signal)

[^1]: Una función es reentrante si puede ser interrumpida en medio de su ejecución
y vuelta a llamar con total seguridad. En general una función es reentrante si
no modifica variables estáticas o globales, no modifica su propio código y no
llama a otras funciones que no sean reentrantes.
[^2]: Una función puede ser no interrumpible respecto a las señales si al entrar
en la función el programa las bloquea, desbloqueándolas antes de salir.

[Qt]: |filename|/Overviews/proyecto-qt.md "Proyecto Qt"
[QCoreApplication]: http://qt-project.org/doc/qt-5.0/qtcore/qcoreapplication.html "QCoreApplication"
[QSocketNotifier]: http://qt-project.org/doc/qt-5.0/qtcore/qsocketnotifier.html "QSocketNotifier"
[QApplication]: http://qt-project.org/doc/qt-5.0/qtcore/qapplication.html "QApplication"
[exec]: http://qt-project.org/doc/qt-5.0/qtcore/qcoreapplication.html#exec "QApplication::exec"
[quit]: http://qt-project.org/doc/qt-5.0/qtcore/qcoreapplication.html#quit "QApplication::quit"
[señales]: http://en.wikipedia.org/wiki/Unix_signal "UNIX signal"
[acción]: http://pubs.opengroup.org/onlinepubs/000095399/functions/xsh_chap02_04.html#tag_02_04_03 "Signal Actions"
[socketpair]: http://linux.die.net/man/2/socketpair "socketpair(2)"
[sigaction]: http://linux.die.net/man/2/sigaction "sigaction(2)"
[activated]: http://qt-project.org/doc/qt-5.0/qtcore/qsocketnotifier.html#activated "QSocketNotifier::activated()"
