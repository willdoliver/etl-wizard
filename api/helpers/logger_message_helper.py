import os
from datetime import datetime

class LoggerMessageHelper():
    def log_message(filename, message):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")

        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write(current_datetime + str(message) + '\n')
        else:
            with open(filename, 'a') as file:
                file.write(current_datetime + str(message) + '\n')
