Title: Introducción al uso de hilos en Qt
Tags: qt, hilos, mutex, condición de espera, variables de condición, productor-consumidor, buffer finito
Date: 2013-02-16
Status: draft

Debido a la existencia del bucle de mensajes, no se pueden ejecutar tareas de
larga duración en los _slots_. Si lo hiciéramos la ejecución tardaría en
volver al bucle de mensajes, retrasando el momento en el que la aplicación puede
procesar nuevos eventos de los usuarios.

Por eso lo habitual es que desde los _slots_ se deleguen esas tareas a hilos de
trabajo —o _worker thread_— de tal manera que se ejecuten mientras el hilo
principal sigue procesando los eventos que llegen a la aplicación.

## Crear hilos

Para usar hilos en [Qt] se utiliza la clase [QThread], donde cada instancia de
dicha clase representa a un hilo de la aplicación.

Crear un hilo es tan sencillo como heredar la clase [QThread] y reimplementar
el método [run][]() insertando el código que queremos que ejecute el hilo.
En este sentido el método [QThread]::[run][]() es para el hilo lo que la función
`main()` es para la aplicación.

~~~~.cpp
class MyThread : public QThread
{
    Q_OBJECT

    protected:
        void run();
};

void MyThread::run()
{
    // Aquí el código a ejecutar en el hilo...
}
~~~~
    
Una vez instanciada la clase, iniciar el nuevo hilo es tan sencillo como
invocar el método [QThread]::[start][]().

~~~~.cpp
MyThread thread;
thread.start()
~~~~

El hilo terminará cuando la ejecución retorne de su método MyThread::[run][]()
o si desde el código del hilo se invocan los métodos [QThread]::[exit][]() o
[QThread]::[quit][]().

## Problema del buffer finito

Generalmente los hilos no se crean directamente en los _slots_ en los que son
necesarios, sino en la función `main()`, en el constructor de la clase de la
ventana que los va a utilizar o en otros sitios similares. Eso se así por una
cuestión de eficiencia, ya que crear y destruir hilos según cuando son
necesarios tiene cierto coste.

La única cuestión es que entonces un _slot_ debe poder entregar la tarea
al hilo correspondiente que ha sido creado previamente. Como todos los hilos
comparten la memoria del proceso, esto no debe ser un problema, pero realmente
entraña ciertas dificultades relacionadas con la concurrencia.

Para ilustrarlo supongamos que hemos abierto un archivo de vídeo para procesarlo
y que un _slot_ de la clase de la ventana es invocado cada vez que se dispone
de un nuevo _frame_. La función del _slot_ sería la de transferir al hilo
el _frame_ para que se haga cargo de su procesamiento. Teniendo esto en cuenta,
el problema al que nos enfrentamos podría ser descrito de la siguiente manera:

 1. El _slot_ obtiene los _frames_ por lo que sería nuestro _productor_. Como
 se ejecuta desde la bomba de mensajes sabemos que siempre lo hace dentro
 del hilo principal del proceso.

 2. El hilo de trabajo encargado del procesamiento sería nuestro _consumidor_,
 ya que toma los _frames_ entregados por el productor.

 3. Ambos comparten un _buffer_ de _frames_ de tamaño fijo que se usa a modo
 de cola. El _productor_ insertaría los _frames_ en la cola mientras el
 _consumidor_ los extraería.

 4. Para evitar que el _productor_ añada más _frames_ de los que caben en la
 cola y que el _consumidor_ intente extraer más cuando ya no queden,
 ambos comparten un contador con el número de _frames_ almacenados.

Para que todo esto funcione correctamente vamos a necesitar una serie de
elementos de sincronización que ayuden a ambos hilos a coordinarse:

  * Un cerrojo —o _mutex_— de exclusión mutua [QMutex] que serialice la
  ejecución del código en ambos hilos que manipulan la cola y su contador. La
  idea es que mientras uno de los hilos esté manipulando la cola, el otro tenga
  que esperar.

  * Una condición de espera [QWaitCondition] para que el _productor_ pueda
  dormir —o descartar los nuevos _frames_— mientras la cola esté llena. La
  siguiente vez que el consumidor extraiga un _frame_ de la cola, utilizaría la
  condición de espera para notificar al productor que puede volver a insertar
  _frames_.

  * Una condición de espera [QWaitCondition] para que el _consumidor_ pueda
  dormir mientras la cola esté vacía. La siguiente vez que el productor
  inserte un _frame_ en la cola, utilizaría la condición de espera para
  notificar al consumidor que puede volver a extraerlos.

Teniendo todo esto presente, a continuación desarrollamos un posible solución.

### Variables globales

Como ya hemos comentado, ambos hilos deben compartir la cola, el contador y
una serie de elementos de sincronización:

~~~~.cpp
const int BufferSize = 20;       // Tamaño de la cola
QImage buffer[BufferSize];       // Cola de frames como array de C
int numUsedBufferItems = 0;      // Contador de frames en la cola

QWaitCondition bufferNotEmpty;
QWaitCondition bufferNotFull;
QMutex mutex;
~~~~

### El productor

El código del _productor_ en el _slot_ podría tener el siguiente aspecto:

