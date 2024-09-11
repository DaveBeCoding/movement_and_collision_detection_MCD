import pygame
import math
import asyncio
import websockets
import json

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Simulation properties
bullet_radius = 5
bullet_speed = 100
bullet_x, bullet_y = WIDTH // 2, HEIGHT - 50
target_radius = 50
target_x, target_y = WIDTH // 2, 100
running = True

# Function to calculate distance
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to update bullet position
def update_bullet():
    global bullet_y
    bullet_y -= bullet_speed / 60  # Update bullet position (assuming 60 FPS)
    if bullet_y <= target_y + target_radius:
        return False  # Bullet hit the target
    return True

# WebSocket handler
async def handle_client(websocket, path):
    global running
    clock = pygame.time.Clock()

    while running:
        running = update_bullet()

        # Prepare data to send
        data = {
            "bullet_x": bullet_x,
            "bullet_y": bullet_y,
            "target_x": target_x,
            "target_y": target_y,
            "target_radius": target_radius
        }

        # Send data to client
        await websocket.send(json.dumps(data))

        # Control the simulation frame rate
        await asyncio.sleep(1 / 60)  # 60 FPS
        clock.tick(60)

    # Stop the server after the simulation ends
    pygame.quit()
    await websocket.close()

# Start the WebSocket server
async def start_server():
    server = await websockets.serve(handle_client, "localhost", 8765)
    await server.wait_closed()

asyncio.get_event_loop().run_until_complete(start_server())
