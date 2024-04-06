from .plugins_data import initdata,wdata,rdata
jsonname = "HWP.json"
bashdata = {
    "status":1,
    "cmdlist":{}
}
initdata(jsonname)

def addHWP(
    command :str,
    text :str = "",
    perm : str = "user"
):
    
    temp = rdata(jsonname)
    cmdlist = temp.get("cmdlist",{})
    cmdlist[command]={
        "text" : text,
        "perm" : perm
    }
    temp["cmdlist"]=cmdlist
    wdata(jsonname,temp)
    return True

def delHWP(
    command :str,
):
    temp = rdata(jsonname)
    a = temp["cmdlist"].pop(command,"NotFound")
    wdata(jsonname,temp)
    return a
    
def format_data():
    temp = rdata(jsonname)
    cmdlist = temp.get("cmdlist",{})
    data = []
    for key , values in cmdlist.items():
        data.append(
            [ key , values["text"] , values["perm"] ]
        )
    return data

#本插件由 cubstaryow 编写