# MICROBIT-GAMES-COLLECTION

## Description

This repository contains a collection of games developed for the BBC micro:bit platform. The games are periodically updated and uploaded to the collection. Each folder represents a

## Games

### 1. Snake

A classical snake game where player has to get food and grow the snake.

### 2. Space Invaders

A space invaders game where player shoots down waves of invaders before they reach the bottom of the screen.

## Getting Started - to get started, follow these steps:

1. Clone this repository.
2. Connect your micro:bit device to your computer.
3. Flash the game code (.hex) to your micro:bit.
4. Enjoy the games!

## Creating .hex Files with uflash

If you want to modify the game code and create your own .hex file, follow these steps:

### Prerequisites
- Python 3.x installed on your computer
- The game repository cloned locally

### Installation
1. Open a terminal or command prompt
2. Install `uflash` using pip:
   ```bash
   pip install uflash
   ```

### Creating a .hex File
1. Navigate to the game directory:
   ```bash
   cd ./snake
   ```
   or
   ```bash
   cd ./space-invaders
   ```

### Option 1: Flash Directly to Micro:bit (Recommended)
If your micro:bit is connected via USB:
```bash
uflash main.py
```
The device will reboot automatically and run your game!

### Option 2: Create main.hex File for Manual Transfer
If you want to create a `.hex` file to transfer manually later:

1. Use the [Official Micro:bit Python Editor](https://python.microbit.org/):
   - Open https://python.microbit.org/
   - Click **Open** and select your `main.py` file
   - Click **Download** to get the `main.hex` file

2. Or use `uflash` with output redirection (Windows):
   ```bash
   uflash main.py > main.hex
   ```

3. Then manually transfer the `.hex` file to your micro:bit:
   - Connect your micro:bit via USB
   - Drag and drop `main.hex` onto the micro:bit drive
   - The device will reboot automatically and run your game!
