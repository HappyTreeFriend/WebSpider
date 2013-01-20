#coding=utf-8
import sys
import time,threading

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer

examples = []
def example(fn):
    try: name = 'Example %d' % int(fn.__name__[7:])
    except: name = fn.__name__

    def wrapped():
        try:
            sys.stdout.write('Running: %s\n' % name)
            fn()
            sys.stdout.write('\n')
        except KeyboardInterrupt:
            sys.stdout.write('\nSkipping example.\n\n')

    examples.append(wrapped)
    return wrapped



@example
def example4():
    widgets = [' ', Percentage(), ' ',
               Bar(marker='=',left=' [',right='] '),
               ' ', ETA(), ' ', '']
    pbar = ProgressBar(widgets=widgets, maxval=500)
    pbar.start()
    for i in range(100,500+1,50):
        time.sleep(3)
        pbar.update(i)
    pbar.finish()

def test():
    global i
    print '\n',i
    t = threading.Timer(3, test)
    t.start()
    i+=1

if __name__ == '__main__':
    i = 1
    test()
    try:
        for example in examples: example()
    except KeyboardInterrupt:
        sys.stdout('\nQuitting examples.\n')
