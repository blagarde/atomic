import os
import uuid
import shutil
import sys
from subprocess import call


TMP = '/tmp'


def atomic(f):
    ''' Decorator that uses temp files to make the target function atomic '''

    def decorated(infile, outfile):
        if os.path.isdir(outfile):
            raise OSError("'%s' is a folder")
        tmp = str(uuid.uuid1())
        tmp_in = os.path.join(TMP, tmp + '.in')
        tmp_out = os.path.join(TMP, tmp + '.out')
        shutil.copy(infile, tmp_in)
        try:
            out = f(tmp_in, tmp_out)
            shutil.move(tmp_out, outfile)
        except Exception as e:
            try:
                os.remove(tmp_in)
                os.remove(tmp_out)
            except OSError:
                pass
            raise e
        os.remove(tmp_in)
        return out

    return decorated


@atomic
def f(infile, outfile):
    return call(' '.join(('cat', infile, infile, '>', outfile)), shell=True)


if __name__ == '__main__':
    inpath = os.path.abspath(sys.argv[1])
    outpath = os.path.abspath(sys.argv[2])
    print f(inpath, outpath)
