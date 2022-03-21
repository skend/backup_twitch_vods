HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
ERROR = '\033[31m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def info(msg):
    print(OKGREEN + 'INFO: ' + msg + ENDC)


def warn(msg):
    print(WARNING + 'WARN: ' + msg + ENDC)


def error(msg):
    print(ERROR + 'ERROR: ' + msg + ENDC)