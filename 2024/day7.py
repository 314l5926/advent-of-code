# DFS is the fastest
def find_op(res: int, head: int, tail: list):
    if len(tail) == 0:
        if res == head:
            yield []
        return

    if res != head and str(res).endswith(str(head)):
        r = int(str(res)[:-len(str(head))])
        for ops in find_op(r, tail[0], tail[1:]):
            yield ['||'] + ops

    if res % head == 0:
        for ops in find_op(int(res / head), tail[0], tail[1:]):
            yield ['*'] + ops

    if res - head > 0:
        for ans in find_op(res - head, tail[0], tail[1:]):
            yield ['+'] + ans

