Title: Como usar QMovie en Qt
Tags: qt, gui, qmovie
Date: 2013-02-13

[Qt] trae una clase denominada [QMovie] que facilita mostrar pequeñas
animaciones sin mucho esfuerzo.

[QMovie] está diseñada para ser independiente del formato de archivo pero como
internamente depende de [QImageReader], sólo puede utilizarse con los que esta
última soporta (véase [QMovie]::[supportedFormats][]()). Esto incluye GIF
animados, archivos MNG y MJPEG. Para mostrar vídeo y otros contenidos
multimedia, es mejor utilizar el _framework_ [Qt Multimedia].

## Primeros pasos

La forma más sencilla de usar [QMovie] es asignar un objeto [QMovie] a un
control [QLabel] usando el método [QLabel]::[setMovie][]():

    QMovie *movie = new QMovie("video.mjpeg");
    ui->label->setMovie(movie);

donde `ui` es el miembro de la clase que tiene asignada la instancia de la
ventana creada previamente con Qt Creator.
    
## Nombre de archivo especificado por el usuario

No siempre ocurre que el nombre del archivo a reproducir se conozca de antemano
al desarrollar el programar. Si por ejemplo se pretende que el usuario lo
escoja de entre los disponibles en su disco duro podemos:

 1. Crear un objeto [QMovie], guardarlo en un miembro de la clase (manteniendo
 así un puntero al mismo que nos permita referenciarlo más adelante[^1]) y asignar
 dicho objeto [QMovie] a [QLabel]:

        MovieViewerWindow::MovieViewerWindow(QWidget *parent)
            : QMainWindow(parent),
              ui(new Ui::MovieViewerWindow)
        {
            // Aquí otro código de inicialización de la instancia...

            movie_ = new QMovie();
            ui->label->setMovie(movie_);
        }

 2. En el slot de la acción que abre el cuadro de diálogo _abrir archivo_,
 asignar al objeto [QMovie] el nombre escogido por el usuario mediante el
 método [QMovie]::[setFileName][]():

        void MovieViewerWindow::on_actionOpen_triggered()
        {
            // Aquí el código que abre el cuadro de diálogo y comprueba si
            // el usuario seleccionó algún archivo...
            //
            // QString fileName = QFileDialog::getFileName(...);
            //
            // ...
            //

            movie_->setFileName(fileName);
            if (!movie_->isValid()) {
                QMessageBox::critical(this, tr("Error"),
                    tr("No se pudo abrir el archivo o el formato es inválido"));
                return;
            }
            movie_->start();    // Iniciar la reproducción de la animación
        }

    Como se puede observar es conveniente utilizar el método [QMovie]::[isValid][]()
para comprobar si el archivo pudo ser abierto y tiene uno de los formatos soportados.

    Para distinguir entre ambos tipos de error, con el objeto de mostrar al usuario
un mensaje diferente según el caso, podemos emplear el método [QMovie]::[device][]().
Este devuelve el objeto [QFile] (realmente una instancia de [QIODevice][^2] que es la clase
base de [QFile] y de todas clases que representan dispositivos de E/S) vinculado con
la instancia de [QMovie]. Así podemos comprobar mediante el método
[QIODevice]::[isOpen][]() si el archivo se pudo abrir con éxito o no.

## Control de la reproducción

El control de la reproducción se puede hacer mediante los _slots_
[QMovie]::[start][]() y [QMovie]::[stop][]().

En el ejemplo anterior se puede observar como el _slot_ [QMovie]::[start][]()
es invocado exactamente de la misma manera que un método convencional para
iniciar la reproducción de la animación. Sin embargo el hecho de que los
desarrolladores de [Qt] lo hayan declarado como un _slot_ y no como un
método nos permitiría conectarlo a una señal emitida desde otro control.

Por ejemplo, si tuvieramos un botón de _play_ podríamos conectar su señal
[clicked][]() al slot [QMovie]::[start][]() de la siguiente manera:

    connect(ui->playButton, SIGNAL(clicked()), movie_, SLOT(start()));

de forma que al pulsar dicho botón se inicie automáticamente la reproducción.

Otro detalle a tener en cuenta es que los _slots_ [QMovie]::[start][]()
y [QMovie]::[stop][]() indican a la instancia de [QMovie] que inicie o detengan
la reproducción pero, una vez hecho, vuelven inmediatamente. Es decir, que no
se quedan a la espera de que la animación se reproduzca o esperan a que termine.

Este es un detalle importante porque al _slot_ `on_actionOpen_triggered()` de
nuestro ejemplo se llega a través del bucle de mensajes, cuando el sistema de
ventanas notifica a la aplicación un _click_ sobre la acción correspondiente. Si
en el _slot_ introduciésemos tareas de larga duración, la ejecución tardaría en
volver al bucle de mensajes, retrasando el momento en el que la aplicación puede
procesar nuevos eventos de los usuarios. Es decir, que si
[QMovie]::[start][]() se quedara a la espera y añadiéramos un botón para detener
la reproducción, este nunca funcionaría porque la aplicación no volvería al bucle
de mensajes hasta que la reproducción no hubiera terminado.

Podemos comprobar esto añadiendo una espera justo después de invocar el
_slot_ [start][]():

    QWaitCondition sleep;
    QMutex mutex;
    sleep.wait(&mutex, 2000);    // Espera de 2 segundos

Debido a los efectos desastrosos que este tipo de esperas tienen en las aplicaciones
dirigidas por eventos, [Qt] no incluye funciones del tipo de `sleep()`, `delay()`,
`usleep()` y `nanosleep()`, que muchos sistemas operativos sí soportan.
                     
