import config
import importlib

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