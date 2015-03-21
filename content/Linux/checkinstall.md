Title: Crear paquetes de Debian con checkinstall
Tags: checkinstall, .deb, debian, paquetes
Date: 2014-05-06
status: draft

Ya hablamos de como modificar nuestro archivo de proyecto `.pro` para preparar
las reglas para [make install]. De tal forma que si lo hemos hecho bien podemos
compilar e instalar nuestra aplicación en el sistema simplemente ejecutando
los siguientes comandos:

~~~~.sh
$ qmake
$ make
$ make install
~~~~

# Sistemas de gestión de paquetes

Sin embargo esta no es la forma más conveniente de distribuir software destinado
a sistemas Linux. 

Por lo general las distribuciones de Linux usan algún [sistema de gestión de
paquetes](http://es.wikipedia.org/wiki/Sistema_de_gesti%C3%B3n_de_paquetes).
Estos están formados por una colección de herramientas diseñadas para
automatizar la instalación, actualización, configuración y deinstalación de
paquetes de software de forma consistente. Por lo general estos paquetes contiene
programas, librerías y datos, además de algunos metadatos relevalentes para
el funcionamiento del sistema de gestión de paquetes, como: nombre, descripción
fabricante, suma de comprobación, versión y una lista de depedencias necesarias
para que el software funcione convenientemente.

En sistemas [Debian] y derivados [deb] es la extensión de los paquetes de
software. Mientras que `dpkg` es el programa diseñado para manejarlos,
generalmente a través de otros programas como `apt`/`aptitude`, Ubuntu Software
Center, Synaptic o Gdebi.

Estos paquetes Debian pueden convertirse en otros formatos de paquete usando
`alien` y creados apartir del proyecto de código fuente usando [CheckInstall] o
Debian Package Maker.

# CheckInstall

[CheckInstall] es uno de esos programas que permiten crear paquetes `rpm` o
[deb] a partir del código fuente.

Para usarlo empezamos generando el archivo `Makefile` en el directorio del
proyecto para después compilar el programa:

~~~~.sh
$ qmake
$ make
~~~~

y ahora sólo tenemos que invocar el programa [CheckInstall] desde el mismo
directorio:

~~~~.sh
$ sudo checkinstall
~~~~

Un ejemplo, por ejemplo si quieres compilar el codigo fuente de wine 1.3 los pasos serian.

- Nos descargamos el codigo fuente de wine 1.3 desde el siguiente enlace. Ojo, puede que si lees este post mas tarde de Agosto 2010 la version de wine haya cambiado, tendras que buscar en la web oficial el enlace al codigo fuente correspondiente.

- Despues añadimos las siguientes instrucciones, solo son necesarias para compilar wine:


sudo apt-get build-dep wine
sudo apt-get install fakeroot

- Descomprimimos el codigo, nos metermos al directorio y ejecutamos: (Ojo, la compilacion de wine a mi me llevo mas de 15 minutos).

./configure
make
sudo checkinstall

En principio podemos pulsar intro en las preguntas que nos hace checkinstall, o cambia la respuesta si quieres modificar algun parametro.


checkinstall 1.6.1, Copyright 2002 Felipe Eduardo Sanchez Diaz Duran
Este software es distribuído de acuerdo a la GNU GPL

The package documentation directory ./doc-pak does not exist.
Should I create a default set of package docs? [y]: n

*****************************************
**** Debian package creation selected ***
*****************************************

Este paquete será creado de acuerdo a estos valores:

0 - Maintainer: [ root@soledad ]
1 - Summary: [ Wine 1.3 ]
2 - Name: [ wine ]
3 - Version: [ 1.3.0 ]
4 - Release: [ 1 ]
5 - License: [ GPL ]
6 - Group: [ checkinstall ]
7 - Architecture: [ i386 ]
8 - Source location: [ wine-1.3.0 ]
9 - Alternate source location: [ ]
10 - Requires: [ ]
11 - Provides: [ wine ]


Introduce un número para cambiar algún dato u oprime ENTER para continuar:

Al finalizar, tendremos un .deb de wine 1.3 en el directorio. Pues bien, el proceso para cualquier otra aplicacion que compiles mediante (./configure/make/sudo make install) seria similar.


# Referencias

 1. [Make install con qmake](|filename|/Qt/qmake-make-install.md)
 2. Wikipedia - [Sistema de gestión de paquetes](http://es.wikipedia.org/wiki/Sistema_de_gesti%C3%B3n_de_paquetes)
 3. Wikipedia - [deb (file format)](http://en.wikipedia.org/wiki/Deb_(file_format))
 4. Wikipedia - [CheckInstall](http://en.wikipedia.org/wiki/CheckInstall)

[make install]: |filename|/Qt/qmake-make-install.md "Make install con qmake"
[Debian]: https://www.debian.org "Debian - the universal operating system"
[deb]: http://en.wikipedia.org/wiki/Deb_(file_format) "Wikipedia - deb (file format)"
[CheckInstall]: http://en.wikipedia.org/wiki/CheckInstall "Wikipedia - CheckInstall"
