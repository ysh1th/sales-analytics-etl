import subprocess

processes = [
    subprocess.Popen(["python", "-m", "data_producers.orders_producer"]),
    subprocess.Popen(["python", "-m", "data_producers.user_activity_producer"]),
    subprocess.Popen(["python", "-m", "data_producers.product_views_producer"]),
]

try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    for p in processes:
        p.terminate()