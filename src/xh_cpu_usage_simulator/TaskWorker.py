import time


def worker(index: int, d: dict, do_something) -> [int, int]:
    def get_time():
        t = time.time_ns()
        ms = t // 1_000_000
        s = ms // 1000
        return s, ms

    s, _ = get_time()
    task_to_run = d[f"{index}"]
    target = d[f"{index}"]
    while True:
        n_s, n_ms = get_time()
        if n_s != s:
            target = d[f"{index}"]
            s = n_s

        if target > 0:
            target -= 1
            do_something()  # payload
        elif target == 0:
            # print(f"[Worker {index}]Taking {(n_ms - (s * 1000))} ms for {task_to_run} tasks")
            task_to_run = d[f"{index}"]
            target = task_to_run
            diff = (s + 1) * 1000 - n_ms
            if diff > 0:
                time.sleep(diff/1000)
            else:
                continue
