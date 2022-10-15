# Graficas por computador
# Angel Higueros - 20460
# SR1

import struct

# Métodos de escritura
def char(c): 
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([b, g, r])



class Render(object):

    def glInit(self, filename = 'sr1.bmp'):
        self.filename = filename 
        self.width = 100 
        self.height = 100
        self.viewport_x = 0 
        self.viewport_y = 0 
        self.viewport_width = 100 
        self.viewport_height = 100
        self.current_color = color(255, 255, 255) # por defecto blanco
        self.vertex_color = color(200, 0, 0) # por defecto rojo
        self.framebuffer = []
        self.glClear()

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewPort(self, x, y, width, height):

        if self.width < x + width or self.height < y + height:
            print("[!] El viewport debe estar dentro de las medidas de la pantalla")
            self.viewport_x = 0
            self.viewport_y = 0
            self.viewport_width = self.width
            self.viewport_height = self.height
            self.glClear()
        else:
            self.viewport_x = x
            self.viewport_y = y
            self.viewport_width = width
            self.viewport_height = height
            self.glClear()

    def glClear(self):
        self.framebuffer= [
            [color(0, 0, 0) for x in range(self.width)]
            for y in range(self.height)
        ]

        for x in range(self.width):
            for y in range(self.height):
                if x >= self.viewport_x and x <= self.viewport_width and y >= self.viewport_y and y <= self.viewport_height:
                    self.framebuffer[x][y] = self.current_color 

    def glClearColor(self, r, g, b):
        self.current_color = color(r, g, b)

    def glVertex(self, x, y):

        # convertir coordenadas normalizadas a cordenadas del dispositivo
        half_size_width = self.viewport_width / 2
        half_size_height = self.viewport_height / 2

        coord_x = int((( x + 1 ) * half_size_width ))
        coord_y = int((( y + 1 ) * half_size_height ))

        self.framebuffer[coord_x][coord_y] = self.vertex_color


    def glColor(self, r, g, b):
        self.vertex_color = color(r, g, b)

    def glFinish(self):
        f = open(self.filename, 'bw')

        # Pixel header
        f.write(char('B'))
        f.write(char('M'))
        # tamaño archivo = 14 header + 40  info header + resolucion
        f.write(dword(14 + 40 + self.width * self.height * 3)) 
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))

        # Info header
        f.write(dword(40)) # tamaño header
        f.write(dword(self.width)) # ancho
        f.write(dword(self.height)) # alto
        f.write(word(1)) # numero de planos (siempre 1)
        f.write(word(24)) # bits por pixel (24 - rgb)
        f.write(dword(0)) # compresion
        f.write(dword(self.width * self.height * 3)) # tamaño imagen sin header
        f.write(dword(0)) # resolucion
        f.write(dword(0)) # resolucion
        f.write(dword(0)) # resolucion
        f.write(dword(0)) # resolucion


        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])


# IMPLEMENTACION
r = Render()
r.glInit('sr1-point.bmp')
r.glCreateWindow(1024, 1024)
r.glViewPort(50,50, 900, 900)
r.glClearColor(255, 0, 0)
r.glClear()
r.glVertex(1, 1)
r.glColor(1, 1, 1)
r.glFinish()