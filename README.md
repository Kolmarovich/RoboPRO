# Сalculation end-effector position

Solves the direct problem of kinematics, which consists in calculating the position of the robot in Cartesian coordinates based on the angular rotation of the joints.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone git@github.com:Kolmarovich/RoboPRO.git
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:

    For Linux and macOS:

    ```bash
    source venv/bin/activate
    ```

    For Windows:

    ```bash
    venv\Scripts\activate
    ```

4. Install dependencies:

    ```bash
    pip install numpy
   ```

5. Change the server address in config.py. The default is a local address.

## Usage

1. Running server:

    ```bash
    gcc main.c
    ```
    
    ```bash
    ./a.out
    ```

2. Running client:

    ```bash
    python3 Robopro.py
    ```
