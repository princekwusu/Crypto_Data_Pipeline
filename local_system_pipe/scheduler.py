import schedule
import time
import subprocess

def run_script():
    # Replace 'python_script.py' with the path to your Python script
    subprocess.run(["python", "D:\ppp\Crypto_Data_Pipeline\local_system_pipe\orchestrator.py"])

# Schedule the task to run at 3:30 PM every day
schedule.every().day.at("1:00").do(run_script)

while True:
    schedule.run_pending()
    time.sleep(5)
    