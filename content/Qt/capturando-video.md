Title: Capturando secuencias de vídeo con Qt
Tags: qt, multimedia, qcamera
Date: 2014-02-11

[Qt] incluye el módulo [Qt Multimedia] para facilitar la manipulación de
contenidos multimedia. Entre otras cosas permite reproducir audio y vídeo y
capturar desde dispositivos de adquisición soportados por el sistema operativo.

Como por defecto no viene activado, es necesaro abrir el archivo `.pro` del
proyecto y añadir la línea

    QT       += multimedia multimediawidgets

## Primeros pasos con la webcam

Capturar de una webcam es tan sencillo como crear un objeto [QCamera] e iniciar
la captura mediante el método [QCamera]::[start][]():

~~~~.cpp
camera = new QCamera;
camera->start();
~~~~

Por lo general suele ser interesante incorporar un visor en el que mostrar
al usuario lo que la cámara está capturando. Para simplifcar esta tarea, [Qt]
nos ofrece el control [QCameraViewfinder] que hereda del más generico [QVideoWidget]:

~~~~.cpp
camera = new QCamera;
viewfinder = new QCameraViewfinder;
camera->setViewfinder(viewfinder);
~~~~

Como [QCameraViewfinder] —al igual que otros controles de [Qt Multimedia]— no
está disponible en Qt Designer, tendremos que colocarlo en nuestra ventana
desde el propio código. Por ejemplo como el control central de la misma:

~~~~.cpp
viewfinder->setSizePolicy(QSizePolicy::Maximum, QSizePolicy::Maximum);
setCentralWidget(viewfinder);
~~~~

<img src="http://qt-project.org/doc/qt-5/images/mainwindowlayout.png" alt="Organización de controles en la ventana principal" class="centered">

Hecho esto, finalmente, podemos iniciar la cámara:

~~~~.cpp
// camera->setCaptureMode(QCamera::CaptureVideo);
camera->setCaptureMode(QCamera::CaptureViewfinder);
camera->start();
~~~~

## Acceder a un dispositivo específico

En un mismo sistema pueden haber varios dispositivos de captura, de tal forma
que puede ser necesario crear un objeto [QCamera] para un dispositivo
concreto. En ese caso simplemente tenemos que indicarlo en el constructor:

~~~~.cpp
camera = new QCamera("/dev/video0");
~~~~

Obviamente para hacerlo necesitamos conocer la lista de los dispositivos
disponibles en el sistema. Esto se puede hacer a través del método
[QCamera]::[availableDevices][](). Al igual que se puede obtener para cada uno
de ellos un texto más descriptivo, principalmente de cara a los usuarios, usando [QCamera]::[deviceDescription][]()

~~~~.cpp
QList<QByteArray> devices = QCamera::availableDevices();
qDebug() << "Capturando de... " << QCamera::deviceDescription(devices[0]);
camera = new QCamera(devices[0]);
~~~~

## Accediendo a los frames individualmente

En el módulo [Qt Multimedia] cada objeto de la clase [QVideoFrame] representa un
_frame_ de vídeo.

### La clase QVideoFrame

El motivo por el que no se usa para esto la clase [QImage] es
porque [QVideoFrame] no siempre contiene los datos de los píxeles del _frame_,
como sí ocurre con la clase [QImage].

Cada sistema operativo tiene su propio API multimedia que tiene una manera
particular de gestionar los _buffers_ de memoria —por ejemplo, como una textura
en OpenGL, como un _buffer_ de memoria compartida en XVideo, como una CImage en
MacOS X, etc—. Estos _buffers_ suelen ser internos al API, así que las
aplicaciones los identifican a través de manejadores o _handlers_. Copiar los
datos de los píxeles desde los _buffers_ internos a la memoria del programa
suele tener cierto coste, por lo que [QVideoFrame] evita hacerlo, a menos que el
programador lo solicite. Esto tiene una serie de implicaciones para nuestros fines:

 * Por lo general [QVideoFrame] no contiene los datos de los píxeles sino un
manejador al _buffer_ interno del API donde están almacenados. Dicho manejador
se puede obtener a través del método [QVideoFrame]::[handle][]().
 * Para conocer el tipo de manejador —algo que depende del API nativo que esté
usando el módulo [Qt Multimedia]— se puede usar el método
[QVideoFrame]::[handleType][]().
 * Para acceder al contenido de los píxeles se puede usar el método
[QVideoFrame]::[bits][]() pero primero hay que asegurarse de que dichos datos son
copiados desde el _buffer_ interno a la memoria del programa. Eso se hace
invocando previamente el método [QVideoFrame]::[map][](). Cuando el acceso a
estos datos ya no es necesario se debe usar el método [QVideoFrame]::[unmap][]()
para liberar la memoria.
 * El contenido de los objetos [QVideoFrame] se comparte explícitamente, por lo
que cualquier cambio en un _frame_ será visible en todas las copias.

### Ganar acceso a los frames

Si estamos interesados en procesar los _frames_ capturados, la forma más sencilla
—aunque no la única— es crear nuestro propio visor para la cámara. El método
[QCamera]::[setViewfinder][]() admite un puntero a objetos de la clase [QAbstractVideoSurface], que define la interfaz genérica para las superficies
que saben como mostrar vídeo. Por lo que será esa la clase de la que heredaremos
la nuestra:

