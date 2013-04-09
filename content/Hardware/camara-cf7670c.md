Title: Cámara CF7670C-V2
Tags: cf7670c, i2c, ov7670, al422
Date: 2013-01-13

Los módulos de cámara CF7670C y CF7670C-V2 combinan el sensor CMOS [OmniVision OV7670]
con una memoria FIFO [Averlogic AL422] de 3Mb.

<img src="https://drive.google.com/uc?export=download&confirm=&id=0B4Cklvu_Zw9fS20tR1lnYmFHZVk" width="300" alt="Cámara CF7670C-V2" class="right-float">

La idea es que las imágenes capturadas por el sensor se almacenen en la memoria FIFO,
dando tiempo a la CPU externa a recuperarlas al ritmo que le sea posible.

Las principales características del sensor [OmniVision OV7670] son:

 * Resolución de 640x480 pixels (VGA).
 * Hasta 30 fps para resolución VGA.
 * Formatos de salida (8 bits):
    * [YUV]/[YCbCr] 4:2:2
    * RGB 565/555/444
    * GRB 4:2:2
    * Raw RGB Data
 * Modo de [escaneo progresivo](http://es.wikipedia.org/wiki/Escaneo_progresivo).
 * Interfaz de control mediante [SCCB].

Tal y como se puede observar en el [esquemático] del módulo, tanto el bus
[SCCB] (que prácticamente es un [I2C]) como las líneas del OV7670 que informan
del barrido vertical (VSYNC) y horizontal (HREF) están disponibles para que
sean accesibles a una CPU externa.

Por el contrario, las líneas de datos del OV7670 están conectadas al AL422
para almacenar en el la imagen capturada. Es la salida de esta memoria FIFO,
así como las líneas necesarias para controlar la lectura de la misma, las que
son  accesibles desde el conector del módulo.

## Referencias adicionales

 1. [OmniVision OV7670].
 1. [Averlogic AL422].
 1. [Esquemático del módulo CF7670C-V2](https://docs.google.com/a/isaatc.ull.es/file/d/0B4Cklvu_Zw9fNFJ3QTdaY284Znc/edit).
 1. [Pines del módulo CF7670C-V2](https://docs.google.com/a/isaatc.ull.es/file/d/0B4Cklvu_Zw9fNzFIbml0dHNXaTQ/edit).
 1. [Controlador de ejemplo para el módulo CF7670C-V2](https://drive.google.com/uc?export=download&confirm=&id=0B4Cklvu_Zw9fS3c4VTRTNHJvMEU).
 1. [OV7670 Implementation Guide](https://docs.google.com/a/isaatc.ull.es/file/d/0B4Cklvu_Zw9feEVCU3BzZHY4SEk/edit).

[OmniVision OV7670]: https://docs.google.com/a/isaatc.ull.es/file/d/0B4Cklvu_Zw9fanZqcWUyVUQxaTg/edit "Sensor CMOS OmniVision OV7670"
[Averlogic AL422]: https://docs.google.com/a/isaatc.ull.es/file/d/0B4Cklvu_Zw9fV3gyQ3dfTkRETDg/edit "FIFO Averlogic AL422"
[SCCB]: https://docs.google.com/a/isaatc.ull.es/file/d/0B4Cklvu_Zw9fTThIUmdRYUw4TXM/edit "Serial Camera Control Bus"
[YUV]: http://es.wikipedia.org/wiki/YUV "YUV"
[YCbCr]: http://es.wikipedia.org/wiki/YCbCr "YCbCr"
[esquemático]: https://docs.google.com/a/isaatc.ull.es/file/d/0B4Cklvu_Zw9fNFJ3QTdaY284Znc/edit "CF7670C-V2 Camera Module Schematic"
[I2C]: http://es.wikipedia.org/wiki/I2C "I²C (Inter-Integrated Circuit)"