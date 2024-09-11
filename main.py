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
object_radius = 5
object_speed = 100
object_x, object_y = WIDTH // 2, HEIGHT - 50
target_radius = 50
target_x, target_y = WIDTH // 2, 100
running = True

# Function to calculate distance
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to update object position
def update_object():
    global object_y
    object_y -= object_speed / 60  # Update object position (assuming 60 FPS)
    if object_y <= target_y + target_radius:
        return False  # object hit the target
    return True

# WebSocket handler
async def handle_client(websocket, path):
    global running
    clock = pygame.time.Clock()

    while running:
        running = update_object()

        # Prepare data to send
        data = {
            "object_x": object_x,
            "object_y": object_y,
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
