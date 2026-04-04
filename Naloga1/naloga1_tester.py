import naloga1

if __name__ == "__main__" :
    option = input("Kaj želiš testirati : (1 - encode, 2 - decode, 3 - efficiency)? : ")
    
    if option == "1" :
        for i in range (1,7) :
            inputPath = "primeri/"+str(i)+".txt"
            # DEBUG
            # print(inputPath)
            ####
            outPath = "TestniIzhodi/"+str(i)+"_mine_auto.json"
            outTestPath = "primeri/"+str(i)+".json"
            
            vhod = naloga1.read_raw_text(inputPath)
            izhod, izhodS = naloga1.encode(vhod)
            naloga1.write_coded_msg(outPath, izhod, izhodS)
            test_izhod, test_izhodS = naloga1.read_coded_msg(outTestPath)
                
            if izhod == test_izhod and izhodS == test_izhodS:
                print("Test ", i, "matches test case")
            else:
                print("Error - no match for case ", i)
                
                
    elif option == "2" :
        for i in range (1,7) : 
            inputPath = "primeri/"+str(i)+".json"
            outPath = "TestniIzhodi/"+str(i)+"_mine_auto.txt"
            outTestPath = "primeri/"+str(i)+".txt"
            
            vhod, vhodS = naloga1.read_coded_msg(inputPath)
            izhod = naloga1.decode(vhod,vhodS)
            naloga1.write_raw_text(outPath, izhod)
            test_izhod = naloga1.read_raw_text(outTestPath)
            
            if izhod == test_izhod :
                print("Test ", i, "matches test case")
            else:
                print("Error - no match for case ", i)
                
    elif option == "3" :
        for i in range (1,7) : 
            inputPath = "primeri/"+str(i)+".txt"
            
            vhod = naloga1.read_raw_text(inputPath)
            izhod , izhodS = naloga1.encode(vhod)
            
            print("Efficiency of case ",i, "is : ", naloga1.compute_efficiency(vhod,izhod))