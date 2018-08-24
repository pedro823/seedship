class Logger:
    """ Base class for logging """
    def __init__(self, otr, outfile='stdout'):
        self.logger_outfile = outfile
        self.class_name = otr.__class__.__name__
        if self.logger_outfile != 'stdout':
            self.log_file = open(outfile, 'a') # Auto-raises error

    def log(self, *args):
        msg = self.class_name + ' -- ' \
              + ' '.join(tuple(str(i) for i in args))
        if self.logger_outfile != 'stdout':
            self.log_file.write(msg + '\n')
        else:
            print(msg)
