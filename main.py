import asyncio
import pyautogui
import time
import websockets

velocity = [0., 0., 0.]


async def hello(web_socket, path):
    global velocity
    next_tick = 0
    print("New connection")
    while True:
        try:
            message = await web_socket.recv()
            for i, val in enumerate(message.split(' ')):
                velocity[i] = velocity[i] + float(val)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            break
        if time.time() >= next_tick:
            pyautogui.moveRel(velocity[0], velocity[1])
            next_tick = time.time() + 0.16
            print(velocity)
            velocity = [0., 0., 0.]


start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
