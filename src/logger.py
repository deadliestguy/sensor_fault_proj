import logging 
from datetime import datetime

# lof file create korbo 
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# log folder path crete korbo 
logs_path = os.path.join(os.getcwdb(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

# log file er path 
LOG_PATH = os.path.join(logs_path,LOG_FILE)

# basic config set korbo 
logging.basicConfig(
    filename= LOG_PATH,
    level= logging.INFO,
    format= '[%(asctime)s] %(lineno)d %(name)s-%(levelname)s-%(message)s '
)


