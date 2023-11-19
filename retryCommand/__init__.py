import subprocess
import sys
import argparse
import os
import rich
import time
import io

def ordinalInt(value:int):
        number=str(value)
        suffix="th"
        if (number.endswith("1")):
            suffix="st"
        elif (number.endswith("2")):
            suffix="nd"
        elif (number.endswith("3")):
            suffix="rd"
        return number+suffix

def retryCommand():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--no-stop-after-success',action='store_true',default=False,required=False,help="no stop after success")
    argparser.add_argument('-p', '--no-ignore-process-error',action='store_true',default=False,required=False,help="no stop after success")
    argparser.add_argument('-m', '--max-num-of-retry', required=False,default=-1,type=int,help="max number of retry")
    argparser.add_argument('-i', '--interval', required=False,default=1,type=int,help="interval to retry")
    argparser.add_argument('-t', '--time-out', required=False,default=-1,type=int,help="time out to kill process")
    argparser.add_argument('-d','--cwd', required=False,default=os.getcwd(),help="current working directory")
    argparser.add_argument('-n','--success-return-code', required=False,nargs="+",type=int,action="extend",default=[0],help="current working directory")
    argparser.add_argument('-q','--quiet',action='store_true',default=False,required=False,help="mute more output")
    argparser.add_argument('--mute',required=False,default=False,action="store_true",help="mute all output")
    argparser.add_argument('-o','--overwrite-stdin',nargs="*",action="extend",default=[],help="overwrite stdin")
    argparser.add_argument('-c', '--command',nargs=argparse.REMAINDER, required=True,help="command to execute")
    args=argparser.parse_args(sys.argv[1:]).__dict__
    
    if args['time_out']==-1:
        args['time_out']=None
    
    
    def output(*arg,**kw):
        if (not args['quiet'] and not args['mute']):
            rich.print(*arg,**kw)
    
    i=0
    
    stdout=io.BytesIO() if args['mute'] else None
    
    while args['max_num_of_retry']==-1 or i<args['max_num_retries']:
        i+=1
        output(f"[bold blue]the {ordinalInt(i)} attempt:[/bold blue]")
        try:
            popen=subprocess.Popen(args["command"],cwd=args["cwd"],stdout=stdout,stderr=stdout)
            print(stdout)
        except BaseException as e:
            output(f"[bold red]failed to execute command[/bold red]")
            output(f"[red]{e.__class__.__name__}:{e}[/red]")
            if args['no_ignore_process_error']:
                output("[bold blue]stop after error[/bold blue]")
                break
        else:
            try:
                popen.wait(args["time_out"])
            except subprocess.TimeoutExpired:
                output(f"[bold yellow]time out[/bold yellow]")
                popen.kill()
            output(f"[bold green]return code: {popen.returncode}[/bold green]")
            if popen.returncode in args['success_return_code']:
                if not args['no_stop_after_success']:
                    output("[bold blue]stop after success[/bold blue]")
                    break
        time.sleep(args["interval"])
        output("[blue]---------[/blue]")
    output("[bold blue]done[/bold blue]")
    
    
if __name__ == "__main__":
    retryCommand()