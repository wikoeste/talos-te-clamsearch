import getpass,os,re,requests
requests.packages.urllib3.disable_warnings()

# Global List
def init():
    global uname,vrt,search01,sigmgr,version

def getKey(keyname):     #take the search keyname and return the appropriate api key
    key       = None
    match     = ''
    freebsd   = "/home/{}".format(uname)+"/.profile"
    osx       = "/Users/{}".format(uname)+"/.profile"
    if os.path.exists(freebsd):         # if frebsd set the paths
        fname    = freebsd
    else:                              # else this is a mac osx
        fname    = osx
    # get api keys for any tool but sds
    with open(fname, 'r') as fp:
        lines = fp.read().splitlines()
        for l in lines:
            if l.startswith('#'):
                pass
            if keyname.upper() in l:
                match = l
    fp.close()
    key = re.sub(r'.*=','',match)   # remove key name and = sign
    key = re.sub(r'"','',key)       # remove the quotations from the key
    return key                      # return the api key


#Get user creds and API Keys at start
uname        = getpass.getuser()
print("Talos Login for Script Use ONLY!")
print("===============================\n")
vrt          = getpass.getpass('VRT Password:')
search01     = "https://search01.vrt.sourcefire.com/"
sigmgr       = "https://sigmanager.talos.cisco.com/"
sigkey       = getKey("sigmgr")
version      = "0.3"