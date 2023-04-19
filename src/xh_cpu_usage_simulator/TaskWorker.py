import time


def worker(index: int, d: dict, do_something) -> [int, int]:
    def get_time():
        t = time.time_ns()
        ms = t // 1_000_000
        s = ms // 1000
        return s, ms

    s, _ = get_time()

    task_to_run = int(d[f"{index}"])
    target = task_to_run
    while True:
        n_s, n_ms = get_time()
        if n_s != s:
            new_task_to_run = int(d[f"{index}"])
            if task_to_run != new_task_to_run:
                print(f"[Worker {index}]Target to run updated from {task_to_run} -> {new_task_to_run}")
            if target != 0:
                print(f"[Worker {index}] Completed {task_to_run - target}/{task_to_run} [{round(1- target/task_to_run, 2)} %]")
            task_to_run = new_task_to_run
            print(f"[Worker {index}]Rest target")
            target = task_to_run
            s = n_s

        if target > 0:
            target -= 1
            do_something()  # payload
        elif target == 0:
            diff = (s + 1) * 1000 - n_ms
            print(f"[Worker {index}]Taking {(n_ms - (s * 1000))} ms for {task_to_run} tasks [Sleep for {round(diff/1000, 4)} s]")
            task_to_run = d[f"{index}"]
            target = task_to_run
            if diff > 0:
                time.sleep(diff/1000)
            else:
                continue