~~~~.cpp
class CaptureBuffer : public QAbstractVideoSurface
{
    Q_OBJECT

public:
    QList<QVideoFrame::PixelFormat> supportedPixelFormats(
            QAbstractVideoBuffer::HandleType handleType =
            QAbstractVideoBuffer::NoHandle) const
    {
        // A través de este método nos preguntan que formatos de vídeo
        // soportamos. Como vamos a guardar los frames en objetos QImage
        // nos sirve cualquiera de los formatos sorportados por dicha clase:
        // http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html#PixelFormat-enum
        QList<QVideoFrame::PixelFormat> formats;
        formats << QVideoFrame::Format_ARGB32;
        formats << QVideoFrame::Format_ARGB32_Premultiplied;
        formats << QVideoFrame::Format_RGB32;
        formats << QVideoFrame::Format_RGB24;
        formats << QVideoFrame::Format_RGB565;
        formats << QVideoFrame::Format_RGB555;
        return formats;
    }

    bool present(const QVideoFrame &frame)
    {
        // A través de este método nos darán el frame para que lo mostremos.
        return true;
    }
};
~~~~

De tal forma que sólo tenemos que instanciarla y configurarla como visor de
nuestra cámara.

~~~~.cpp
CaptureBuffer *captureBuffer = new CaptureBuffer;
camera->setViewfinder(captureBuffer);
~~~~

### Convertir objetos QVideoFrame en QImage

A través del método `present()` de nuestra clase `CaptureBuffer` obtenemos
los _frames_ capturados. Sin embargo estos son de poca utilidad si no podemos
acceder al contenido de los píxeles. Así que vamos a convertir el objeto
[QVideoFrame] en un objeto [QImage].

Como ya sabemos, [QImage] tiene diversos constructores. Entre ellos el siguiente:

~~~~.cpp
QImage (const uchar *data, int width, int height, int bytesPerLine,
        QImage::Format format)
~~~~

que permite crear un objeto [QImage] si tenemos:

 * El ancho —width— y el alto —height— del frame. Esto lo podemos obtener a
través de los métodos [QVideoFrame]::[width][]() y [QVideoFrame]::[width][]().
 * El número de bytes por línea —bytesPerLine—. Para lo que tenemos el método [QVideoFrame]::[bytesPerLine][]().
 * El formato de los píxeles —format—. En este caso el método
[QVideoFrame]::[pixelFormat][]() proporciona dicho formato para el _frame_ y
podemos convertirlo en uno equivalente de [QImage] usando [QVideoFrame]::[imageFormatFromPixelFormat][]().
  * Un puntero al _buffer_ en memoria que contiene los datos de los píxeles.
Como comentamos anteriormente, [QVideoFrame]::[bits][]() nos proporciona esa
información pero primero tenemos que invocar al método [QVideoFrame]::[map][]()
para que dichos datos sean copiados desde el _buffer_ interno a la memoria
del programa.

~~~~.cpp
frame.map(QAbstractVideoBuffer::ReadOnly);
QImage frameAsImage = QImage(frame.bits(), frame.width(),
    frame.height(), frame.bytesPerLine(),
    QVideoFrame::imageFormatFromPixelFormat(frame.pixelFormat()));
//
// Aquí hacemos lo que queramos hacer con la imagen
//
// ...
//
frame.unmap();
~~~~

Hay que tener en cuenta que cuando se crea un objeto [QImage] de esta manera,
no se hace una copia del contenido de los píxeles, por lo que es importante
asegurarse de que el puntero devuelto por [QVideoFrame]::[bits][]() es válido
mientras se esté haciendo uso del objeto. Por eso se invoca al método
[QVideoFrame]::[unmap][]() después de manipularlo y no antes.

Si se quiere conservar la imagen del objeto [QImage] después de invocar a
[QVideoFrame]::[unmap][]() es necesario hacer una copia usando, por ejemplo, [QImage]::[copy][]().

## Referencias

 1. [Qt Multimedia]
 2. [QCamera] Class Reference.
 3. [QVideoFrame] Class Reference.
 4. [Video Overview](http://qt-project.org/doc/qt-5.0/qtmultimedia/videooverview.html)

[Qt]: |filename|/Overviews/proyecto-qt.md "Proyecto Qt"
[Qt Multimedia]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qtmultimedia-index.html "Qt Multimedia"
[QCamera]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qcamera.html "QCamera"
[start]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qcamera.html#start "QCamera::start()"
[QVideoWidget]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideowidget.html "QVideoWidget"
[QCameraViewfinder]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qcameraviewfinder.html "QCameraViewfinder"
[setViewfinder]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qcamera.html#setViewfinder "QCamera::setViewfinder()"
[QAbstractVideoSurface]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qabstractvideosurface.html "QAbstractVideoSurface"
[availableDevices]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qcamera.html#availableDevices "QCamera::availableDevices()"
[deviceDescription]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qcamera.html#deviceDescription "QCamera::deviceDescription()"
[QVideoFrame]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html "QVideoFrame"
[QImage]: http://qt-project.org/doc/qt-5/qimage.html "QImage"
[handle]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html#handle "QVideoFrame::handle()"
[handleType]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html#handletype "QVideoFrame::handleType()"
[bits]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html#bits "QVideoFrame::bits()"
[map]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html#map "QVideoFrame::map()"
[unmap]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html#unmap "QVideoFrame::unmap()"
[width]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html#width "QVideoFrame::width()"
[height]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html#height "QVideoFrame::height()"
[bytesPerLine]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html#bytesperline "QVideoFrame::bytesPerLine()"
[pixelFormat]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html#pixelformat "QVideoFrame::pixelFormat()"
[imageFormatFromPixelFormat]: http://qt-project.org/doc/qt-5.0/qtmultimedia/qvideoframe.html#imageformatfrompixelformat "QVideoFrame::imageFormatFromPixelFormat()"
[format]: http://qt-project.org/doc/qt-5/qimage.html#format "QImage::format()"
[copy]: http://qt-project.org/doc/qt-5/qimage.html#copy "QImage::copy()"