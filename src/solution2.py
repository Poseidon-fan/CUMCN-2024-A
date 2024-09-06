from src.bench import get_benches

benches = []

def validate():
    # 先检测第一个
    first = benches[0]
    for i in range(len(benches)):
        if i > 1 and first.overlap_test(benches[i]):
            return False

    second = benches[1]
    for i in range(len(benches)):
        if i > 2 and second.overlap_test(benches[i]):
            return False

    return True

def solve():
    global benches
    benches = get_benches(412.48)
    print(validate())


if __name__ == '__main__':
    solve()