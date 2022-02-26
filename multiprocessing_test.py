import multiprocessing
import time
import main_spec as ms

import sys
# are we running inside Blender?
bpy = sys.modules.get("bpy")
if bpy is not None:
    sys.executable = bpy.app.binary_path_python
    # get the text-block's filepath
    __file__ = bpy.data.texts[__file__[1:]].filepath
del bpy, sys


def test_function(my_argument, seconds):
        print('starting {my_argument}')
        time.sleep(seconds)
        print('finished {my_argument}')
        
        
def main():
    processes = []
    start = time.perf_counter()     

    for i in range(3):
        p = multiprocessing.Process(target=test_function, args=[str(i), 3])
        p.start()
        processes.append(p)
    i = multiprocessing.Process(target=ms.read_spectra)
    i.start()
    processes.append(i)
        
    for process in processes:
        process.join()
    end = time.perf_counter()

    print(f'duration: {end-start}')
    
    
    
if __name__ == '__main__':
    main()