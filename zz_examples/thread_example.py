import threading

def worker():
    """
    :return: funcion qhe realiza el trabaj en el thread
    """
    print("Estoy trabajando ahora mismo")
    return

threads = list()

for i in range(3):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
