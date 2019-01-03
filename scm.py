#from _pytest.python import NoneType
#from _pytest.python import NoneType
__author__ = 'S.Gayathri'

import sys, getopt
import xml.etree.ElementTree as ET
import random
import os
import os.path
import copy
from copy import deepcopy
import subprocess
from subprocess import call
import re
import shutil


# nameoffile= 'timed-gate.xml'
# tree = ET.parse(nameoffile)
# root = tree.getroot()

# FileNeme = nameoffile[:-4]


# current path
currpath= os.getcwd()
print("now ",currpath)
# with open('myverify.txt', 'a') as file:
#     file.write('verifyta -t0 -f tracefile')
# print Address_Invalid_Mut, Address_Valid_Mut



def main(argv):
    inputfile = ''
    templatename = ''
    queryfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:t:q:",["ifile=","tfile=","qfile="])
    except getopt.GetoptError:
        print('Mut_opt.py -i <inputfile> -t <templatename> -q <queryfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('mut_opt.py -i <inputfile> -t <templatename> -q <queryfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-t","--tfile"):
            templatename = arg
        elif opt in ("-q", "--qfile"):
            queryfile = arg
    print('Input file is "', inputfile)
    print('template is "',templatename)
    #print('Query file is "', queryfile)
#   flag = False
#     while(flag is False):
#         stage = input("Which stage LIT to mutate? Specify 1,2,3.. ")
#         if (stage in range(1,6)):
#             flag = True
#         else:
#             print"Specify LIT to mutate in range 1 to 5"
#         
#     print "LIT to mutate is LIT"+str( stage)+ "01"
#     type(stage)
        
        
    mut_list = ['ASD','ALD','ARD','STZ','STO','STS','BSL','BSR']
    #mut_list = ['STO']
    
    global Address_Invalid_Mut, Address_Valid_Mut
    Address_Valid_Mut= '/Mutants_'+inputfile[:-4]+'_Valid/'
    Address_Invalid_Mut = '/Mutants_'+inputfile[:-4]+'_INValid/'
    # MakeTree (inputfile)
    global tree, root
    tree= ET.parse(inputfile)
    root= tree.getroot()
    #print 'my test', [t.find(templatename) for t in root.findall(".//name")]
    #print 'hello'
    #print(root.tag, 'hello', inputfile[:-4])
    #NewDir (inputfile[:-4]) 
    
    #"Level_T"+str(stage)+" = Level_T"+str(stage)+" + "+ str_to_append
    
    #LIT_state = [1,3,4]
    flag_temp = 0
    state_var = ''
    state_var_list = get_state_var(inputfile[:-4],templatename)
    for item in state_var_list:
        if True:
            print str(item)
            if "Level_" in str(item):
                flag_temp = 1
                state_var = str(item)
                toks = state_var.split('=')
                state_var = toks[0]
            if "F_" in str(item):
                if flag_temp != 1:
                    flag_temp = 2
                    state_var = str(item)
                    toks = state_var.split('=')
                    state_var = toks[0]
            if "AIT" in str(item):
                print('AIT in state variable: printing')
                print flag_temp
                if flag_temp != 1 and flag_temp != 2:
                    flag_temp = 3
                    state_var = str(item)
                    toks = state_var.split('=')
                    state_var = toks[0]
                    print state_var
                    print toks
                    break
            if "DPIT" in str(item) :
                if flag_temp == 0:
                    flag_temp = 4
                    state_var = str(item)
                    toks = state_var.split('=')
                    state_var = toks[0]
    print state_var
    print('entering state var assignment')
    if 'Level_' in state_var:
        delta_list_add = [100,1200,1,50, 150, 200, 500, -50, -400, -10 ]
        delta_list_set = [1,1000, 500, 800, 350, 200, 950]
    elif 'FIT_' in state_var:
        delta_list_add = [0.5,2,5,1,-2]
        delta_list_set = [0.5,2,5]
    
    elif 'AIT_' in state_var:
        print('AIT in state variable')
        delta_list_add = [0.5,2,1.5,-1,-2]
        delta_list_set = [5,6.2,7.5,8]
    else:
        delta_list_add = [0.5,2,5,1,2]
        delta_list_set = [0.5,2,5]
            
    if flag_temp != 0:  
        state_mut_count = 0
        
        for mut_type in mut_list :
            if mut_type in ['ASD', 'ALD', 'ARD']:
                if mut_type is 'ASD' :
                    val = str(delta_list_add[0])
                    if mut_type is 'ALD':
                        val = str(delta_list_add[1])
                        if mut_type is 'ARD':
                            for i in range(len(delta_list_add)-4):
                                val = str(delta_list_add[i+4])
                                str_to_append = str(state_var) + " = "+str(state_var) +  " + ( " + val +")"
                                MUT(inputfile[:-4], templatename, mut_type, str_to_append, state_mut_count, state_var)
                                state_mut_count = state_mut_count + 1
                                
                            val = str(random.randint(delta_list_add[2], delta_list_add[3]))
                str_to_append = str(state_var) + " = "+str(state_var) +  " + ( " + val +")" 
            if mut_type in ['STZ', 'STO', 'STS']:
                if mut_type is 'STZ':
                    val = str(0)
                if mut_type is 'STO':
                    val = str(1)
                if mut_type is 'STS':
                    for i in range(len(delta_list_set)-2):
                        val = str(delta_list_set[i+2])
                        str_to_append = str(state_var) + " = " +  " + ( " + val +")"
                        MUT(inputfile[:-4], templatename, mut_type, str_to_append, state_mut_count, state_var)
                        state_mut_count = state_mut_count + 1
                    val = str(round(random.uniform(delta_list_set[0], delta_list_set[1]), 2))
                    #val = str(random.randint(delta_list_set[0], delta_list_set[1]))
                str_to_append =  str(state_var) + " = " + val
            if mut_type is 'BSL':
                str_to_append =  str(state_var) +  " = " +  str(state_var) +  " * 2 " 
            if mut_type is 'BSR':
                str_to_append =  str(state_var) +  " = " +  str(state_var) +   " /2 " 
            print ('str_to_Append: ', str_to_append)
            MUT(inputfile[:-4], templatename, mut_type, str_to_append, state_mut_count, state_var)
            state_mut_count = state_mut_count + 1
    
    print('Mut_command::::::')
    MUT_command(inputfile[:-4], templatename)
    print('Mut_state_mv::::::') 
    MUT_state_mv(inputfile[:-4], templatename) 
    print('Mut_state_pump::::::')   
    MUT_state_pump(inputfile[:-4], templatename)
    print('Mut_Change target::::::') 
    CT(inputfile[:-4], templatename)
    print('Mut_change Source::::::') 
    CS(inputfile[:-4], templatename)    
    #print('Mut_SL::::::') 
    #SL(inputfile[:-4], templatename)
    print('Mut_CI::::::') 
    C_I(inputfile[:-4], templatename)
    
    print('Mut_Change Guard::::::') 
    CG(inputfile[:-4], templatename)
    
def NewDir(i):
    print('in NewDir')
    if not os.path.exists('Mutants_'+i+'_Valid'):
        os.makedirs('Mutants_'+i+'_Valid')

    if not os.path.exists('Mutants_'+i+'_INvalid'):
        os.makedirs('Mutants_'+i+'_INvalid')

def Change_dir(MyMy,answer):
    dist_inv = str(os.getcwd())+Address_Invalid_Mut+str(MyMy)
    dist_val = str(os.getcwd())+Address_Valid_Mut+str(MyMy)
    src=str(os.getcwd())+'\\'+str(MyMy)
    if answer=='yes':
        shutil.move(MyMy,dist_val)
        print('moved to valid folder')
    if answer=='no':
        shutil.move(MyMy,dist_inv)
        print('moved to invalid folder')





def CheckQueryMut(reachability, MyName):
    try:
        if reachability: # if reachability variable is true, then check reachability and deadlockfreeness,

            #print 'The name of the model: ', MyName
            output = subprocess.check_output('verifyta -t0 -f mytrace '+MyName+' query1.q', shell=False)
            #print 'output is ',output
            result_sat = re.search(r'\bProperty is satisfied',str(output))
            #result_not_sat = re.search(r'\bProperty is NOT satisfied.',str(output))
            output2 = subprocess.check_output('verifyta -t0 -f mytrace '+MyName+' query2.q', shell=False)

            result_sat2 = re.search(r'\bProperty is satisfied', str(output2))
            #result_not_sat2 = re.search(r'\bProperty is NOT satisfied.', str(output2))
            #print 'result of regex:', result_sat, result_not_sat
            if result_sat2!= None and result_sat != None:
                return True
            else:
                return False
        else: # otherwise we only check the deadlockfreeness
            output = subprocess.check_output('verifyta -t0 -f mytrace ' + MyName + ' query1.q', shell=False)
            # print 'output is ',output
            result_sat = re.search(r'\bProperty is satisfied', str(output))

            if result_sat!=None :
                return True
            else:
                return False

    except subprocess.CalledProcessError:
        # print 'here is an error'
        return False



def CG(inp,tem):
    for t in root.findall('template'):
        r = [loc.find("label[@kind='guard']") for loc in t.findall('transition')]
        #print r
        h=0
        for loc in t.findall('transition'):
            x=loc.find("label[@kind='guard']")
            if x!= None: h+=1
        #print 'number of inv:',h
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(h):
                for k in range(len(r)):
                    strin = 'transition['+str(k)+']'
                    MyName= inp+ 'MUT_CG_'+str(k)+'_'+str(h)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        #print 'inside temp', t.find('name').text
                        #print ('t.find(name).text: ',t.find('name').text)
                        if t.find('name').text==tem:
                            #print strin
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            x=tra.find("label[@kind='guard']")
                            #print 'x is',x
                            if x != None:
                                if 'clk' in x.text:
                                #print 'and text is ', x.text
                                    x.text=x.text+'-1'
                                    treex.write(MyName)
                                    print('Change Guard: ',MyName, ' Updated text: ', x.text)
                                #print 'created'
                                else:
                                    print('clk not in guard.')
                                    os.remove(MyName)
                            else:
                                os.remove(MyName)

   
                                
def C_I(inp,tem):               
    #print 'here i am'
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        h=0
        for loc in t.findall('location'):
            x=loc.find("label[@kind='invariant']")
            if x!= None: h+=1
        #print 'number of inv:',h
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(h):
                for k in range(len(r)):
                    strin = 'location['+str(k)+']'
                    MyName= inp+ 'MUT_CI_'+str(k)+'_'+str(h)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        ##print 'inside temp', t.find('name').text
                        #print ('t.find(name).text: ',t.find('name').text)
                        if t.find('name').text==tem:
                            #print strin
                            strin = 'location['+str(k)+']'
                            tra = t.find(strin)
                            x=tra.find("label[@kind='invariant']")
                            #print 'x is',x
                            if x != None:
                                if 'clk' in x.text:
                                #print 'and text is ', x.text
                                    x.text=x.text+'+1'
                                    treex.write(MyName)
                                    print('Change Invariant: ',MyName, ' Updated text: ', x.text)
                                #print 'created'
                                else:
                                    'clk not in invariant'
                                    os.remove(MyName)
                                
                            else:
                                os.remove(MyName)



def MUT_state_mv(inp,tem):
    print 'mutate command status Motorised valve'
    
    t = root.find(".//template[name='" + str(tem) + "']"); 
    listoflocations = [loc.attrib['id'] for loc in t.findall('location')]; #print(listoflocations); 
    #print listoflocations
    listoftrans = [loc.find("label[@kind='assignment']") for loc in t.findall('transition')]
    #print 'listofTemp'
    #print type(listoftrans)
    #print listoftransitions
    for temp in listoftrans:
        if temp != None:
            listoftransitions = temp.text
            #print listoftransitions
    #print listoftransitions   
    
    
    is_mutated = False    
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        #print 'transitions:',  r2
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    if(is_mutated == True):
                        continue
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_state_mv'+str(k)+'.xml'
                    #print "new file :"+ str(MyName)
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        
                        #print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            
                            strin = 'transition['+str(k)+']'
                            #print strin
                            #print "k:"+ str(k)
                            tra = t.find(strin)
                            assignment =  tra.find("label[@kind='assignment']")
                            #print 'the assign is:', assignment.text
                            #print "range:" +str(range(len(r2)))
                            try:
                                temp_var = assignment.text
                            except:
                                continue
                            while (k  <= len(r2)) & ("MV" not in assignment.text):
                                #print "in while: k & assignment.text:"
                                #print str(k)+ "& "+ str(assignment.text)
                                k = k+1
                                #strin = 'transition['+str(k)+']'
                                #print strin
                                #print "k:"+ str(k)
                                tra = t.find(strin)
                                #print tra
                                if tra == None:
                                    continue
                                assignment =  tra.find("label[@kind='assignment']")
                                try:
                                    temp_var = assignment.text
                                except:
                                    print ('exception')
                                    continue
                                #print 'the assign is:', assignment.text
                            
                            #print assignment.index('kind')
                            #print 'the final assign is:', assignment.text
                            if assignment:
                                assi_split =  assignment.text.split(",")
                                mut_text = ''
                                for index in range(len(assi_split)) :
                                    if "MV" not in assi_split[index]:
                                        continue
                                    else:
                                        is_mutated = True
                                        mut_text= assi_split[index]  
                                        pos= mut_text.find('=')      
                                        if 'CLOSE' in assi_split[index]:
                                            mut_text=mut_text[:pos]+"= OPEN"
                                        else:
                                            mut_text=mut_text[:pos]+"= CLOSE"                             
                                        
                                        #print mut_text
                                        #print  "$$$$$$$$$$$$$$$$$$ MUTATION DONE $$$$$$$$$$$$$$$$$$$"
                                        assi_split[index] = mut_text
                                assignment.text = ','.join(map(str, assi_split))
                                #assignment.text += ', \ntrap=true'
                                print ('new assign: ', tra.find("label[@kind='assignment']").text, 'MUT_state_mv: ',MyName)
                                #print 'in ',MyName,' is mutating with new target and new source :'
                                #print '----------------------------------------'
                                #print 'isMutated ='+str(is_mutated)
                                treex.write(MyName)
                                if(is_mutated != True):
                                    print "to del file:" +str(MyName)
                                    os.remove(MyName)  
def MUT_state_pump(inp,tem):
    print 'mutate command status Pump'
    
    t = root.find(".//template[name='" + str(tem) + "']"); 
    listoflocations = [loc.attrib['id'] for loc in t.findall('location')]; print(listoflocations); 
    #print listoflocations
    listoftrans = [loc.find("label[@kind='assignment']") for loc in t.findall('transition')]
    #print 'listofTemp'
    #print type(listoftrans)
    #print listoftransitions
    for temp in listoftrans:
        if temp != None:
            listoftransitions = temp.text
            #print listoftransitions
    #print listoftransitions   
    
    
    is_mutated = False    
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        #print 'transitions:',  r2
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    if(is_mutated == True):
                        continue
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_state_pump_'+str(k)+'.xml'
                    #print "new file :"+ str(MyName)
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        
                        #print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            
                            strin = 'transition['+str(k)+']'
                            #print strin
                            #print "k:"+ str(k)
                            tra = t.find(strin)
                            assignment =  tra.find("label[@kind='assignment']")
                            #print 'the assign is:', assignment.text
                            #print "range:" +str(range(len(r2)))
                            temp_var = ''
                            try:
                                temp_var = assignment.text
                            except:
                                print ('exception')
                                continue
                            while (k  <= len(r2)) & ("P" not in temp_var):
                                #print "in while: k & assignment.text:"
                                #print str(k)+ "& "+ str(temp_var)
                                k = k+1
                                strin = 'transition['+str(k)+']'
                                #print strin
                                #print "k:"+ str(k)
                                tra = t.find(strin)
                                #print tra
                                if tra == None:
                                    continue
                                assignment =  tra.find("label[@kind='assignment']")
                                try:
                                    temp_var = assignment.text
                                except:
                                    print ('exception')
                                    continue
                                #print 'the assign is:', assignment.text
                            
                            #print assignment.index('kind')
                            #print 'the final assign is:', assignment.text
                            if assignment:
                                assi_split =  assignment.text.split(",")
                                mut_text = ''
                                for index in range(len(assi_split)) :
                                    if "P" not in assi_split[index]:
                                        continue
                                    else:
                                        is_mutated = True
                                        mut_text= assi_split[index]  
                                        pos= mut_text.find('=')      
                                        if 'ON' in assi_split[index]:
                                            mut_text=mut_text[:pos]+"= OFF"
                                        else:
                                            mut_text=mut_text[:pos]+"= ON"                             
                                        
                                        #print mut_text
                                        #print  "$$$$$$$$$$$$$$$$$$ MUTATION DONE $$$$$$$$$$$$$$$$$$$"
                                        assi_split[index] = mut_text
                                assignment.text = ','.join(map(str, assi_split))
                                #assignment.text += ', \ntrap=true'
                                print ('new assign: ', tra.find("label[@kind='assignment']").text, ' Mutating Pump: ',MyName)
                                #print 'in ',MyName,' is mutating with new target and new source :'
                                #print '----------------------------------------'
                                #print 'isMutated ='+str(is_mutated)
                                treex.write(MyName)
                                if(is_mutated != True):
                                    print "to del file:" +str(MyName)
                                    os.remove(MyName)  
def MUT_command(inp, tem):
    print "Command Mutation"
    t = root.find(".//template[name='" + str(tem) + "']"); 
    #print tem
    #print 't:' 
    #print t
    listoflocations = [loc.attrib['id'] for loc in t.findall('location')]; print(listoflocations);
    
    print listoflocations 
    print t.findall('transition')
    for loc in t.findall('transition'):
        pass
        #print 'assign attri: '
        #print str(loc.find("label[@kind='assignment']"))
    #print listoflocations
    listofsyncTemp = [loc.find("label[@kind='synchronisation']") for loc in t.findall('transition')]
    #print 'listofTemp'
    #print type(listofsyncTemp)
    #print listoftransitions
    for temp in listofsyncTemp:
        if temp != None:
            listofsync = temp.text
            #print listofsync
    
    
    is_mutated = False    
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        #print 'transitions:',  r2
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
#                     if(is_mutated == True):
#                         continue
                    is_mutated = False
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_CMD'+str(k)+'.xml'
                    #print "new file :"+ str(MyName)
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        
                        #print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            
                            strin = 'transition['+str(k)+']'
                            #print strin
                            #print "k:"+ str(k)
                            tra = t.find(strin)
                            sync =  tra.find("label[@kind='synchronisation']")
                            if sync == None:
                                continue
                            #print 'the assign is:', sync.text
                            while ("MV" not in sync.text) & ("P" not in sync.text) & (k  <= range(len(r2))):
                                k = k+1
                                strin = 'transition['+str(k)+']'
                                #print strin
                                #print "k:"+ str(k)
                                tra = t.find(strin)
                                sync =  tra.find("label[@kind='synchronisation']")
                                #print 'the assign is:', sync.text
                            
                            #print assignment.index('kind')
                            #print 'the final assign is:', sync.text
                            if sync == None:
                                continue
                            else:
                                mut_text = ''
                                if "MV" in sync.text:
                                    strin = sync.text
                                    if "OPEN" in sync.text:
                                        mut_text = strin[:6]+'CLOSE'
                                    else:
                                        mut_text = strin[:6]+'OPEN'
                                elif "P" in sync.text:
                                    strin = sync.text
                                    if "ON" in sync.text:
                                        mut_text = strin[:5]+'OFF'
                                    else:
                                        mut_text = strin[:5]+'ON'
                                is_mutated = True                                    
                                #print mut_text
                                #print  "$$$$$$$$$$$$$$$$$$ MUTATION DONE $$$$$$$$$$$$$$$$$$$"
                                
                                sync.text = mut_text+'!'
                                #assignment.text += ', \ntrap=true'
                                print ('new sync: ', tra.find("label[@kind='synchronisation']").text,' Mutating command: ',MyName )
                                #print 'in ',MyName,' is mutating with new target and new source :'
                                #print '----------------------------------------'
                                #print 'isMutated ='+str(is_mutated)
                                treex.write(MyName)
                                if(is_mutated != True):
                                    print "to del file:" +str(MyName)
                                    os.remove(MyName)  
    
    
    
    
def get_state_var(inp,tem):
    t = root.find(".//template[name='" + str(tem) + "']"); 
    listoflocations = [loc.attrib['id'] for loc in t.findall('location')]; #print(listoflocations); 
    listoftrans = [loc.find("label[@kind='assignment']") for loc in t.findall('transition')]
    #print 'listofTemp'
    #print type(listoftrans)
    #print listoftransitions
    for temp in listoftrans:
        if temp != None:
            listoftransitions = temp.text
            #print listoftransitions
    
    state_var_list = list()
    
    is_mutated = False    
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        #print r2
        #print len(r2)
        #return
        
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_'+'.xml'
                    print "new file :"+ str(MyName)
                    tree.write(MyName)
                    treex = ET.parse(MyName)

                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        if t.find('name').text==tem:
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            #print strin
                            #print tra
                            assignment =  tra.find("label[@kind='assignment']")
                            #print('assign.text',assignment.text)
                            
                            if assignment is None:
                                continue
                            
                            temp_var = assignment.text
                                #print ('temp_var', temp_var)
                            tok = temp_var.split(",")
                                
                            
                            assign_split = tok
                            print(assign_split)
                            for iter in range(len(assign_split)):
                                
                                flag = False
                                assign_split[iter]= assign_split[iter].replace("\n","")
                                print ('assign_split[iter]',assign_split[iter])
                                if 'Level_' in assign_split[iter]:
                                    flag = True
                                elif 'F_' in assign_split[iter]:
                                    flag = True
                                elif 'AIT' in assign_split[iter]:
                                    flag = True
                                elif 'DPIT' in assign_split[iter]:
                                    flag = True
                                            
                                if flag is True:
                                    if assign_split[iter] not in state_var_list:
                                        state_var_list.append(assign_split[iter])
                try:
                    os.remove(MyName)
                except:
                    pass 
    print ('state_Var_list: ',state_var_list)        
    return state_var_list                                    
                            
                            
        


#State mutation (Bias)
def MUT(inp, tem, m_type,str_to_append, state_mut_count, state_var):
    print m_type
    print tem
    t = root.find(".//template[name='" + str(tem) + "']"); 
    listoflocations = [loc.attrib['id'] for loc in t.findall('location')]; #print(listoflocations); 
    #print listoflocations
#     listoftrans = [loc.find("label[@kind='assignment']").text for loc in
#                           t.findall('transition')]
    #print listoftransitions
    listoftrans = [loc.find("label[@kind='assignment']") for loc in t.findall('transition')]
    #print 'listofTemp'
    #print type(listoftrans)
    #print listoftransitions
    for temp in listoftrans:
        if temp != None:
            listoftransitions = temp.text
            #print listoftransitions
    
    
    is_mutated = False    
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    if(is_mutated == True):
                        continue
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_'+m_type+'_'+str(state_mut_count)+'.xml'
                    #print "new file :"+ str(MyName)
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        
                        #print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            
                            strin = 'transition['+str(k)+']'
                           
                            tra = t.find(strin)
                            assignment =  tra.find("label[@kind='assignment']")
                            #print ('assignment:',assignment)
                            if assignment is None:
                                #print('continue!!!')
                                continue
                            
                            if assignment is not None:
                                assi_split =  assignment.text.split(",")
                                
                                for index in range(len(assi_split)) :
                                    assi_split[index]= assi_split[index].replace("\n","")
                                    if state_var in assi_split[index]:
                                        is_mutated = True                                    
                                        mut_text = str_to_append
                                        print mut_text
                                        #print  "$$$$$$$$$$$$$$$$$$ MUTATION DONE $$$$$$$$$$$$$$$$$$$"
                                        assi_split[index] = str_to_append
                                        assignment.text = ','.join(map(str, assi_split))
                                        treex.write(MyName)
                                if(is_mutated != True):
                                    print "to del file:" +str(MyName)
                                    os.remove(MyName)  
                                
def CS(inp,tem):#change Source of transition
    print('in cc')
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        #print('number of transitions:', len(r),r, len(r2), r2)
        #print('main temp', t.find('name').text)
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    strin = 'transition['+str(k)+']'
                    MyName =inp+'MUT_CS'+str(k)+'_'+str(ii)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        #print('inside temp', t.find('name').text)
                        if t.find('name').text==tem:
                            #print(strin)
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            #print 'in Template and transition is',tra.find('label').text
                            for s in tra.iter('source'):
                                #  print 'with source location',s.attrib,'candidate location is : ',r[ii]
                                before= s.attrib['ref']
                                if before != r[ii]:
                                    s.attrib['ref']=r[ii]
                                    print 'location',before,'changes to', s.attrib
                                    # os.path
                                    treex.write(MyName)
                                    # addme= 'MUT_CS'+str(k)+'_'+str(ii)+'.xml'
                                    # print 'new tree is made'
#                                     if CheckQuery(MyName):
#                                         Change_dir(MyName,'yes')
#                                     else:
#                                         Change_dir(MyName,'no')
                                else:
                                    os.remove(MyName)
                          
def SL(inp, tem): # has problem
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        # for loc in t.findall('transition'):
        #     x=loc.find("label[@kind='guard']")
        #     if x!= None: h+=1
        #print 'number of trans:',len(r)
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r)):
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_SL_'+str(k)+'_'+str(ii)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        ##print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            #print strin
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            x=tra.find("label[@kind='target']") #find traget of a transition
                            #print 'target of '+tra+ ' is',x
                            if x is None:
                                continue
                            x.text='id_new'
                            treex.write(MyName)
                            # if CheckQuery(MyName):
                            #     Change_dir(MyName,'yes')
                            # else:
                            #     Change_dir(MyName,'no')

