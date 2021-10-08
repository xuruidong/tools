
import sys
import os
from glob import iglob
from natsort import natsorted

# unit: ms
g_cfg_ac_tim = 0
g_cfg_ac_tim_dict = {
    1: 40,
    2: 20,
    4: 10,
    7: 10
}

def process(file_path):
    for k in g_cfg_ac_tim_dict:
        print (k)
    
    for f_name in natsorted(iglob(file_path)):
        omit_out_of_order = 0
        out_of_order = 0
        with open(f_name, "rb") as fn:
            print ("==== %s ==== "%os.path.basename(f_name))
            delta = g_cfg_ac_tim * int(os.path.basename(f_name).split("m")[0])/8
            while True:
                l_bytes = fn.readline()
                if (not l_bytes):
                    break 
                
                if (l_bytes.startswith(b"iperf3: OUT OF ORDER")):
                    list_tmp = l_bytes.split(b" ")
                    # print (f"{list_tmp[8]}\t{list_tmp[13]}")
                    if(int(list_tmp[13]) - int(list_tmp[8]) > delta):
                        # print (l_bytes)
                        print (".", end="")
                        pass
                    else:
                        omit_out_of_order += 1
                    continue
                
                if(l_bytes.startswith(b"[SUM]")):
                    list_tmp = l_bytes.split(b" ")
                    # print (f"ofo {list_tmp[5]}")
                    out_of_order = int(list_tmp[5])
                    continue
                    
                if (l_bytes.startswith(b"[ ")):
                    list_tmp = l_bytes.split(b"]")
                    list_tmp2 = list_tmp[1].split(b" sec") 
                    # Interval
                    list_tmp3 = list_tmp2[0].strip().split(b"-")
                    if(len(list_tmp3) < 2):
                        # print (list_tmp2)
                        continue
                    if (float(list_tmp3[1]) - float(list_tmp3[0]) < 2):
                        # print (list_tmp2)
                        continue
                    
                    #Jitter
                    try:
                        list_tmp6 = list_tmp2[1].split(b"ms")
                        # content_list.append(list_tmp6[0].strip())

                        #lost
                        list_tmp7 = list_tmp6[1].split(b"/")
                        lost = int(list_tmp7[0])
                        total = int(list_tmp7[1].split(b" ")[0])
                        
                    except Exception as e:
                        print ("===%s"%e) 
                        print (list_tmp3)
            
            print("")
            if(lost < omit_out_of_order):
                print ("Warning: lost < omit_out_of_order")            
            # print(f"total:{total}, lost:{lost}, ofo:{out_of_order}, omitted_ofo:{omit_out_of_order}")
            print("total:%s, lost:%s, ofo:%s, omitted_ofo:%s"%(total, lost, out_of_order, omit_out_of_order))
            if(lost < omit_out_of_order):
                # print ("Warning: lost < omit_out_of_order")
                print ("lost:0.00%")
            else:
                print ("lost:%.3f%%"%(100*(lost-omit_out_of_order)/total))
            print ("ofo:%.3f%%"%(100*out_of_order/total))
            

if __name__ == "__main__":

    f_path = "./"
    try:
        #print (len(sys.argv))
        #print (sys.argv[0])
        f_path = sys.argv[1]
        #print (sys.argv)
    except IndexError:
        print ("use default path: ./testdata")
        f_path = "./testdata"
    except Exception as e:
        print (e)
        print("usage :python3 %s path [flag]"%(sys.argv[0]))
        e_type, e_value, tb_obj = sys.exc_info()
        print(e_type, e_value, tb_obj)        
        sys.exit(1)


    process("%s/*.txt"%(f_path))




    print ("end")