import logging

def setlogger():
    logging.basicConfig(filename="logfiles/app.log", filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)



def applog(message):
    msg = str(message)
    logging.info(msg)
