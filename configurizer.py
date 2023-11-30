def load_config(filename="config.cfg", default=None, lists=None):
    if default == None:
        raise Exception("No default configuration defined on configurizer init")
    try: # check if file exists
        f = open(filename, "r")
    except:
        f = open(filename, "w")
        f.write(default)
    f.close()
    result = {}
    with open(filename, "r") as f:
        for line in f:
            if line[0]=="#" or line in ["", " ", "\n"]: # ignore comments and blankspace
                pass
            else:
                name = line.split("=")[0]
                prawvalue = line.split("=")[1]
                rawvalue = prawvalue.strip("\n")
                if rawvalue.lower() == "true":
                    value = True
                elif rawvalue.lower() == "false":
                    value = False
                elif rawvalue.lower() in ["none", "null", "none", "null"]:
                    value = None
                else:
                    try:
                        if "." in rawvalue:
                            value = float(rawvalue)
                        else:
                            value = int(rawvalue)
                    except:
                        if name in lists:
                            value = rawvalue.split(";")
                        else:
                            value = rawvalue
                result[name] = value
    return result
            
    
            
        
