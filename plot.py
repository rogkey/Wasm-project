import os
from attr import attr
import pandas as pd
from IPython.display import display
import numpy as np
import re

homeDir = os.getenv('HOME')
rootDir=str(homeDir)+"/Wasm-project/out/"
chunksDir=str(homeDir)+"/Wasm-project/chunks-out/"


def get_source_names(rootDir) :
    #source names define colum entries in each tool chain's table (line entries are the attributes we get)
    source_name=[]
    for root,dirnames,filenames in os.walk(rootDir):
    # search all text files recursively
        for filename in filenames:
            #strip tool chain names from source file names
            if ".txt" in filename:
                srccomp=filename.split("-")[0]
                if "emcc" in srccomp:
                    srccomp=srccomp.replace("emcc","")
                if "cheerp" in srccomp:
                    srccomp=srccomp.replace("cheerp","")
                if "llvm" in srccomp:
                    srccomp=srccomp.replace("llvm","")
                if "wasi" in srccomp:
                    srccomp=srccomp.replace("wasi","")
                source_name.append(srccomp)
    #checking for duplicates
    #updated list of source file names
    source_name[:]=list(set(source_name))
    source_name.sort()
    column_entries=source_name
    return column_entries


def get_general_attributes():
    # table_name lists the names for each tool chain's table
    table_name=['Cheerp_tool_chain','Emscripten_tool_chain','Clang/llvm_tool_chain','Wasi_tool_chain']
    
    column_entries=get_source_names(rootDir)
    line_entries=['Functions','Imported','Non-imported','Exported','Tables','Table entries at init','Of those unique functions','Instructions','call','call_indirect','Globals','Likely Stack Pointer (global id)','Functions using stack pointer','Functions w/ stack allocation','Unique Function Types','Functions w/ AL. one indirect call','Classes']
    
    df_emcc=pd.DataFrame(index=line_entries, columns=column_entries)
    df_wasi=pd.DataFrame(index=line_entries, columns=column_entries)
    df_llvm=pd.DataFrame(index=line_entries, columns=column_entries)
    df_cheerp=pd.DataFrame(index=line_entries, columns=column_entries)
    
    chunkname=['chunk2.txt','chunk3.txt','chunk4.txt','chunk5.txt','chunk6.txt','chunk8.txt','chunk9.txt','chunk12.txt','chunk13.txt']
    for item in chunkname[0:3]:
        itm1_file= open(os.path.join(chunksDir,str(item)),"r+")
        file = itm1_file.read()
        for paragraph in file.strip().split("\n\n"):
            src_comp=""
            src=""
            for line in paragraph.split("\n"):
                try: 
                    attrs=line.split(",")
                    first_attr=attrs[0].strip(" []'")
                    second_attr=attrs[1].strip(" []'")
                    if "Of those" in first_attr :
                        first_attr=first_attr+" "+second_attr
                        second_attr=attrs[2].strip(" []'")
                    try :
                        if "emcc" in src_comp:
                            if "(" in second_attr :second_attr=second_attr.split("(")[0].strip(" ")
                            df_emcc.at[first_attr,src]=second_attr
                        if "cheerp" in src_comp:
                            if "(" in second_attr :second_attr=second_attr.split("(")[0].strip(" ")
                            df_cheerp.at[first_attr,src]=second_attr
                        if "llvm" in src_comp:
                            if "(" in second_attr :second_attr=second_attr.split("(")[0].strip(" ")
                            df_llvm.at[first_attr,src]=second_attr
                        if "wasi" in src_comp:
                            if "(" in second_attr :second_attr=second_attr.split("(")[0].strip(" ")
                            df_wasi.at[first_attr,src]=second_attr
                    except:
                        if "emcc" in src_comp:
                            df_emcc.at[first_attr,src]=""
                        if "cheerp" in src_comp:
                            df_cheerp.at[first_attr,src]=""
                        if "llvm" in src_comp:
                            df_llvm.at[first_attr,src]=""
                        if "wasi" in src_comp:
                            df_wasi.at[first_attr,src]=""

                    #rint(first_attr," : ",second_attr)
                except:
                    src_comp=attrs[0].split("-")[0]
                    if "emcc" in src_comp:
                        src=src_comp.replace("emcc","")
                    if "cheerp" in src_comp:
                        src=src_comp.replace("cheerp","")
                    if "llvm" in src_comp:
                        src=src_comp.replace("llvm","")
                    if "wasi" in src_comp:
                        src=src_comp.replace("wasi","")

                    #print("filename_compilatorname : ",src_comp)
    for item in chunkname[3:]:
        itm1_file= open(os.path.join(chunksDir,str(item)),"r+")
        file = itm1_file.read()
        for paragraph in file.strip().split("\n\n"):
            src_comp,src,comp,lsp,fsp,fsa,uft,fic="","","","","","","",""
            i,j=0,0
            if "Globals" in paragraph: #chunk5
                for line in paragraph.split("\n"):
                    if ".txt" in line:
                        src_comp=line.split("-")[0]
                        digit=re.search(r'\d',src_comp)
                        comp=src_comp.split(digit.group())[1]
                        src=src_comp.replace(comp,"")
                    if "#" in line:
                        i+=1
                if comp == "emcc":
                    df_emcc.at['Globals',src]=i
                if comp == "cheerp":
                    df_cheerp.at['Globals',src]=i
                if comp == "llvm":
                    df_llvm.at['Globals',src]=i
                if comp == "wasi":
                    df_wasi.at['Globals',src]=i
            if "Likely the stack pointer" in paragraph: #chunk6
                for line in paragraph.split("\n"):
                    if ".txt" in line:
                        src_comp=line.split("-")[0]
                        digit=re.search(r'\d',src_comp)
                        comp=src_comp.split(digit.group())[1]
                        src=src_comp.replace(comp,"")
                    if "Likely the stack pointer" in line:
                        lsp=line.split(",")[1].strip(" '[]")
                    if "Functions using stack pointer" in line : 
                        fsp=line.split(",")[1].split("(")[0].strip(" '")
                    if "functions with stack allocation total" in line :
                        fsa=line.split(",")[1].split("(")[0].strip(" '")
                if comp == "emcc":
                    df_emcc.at['Likely Stack Pointer (global id)',src]=lsp
                    df_emcc.at['Functions using stack pointer',src]=fsp
                    df_emcc.at['Functions w/ stack allocation',src]=fsa
                if comp == "cheerp":
                    df_cheerp.at['Likely Stack Pointer (global id)',src]=lsp
                    df_cheerp.at['Functions using stack pointer',src]=fsp
                    df_cheerp.at['Functions w/ stack allocation',src]=fsa
                if comp == "llvm":
                    df_llvm.at['Likely Stack Pointer (global id)',src]=lsp
                    df_llvm.at['Functions using stack pointer',src]=fsp
                    df_llvm.at['Functions w/ stack allocation',src]=fsa
                if comp == "wasi":
                    df_wasi.at['Likely Stack Pointer (global id)',src]=lsp
                    df_wasi.at['Functions using stack pointer',src]=fsp
                    df_wasi.at['Functions w/ stack allocation',src]=fsa
            if "Counts of function types" in paragraph: #chunk8
                for line in paragraph.split("\n"):
                    if ".txt" in line:
                        src_comp=line.split("-")[0]
                        digit=re.search(r'\d',src_comp)
                        comp=src_comp.split(digit.group())[1]
                        src=src_comp.replace(comp,"")
                    if "Counts of function types" in line:
                        uft=line.split("(")[1].split()[0].strip()
                if comp == "emcc":
                    df_emcc.at['Unique Function Types',src]=uft
                if comp == "cheerp":
                    df_cheerp.at['Unique Function Types',src]=uft
                if comp == "llvm":
                    df_llvm.at['Unique Function Types',src]=uft
                if comp == "wasi":
                    df_wasi.at['Unique Function Types',src]=uft
            if "Functions with at least one call_indirect" in paragraph: #chunk9
                for line in paragraph.split("\n"):
                    if ".txt" in line:
                        src_comp=line.split("-")[0]
                        digit=re.search(r'\d',src_comp)
                        comp=src_comp.split(digit.group())[1]
                        src=src_comp.replace(comp,"")
                    if "Functions with at least one call_indirect" in line:
                        fic=line.split(",")[1].split("(")[0].strip(" '")
                if comp == "emcc":
                    df_emcc.at['Functions w/ AL. one indirect call',src]=fic
                if comp == "cheerp":
                    df_cheerp.at['Functions w/ AL. one indirect call',src]=fic
                if comp == "llvm":
                    df_llvm.at['Functions w/ AL. one indirect call',src]=fic
                if comp == "wasi":
                    df_wasi.at['Functions w/ AL. one indirect call',src]=fic
            if "call_indirect target equivalence classes" in paragraph: #chunk5
                for line in paragraph.split("\n"):
                    if ".txt" in line:
                        src_comp=line.split("-")[0]
                        digit=re.search(r'\d',src_comp)
                        comp=src_comp.split(digit.group())[1]
                        src=src_comp.replace(comp,"")
                    if "#" in line:
                        j+=1
                if comp == "emcc":
                    df_emcc.at['Classes',src]=j
                if comp == "cheerp":
                    df_cheerp.at['Classes',src]=j
                if comp == "llvm":
                    df_llvm.at['Classes',src]=j
                if comp == "wasi":
                    df_wasi.at['Classes',src]=j
    print("\n -- cheerp table :\n")
    display(df_cheerp.to_string())  
    print("\n -- llvm table :\n")
    display(df_llvm.to_string())
    print("\n -- wasi table :\n")
    display(df_wasi.to_string())
    print("\n -- emscipten table :\n")
    display(df_emcc.to_string())
    #needs nb of globals/ nb of classes/ which gb is the stack pointer /nb of unique func types / chunk 9 


