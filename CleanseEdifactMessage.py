import os
import sys
import re


#This function will cleanse the messages having special character
def cleanse_edifact_message(input_dir,file_name,outputDir):
    with open(os.path.join(input_dir,file_name),"rb") as sbr_file:
        pnr_list_success = list()
        pnr_set = set()
        pnr_rloc_dict = dict()
        pnr_rloc_list,message_list_tmp = list(),list()
        pnr_rloc_regex = 'RCI\x1d1A\x1f\w\w\w\w\w\w'
        #env_no_regex = '(?<=\x1c)RSI\x1dRP(.*?)(?=\x1c)'
        env_no_regex = 'PTD\x1d\d\d\d\d\d\d\x1d\d+(?=\x1c)'
        line_regex = 'UNB.IATB.*?UNH.1.SBRRES.*?1.UNZ.*?'
        for line in sbr_file:
            message_list = re.findall(line_regex,line)
            #print len(message_list)
            if (len(message_list) > 0):
                for message in message_list:
                    env_no = -1
                    pnr_rloc_regex_list = re.findall(pnr_rloc_regex,message)
                    env_no_regex_list = re.findall(env_no_regex,message)
                    if len(pnr_rloc_regex_list) >= 1 and len(env_no_regex_list) >= 1 :
                        pnr_rloc = pnr_rloc_regex_list[0].split("\x1f")[1]
                        #env_no = env_no_regex_list[0].split("\x1f")[1]
                        env_no = env_no_regex_list[0].split("\x1d")[-1]
                        #pnr_list_success.append((pnr_rloc,env_no,message))
                    elif(len(pnr_rloc_regex_list) >= 1 and len(env_no_regex_list) == 0):
                        pnr_rloc = pnr_rloc_regex_list[0].split("\x1f")[1]
                        #pnr_list_success.append((pnr_rloc,env_no,message))

                    pnr_rloc_list.append(pnr_rloc+","+env_no)
                    message_list_tmp.append(message)

                    if pnr_rloc in pnr_set:
                        prev_env, prev_message = pnr_rloc_dict.get(pnr_rloc)
                        if (int(prev_env) < int(env_no)):
                            pnr_rloc_dict[pnr_rloc] = (env_no,message)
                    else:
                        pnr_set.add(pnr_rloc)
                        pnr_rloc_dict[pnr_rloc] = (env_no,message)

    write_to_file(os.path.join(outputDir,file_name),pnr_rloc_list)
    write_to_file(os.path.join(outputDir,file_name+"_tmp"),message_list_tmp)

#Write to File
def write_to_file(file_name,data_set):
    with open(file_name,"w") as fs:
        for i in data_set:
            fs.write(str(i))
            fs.write("\n")


if __name__ == '__main__':
    if (len(sys.argv) > 2):
        inputDir = sys.argv[1]
        outputDir = sys.argv[2]

        #entity_name = str(sys.argv[4]).upper()
    else:
        inputDir = raw_input("Please provide the input directory path: ")
        outputDir = raw_input("Please provide the output directoy path: ")

    files = os.listdir(inputDir)
    print "Processing file: "+ str(files)
    for file in files:
        cleanse_edifact_message(inputDir,file,outputDir)