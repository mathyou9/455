from pprint import pprint
import sys
import numpy as np
from PIL import Image as im

HEIGHT = 480
WIDTH = 480


class Material:
    def __init__(self, d, s, p):
        self.diffuse = d
        self.specular = s
        self.phong = p


class Sphere:
    def __init__(self, c, r, m):
        self.center = c
        self.radius = r
        self.material = m


class Triangle:
    def __init__(self, p1, p2, p3, m):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.material = m


def raytrace(rayFrom, rayTo, index):
    return np.array([.1, .1, .5])


def main():
    if (len(sys.argv) > 1):
        print(sys.argv[1])
        f = open(sys.argv[1], "r")
    else:
        f = open("diffuse.rayTracing", "r")
    # print(f.read())

    # Camera
    lookAt = list(map(int, f.readline().split()[1::]))
    print(lookAt)

    lookFrom = list(map(int, f.readline().split()[1::]))
    print(lookFrom)

    lookUp = list(map(int, f.readline().split()[1::]))
    print(lookUp)

    fov = list(map(int, f.readline().split()[1::]))[0]
    print(fov)

    lightDirectionString = f.readline().split()[1::]
    lightDirection = list(map(int, lightDirectionString[0:3:]))
    print(lightDirection)
    lightColor = list(map(int, lightDirectionString[4:7:]))
    print(lightColor)

    lightAmbient = list(map(float, f.readline().split()[1::]))
    print(lightAmbient)

    backgroundColor = list(map(float, f.readline().split()[1::]))
    print(backgroundColor)
    objs = []
    obj = f.readline().split()
    while (obj):
        if (obj[0] == "Sphere"):
            print("sphere")
            center = list(map(float, obj[2:5]))
            radius = obj[6]
            diffuse = list(map(float, obj[9:12:]))
            specular = list(map(float, obj[13:16:]))
            phong = obj[17]
            # print(center, radius, diffuse, specular, phong)
            m1 = Material(diffuse, specular, phong)
            s1 = Sphere(center, radius, m1)
            print(s1.center, s1.radius, s1.material.specular)
            objs.append(s1)
        else:
            p1 = list(map(float, obj[1:4:]))
            p2 = list(map(float, obj[4:7:]))
            p3 = list(map(float, obj[7:10:]))
            diffuse = list(map(float, obj[12:15:]))
            specular = list(map(float, obj[16:19:]))
            phong = obj[20]
            print("triangle")
            # print(p1, p2, p3, diffuse, specular, phong)
            m1 = Material(diffuse, specular, phong)
            t1 = Triangle(p1, p2, p3, m1)
            print(t1.p1, t1.p2, t1.p3, t1.material.diffuse)
            objs.append(t1)
        obj = f.readline().split()
    fw = open("test.ppm", "w")
    for i in range(len(objs)):
        if(type(objs[i]) is Sphere):
            fw.write(str(vars(objs[i])) + "\n")
        else:
            fw.write(str(vars(objs[i])) + "\n")

    W = np.subtract(lookAt, lookFrom)
    U = np.cross(W, lookUp)
    V = np.cross(U, W)
    U = np.append(U, np.negative(lookAt)[0])
    V = np.append(V, np.negative(lookAt)[1])
    W = np.append(W, np.negative(lookAt)[2])
    transformMatrix = np.matrix([U, V, W, (0, 0, 0, 1)])
    print(transformMatrix)

    scaleY = np.tan((np.pi / 180) * fov)
    scaleX = scaleY / (HEIGHT/WIDTH)

    pixels = np.zeros([HEIGHT, WIDTH, 3])
    # print(pixels)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            viewY = ((i / HEIGHT) * 2 - 1) * scaleY
            viewX = ((j / WIDTH) * 2 - 1) * scaleX
            transform = np.multiply(transformMatrix, [viewX, viewY, 0, 1])
            # print(transform)
            color = raytrace(lookFrom, lookAt, 0)

            # pixel = (i * WIDTH * 4) + j * 4
            # print(pixel, color)
            pixels[i][j][0] = color[0]*255
            pixels[i][j][1] = color[1]*255
            pixels[i][j][2] = color[2]*255

    data = im.fromarray(pixels.astype(np.uint8))

    data.save('test.png')


if __name__ == "__main__":
    main()
