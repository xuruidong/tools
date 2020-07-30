
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

                    if (b"connected with" in l_bytes):
                        continue

                    if (b"Interval" in l_bytes):
                        continue

                    if (b"datagrams received out-of-order" in l_bytes):
                        continue


                    content_list = []
                    list_tmp = l_bytes.split(b"]")
                    list_tmp2 = list_tmp[1].split(b" sec")
                    #Interval
                    content_list.append(list_tmp2[0])
                    #speed
                    list_tmp3 = list_tmp2[1].split(b"its/sec")
                    list_tmp4 = list_tmp3[0].split(b"Bytes")
                    list_tmp5 = list_tmp4[1].split()

                    if (list_tmp5[1] == b"b"):
                        content_list.append(b"0.00")
                    elif (list_tmp5[1] == b"Kb"):
                        content_list.append(list_tmp5[0])
                    elif(list_tmp5[1] == b"Mb"):
                        v = float(list_tmp5[0]) *1024
                        content_list.append(str(v).encode())
                    else:
                        print ("error: speed uint")
                        return -1

                    #Jitter
                    try:
                        list_tmp6 = list_tmp3[1].split(b"ms")
                        content_list.append(list_tmp6[0].strip())

                        #lost
                        list_tmp7 = list_tmp6[1].split(b"/")
                        bytes_v = list_tmp7[1].split(b"(")[1].split(b")")[0]
                        if (b"e" in bytes_v):
                            v = eval(bytes_v.strip(b"%"))
                            content_list.append((str(v)+"%").encode())
                        else:
                            content_list.append (list_tmp7[1].split(b"(")[1].split(b")")[0])
                    except:
                        pass    
                    #list_tmp = l_bytes.split()
                    #print (b",".join(list_tmp))
                    f_csv.write(b",".join(content_list) + b"\n")


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