import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

numbers_buffer = []
access_control = threading.Lock()
is_producer_done = False

ALL_NUMBERS_FILE = "all.txt"
EVEN_NUMBERS_FILE = "even.txt"
ODD_NUMBERS_FILE = "odd.txt"

def generate_numbers():
    global is_producer_done
    for _ in range(MAX_COUNT):
        number = random.randint(LOWER_NUM, UPPER_NUM)
        with access_control:
            if len(numbers_buffer) < BUFFER_SIZE:
                numbers_buffer.append(number)
                with open(ALL_NUMBERS_FILE, "a") as file:
                    file.write(f"{number}\n")
    is_producer_done = True

def handle_even_numbers():
    while not is_producer_done or numbers_buffer:
        with access_control:
            if numbers_buffer and numbers_buffer[-1] % 2 == 0:
                even_number = numbers_buffer.pop()
                with open(EVEN_NUMBERS_FILE, "a") as file:
                    file.write(f"{even_number}\n")

def handle_odd_numbers():
    while not is_producer_done or numbers_buffer:
        with access_control:
            if numbers_buffer and numbers_buffer[-1] % 2 != 0:
                odd_number = numbers_buffer.pop()
                with open(ODD_NUMBERS_FILE, "a") as file:
                    file.write(f"{odd_number}\n")

if __name__ == "__main__":
    threads = [
        threading.Thread(target=generate_numbers),
        threading.Thread(target=handle_even_numbers),
        threading.Thread(target=handle_odd_numbers),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Execution of the program is complete.")