def CT(inp, tem):#change Target of transition
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        #print 'number of transitions:', len(r),r, len(r2), r2
        #print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_CT'+str(k)+'_'+str(ii)+'.xml'
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        #print 'inside temp', t.find('name').text
                        if t.find('name').text==tem:
                            #print strin
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            #print 'in Template and transition is',tra.find('label').text
                            for s in tra.iter('target'):
                                #print('with source location',s.attrib,'candidate location is : ',r[ii])
                                before= s.attrib['ref']
                                if before != r[ii]:
                                    s.attrib['ref']=r[ii]
                                    print 'location',before,'changes to', s.attrib
                                    treex.write(MyName)
                                    #print 'new tree is made'
                                    
                                else:
                                    os.remove(MyName)
                                #print 'it is deleted'
                              
    
    
def old_cg(inp,tem):
     for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        h=0
        for loc in t.findall('transition'):
            x=loc.find("label[@kind='guard']")
            #print ('loc.find(guard): ',x)
            if x!= None: h+=1
        print ('Num of guards: ',h)

        #print 'number of gurads:',h
        ##print 'main temp', t.find('name').text
        if t.find('name').text==tem:
            # for ii in range(len(r)):
            #print('current template name: ',t.find('name').text)
            for k in range(h):
                strin = 'transition['+str(k)+']'
                MyName =inp+'MUT_CG'+str(k)+'_'+str(h)+'.xml'
                tree.write(MyName)
                treex = ET.parse(MyName)
                rootx = treex.getroot()
                for t in rootx.findall('template'):
                    ##print 'inside temp', t.find('name').text
                    #print ('t.find(name).text: ',t.find('name').text)
                    if t.find('name').text==tem:
                        print 'inside tem'
                        ##print strin
                        strin = 'transition['+str(k)+']'
                        tra = t.find(strin)
                        #print('strin: ',strin)
                        #print('tra: ',tra)
                        ##print 'in Template and transition is',tra.find('label').tag
                        x=tra.find("label[@kind='guard']")
                        #print ('tra.find(guard)',x)
                        if x != None:
                            #print x.text
                            #x.text='cl<=5'
                            x.text = x.text+'+1'
                            treex.write(MyName)
                            print('Change Gaurd: ',MyName, ' Updated text: ', x.text)
                        
                        else:
                            try:
                                os.remove(MyName)
                            except:
                                pass


 
