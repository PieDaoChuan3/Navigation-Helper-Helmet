import sys
import multiprocessing
import raspberrypi_camera
import Voice_prompts

p1 = multiprocessing.Process(sys.modules['raspberrypi_camera']._dict_.clear())
p2 = multiprocessing.Process(sys.modules['Voice_prompts']._dict_.clear())

if _name_ == '_main_':
    p2.start()
    p1.start()
    