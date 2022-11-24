from Logs.Log import Log

if __name__ == "__main__":
    log_obj = Log()
    log_obj.log("Log file created", True)

    # code will go here

    log_obj.close_logging()