def old_CG_v2(inp,tem):
    t = root.find(".//template[name='" + str(tem) + "']"); 
    listoflocations = [loc.attrib['id'] for loc in t.findall('location')]; #print(listoflocations); 
    
    listoftrans = [loc.find("label[@kind='assignment']") for loc in t.findall('transition')]
    
    for temp in listoftrans:
        if temp != None:
            listoftransitions = temp.text
    
    is_mutated = False    
    for t in root.findall('template'):
        r =  [loc.attrib['id'] for loc in t.findall('location')]
        r2 = [loc.find('label') for loc in t.findall('transition')]
        if t.find('name').text==tem:
            for ii in range(len(r)):
                for k in range(len(r2)):
                    if(is_mutated == True):
                        continue
                    strin = 'transition['+str(k)+']'
                    MyName=inp+'MUT_CG'+str(k)+'_'+str(ii)+'.xml'
                   
                    tree.write(MyName)
                    treex = ET.parse(MyName)
                    rootx = treex.getroot()
                    for t in rootx.findall('template'):
                        if t.find('name').text==tem:
                            
                            strin = 'transition['+str(k)+']'
                            tra = t.find(strin)
                            guard_text =  tra.find("label[@kind='guard']")
                            try:
                                temp_var = guard_text.text
                            except:
                                print ('exception')
                                continue
                            #print 'the guard_text is:', guard_text.text
                            tree.write(MyName)
                            treex = ET.parse(MyName)
                            rootx = treex.getroot()
                            
                            if temp_var!= None:
                                guard_text.text = guard_text.text+'+1'
                                treex.write(MyName)
                                print('Change Gaurd: ',MyName, ' Updated text: ', guard_text.text)
                            else:
                                os.remove(MyName)

# NewDir()


# current_path='\gayathri\Mutation_UPTA\mut_locations'
# ChangeDIR()


if __name__ == "__main__":
    main(sys.argv[1:])

