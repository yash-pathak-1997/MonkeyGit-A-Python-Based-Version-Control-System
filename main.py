from Logs.Log import Log
from git import VCS
if __name__ == "__main__":
    log_obj = Log()
    log_obj.log("Log file created", True)

    # code will go here
    obj=VCS()
    obj.initialize()
    log_obj.close_logging()
