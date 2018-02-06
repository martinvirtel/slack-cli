Create Message (Channel, Thread)

get emoji list
r=api.emoji.list()      
with open("emojis.txt","w") as ff :
     ...:     for (k,v) in r.body["emoji"].items() :
     ...:         ff.write("".join(k,"\t",v,"\n"))

