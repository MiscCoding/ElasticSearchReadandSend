# -*- coding: utf-8 -*-
import ctas
import sys
import schedule
import time


reload(sys)
sys.setdefaultencoding('utf-8')

# if __name__ == "__main__":
#     app.config.update(DEBUG=True)
#     app.run(host="0.0.0.0", threaded=True, port=80, debug=True)
#schedule.every().hour.do(ctas.ElasticSearchDataToCtasServerPeriodically)
#schedule.every(20).seconds.do(ctas.ElasticSearchDataToCtasServerPeriodically)
#schedule.every(20).seconds.do(ctas.logFileMover)
schedule.every().day.at("00:20").do(ctas.logFileMover)
schedule.every().hour.do(ctas.ElasticSearchDataToCtasServerPeriodically)

while True:
     schedule.run_pending()
     time.sleep(1)
#ctas.ElasticSearchDataToCtasServerPeriodically()


