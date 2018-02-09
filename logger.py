class Logger:
    """ Base class for logging """
    def __init__(self, min_priority=0, outfile='stdout'):
        self.logger_outfile = outfile
        self.logging_priority = min_priority
        self.class_name = self.__class__.__name__
        if self.logger_outfile != 'stdout':
            self.log_file = open(outfile, 'a') # Auto-raises error

    def log(priority, *args):
        if priority >= min_priority:
            msg = '[' + str(priority) + '] ' \
                  + self.class_name + ' -- ' \
                  + ' '.join(tuple(str(i) for i in args))
            print(msg)
            if self.logger_outfile != 'stdout':
                self.log_file.write(msg + '\n')
