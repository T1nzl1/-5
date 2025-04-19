import multiprocessing
import os
import math

def is_prime(n):

    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def find_primes_in_range(start, end, result_queue):

    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    result_queue.put(primes)
    print(f"Процесс {os.getpid()} завершил работу. Найденные простые числа: {primes[:10]}...")

def find_primes_multiprocessing(limit, num_processes):


    range_size = limit // num_processes
    result_queue = multiprocessing.Queue()
    processes = []

    for i in range(num_processes):
        start = i * range_size + 1
        end = (i + 1) * range_size
        if i == num_processes - 1:
            end = limit

        process = multiprocessing.Process(target=find_primes_in_range, args=(start, end, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


    all_primes = []
    while not result_queue.empty():
        primes = result_queue.get()
        all_primes.extend(primes)

    all_primes.sort()
    return all_primes


if __name__ == "__main__":
    try:
        limit = int(input("Введите предел поиска простых чисел: "))
        if limit <= 1:
            print("Предел должен быть больше 1.")
            exit()

        num_processes = int(input(f"Введите количество процессов (максимум {multiprocessing.cpu_count()}): "))
        if num_processes < 1 or num_processes > multiprocessing.cpu_count():
            print(f"Недопустимое количество процессов.  Введите число от 1 до {multiprocessing.cpu_count()}.")
            exit()

        primes = find_primes_multiprocessing(limit, num_processes)
        print(f"\nВсе простые числа до {limit}:")
        print(primes)

    except ValueError:
        print("Ошибка: Введите целое число.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")