get_general_attributes()

def get_source_tool_names(rootDir) :
    #source names define colum entries in each tool chain's table (line entries are the attributes we get)
    source_tool_name=[]
    for root,dirnames,filenames in os.walk(rootDir):
    # search all text files recursively
        for filename in filenames:
            #strip tool chain names from source file names
            if ".txt" in filename:
                srccomp=filename.split("-")[0]
                source_tool_name.append(srccomp)
    #updated list of source file names
    source_tool_name[:]=list(set(source_tool_name))
    source_tool_name.sort()
    column_entries=source_tool_name
    return column_entries


def get_globals():
    column_entries=get_source_tool_names(rootDir)
    line_entries=['Global_id','type','export','init_method','init_value','gets','sets']
    df_globals=pd.DataFrame(index=line_entries, columns=column_entries)
    chunkname=['chunk5.txt']
    for item in chunkname:
        itm1_file= open(os.path.join(chunksDir,str(item)),"r+")
        file = itm1_file.read()
        for paragraph in file.strip().split("\n\n"):
            src_comp=""
            attrs0=""
            global_id,global_type,init_method,init_val,export_attr,gets,sets=([],[],[],[],[],[],[])
            for line in enumerate(paragraph.split("\n")):
                if ".txt" in line[1]:
                    src_comp=line[1].split("-")[0].strip("")
                    print("\n"+src_comp)           
                if "Globals" or "init" or "export" in line[1]: 
                    attrs=line[1].split(",")
                    if "Globals" in attrs[0] :
                        print("")
                    if "init" in attrs[0]:
                        interm_var=attrs[1].strip(" []'")
                        init_method.append(interm_var.split()[0])
                        init_val.append(interm_var.split()[1])
                    if "export" in attrs[0]:
                        interm_var=attrs[1].strip(" []'")
                        export_attr.append(interm_var)
                if "global.get" or "#" in line[1] :  
                    attrs0=line[1].strip("' []")
                    if "global.get" in attrs0:
                        gets.append(attrs0.split()[0])
                        sets.append(attrs0.split()[3])
                    if "#" in attrs0:
                        attrs0=attrs0.strip(" #")
                        global_id.append(attrs0.split()[0])
                        global_type.append(attrs0.split()[1])
                        if not "export" in paragraph.split("\n")[line[0]+1] :
                            export_attr.append(None)
            
            dfGlobal=pd.DataFrame(index=range(7),columns=range(len(global_id)))
            for item in dfGlobal.columns:
                dfGlobal.at[0,item]=global_id[int(item)]
                dfGlobal.at[1,item]=global_type[int(item)]
                dfGlobal.at[2,item]=export_attr[int(item)]
                dfGlobal.at[3,item]=init_method[int(item)]
                dfGlobal.at[4,item]=init_val[int(item)]
                dfGlobal.at[5,item]=gets[int(item)]
                dfGlobal.at[6,item]=sets[int(item)]
            df = dfGlobal.set_axis(['Global_id','type','export','init_method','init_value','gets','sets'],axis=0)
            display(df.to_string())


        #display(df_globals.to_string())          
                 
