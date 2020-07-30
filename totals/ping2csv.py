
import sys
from glob import iglob
from natsort import natsorted


def process(file_path):
    for f_name in natsorted(iglob(file_path)):
        with open("%s-.csv"%(f_name), "wb") as f_csv:
            with open(f_name, "rb") as fn:
                while True:
                    l_bytes = fn.readline()
                    if (not l_bytes):
                        break   
                    
                    if (l_bytes.startswith(b"[")):
                        pass
                    else:
                        continue
                    
                    list_tmp = l_bytes.split()
                    #print (b",".join(list_tmp))
                    f_csv.write(b",".join(list_tmp) + b"\n")
                       

def process_ping()
if __name__ == "__main__":
    
    f_path = "./"
    try:
        #print (len(sys.argv))
        #print (sys.argv[0])
        f_path = sys.argv[1]
        print (sys.argv)
    except Exception as e:
        print (e)
        print("usage :python3 %s time_start time_end [flag]"%(sys.argv[0]))
        #sys.exit(1)
    
    
    process("%s/*.txt"%(f_path))
    
    
                
    
    print ("end")