import datetime


class Log:

    def __init__(self):
        self.path_to_log = "./Logs/logs/"
        self.curr_ts = str(datetime.datetime.now()).replace(" ", "").replace(".", "").replace(":", "")
        self.logfile_name = self.path_to_log + "log_" + self.curr_ts + ".txt"
        self.logfile_obj = open(self.logfile_name, "w")
        self.logfile_obj.close()

    def log(self, msg, print_console=False):
        self.logfile_obj = open(self.logfile_name, "a")
        self.logfile_obj.write(msg + "\n")
        if print_console:
            print(msg)
        self.logfile_obj.close()

    def close_logging(self):
        self.logfile_obj.close()