#get_globals()

def get_count_of_func_types():
    column_entries=get_source_tool_names(rootDir)
    line_entries=['Unique_types','func_type','','']
    chunkname=['chunk8.txt']
    for item in chunkname:
        itm1_file= open(os.path.join(chunksDir,str(item)),"r+")
        file = itm1_file.read()
        src_comp,ufc="",""
        src_comps,unique_func_count=([],[])
        for paragraph in file.strip().split("\n\n"):
            func_type,func_type_count,func_type_pct=([],[],[])
            for line in paragraph.split("\n"):
                if ".txt" in line:
                    src_comp=line.split("-")[0].strip("")
                    src_comps.append(src_comp)
                if "unique" in line:
                    ufc=line.split("(")[1].strip("").split()[0]
                    unique_func_count.append(ufc)
                if "×" in line:
                    func_type_count.append(line.split("×")[0].strip(" '[").split()[0])
                    func_type_pct.append(line.split("×")[0].strip(" '[").split()[1].strip("()"))
                    func_type.append(line.split("×")[1].strip().split("'")[0].strip())
            idx=len(func_type_count)
            df_uft=pd.DataFrame(index=range(idx),columns=['function_type','type_count','type_count_%_'])
            df_uft.at[:,'function_type']=func_type
            df_uft.at[:,'type_count']=func_type_count
            df_uft.at[:,'type_count_%_']=func_type_pct
            print("\n",src_comp)
            print("have ",ufc," unique_types")
            display(df_uft.to_string())

        #returns df and 2d tuple containing src_comps + ufcs for general attributes            
            
            
