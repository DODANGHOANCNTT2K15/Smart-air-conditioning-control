import websockets
import asyncio
import json
import importlib
import config

async def handle_connection(websocket, path):
    print("New connection established")
    try:
        while True:
            # Nhận dữ liệu từ Flutter
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=1)
                data = json.loads(message)
                if "temperature" in data:
                    # Cập nhật giá trị nhiệt độ từ Flutter
                    new_temperature = data['temperature']
                    config.temperature = new_temperature
                    update_config_file('temperature', new_temperature)
                    print(f"Updated temperature to: {new_temperature}")
                    
                if "current_mode_index" in data:
                    new_mode_index = data['current_mode_index']
                    config.current_mode_index = new_mode_index
                    update_config_file('current_mode_index', new_mode_index)
                    print(f"Updated current_mode_index to: {new_mode_index}")
                    
                if "current_wind_index" in data:
                    new_wind_index = data['current_wind_index']
                    config.current_wind_index = new_wind_index
                    update_config_file('current_wind_index', new_wind_index)
                    print(f"Updated current_wind_index to: {new_wind_index}")
                    
                if "status" in data:
                    new_status = data['status']
                    config.status = new_status
                    update_config_file('status', new_status)
                    print(f"Updated status to: {new_status}")
                    
                if "time_on" in data:
                    new_time_on = data['time_on']
                    config.time_on = new_time_on
                    update_config_file('time_on', new_time_on)
                    print(f"Updated time_on to: {new_time_on}")
                    
                # Gửi phản hồi về Flutter sau khi cập nhật thành công
                await websocket.send(json.dumps({"status": "updated"}))
                    
            except asyncio.TimeoutError:
                pass  # Timeout mỗi giây nếu không nhận được tin nhắn, tiếp tục gửi dữ liệu

            # Luôn reload config để có giá trị mới nhất từ file config.py
            importlib.reload(config)

            # Tạo dữ liệu JSON chứa các biến từ Python gửi về Flutter
            config_data = {
                "temperature": config.temperature,
                "humidity": config.humidity,
                "cur_temp": config.cur_temp,
                "cur_hum": config.cur_hum,
                "current_mode_index": config.current_mode_index,
                "current_wind_index": config.current_wind_index,
                "status": config.status,
                "time_on": config.time_on
            }

            # Gửi dữ liệu này về Flutter
            await websocket.send(json.dumps(config_data))

            await asyncio.sleep(1)  
    except websockets.ConnectionClosed:
        print("Connection closed")

def update_config_file(variable, value):
    """Cập nhật giá trị trong file config.py."""
    with open('config.py', 'r') as file:
        lines = file.readlines()

    with open('config.py', 'w') as file:
        for line in lines:
            if line.startswith(f'{variable} ='):
                file.write(f'{variable} = {value}\n')
            else:
                file.write(line)

    # Tải lại module config để các thay đổi có hiệu lực
    importlib.reload(config)

async def start_websocket_server():
    try:
        # Khởi tạo server WebSocket
        server = await websockets.serve(handle_connection, "0.0.0.0", 8765)
        print("WebSocket server started on port 8765")
        await server.wait_closed()
    except Exception as e:
        print(f"Error starting WebSocket server: {e}")

def run_websocket_server():
    # Tạo event loop mới cho thread này
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    new_loop.run_until_complete(start_websocket_server())
    new_loop.run_forever()

