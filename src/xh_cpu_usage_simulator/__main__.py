# This is a sample Python script.
from threading import Thread

import psutil

from xh_cpu_usage_simulator import TaskWorker
from xh_cpu_usage_simulator.MovingAvg import MovingAvg
from xh_cpu_usage_simulator.PsMonitor import PsMonitor
from xh_cpu_usage_simulator.LinearRegressionPrediction import LinearRegressionPredication

if __name__ == '__main__':
    d = dict()
    r = dict()
    for i in range(psutil.cpu_count(logical=False)):
        d.update({f"{i}": 10})
        r.update({f"{i}-complete": 0})
        bucket = MovingAvg(10)
        Thread(target=TaskWorker.worker, args=[i, d, r, lambda: bucket.insert(1)]).start()

    total_operation = sum([d[i] for i in d])

    m_avg = MovingAvg(10)

    target = 70
    rounds = 0
    prediction = LinearRegressionPredication(10)
    for m in PsMonitor().monitor():
        if m_avg.cur_index == 0:
            if rounds == 0:
                rounds += 1
            else:
                rounds += 1
                cur_total_operation = round(sum([d[i] for i in d]), 2)
                cur_total_mv = round(sum([r[i] for i in r], 2))
                prediction.insert(m_avg.avg, cur_total_mv)
                if prediction.is_ready():
                    next_operation = prediction.predict(71)
                else:
                    next_operation = None

                if target * 0.95 > m_avg.avg:
                    for i in d:
                        d[i] = next_operation if next_operation is not None else d[i] * 2
                    new_total_operation = round(sum([d[i] for i in d]), 2)
                    print(
                        f"{rounds:05d}::Targeting[{target}], now[{m_avg.avg}], increase operation with loading[{cur_total_mv}] from {cur_total_operation} to {new_total_operation}")
                elif target * 1.05 < m_avg.avg:
                    for i in d:
                        d[i] = next_operation if next_operation is not None else d[i] * 0.85
                    new_total_operation = sum([d[i] for i in d])
                    print(
                        f"{rounds:05d}Targeting[{target}], now[{m_avg.avg}], decrease operation with loading[{cur_total_mv}] from {cur_total_operation} to {new_total_operation}")
                else:
                    print(
                        f"{rounds:05d}Targeting[{target}], now[{m_avg.avg}], nothing to do with loading[{cur_total_mv}]")
        m_avg.insert(m.avg)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