#get_count_of_func_types()

def get_init_tables():
    chunkname=['chunk10.txt']
    for item in chunkname:
        itm1_file= open(os.path.join(chunksDir,str(item)),"r+")
        file = itm1_file.read()
        src_comp,tir="",""
        src_comps,table_init_ranges=([],[])
        for paragraph in file.strip().split("\n\n"):
            ranges,lengths,unique_funcs,types=([],[],[],[])
            for line in paragraph.split("\n"):
                if ".txt" in line:
                    src_comp=line.split("-")[0].strip("")
                    src_comps.append(src_comp)
                if "table init ranges in total" in line:
                    tir=line.split("t")[0].strip(" '[")
                    table_init_ranges.append(tir)
                if "range'" in line:
                    itm0=line.split("'")
                    itm1=line.split(",")
                    ranges.append(itm0[3].strip().split("l")[0].strip())
                    lengths.append(itm1[3].strip("'").split("u")[0].strip(" '"))
                    unique_funcs.append(itm1[4].strip(" '").split("t")[0].strip())
                    types.append(itm0[9].strip())
            idx=len(ranges)
            df_it=pd.DataFrame(index=range(idx),columns=['range','length','unique_functions','type'])
            df_it.at[:,'range']=ranges
            df_it.at[:,'length']=lengths
            df_it.at[:,'unique_functions']=unique_funcs
            df_it.at[:,'type']=types
            print("\n",src_comp)
            print("have ",tir," table init ranges")
            display(df_it.to_string())
        # returns df and 2d tuple src_comps + tirs for general attributes

#get_init_tables()