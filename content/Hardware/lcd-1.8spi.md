Title: LCD 1.8" SPI (ST7735)
Tags: lcd, spi, st7735
Date: 2013-01-13

El módulo en cuestión tiene las siguientes características:

<img src="https://drive.google.com/uc?export=download&confirm=&id=0B4Cklvu_Zw9fUmF1d0YzNzMwNG8" style="float:right;margin:0 0px 10px 0">

 * Resolución de 128x160 pixels.
 * 262K colores.
 * Retro-iluminación LED.
 * Interfaz [SPI] a través del chip controlador ST7735R.
 * Compatible con lógica TTL de 3.3 y 5v.

El corazón del módulo es el chip controlador ST7735. Este se conecta por un lado
a la LCD propiamente dicha y por el otro ofrece una interfaz [SPI] a la que
se puede conectar una CPU externa. Los datos a mostrar se pueden almacenar
en una RAM interna con capacidad para 132x162x18 bits.

Las aplicaciones pueden acceder directamente al módulo a través de la
interfaz de programación [SPI] que el núcleo puede hacer pública al espacio de
usuario. Sin embargo una de las características más interesantes de este
módulo es la existencia de un [controlador de vídeo] [framebuffer] para sistemas
Linux. Haciendo uso del mismo las aplicaciones pueden utilizar la pantalla LCD
como si de una tarjeta gráfica convencional se trata, ignorando la interfaz [SPI]

## Referencias adicionales

 1. [Hoja de datos Sitronix ST7735 262K Color Single-Chip TFT Controller/Driver](https://docs.google.com/file/d/0B4Cklvu_Zw9fMmM3U0I2NU53Y3c/edit).
 1. [Librería para Arduino y programas de ejemplo](https://drive.google.com/uc?export=download&confirm=&id=0B4Cklvu_Zw9fT2hjVmpIQ2x0NVU)
 1. [FB driver for ST7735 LCD controller](https://github.com/ohporter/linux-am33x/blob/st7735fb/drivers/video/st7735fb.c)

[SPI]: http://es.wikipedia.org/wiki/SPI "Serial Peripheral Interface"
[framebuffer]: http://es.wikipedia.org/wiki/Framebuffer "Framebuffer"
[controlador de vídeo]: https://github.com/ohporter/linux-am33x/blob/st7735fb/drivers/video/st7735fb.c "FB driver for ST7735 LCD controller"
