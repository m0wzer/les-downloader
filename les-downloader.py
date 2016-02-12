# Imports
import subprocess
import os
import urllib
import sys
import argparse

# Print GBanner
headerBanner = """[#] Linux Exploit Suggester Downloader
[#]"""
print headerBanner

# parse args
if not len(sys.argv) > 1:
    print "[#] Not enough arguments"
    print "[#] Exiting..."
    sys.exit()

argParser = argparse.ArgumentParser()
inputGroup = argParser.add_mutually_exclusive_group()
inputGroup.add_argument("-k", "--kernel", help="The kernel version to pass to Linux Exploit Suggestor")
inputGroup.add_argument("-p", "--pipe", help="Takes an input from stdin, to support piping from Linux Exploit Suggestor", action="store_true")
args = argParser.parse_args()


# Print GBanner
headerBanner = """[#] Linux Exploit Suggester Downloader
[#]"""

print headerBanner

# Parse Parameters - are we using stdin or calling LES?
if not args.pipe:
    kernel = args.kernel

    print "[#] Running Linux-Exploit-Suggester against kernel %s" % kernel
    print "[#] -----------------------------------------------------"

    lesProcess = subprocess.Popen('perl Linux-Exploit-Suggester.pl -k %s' % kernel, shell=True, stdout=subprocess.PIPE)
    inputData = lesProcess.stdout
else:
    kernel = None
    inputData = sys.stdin.readlines()
    for line in inputData:
        if "Kernel local:" in line:
            kernel = line.split()[-1]
    if kernel is None:
        print "[#] Unable to identify Kernel version from stdin"
        print "[#] Exiting..."
        sys.exit()
    print "[#] Parsing stdin for Kernel version: {}" . format(kernel)
    print "[#] -----------------------------------------------------"

# Dict to store off exploits + there names
exploitList = dict()

# Parse Results
iterableOutput = iter(inputData)
for line in iterableOutput:
    if "[+]" in line:
        #print line.strip().replace("[+]","")
        nextLine = next(iterableOutput)
        while "Source" not in nextLine:
            nextLine = next(iterableOutput)

        title = line.strip().replace("[+]","")
        url = nextLine.split()[1]
        exploitList[title] = url

numExploitsFound = len(exploitList)
if numExploitsFound is 0:
    print "[#] No exploits were found"
    print "[#] Exiting..."
    sys.exit()

if not os.path.exists(kernel):
    os.mkdir(kernel)

print "[#] Found a total of {} pottential exploits..." . format(numExploitsFound)

# Results parsed - lets iterate and download each one
for title, url in exploitList.iteritems():

    downloadUrl = ""
    # Is it on exploit-db?
    if "exploit-db.com" in url:
        # Some exploit-db URLs have a trailing slash, some do not...
        if url.endswith("/"):
            url = url[:-1]

        edbId = url.split("/")[-1]
        downloadUrl = "https://www.exploit-db.com/download/{}" . format(edbId)


    # Is it on Security Focus?
    # Some security focus URLs are simple - they point directly to the code, however some point to the info page :(
    # TODO: Fetch exploits from the info urls
    if "securityfocus.com" in url:
        downloadUrl = url

    # Is it on Packetstorm?

    if downloadUrl is "":
	print "[+] Error - Unrecocnised download URL for {} : {}" . format(title, url)
	continue
    # Lets download it!
    savePath = kernel + '/' + title.strip()

    try:
	 urllib.urlretrieve(downloadUrl, savePath)
  	 print "[+] Downloaded {}" . format(title)
    except:
	 print "[+] Error downloading {} at : {}" . format(title, downloadUrl)

    #subprocess.Popen('wget {} -O {}' . format(downloadUrl, savePath), shell=True, stdout=PIPE)
print "[#] Finished!"