~~~~.cpp
void MyWindow::on_video_updated(const QRect& rect)
{
    static int i = -1;           // Posición último frame insertado

    mutex.lock();                // Bloquear el cerrojo
    // El código del productor a partir de este punto y hasta
    // el unlock() no se ejecutará si el consumidor ha bloqueado el
    // cerrojo primero.

    if (numUsedBufferItems == BufferSize)  // ¿Cola llena?
        bufferNotFull.wait(&mutex);   // Dormir hasta que haya sitio
                                        // en la cola.

    mutex.unlock();              // Liberar el cerrojo

    // Insertar el frame en la cola
    buffer[++i % BufferSize] = movie_->currentImage();

    mutex.lock();                // Bloquear el cerrojo
    // El código del productor a partir de este punto y hasta
    // el unlock() no se ejecutará si el consumidor ha bloqueado el
    // cerrojo primero.

    ++numUsedBufferItems;
    bufferNotEmpty.wakeAll();     // Despertar al consumidor si
                                    // esperaba por más frames.

    mutex.unlock();               // Liberar el cerrojo
}
~~~~

Donde la instancia `mutex` de la clase [QMutex] sirve para evitar que el
_productor_ y el _consumidor_ accedan al contador compartido al mismo tiempo.
Concretamente:

 * El primero en llegar al método [QMutex]::[lock][]() obtiene el cerrojo. Si
un segundo hilo llega a ese método mientras el otro tiene el cerrojo,
simplemente se duerme a la espera de que el cerrojo sea liberado por el primero.

 * Con el método [QMutex]::[unlock][]() se libera el cerrojo. En ese momento
uno de los hilos que espera en [QMutex]::[lock][]() se despierta y obtiene
el cerrojo.

Por otro lado las instancias de condiciones de espera [QWaitCondition] permiten
dormir un hilo hasta que se de una condición determinada. En nuestro ejemplo el
_productor_ utiliza el método [QWaitCondition]::[wait][]() para dormir si la
cola está llena. Antes de hacerlo libera temporalmente el cerrojo `mutex`,
permitiendo que el _consumidor_ se pueda ejecutar en el código que protege.

Como se verá a continuación, el _consumidor_ utiliza el método
[QWaitCondition]::[weakAll][]() después de extraer un elemento con el objeto
de despertar al productor. Obviamente este deberá bloquear el cerrojo `mutex`
antes de volver del método [QWaitCondition]::[wait][]().

### El consumidor

El código del consumidor podría tener el siguiente aspecto, que es muy similar
al del productor:

~~~~.cpp
class FrameProcessingThread : public QThread
{
    Q_OBJECT

    public:

        FrameProcessingThread(QObject *parent = NULL)
            : QThread(parent)
        {}

        void run()
        {
            static int i = -1;     // Posición último frame extraido

            mutex.lock();          // Bloqueamos el cerrojo
            // El código del consumidor a partir de este punto y
            // hasta el unlock() no se ejecutará si el productor ha
            // bloqueado el cerrojo primero.

            if (numUsedBufferItems == 0)     // ¿Cola vacía?...
                bufferNotEmpty.wait(&mutex); // Dormir si es así

            mutex.unlock();        // Liberar el cerrojo

            QImage image = buffer[++i % BufferSize];

            mutex.lock();                    // Bloquear el cerrojo
            // El código del consumidor a partir de este punto y
            // hasta el unlock() no se ejecutará si el productor ha
            // bloqueado el cerrojo primero.

            --numUsedBufferItems;
            bufferNotFull.wakeAll();  // Despertar al productor si
                                        // esperaba por un hueco.

            mutex.unlock();        // Liberar el cerrojo

            // Aquí va el código para procesar el frame...
        }
};
~~~~

### La función principal

Finalmente es en la función principal del programa `main()` donde debe crearse
el hilo encargado del procesamiento de los _frames_. Es decir, nuestro
consumidor.

~~~~.cpp
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    FrameProcessingThread frameProcessingThread;
    frameProcessingThread.start();

    MyWindow w;
    w.show();

    return a.exec();
}
~~~~       

# Referencias

 1. [Starting Threads with QThread](http://qt-project.org/doc/qt-5.0/qtcore/threads-starting.html)
 2. [Wait Conditions Example](http://qt-project.org/doc/qt-4.8/threads-waitconditions.html)
 3. [Producer-consumer problem](http://en.wikipedia.org/wiki/Producer-consumer_problem)

[Qt]: |filename|/Overviews/proyecto-qt.md "Proyecto Qt"
[QThread]: http://qt-project.org/doc/qt-5.0/qtcore/qthread.html "QThread"
[run]: http://qt-project.org/doc/qt-5.0/qtcore/qthread.html#run "QThread::run()"
[start]: http://qt-project.org/doc/qt-5.0/qtcore/qthread.html#start "QThread::start()"
[exit]: http://qt-project.org/doc/qt-5.0/qtcore/qthread.html#exit "QThread::exit()"
[quit]: http://qt-project.org/doc/qt-5.0/qtcore/qthread.html#quit "QThread::quit()"
[QMutex]: http://qt-project.org/doc/qt-5.0/qtcore/qmutex.html "QMutex"
[lock]: http://qt-project.org/doc/qt-5.0/qtcore/qmutex.html#lock "QMutex::lock()"
[unlock]: http://qt-project.org/doc/qt-5.0/qtcore/qmutex.html#unlock "QMutex::unlock()"
[QWaitCondition]: http://qt-project.org/doc/qt-5.0/qtcore/qwaitcondition.html "QWaitCondition"
[wait]: http://qt-project.org/doc/qt-5.0/qtcore/qwaitcondition.html#wait "QWaitCondition::wait()"
[weakAll]: http://qt-project.org/doc/qt-5.0/qtcore/qwaitcondition.html#weakAll "QWaitCondition::weakAll()"