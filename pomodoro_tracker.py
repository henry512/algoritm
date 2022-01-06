from datetime import datetime, timedelta
from time import time, sleep


def execute(working_minutes: int, sleep_minutes: int, max_number_alarms: int) -> None:
    next_time_in_steep: time = (datetime.now() + timedelta(minutes=working_minutes)).time()
    round_while_alarm: int = 0

    while round_while_alarm <= max_number_alarms:
        try:
            if datetime.now().time() > next_time_in_steep:
                print("Iniciamos descanso...")
                sleep(sleep_minutes * 1000 * 60)
                next_time_in_steep = (datetime.now() + timedelta(minutes=working_minutes)).time()
                round_while_alarm += 1
            else:
                print("Trabajando...")
                sleep(5)
        except KeyboardInterrupt:
            print("Close tracker")
            break


if __name__ == "__main__":
    execute(1, 1, 1)

