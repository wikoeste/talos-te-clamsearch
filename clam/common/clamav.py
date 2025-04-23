from clam.common import settings
settings.init()
import requests, json, re
from terminaltables import AsciiTable

# list of sigs pending review
'''
def review():
    headers  = {'Content-type': 'application/json','X-APIKEY': settings.sigkey}
    url       = settings.sigmgr + "/v1/signature/review/list"
    response  = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        rjson = response.json()
        print(json.dumps(rjson, indent=2))
    else:
        print(f"HTTP ERROR {response.status_code}")
'''

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
    print("================")
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
            error = [["SIG Manager API Error"],
                ["HTTP ERROR: "+ str(response.status_code)]]
            err = AsciiTable(error)
            print(err.table)

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
        data = [
            ["S256: " + s256],
            ["SampleID: " + sid],
            ["Updated: " + updated],
            ["File Type: "+ ftype],
            ["AmpDections: " + amphits],
            ["ClamAV: " + clamhits],
            ["Origin: " + origin]
        ]
        res     = AsciiTable(data, "VRT Search01 Results")
        print(res.table)
        clamid  = re.sub(r"-0|\D","",clamhits)
        # Drop the clam av sig found in the search
        dropsig(clamid)
    else:
        error = [["VRT Search01 API Error"],
            [f"HTTP ERROR - {response.status_code}"]]
        err = AsciiTable(error)
        print(err.table)