from clam.common import settings
settings.init()
import requests,json,re
from terminaltables import AsciiTable

# Drop the clamav signature with new sigmgr
def dropsig(sid):
    print(f"\n\n===Drop a ClamAV SigID: {sid}===")
    reason   = 0
    cnt      = 1
    notes    = ""
    headers  = {'Content-type': 'application/json','X-APIKEY': settings.sigkey}
    options  = ["Reviewer rejected","Failed FP check","FP in field","Replaced","Other"]
    print("Select an Drop Reason")
    for o in options:
        print(str(cnt)+". "+o)
        cnt+=1
    print("N or n to Exit")
    print("==============")
    reason   = input("Option: ")
    if reason == "n" or reason == "N":
        pass
    else:
        notes      = input("\nEnter a comment on why this should be dropped: ")
        payload    = {"signature_id": sid, "reason": options[int(reason)-1], "message": notes}
        url        = settings.sigmgr+"/v1/signature/drop"
        response   = requests.post(url, headers=headers,json=payload,verify=False)
        if response.status_code == 200:
            rjson  = response.json()
            status = rjson["success"]
            if status == 0:
                status = "Fail"
            else:
                status = "Pass"
            #print(json.dumps(rjson, indent=2))
            print("===SigMgr Drop Status===")
            print("Status : "+ status)
            print(f"SigID: {sid}")
            msg = (rjson["message"])
            msg = re.sub(r" at.+","",msg)
            print(msg)
        else:
            error = [
                ["SIG Manager API Error"],
                ["HTTP ERROR: "+ str(response.status_code)]
            ]
            err = AsciiTable(error)
            print(err.table)
    '''
    # Try to get the FP list for review
    r = requests.get(settings.sigmgr+"/v1/signature/review/list",headers=headers,verify=False)
    if r.status_code == 200:
        rjson = r.json()
        print(json.dumps(rjson, indent=2))
    else:
        print("HTTP ERR {}".format(r.status_code))
        print(r.text)
    '''

# Search for ClamAV and Amp hits by SHA256 or SampleID (sid)
# this still uses search01.vrt.sourcefire
def searchvrt(sample):
    url      = settings.search01+"sample/"+sample
    response = requests.get(url, auth =(settings.uname,settings.vrt),verify=False)
    if response.status_code == 200:
        rjson = response.json()
        #print(json.dumps(rjson, indent=2))
        sid              = 0
        s256,ftype       = (None,None)
        fireamp,clam     = ([],[])
        amphits,clamhits = (None,None)
        # get AMP detection
        if len(rjson["fireamp_detection"]["current"]) == 0:
            amphits = "None"
        else:
            [fireamp.append(i) for i in rjson["fireamp_detection"]["current"]]
            amphits = "\n".join(i for i in fireamp)
        # get clam detection
        if len(rjson["clamav_detection"]["current"]) == 0:
            clamhits = "None"
        else:
            [clam.append(i) for i in rjson["clamav_detection"]["current"]]
            clamhits = "\n".join(i for i in clam)
        # get the sid
        if "sample_id" in json.dumps(rjson):
            sid = rjson["sample_id"]
        else:
            sid = "None"
        if "updated" in json.dumps(rjson):
            updated = rjson["updated"]
            updated = re.sub(r"T|Z","",updated)
        else:
            updated = "None"
        try:
            origin = rjson["origin"]
        except KeyError:
            origin = "None"
        try:
            s256 = rjson["SHA256"]
        except KeyError:
            s256 = "None"
        try:
            ftype = rjson["current_mimetype"]
        except KeyError:
            ftype = "Unknown"
        #Print the results from Search01
        #print(s256,sid,updated,clamhits,amphits,origin)

        data = [
            #["VRT Search01 Results"],
            ["S256: " + s256],
            ["SampleID: " + sid],
            ["Updated: " + updated],
            ["File Type: "+ ftype],
            ["AmpDections: " + amphits],
            ["ClamAV: " + clamhits],
            ["Origin: " + origin]
        ]
        res = AsciiTable(data, "VRT Search01 Results")
        print(res.table)
        clamid = re.sub(r"\D","",clamhits)
        clamid = re.sub(r"-0","",clamid)
        #print(clamid)
        #Drop the clam av sig found in the search
        dropsig(clamid)
    else:
        error = [["VRT Search01 API Error"],
            ["HTTP ERROR".format(response.status_code)]]
        err = AsciiTable(error)
        print(err.table)

##########
#MAIN
def main():
    shas,invalid    = ([],[])
    data            = ""
    print("===ClamAV Signature Search Tool==="+settings.version+"===")
    print("Input a list of valid SHA256 file hashes of SID:\n")
    while data != 'done':
        data = input()
        # validate the input is a sha256 value if true add to list  for analysis
        if re.findall(r"([A-Fa-f0-9]{64})", data) is not None:
            shas.append(data)
        # if the input is a sid add to list for analysis
        elif re.findall(r"(\d{11})",data) is not None:
            shas.append(data)
        else:
            invalid.append(data)
            print('Not a valid SHA256 Entry!')
            for i in invalid:
                print(i)
    print('\nSearching for matches......\n')
    # Remove the empty lines and the word done from list
    shas = list(filter(None, shas))
    shas.remove('done')
    # loop through shas for analysis
    if len(shas) > 0:
        for s in shas:
            searchvrt(s)
    else:
        print("The list of sha 256 entries is empty")
        print("SHAs: " +str(shas))

# Run Main As Program
if __name__ == "__main__":
    main()