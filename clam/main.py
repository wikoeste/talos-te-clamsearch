from clam.common import settings,clamav
settings.init()
import re

######
#MAIN
def main():
    shas,invalid    = ([],[])
    data            = ""
    print("===[TE] ClamAV Search Tool==="+settings.version+"===")
    print("Input a list of valid SHA256 file hashes or a Sample ID; type done\n")
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
            clamav.searchvrt(s)
    else:
        print("The list of sha 256 entries is empty")
        print("SHAs: " +str(shas))
    # print list of sigs pending review
    #clamav.review()

# Run Main As Program
if __name__ == "__main__":
    main()