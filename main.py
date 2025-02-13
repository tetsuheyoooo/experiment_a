from threading import Timer
from multiprocessing import Process, Value, Array
import sys
sys.path.append("srcs") # 相対パスimportしようとしたが，子プログラムからも実行するときにバグるので検索ディレクトリを追加することにした
sys.dont_write_bytecode = True # pycache要らない
from srcs.buzzer_ring import *
from srcs.led_brink import *
from srcs.cds_sensing import *
from srcs.infrared_sensing import *
from srcs.line_commu import *

timers = {}
led_process = {"quit_flag": Value('i', 0), # quit_flag = false
              "pwm": Value('i', 0), "mode": Value('i', 0), "color": Array('i', [0,0,0])} # [R,G,B]=[F,F,F]

def multiprocess_caller():
  led_process["led"] = Process(target=led_brink, kwargs=led_process) # args=(CdS_caller.data)
  led_process["led"].start()

def CdS_caller():
  timers["CdS"] = Timer(1, CdS_caller)
  timers["CdS"].start()
  CdS_sensing()

def infrared_caller():
  timers["inf"] = Timer(10, infrared_caller)
  timers["inf"].start()
  infrared_sensing()

if __name__ == "__main__":
  try: # 初期化処理
    # line_init() # これが一番初め
    CdS_caller()
    infrared_caller()
    multiprocess_caller()

    while True:
      print("aaaaa")
      sleep(3)
      # CdS_sensing()
      
  except KeyboardInterrupt:
    for timer in timers.values():
      timer.cancel()
    led_process["quit_flag"].value = 1 # 脱出
    led_process["led"].join()
