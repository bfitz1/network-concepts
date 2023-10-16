import sys
import threading

def worker(tid, start, end, results):
    print(f"Running thread {tid}...")
    # The linear-time [O(n)] way is to loop over a range.
    # results[tid] = sum(x for x in range(start, end+1))

    # The constant-time [O(1)] way is to use the closed-form expression n*(n-1)/2.
    def gauss(n):
        return n*(n+1) // 2

    # Use start-1 so we don't exclude the bottom-end of the range!
    results[tid] = gauss(end) - gauss(start-1)

    print(f"Finished thread {tid}!")

def main(lols):
    results, threads = [None for _ in range(len(lols))], []
    for i, (start, end) in enumerate(lols):
        t = threading.Thread(target=worker, args=(i, start, end, results))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return print(f"{results}\n{sum(results)}")
    return 0

if __name__ == '__main__':
    try:
        lols = eval(sys.argv[1]) # Rare eval sighting.
        assert isinstance(lols, list)

        for x in lols:
            assert isinstance(x, list)
            assert len(x) == 2
            assert isinstance(x[0], int) and isinstance(x[1], int)
    except:
        print("usage: threads.py {list-of-lists}", file=sys.stderr)
        sys.exit(1)

    sys.exit(main(lols))
