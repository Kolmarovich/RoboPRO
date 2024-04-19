import socket
import struct
import numpy as np
from dataclasses import dataclass

from config import udp_ip


@dataclass
class Payload:
    timestamp: int
    theta: list


def dh_matrix(theta, d, a, alpha):
    """
    Function for calculating the transformation matrix
    using the Denavit-Hartenberg (DH) method
    """
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    cos_alpha = np.cos(alpha)
    sin_alpha = np.sin(alpha)

    dh = np.array([
        [cos_theta, -sin_theta*cos_alpha, sin_theta*sin_alpha, a*cos_theta],
        [sin_theta, cos_theta*cos_alpha, -cos_theta*sin_alpha, a*sin_theta],
        [0, sin_alpha, cos_alpha, d],
        [0, 0, 0, 1]
    ])

    return dh


def main():
    UDP_IP = udp_ip
    UDP_PORT = 8088

    params = [
        [0, 0.21, np.pi/2],
        [-0.8, 0.193, 0],
        [-0.598, -0.16, 0],
        [0, 0.25, np.pi/2],
        [0, 0.25, -np.pi/2],
        [0, 0.25, 0]
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
                theta = np.radians(payload.theta[i])
                d = params[i][1]
                a = params[i][0]
                alpha = params[i][2]
                transform_matrix = np.dot(transform_matrix,
                                          dh_matrix(theta, d, a, alpha)
                                          )

            position = transform_matrix[:3, 3]

            print(f"Received message {payload.timestamp}:")
            print("End-effector position")
            print(position)
            print("\n")

    finally:
        sock.close()


if __name__ == "__main__":
    main()
