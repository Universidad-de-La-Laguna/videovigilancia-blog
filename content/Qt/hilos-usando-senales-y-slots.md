Title: Hilos de trabajo usando señales y slots
Tags: qt, hilos, señales, slots
Date: 2013-02-18

[Qt] proporciona clases para hilos y mecanismos de sincronización que facilitan
sacar las tareas de larga duración del hilo principal de la aplicación, lo que
de lo contrario bloquearía la interfaz de usuario.

Una forma práctica de hacerlo la hemos visto [anteriormente](|filename|/Qt/hilos-en-qt.md)
utilizando un _buffer_ compartido. Sin embargo [Qt] provee a cada hilo de una
cola de mensajes, lo que permite enviar señales a _slots_ en otros hilos. Esto
nos proporciona una forma sencilla de pasar datos entre los hilos de la
aplicación.

Si no se indica lo contrario, las señales emitidas desde un hilo a un objeto
en el mismo hilo son entregadas directamente. Es decir, que al emitir la señal
se invoca el _slot_ como si de un método convencional se tratara. Sin embargo
si el emisor y el receptor residen en hilos diferentes, la señal es insertada
en la cola de mensajes del hilo del objeto de destino. Así el _slot_
correspondiente será invocado en el hilo receptor desde su bucle de mensajes.

En la actualidad esta es la forma recomendada de usar hilos en [Qt] ya que
permite evitar el uso de de mecanismos de sincronización como [QMutex],
[QWaitCondition], etc.

## El ejemplo. Ordenar números enteros

El ejemplo que vamos a seguir básicamente consiste en ordenar
un vector de enteros en un hilo de trabajo distinto al hilo principal.

Como se puede observar en la figura utilizaremos dos objetos, uno vinculado
al hilo principal (clase `Sorter`) y otro al hilo de trabajo
(clase `SorterWorker`). En una aplicación gráfica convencional con [Qt] la
clase `Sorter` podría ser una ventana o cualquier otro control que
quiera ceder una tarea al hilo de trabajo. Aquí no lo haremos así para
que el ejemplo sea lo más sencillo posible.

<img src="https://docs.google.com/drawings/d/1tZ0CMTNJoLsbHx3TjgecQuRXGEM5hf3pYwm9_s1R8bI/pub?w=960&amp;h=720" alt="Ejemplo de comunicación entre hilos en Qt" class="centered">

En [Qt] un objeto se dice que vive en el hilo en el que es creado. Esto se
puede cambiar utilizando el método [moveToThread][]() que tienen todas las
clases de [Qt][^1].

## La clase Sorter

~~~~.cpp
class Sorter : public QObject
{
    Q_OBJECT

    public:
        Sorter();
        ~Sorter();

        // Ordenar asíncronamente un vector en el hilo de trabajo
        void sortAsync(const QVector<int>& list);

    signals:
        // Señal para comunicarnos con el hilo de trabajo
        void sortingRequested(const QVector<int> &list);

    private slots:
        // Slot para saber cuando el vector ha sido ordenado
        void vectorSorted(const QVector<int> &list);

    private:
        // Clase del hilo de trabajo
        QThread workingThread_;
        // Clase que hace el ordenamiento
        SorterWorker sorterWorker_;
};
~~~~

La propia clase `Sorter` se hará cargo de crear el hilo de trabajo, que por
defecto lo único que hace es iterar en su propio bucle de mensajes. Todos
los detalles acerca de la creación de hilos ya los vimos
[anteriormente](|filename|/Qt/hilos-en-qt.md)

La clase `Sorter` provee un método `sortAsync()` que podrá ser llamado por
los clientes para ordenar un vector de números enteros. Puesto que la operación
es asíncrona, necesitamos definir un _slot_ `vectorSorted()` para ser
notificados cuando el ordenamiento haya finalizado con éxito.

La implementación de esta clase sería la siguiente:

