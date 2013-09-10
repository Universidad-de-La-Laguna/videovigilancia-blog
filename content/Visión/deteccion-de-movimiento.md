Title: Detección de movimiento
Tags: visión, imágenes, opencv, qt, qimage
Date: 2013-02-19

Detectar movimiento en una secuencia de vídeo es una tarea relativamente simple
que puede abordarse en unos pocos pasos:

 1. **Supresión del fondo**. Consiste en estimar un modelo del fondo y compararlo
con el _frame_ actual para detectar cambios. El resultado es una imagen binaria
donde los píxeles se clasifican entre si forman parte del fondo o son del
primer plano.

 2. **Operaciones morfológicas**. En la imagen resultado de la operación anterior
suelen aparecer regiones de pequeño tamaño marcadas como de primer plano debido
al ruido en el _frame_ original. Una solución muy común en estos casos es aplicar
operaciones de dilatación y erosión con el objeto de suprimirlas.

 3. **Extracción de blobs**. Los píxeles clasificados como de primer plano
suelen agruparse en regiones que corresponden a objetos en movimiento en el
_frame_ original. La _extracción de blobs_ permite identificar estas regiones
para, por ejemplo, marcarlas con un cuadro delimitador en la imagen original.

## OpenCV

Los pasos a realizar son relativamente sencillos, por lo que no nos costaría
mucho desarrollar nuestra propia implementación, ya que la mayor parte de ellos
están perfectamente documentados de manera muy comprensible en Internet:

 * **Supresión del fondo**:
    * Wikipedia - [Detección de primer plano](http://es.wikipedia.org/wiki/Detecci%C3%B3n_de_primer_plano)

 * **Operaciones morfológicas**
    * Wikipedia - [Morfología matemática](http://es.wikipedia.org/wiki/Morfolog%C3%ADa_matem%C3%A1tica)
    * Universidad Carlos III de Madrid - [Operaciones Morfológicas](http://www.tsc.uc3m.es/imagine/Curso_ProcesadoMorfologico/Contenido/Operaciones/OperacionesMorfologicas.html)

 * **Extracción de blobs**
    * Wikipedia - [Connected-component labeling](http://en.wikipedia.org/wiki/Blob_extraction)

Sin embargo existe una librería de visión por computador, denominada [OpenCV],
que permite que nos ahorremos todo este trabajo.

Además en estos casos siempre debemos tener presente que aunque se trate de
algoritmos sencillos, siempre existen pequeñas cuestiones que deben ser tenidas
en cuenta, fundamentalmente desde el punto de vista de la precisión de los
algoritmos y del rendimiento, lo que puede dificultar el desarrollo. Por eso
suele ser preferible utilizar una librería madura en lugar de hacer nuestra
propia implementación.

## OpenCV y Qt

Si estamos desarrollando una aplicación gráfica en [Qt] debemos tomar una serie
de medidas para poder emplear la librería [OpenCV] desde ella:

### Conversión de QImage en cv::Mat

Las imágenes de las que haremos uso son instancias de la clase [QImage], propia
del _framework_ [Qt]. Sin embargo las funciones, clases y métodos de [OpenCV]
esperan objetos `cv::Mat`. Para convertir entre un formato y otro podemos emplear
el proyecto [QtOpenCV] de [Debao Zhang](https://github.com/dbzhang800) (licencia
[MIT](http://es.wikipedia.org/wiki/MIT_License))

Para utilizarlo sólo necesitamos:

 1. Descargar en el directorio del proyecto los archivos:

     * [cvmatandqimage.cpp]
     * [cvmatandqimage.h]
     * [opencv.pri]
     * [QtOpenCV.pri]

 2. Abrir el archivo `.pro` del proyecto y añadir al final la línea:

        include(QtOpenCV.pri)

Los archivos `.pri` tienen el mismo formato que los `.pro` pero están pensados
para ser incluidos por estos últimos. En nuestro caso el archivo [QtOpenCV.pri]
contiene información sobre como incorporar los archivos [cvmatandqimage.cpp]
y [cvmatandqimage.h] al proyecto, haciendo que las funciones por ellos
definidas estén disponibles para nuestra aplicación.

Tal y como se comenta en el archivo `README.md` de [QtOpenCV], en el proyecto
se definen dos funciones:

~~~~.cpp
namespace QtOcv {
    // channels == 0 significa autodetección
    cv::Mat image2Mat(const QImage &img,
                      int channels = 0,
                      MatChannelOrder rgbOrder = MCO_BGR);
    // format == QImage::Format_Invalid significa autodetección
    QImage mat2Image(const cv::Mat &mat,
                     QImage::Format format = QImage::Format_Invalid,
                     MatChannelOrder rgbOrder = MCO_BGR);
}
~~~~

que podemos usar para convertir objetos [QImage] a `cv::Mat` y viceversa.

### Añadir la librería OpenCV al proyecto

Aunque ya hemos incorporado [QtOpenCV] a nuestro proyecto para la conversión
entre formatos de imagen, aun no hemos añadido la librería OpenCV propiamente
dicha:

 * El archivo [QtOpenCV.pri] incluido anteriormente a su vez incluye a
[opencv.pri], cuya labor es facilitar el añadir [OpenCV] al proyecto. Lo único
que tenemos que hacer es editar el archivo `.pro` e incorporar al final la línea:

        add_opencv_modules(core video imgproc)

    o en Windows:

        add_opencv_modules(core video imgproc, 2.4.4)

    donde `2.4.4` debe sustituirse por el número de la versión actualmente
instalada de OpenCV. Esto es un requisito en los sistemas Windows ya que
dicho número se usa para componer el nombre de las librerías `.dll` con las
que debe enlazarse el ejecutable del proyecto.

    En la [introducción](http://docs.opencv.org/modules/core/doc/intro.html) de
[OpenCV] se explica que el paquete está divido a su vez en distintos módulos
o librerías, cada uno de los cuales está dedicado a un tipo de tarea específico.
En nuestro caso concreto el módulo _video_ incluye las clases y funciones de
supresión del fondo que nos interesa utilizar, mientras que _imgproc_ contiene
las operaciones morfológicas y de detección de contornos.

<a id="incorporar_libreria_manualmente"></a>

 * Si por cualquier motivo no estuviéramos haciendo uso de los archivos `.pri`
tendríamos que incorporar la librería al proyecto manualmente:

    * En Linux y Mac OS X esto se puede hacer como un _paquete instalado en el sistema_:

        1. En el menú contextual del proyecto (botón derecho sobre el proyecto)
seleccionar **Add Library.../System package**.

        2. En el paso posterior indicar **opencv** como nombre del paquete. Obviamente
la librería tiene que haber sido instalada previamente usando el procedimiento
usual de nuestra distribución.

    * En Windows este recurso no existe, por lo que la librería suele incorporarse
al proyecto como _librería externa_:

        1. En el menú contextual del proyecto (botón derecho sobre el proyecto)
seleccionar **Add Library.../External library**.

        2. Indicar el archivo de la librería (_Library file_) que queremos
incorporar y el directorio de cabeceras (_Include Path_). Como lo estamos
haciendo para Windows, sólo tenemos que tener marcada dicha opción en la lista
de plataformas soportadas. Por lo general:

            * Librerías en `C:\opencv\build\<ARQUITECTURA>\mingw\lib`: `libopencv_core<VERSION>.dll.a` y `libopencv_video<VERSION>.dll.a`
            * Ruta de las cabeceras: `C:\opencv\build\include`

    Para ambos sistemas, al terminar se nos abrirá el archivo `.pro` del proyecto con
los cambios correspondientes realizados. Debemos guardarlo para dar por
finalizada la incorporación de la librería.

## QImage vs QPixmap

Una instancia de [QPixmap] es una representación de una imagen optimizada para
ser mostrada. Esto significa que en muchos sistemas sus características
dependen de las de la pantalla (p. ej. su profundida de color puede tener que
ser la misma que la que actualmente tiene el adaptador gráfico: 8 bits,
16 bits, 32 bits, etc.) y que internamente se implementa mediante algún tipo
de objeto del lado del servidor gráfico cuya función es representar a las
imágenes de cara al resto del sistema de ventanas. Por lo tanto, los píxeles
de un objeto [QPixmap] no son accesibles directamente por parte del aplicación.

Una instancia de [QImage] es una representación independiente del hardware de
una imagen. Básicamente permite leer y escribir imágenes desde un archivo y
manipular los píxeles directamente, sin que las características actuales del
adaptador gráfico tengan nada que ver. Los datos de la imagen se almacenan
en el lado de la aplicación, por lo que son accesibles a esta en todo momento.

Normalmente la clase [QImage] se utiliza para cargar una imagen desde un
archivo, opcionalmente manipular los píxeles y después convertirla a un
objeto [QPixmap] para mostrarla en la pantalla.

En nuestro caso existen dos motivos fundamentales para utilizar [QImage]
en lugar de [QPixmap]:

 * Para convertir la imagen a un objeto `cv::Mat` de [OpenCV] se necesita
acceso a los datos de los píxeles. Como hemos comentado, eso sólo es posible
con la clase [QImage].

 * Generamente un objeto [QPixmap] encapsula el acceso a algún tipo de
recurso del servidor gráfico, con el que la aplicación se comunica a través
del hilo GUI (el hilo principal de la aplicación). Puesto que en muchos
sistemas operativos no es seguro comunicarse con el servidor gráfico a través
de un hilo diferente a ese, cualquier manipulación de un objeto [QPixmap]
fuera del hilo principal puede dar lugar a efectos inesperados. Dado que
queremos transferir las imágenes a un hilo de trabajo para su procesamiento,
parece que lo más seguro es utilizar la clase [QImage][^1].

## Detección de movimiento

Con acceso a las clases y funciones de [OpenCV] desde nuestra aplicación,
podemos pasar a resolver el problema que nos habíamos propuesto; detectar
movimiento en una secuencia de vídeo.

Como ocurre con muchas otras tareas en el campo de la visión por computador,
esta se puede resolver de múltiples maneras. Además es muy común que en cada
técnica posible haya una decena de parámetros que den resultados diferentes
según como los ajustemos.

Nosotros nos centraremos en solución concreta:

~~~~.cpp
// std::vector<cv::Mat> images = <vector de imágenes en cv::Mat>

// Definimos algunos tipos para que el código se lea mejor
typedef std::vector<cv::Mat> ImagesType;
typedef std::vector<std::vector<cv::Point> > ContoursType;

// Instancia de la clase del sustractor de fondo
// cv::BackgroundSubtractorMOG2(history=500,
//                              varThreshold=16,
//                              bShadowDetection=true)
cv::BackgroundSubtractorMOG2 backgroundSubtractor;
backgroundSubtractor.nmixtures = 3;
// Desactivar la detección de sombras
backgroundSubtractor.bShadowDetection = false;  

for (ImagesTypes::const_iterator i = images.begin(); i < images.end(); ++i) {
    // Sustracción del fondo:
    //  1. El objeto sustractor compara la imagen en i con su
    //     estimación del fondo y devuelve en foregroundMask una
    //     máscara (imagen binaria) con un 1 en los píxeles de
    //     primer plano.
    //  2. El objeto sustractor actualiza su estimación del fondo
    //     usando la imagen en i.
    cv::Mat foregroundMask;
    backgroundSubtractor(*i, foregroundMask);

    // Operaciones morfolóficas para eliminar las regiones de
    // pequeño tamaño. Erode() las encoge y dilate() las vuelve a
    // agrandar.
    cv::erode(foregroundMask, foregroundMask, cv::Mat());
    cv::dilate(foregroundMask, foregroundMask, cv::Mat());

    // Obtener los contornos que bordean las regiones externas
    // (CV_RETR_EXTERNAL) encontradas. Cada contorno es un vector
    // de puntos y se devuelve uno por región en la máscara.
    ContoursType contours;
    cv::findContours(foregroundMask, contours, CV_RETR_EXTERNAL,
                     CV_CHAIN_APPROX_NONE);

    // Aquí va el código ódigo que usa los contornos encontrados...
    // P. ej. usar cv::boundingRect() para obtener el cuadro
    // delimitador de cada uno y pintarlo en la imagen original
}
~~~~

Donde suponemos que previamente hemos convertido todas las imágenes de
[QImage] a cv::Mat y las hemos almacenado en un vector.

Al final de cada iteración del bucle tenemos para cada imagen un vector de
contornos, donde cada uno es un vector de puntos. Con los contornos se pueden
hacer múltiples operaciones. Por ejemplo calcular el rectángulo que contiene
a cada uno (_bounding box_) con [cv::boundingRect][]() para pintarlos sobre
la imagen antes de mostrársela al usuario.


## Referencias

 1. [OpenCV]
 2. [QtOpenCV]

[Qt]: |filename|/Overviews/proyecto-qt.md "Proyecto Qt"
[OpenCV]: http://opencv.willowgarage.com/wiki/ "OpenCV"
[QtOpenCV]: https://github.com/dbzhang800/QtOpenCV "QtOpenCV"
[QImage]: http://qt-project.org/doc/qt-5.0/qtgui/qimage.html "QImage"
[QPixmap]: http://qt-project.org/doc/qt-5.0/qtgui/qpixmap.html "QPixmap"
[cvmatandqimage.cpp]: https://github.com/dbzhang800/QtOpenCV/blob/master/cvmatandqimage.cpp "cvmatandqimage.cpp"
[cvmatandqimage.h]: https://github.com/dbzhang800/QtOpenCV/blob/master/cvmatandqimage.h "cvmatandqimage.h"
[QtOpenCV.pri]: https://github.com/dbzhang800/QtOpenCV/blob/master/QtOpenCV.pri "QtOpenCV.pri"
[opencv.pri]: https://github.com/dbzhang800/QtOpenCV/blob/master/opencv.pri "opencv.pri"
[cv::boundingRect]: http://opencv.willowgarage.com/documentation/cpp/structural_analysis_and_shape_descriptors.html#cv-boundingrect "cv::boundingRect"

[^1]: Más detalles en el mensaje [QPixmap: It is not safe to use pixmaps outside the GUI thread](http://lists.trolltech.com/qt-interest/2008-11/thread00534-0.html)
de las listas de correo de [Qt].
