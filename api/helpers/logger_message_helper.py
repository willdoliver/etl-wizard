from datetime import datetime

class LoggerMessageHelper():
    def log_message(filename, message):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")

        with open(filename, 'a') as file:
            file.write(current_datetime + str(message) + '\n')