~~~~.cpp
Sorter::Sorter() : QObject()
{
    qDebug() << Q_FUNC_INFO << QThread::currentThreadId();

    // Registrar los parámetros de la señales. Necesitamos registrar
    // QList<int> porque no es un tipo conocido por el sistema de
    // meta-objetos de Qt.
    qRegisterMetaType< QVector<int> >("QVector<int>");

    // Pasar la petición de ordenar a la instancia de SorterWorker
    connect(this, SIGNAL(sortingRequested(QVector<int>)),
        &sorterWorker_, SLOT(doSort(QVector<int>)));
    // Ser notificado cuando el vector haya sido ordenado
    connect(&sorterWorker_, SIGNAL(vectorSorted(QVector<int>)),
        this, SLOT(vectorSorted(QVector<int>)));

    // Migrar la instancia de SorterWorker al hilo de trabajo
    sorterWorker_.moveToThread(&workingThread_);

    // Iniciar el hilo de trabajo
    workingThread_.start();
}

Sorter::~Sorter()
{
    // Le decimos al bucle de mensajes del hilo que se detenga
    workingThread_.quit();
    // Ahora esperamos a que el hilo de trabajo termine
    workingThread_.wait();
}

void Sorter::sortAsync(const QVector<int>& list)
{
    qDebug() << Q_FUNC_INFO << QThread::currentThreadId();

    emit sortingRequested(list);
}

void Sorter::vectorSorted(const QVector<int>& list)
{
    qDebug() << list;
}
~~~~

Como se puede observar, en el constructor de `Sorter` se usa el método
`qRegisterMetaType()`, antes de conectar las señales, para registrar el tipo
`QVector<int>`. Esto debe hacerse porque cuando una señal es encolada sus
parámetros deben ser de tipos conocidos para [Qt], de forma que pueda
almacenar los argumentos en la cola.

Por otro lado en el destructor de `Sorter` tenemos cuidado de detener
el hilo de trabajo en condiciones seguras cuando ya no va a ser necesario.
Si no lo hacemos así, el hilo podría ser destruido por el sistema operativo
en cualquier punto de la secuencia de instrucciones al termina la aplicación,
lo que podría dejar los datos en uso en un estado indeterminado.

## La clase SorterWorker

~~~~.cpp
class SorterWorker : public QObject
{
    Q_OBJECT

    signals:
        // Señal emitida cuando el vector ha sido ordenado
        void vectorSorted(const QVector<int> &list);

    public slots:
        // Método encargado del ordenamiento
        void doSort(const QVector<int> &list) {
            qDebug() << Q_FUNC_INFO << QThread::currentThreadId();

            QVector<int> list_sorted = list;
            qSort(list_sorted);
            emit vectorSorted(list_sorted);
        }
};
~~~~

## Como usar el ejemplo

Para usar el ejemplo sólo necesitamos crear una instancia de `Sorter` y
llamar a su método `sortAsync()` para pedir que ordene el vector especificado.

~~~~.cpp
int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    Sorter sorter;
    sorter.sortAsync(QVector<int>() << 1 << 3 << 2);

    return a.exec();
}
~~~~

## Referencias

 1. [Introducción al uso de hilos en Qt](|filename|/Qt/hilos-en-qt.md)
 3. [Worker Thread in Qt using Signals & Slots](http://cdumez.blogspot.com.es/2011/03/worker-thread-in-qt-using-signals-slots.html)


[Qt]: |filename|/Overviews/proyecto-qt.md "Proyecto Qt"
[QThread]: http://qt-project.org/doc/qt-5.0/qtcore/qthread.html "QThread"
[QMutex]: http://qt-project.org/doc/qt-5.0/qtcore/qmutex.html "QMutex"
[QWaitCondition]: http://qt-project.org/doc/qt-5.0/qtcore/qwaitcondition.html "QWaitCondition"
[moveToThread]: http://qt-project.org/doc/qt-5.0/qtcore/qobject.html#moveToThread "QObject::moveToThread()"
[QObject]: http://qt-project.org/doc/qt-5.0/qtcore/qobject.html "QObject"
[run]: http://qt-project.org/doc/qt-5.0/qtcore/qthread.html#run "QThread::run()"

[^1]: Todas las clases de [Qt] tienen como clase base [QObject] donde se
implementan algunos métodos comunes como [QObject]::[moveToThread][]()
