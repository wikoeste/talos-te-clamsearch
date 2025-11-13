import sys,re
from clam.common import settings,clamav
settings.init()

######
#MAIN
def main():
    shas,invalid    = ([],[])
    data            = ""
    print("===[TE] ClamAV Search Tool==="+settings.version+"===")
    print("Input a list of valid SHA256 file hashes,SampleID's,or SignatureIDs; "
          "type 'done' and press return.\n")
    while data != 'done':
        data = input()
        # validate the input is a sha256 value if true add to list  for analysis
        if re.findall(r"([A-Fa-f0-9]{64})", data) is not None:
            shas.append(data)
        # if the input is a sample id add to list for analysis
        elif re.findall(r"(\d{11})",data) is not None:
            shas.append(data)
        # if the input is a sig id add to list for analysis
        elif re.match(r"(.*|\d{7}|-\d{1})",data) is not None:
            shas.append(data)
        elif data == "quit" or data == "exit":
            sys.exit()
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
            clamav.searchvrt(s)
    else:
        print("The list of sha 256 entries is empty")
        print("SHAs: " +str(shas))
    # print list of sigs pending review
    #clamav.review()

# Run Main As Program
if __name__ == "__main__":
    main()