## Procesando la imagen frame a frame

Aunque [QMovie] se hace cargo de mostrar la animación sin que tengamos que intervenir
de ninguna otra manera, en ocasiones puede ser interesante tener acceso a los
_frames_ de manera individualizada para poder procesarlos antes de que sean mostrados.
Por ese motivo [QMovie] emite una señal [updated][]() cada vez que el _frame_
actual cambia.

Para aprovechar eso:

 1. Declaramos un _slot_ para que reciba la señal [QMovie]::[updated][]():

        private slots:
            // Otros slots...
            //
            // void on_actionOpen_triggered();
            //
            // ...
            //
            void on_movie_updated(const QRect& rect);

 2. Definimos el código del _slot_ para que al ser invocado actualice la
imagen mostrada por el control [QLabel]. En ese sentido el método
[QLabel]::[setPixmap][]() permite indicar al objeto [QLabel] que imagen queremos
mostrar. Mientras que [QMovie]::[currentPixmap][]() nos permite obtener el último
_frame_ del objeto [QMovie] en formato [QPixmap]:

        void MovieViewerWindow::on_movie_updated(const QRect& rect)
        {
            QPixmap pixmap = movie_->currentPixmap();
            ui->label->setPixmap(pixmap);
        }

 3. Suprimimos el uso del método [QLabel]::[setMovie][](), para que el
objeto [QLabel] no sepa nada de nuestra animación, y conectamos la señal
[QMovie]::[updated][]() con nuestro nuevo slot:

            movie_ = new QMovie();
            // ui->label->setMovie(movie_);
            connect(movie_, SIGNAL(updated(const QRect&)),
                    this, SLOT(on_movie_updated(const QRect&)));
        }

Ahora podríamos introducir en el _slot_ todo aquello que nos interese hacer
sobre los _frames_ antes de mostrarlos.

## Referencias

 1. [QMovie] Class Reference.
 2. [Moviel Example](http://qt-project.org/doc/qt-5.0/qtwidgets/widgets-movie.html)
 3. [Image Viewer Example](http://qt-project.org/doc/qt-5.0/qtwidgets/widgets-imageviewer.html)

[Qt]: |filename|/Overviews/proyecto-qt.md "Proyecto Qt"
[QMovie]: http://qt-project.org/doc/qt-5.0/qtgui/qmovie.html "QMovie"
[QImageReader]: http://qt-project.org/doc/qt-5.0/qtgui/qimagereader.html "QImageReader"
[supportedFormats]: http://qt-project.org/doc/qt-5.0/qtgui/qmovie.html#supportedFormats "QMovie::supportedFormats()"
[Qt Multimedia]: http://qt-project.org/doc/qt-5.0/qtmultimedia/multimediaoverview.html "Qt Multimedia"
[QLabel]: http://qt-project.org/doc/qt-5.0/qtwidgets/qlabel.html "QLabel"
[setMovie]: http://qt-project.org/doc/qt-5.0/qtwidgets/qlabel.html#setMovie "QLabel::setMovie()"
[setPixmap]: http://qt-project.org/doc/qt-5.0/qtwidgets/qlabel.html#setPixmap "QLabel::setPixmap()"
[setFileName]: http://qt-project.org/doc/qt-5.0/qtgui/qmovie.html#setFileName "QMovie::setFileName()"
[isValid]: http://qt-project.org/doc/qt-5.0/qtgui/qmovie.html#isValid "QMovie::isValid()"
[QFile]: http://qt-project.org/doc/qt-5.0/qtcore/qfile.html "QFile"
[open]: http://qt-project.org/doc/qt-5.0/qtcore/qfile.html#open "QFile::open()"
[isOpen]: http://qt-project.org/doc/qt-5.0/qtcore/qfile.html#isOpen "QFile::isOpen()"
[device]: http://qt-project.org/doc/qt-5.0/qtgui/qmovie.html#device "QMovie::device()"
[QIODevice]: http://qt-project.org/doc/qt-5.0/qtcore/qiodevice.html "QIODevice"
[QProcess]: http://qt-project.org/doc/qt-5.0/qtcore/qprocess.html "QProcess"
[start]: http://qt-project.org/doc/qt-5.0/qtgui/qmovie.html#start "QMovie::start()"
[stop]: http://qt-project.org/doc/qt-5.0/qtgui/qmovie.html#stop "QMovie::stop()"
[clicked]: http://qt-project.org/doc/qt-5.0/qtwidgets/qabstractbutton.html#clicked "QAbstractButton::clicked"
[updated]: http://qt-project.org/doc/qt-5.0/qtgui/qmovie.html#updated "QMovie::updated()"
[currentPixmap]: http://qt-project.org/doc/qt-5.0/qtgui/qmovie.html#currentPixmap "QMovie::currentPixmap()"
[QPixmap]: http://qt-project.org/doc/qt-5.0/qtgui/qpixmap.html "QPixmap"

[^1]: Sin olvidarnos de que es necesario para liberar la memoria en el destructor de la clase `MovieViewerWindow`.
[^2]: Esta clase es la base de todos los dispositivos de E/S, incluidos los archivos. Su
misión es proporcionar una interfaz común; mediante métodos como [open][](),
`close()`, `read()`, `write()`, `seek()`, etc.; con la que acceder a cualquier
dispositivo. De [QIODevice] heredan clases como `QBuffer`, [QProcess] o [QFile] que
proporcionan implementaciones concretas para cada tipo de dispositivo en particular.