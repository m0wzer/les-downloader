# les-downloader
===================
Parses Linux Exploit Suggester output to auto-download suggested exploits.

les-downloader is a dirty python script written to automatically download suggested exploits from the great Linux Exploit Suggester. I find going through and downloading + renaming the results from LES quite repetitive and time consuming - so I wrote this script

The script is simple, takes one of two options which can be used to either pipe the stdout of Linux Exploit Suggester into the script, or have the script invoke Linux Exploit Suggester with a specified Kernel verison.

Identified exploits are downloaded + saved into a new directory named after the target Kernel verison.

Usage
==================
<pre>
python2 les-downloader.py -h
usage: les-downloader.py [-h] [-k KERNEL | -p]

optional arguments:
  -h, --help            show this help message and exit
  -k KERNEL, --kernel KERNEL
                        The kernel version to pass to Linux Exploit Suggestor
  -p, --pipe            Takes an input from stdin, to support piping from
                        Linux Exploit Suggestor
</pre>

Example: Invoke LES using -k flag
==================
<pre>
python2 les-downloader.py -k 2.4.5
[#] Linux Exploit Suggester Downloader
[#]
[#] Linux Exploit Suggester Downloader
[#]
[#] Running Linux-Exploit-Suggester against kernel 2.4.5
[#] -----------------------------------------------------
[#] Found a total of 3 pottential exploits...
[+] Downloaded  pipe.c_32bit
[+] Downloaded  sock_sendpage
[+] Downloaded  sock_sendpage2
[#] Finished!
</pre>

Example: Pipe from LES using -p flag
==================
<pre>
perl Linux-Exploit-Suggester.pl -k 3.0.0 | python2 les-downloader.py --pipe
[#] Linux Exploit Suggester Downloader
[#]
[#] Parsing stdin for Kernel version: 3.0.0
[#] -----------------------------------------------------
[#] Found a total of 4 pottential exploits...
[+] Downloaded  msr
[+] Downloaded  perf_swevent
[+] Downloaded  memodipper
[+] Downloaded  semtex
[#] Finished!
</pre>
