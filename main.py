import numpy as np
import math
from typing import List

"""
    python version based on this: https://www.a1k0n.net/2011/07/20/donut-math.html
"""

def donut()->None:
    x_axis_step_size:float = 0.04
    z_axis_step_size:float = 0.02

    x_rotation:float = 0
    z_rotation:float = 0

    while True:
        x_rotation = x_rotation %  (2 * math.pi)
        z_rotation = z_rotation %  (2 * math.pi)

        frame:List[List[str]] = get_frame(x_rotation,z_rotation)
        print("\x1b[H")
        draw_frame(frame)
        print("",end="",flush=True)

        x_rotation += x_axis_step_size
        z_rotation += z_axis_step_size



def get_xyz_luminence(theta:float,y_rotation:float,x_rotation:float,z_rotation:float,r1:float,r2:float)->List[float]:
    cos_theta:float =     np.cos(theta)
    cos_y_rotation:float = np.cos(y_rotation)
    sin_theta:float = np.sin(theta)
    sin_y_rotation:float = np.sin(y_rotation)
    cos_x_rotation:float = np.cos(x_rotation)
    sin_x_rotation:float = np.sin(x_rotation)
    cos_z_rotation:float = np.cos(z_rotation)
    sin_z_rotation:float = np.sin(z_rotation)

    circle_x:float = r2 + r1 * cos_theta
    circle_y:float = r1 * sin_theta

    x:float = circle_x * (cos_z_rotation * cos_y_rotation + sin_x_rotation * sin_z_rotation * sin_y_rotation) - circle_y * cos_x_rotation * sin_z_rotation
    y:float = circle_x * (cos_y_rotation * sin_z_rotation - cos_z_rotation * sin_x_rotation * sin_y_rotation) + circle_y * cos_x_rotation * cos_z_rotation
    z:float = cos_x_rotation * circle_x * sin_y_rotation + circle_y * sin_x_rotation

    luminance:float = cos_y_rotation * cos_theta * sin_z_rotation - cos_x_rotation * cos_theta * sin_y_rotation - sin_x_rotation * sin_theta + cos_z_rotation * (cos_x_rotation * sin_theta - cos_theta * sin_x_rotation * sin_y_rotation)

    return [x,y,z,luminance]

def get_one_over_z(z:float)->float:
    one_over_z:float = 0
    try :
        one_over_z = 1 / z
    except(ZeroDivisionError):
        one_over_z = math.inf
    finally:
        return one_over_z


def get_frame(x_rotation:float,z_rotation:float)->List[List[str]]:
    # pass
    # theta:float = 0
    theta_step_size:float = 0.07

    screen_width:int = 80
    screen_height:int = 30

    # y_rotation:float = 0
    y_axis_step_size:float = 0.02

    ascii_luminance_map:str = ".,-~:;=!*#$@"

    r1 = 1
    r2 = 2

    donut_distance_depth:float = 5

    z_prime:float = screen_width * donut_distance_depth * 3 / (8 * (r1 + r2))

    output_frame:List[List[str]] = [
        [" " for _ in range(screen_width)]
        for _ in range(screen_height)
    ]

    depth_level_buffer:np.ndarray = np.zeros(shape=(screen_height,screen_width),dtype=float)
    
    thetas:np.ndarray = np.linspace(0,2*np.pi,(int)(2*np.pi / theta_step_size))
    phis:np.ndarray = np.linspace(0,2*np.pi,(int)(2*np.pi / y_axis_step_size))

    for theta in thetas:
        for phi in phis:
            x, y, z, luminance = get_xyz_luminence(theta,phi,x_rotation,z_rotation,r1,r2)
            # one_over_z:float = get_one_over_z(z)
            one_over_z_plus_depth:float = get_one_over_z(z + donut_distance_depth)

            x_prime:float = (screen_width / 2.0) + one_over_z_plus_depth * x * z_prime if not math.isinf(one_over_z_plus_depth) else 0
            y_prime:float = (screen_height / 2.0) - z_prime * y * one_over_z_plus_depth if not math.isinf(one_over_z_plus_depth) else 0

            x_prime_int:int = (int) (x_prime)
            y_prime_int:int = (int) (y_prime)

            if y_prime_int >= screen_height or x_prime_int >= screen_width or y_prime_int < 0 or x_prime_int < 0:

                # print("yx aaa")
                # print(y_prime,x_prime)
                # raise(Exception)
                continue

            if luminance > 0:
                if one_over_z_plus_depth > depth_level_buffer[y_prime_int][x_prime_int]:
                    depth_level_buffer[y_prime_int][x_prime_int] = one_over_z_plus_depth
                    luminance_index:int = (int) (luminance * 8)
                    output_frame[y_prime_int][x_prime_int] = ascii_luminance_map[luminance_index]
            

    return output_frame


def draw_frame(frame:List[List[str]])->None:
    # pass
    for y in frame:
        for x in y:
            print(x,end="",flush=False)
        print("",flush=False)

def main():
    # pass
    donut()

if __name__ == "__main__":
    main()

