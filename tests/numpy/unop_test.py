import dace
import numpy as np


@dace.program
def uaddtest(A: dace.int64[5, 5], B: dace.int64[5, 5]):
    B[:] = +A

@dace.program
def usubtest(A: dace.int64[5, 5], B: dace.int64[5, 5]):
    B[:] = -A

@dace.program
def inverttest(A: dace.int64[5, 5], B: dace.int64[5, 5]):
    B[:] = ~A


if __name__ == '__main__':
    A = np.random.randint(1, 10, size=(5, 5))
    B = np.zeros((5, 5), dtype=np.int64)

    failed_tests = set()

    for opname, op in {'uadd': '+',
                       'usub': '-',
                       'invert': '~'}.items():
        
        def test(A, B):
            daceB = B.copy()
            exec('{opn}test(A, daceB)'.format(opn=opname))
            numpyB = B.copy()
            exec('numpyB[:] = {op}A'.format(op=op))
            norm_diff = np.linalg.norm(numpyB - daceB)
            if norm_diff == 0.0:
                print('Unary operator {opn}: OK'.format(opn=opname))
            else:
                failed_tests.add(opname)
                print('Unary operator {opn}: FAIL ({diff})'.format(opn=opname,
                                                            diff=norm_diff))
        
        test(A, B)
        
    if failed_tests:
        print('FAILED TESTS:')
        for t in failed_tests:
            print(t)
        exit(-1)
    exit(0)
