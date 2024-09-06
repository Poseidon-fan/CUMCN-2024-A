from src.bench import Bench

benches = []
first = Bench(256)
first.locate(300)

benches.append(first)
cur_bench = first

for i in range(222):
    next_bench = cur_bench.next(165)
    benches.append(next_bench)
    cur_bench = next_bench

for bench in benches:
    print(bench)