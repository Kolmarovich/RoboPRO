import socket
import struct
import numpy as np
from dataclasses import dataclass

from config import udp_ip, udp_port


@dataclass
class Payload:
    timestamp: int
    theta: list[float]  # Angles in degrees


@dataclass
class DHParameters:
    a: float  # link length in meters
    d: float  # offset along Z-axis in meters
    alpha: float  # link twist angle in radians


def dh_matrix(theta, d, a, alpha):
    """
    Function for calculating the transformation matrix
    using the Denavit-Hartenberg (DH) method
    Parameters:
        theta - angle of rotation in radians;
        d - offset along Z-axis in meters
        a - link length in meters
        alpha - link twist angle in radians
    """
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    cos_alpha = np.cos(alpha)
    sin_alpha = np.sin(alpha)

    cos_theta_a = cos_theta * a
    sin_theta_a = sin_theta * a

    dh = np.array([
        [cos_theta, -sin_theta*cos_alpha, sin_theta*sin_alpha, cos_theta_a],
        [sin_theta, cos_theta*cos_alpha, -cos_theta*sin_alpha, sin_theta_a],
        [0, sin_alpha, cos_alpha, d],
        [0, 0, 0, 1]
    ])

    return dh


def main():
    UDP_IP = udp_ip
    UDP_PORT = udp_port

    params = [
        DHParameters(a=0, d=0.21, alpha=np.pi/2),
        DHParameters(a=-0.8, d=0.193, alpha=0),
        DHParameters(a=-0.598, d=-0.16, alpha=0),
        DHParameters(a=0, d=0.25, alpha=np.pi/2),
        DHParameters(a=0, d=0.25, alpha=-np.pi/2),
        DHParameters(a=0, d=0.25, alpha=0)
    ]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(b"get", (UDP_IP, UDP_PORT))

        # Receive packets from the server and unpack
        for i in range(5):
            data, _ = sock.recvfrom(1024)
            pd = struct.unpack("<Q6d", data)
            payload = Payload(pd[0], pd[1:])

            # Calculation of transformation matrices
            # and their sequential multiplication
            transform_matrix = np.eye(4)
            for i in range(len(payload.theta)):
                theta = np.radians(payload.theta[i])  # Convert to radians
                param = params[i]
                transform_matrix = np.dot(transform_matrix, 
                                          dh_matrix(theta, param.d,
                                                    param.a, param.alpha))

            position = transform_matrix[:3, 3]

            print(f"Received message {payload.timestamp}:")
            print("End-effector position")
            # Positions in meters
            print(position)
            print("\n")

    finally:
        sock.close()


if __name__ == "__main__":
    main()
