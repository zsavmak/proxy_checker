import os
import concurrent.futures
from proxy_checking import ProxyChecker
import json
import time
from rich.progress import Progress
from rich.progress import BarColumn, TaskProgressColumn,TimeElapsedColumn 

checking = []

NUM_TASKS = 89*100

def check_proxy(proxy):
    time.sleep(0.001) 
    checker = ProxyChecker()
    r = checker.check_proxy(proxy)
    r["address"] = proxy[:-1]
    return r

def main():
    global checking
    with Progress(BarColumn(), TaskProgressColumn( ),
                  TimeElapsedColumn() ) as progress:
        task = progress.add_task("[green]Checking...", total=NUM_TASKS)
        for i in range(1, 90):
            with open(os.path.join("proxies", str(i)+ ".txt")) as f:
                executor = concurrent.futures.ProcessPoolExecutor(248)
                futures = [executor.submit(check_proxy, line) for line in f]              
                for _ in concurrent.futures.as_completed(futures):
                    try:
                        checking.append(_.result())
                        progress.update(task, advance=1)
                    except Exception as e:
                        print(str(e))
                        continue
    with open("results.json", 'w') as output_file:
	    json.dump(checking, output_file, indent=2)

main()
