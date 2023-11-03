import subprocess
import sys
import argparse
import os
import rich
import time

def retryCommand():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--no-stop-after-success',action='store_true',default=False,required=False,help="no stop after success")
    argparser.add_argument('-p', '--no-ignore-process-error',action='store_true',default=False,required=False,help="no stop after success")
    argparser.add_argument('-m', '--max-num-of-retry', required=False,default=-1,type=int,help="max number of retry")
    argparser.add_argument('-i', '--interval', required=False,default=1,type=int,help="interval to retry")
    argparser.add_argument('-t', '--time-out', required=False,default=-1,type=int,help="time out to kill process")
    argparser.add_argument('-d','--cwd', required=False,default=os.getcwd(),help="current working directory")
    argparser.add_argument('-n','--success-return-code', required=False,nargs="+",type=int,action="extend",default=[0],help="current working directory")
    argparser.add_argument('-c', '--command',nargs=argparse.REMAINDER, required=True,help="command to execute")
    args=argparser.parse_args(sys.argv[1:]).__dict__
    
    if args['time_out']==-1:
        args['time_out']=None
    
    i=0
    while args['max_num_of_retry']==-1 or i<args['max_num_retries']:
        i+=1
        rich.print(f"[bold blue]try {i} time:[/bold blue]")
        try:
            popen=subprocess.Popen(args["command"],cwd=args["cwd"])
        except BaseException as e:
            rich.print(f"[bold red]failed to execute command[/bold red]")
            rich.print(f"[red]{e.__class__.__name__}:{e}[/red]")
            if args['no_ignore_process_error']:
                rich.print("[bold blue]stop after error[/bold blue]")
                break
        else:
            try:
                popen.wait(args["time_out"])
            except subprocess.TimeoutExpired:
                rich.print(f"[bold yellow]time out[/bold yellow]")
                popen.kill()
            rich.print(f"[bold green]return code: {popen.returncode}[/bold green]")
            if popen.returncode in args['success_return_code']:
                if not args['no_stop_after_success']:
                    rich.print("[bold blue]stop after success[/bold blue]")
                    break
        time.sleep(args["interval"])
        rich.print("[blue]---------[/blue]")
    rich.print("[bold blue]done[/bold blue]")
    
    
if __name__ == "__main__":
    retryCommand()