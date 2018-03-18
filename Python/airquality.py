#!/usr/bin/env python

import logging
import logging.handlers
import sys
import serial
import time
import smtplib
from email.mime.text import MIMEText

# Initialize the logging.
LOG_FILENAME = "/var/log/airquality.log"
LOG_LEVEL = logging.INFO

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

sys.stdout = MyLogger(logger, logging.INFO)
sys.stderr = MyLogger(logger, logging.ERROR)

logger.info("Starting air quality service.")

# Define arduino interface
ser = serial.Serial('/dev/ttyACM0',9600)

# Define the alarm limit
ppm_limit = 3000.0

while True:
	try:
		
		read_serial=ser.readline()
		full_line = str(read_serial)
		logger.debug(full_line)
		parts = full_line.split(';')
		raw = parts[1]
		rzero = parts[2]
		ppm = parts[3]
		ppm_float = float(ppm)
		# Write to a file in DEV so you can easily configure your Raspberry Pi Monitor to read from it.
		file = open("/dev/airquality0", "w")
		file.write(ppm)
		file.close()
		if ppm_float < ppm_limit:
			logger.info("PPM: " + ppm)
		if ppm_float > ppm_limit:
			logger.info("Raw: " + raw + "; RZERO: " + rzero + "; PPM: " + ppm)

			title = 'ALERTA Concentracao de gases a : ' + ppm + ' ppm'
			msg_content = '<h2><font color="red">A concentracao de gases no ar esta em ' + ppm + ' ppm. Valores normais entre 0 a ' + str(ppm_limit) + '.</font></h2>\n'.format(title=title)
			message = MIMEText(msg_content, 'html')

			message['From'] = 'Sender Name <EXAMPLE_MAIL@gmail.com>'
			message['To'] = 'Receiver Name <EXAMPLE_MAIL_1@gmail.com>'
			message['Cc'] = 'Receiver2 Name <EXAMPLE_MAIL_2@gmail.com>'
			message['Subject'] = title
			
            # GMail server config
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.starttls()
			server.login('EXAMPLE_MAIL@gmail.com', 'PASSWORD')
			msg_full = message.as_string()
			server.sendmail('EXAMPLE_MAIL@gmail.com', ['EXAMPLE_MAIL_1@gmail.com', 'EXAMPLE_MAIL_2@gmail.com'], msg_full)
			server.quit()
	except:
		logger.error("Unexpected error:", sys.exc_info()[0])

