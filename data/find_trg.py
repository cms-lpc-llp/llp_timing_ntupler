import os

year = 2018 
input_list = "trigger_names_llp_v2.dat" 
output_list = "trigger_names_llp_v3.dat" 
trg_list = "trgs." + str(year)

print(trg_list)
line_num = os.popen("cat "+output_list+" | wc -l").read().replace("\n","")
print(line_num)

with open(output_list, 'a') as fout:
	with open(trg_list, 'r') as fin:
		#print(sum(1 for num in fin))
		#print(os.popen("cat trgs.2018 | wc -l").read().replace("\n",""))
		#print(os.popen("cat "+trg_list+" | wc -l").read().replace("\n",""))
		for line in fin:
			string = line.replace("\n","")[line.find("HLT"):line.find("_v")]
			with open(input_list, 'r') as fset:
				if string in fset.read():
					print(line.replace("\n","")[0:line.find("HLT")-4], "already in.")	
				else:
					print("ADD ", string)
					fout.write(str(line_num)+"  "+string+"\n")
					line_num = int(line_num) +1
	fset.close()
	fin.close()
	fout.close()
