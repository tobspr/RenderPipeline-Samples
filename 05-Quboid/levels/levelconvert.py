from sys import argv
if len(argv) >1:
            level = int(argv[1])
            
data=open("./level_"+str(level))
inputData = data.read().replace("\n","").strip().replace(" ","").lstrip("<").rstrip(">").split("><")
data.close()
output = open("./level_"+str(level),"w" )

xmin=1000
ymin=1000
for tileData in inputData:
    data = tileData.split(",")     
    for i in data:
        if i.startswith("Pos="):
            i = i.split("=")[1].split("_")
            x,y=int(i[0]), int(i[1])
            if x < xmin:
                xmin = x
            if y < ymin:
                ymin = y
         

lastx = 0               
for tileData in inputData:
    
    data = tileData.split(",")         
    output.write("<"+data[0]+",")
    data = data[1].split("=")[1].split("_")
    output.write("Pos="+str( int(data[0])-xmin ) +"_" +str( int(data[1])-ymin )+">")
    print int(data[0])-xmin , lastx
    if int(data[0])-xmin > lastx:
        print "inserting newline"
        lastx=int(data[0])-xmin
        output.write("\n")

"""
#print data
for x in range(0,len(data)):
    for y in range(0,len(data[x])):
        if data[x][y] == "0":
            continue
        elif data[x][y] == "1":
            output.write("<Type=tile,Pos="+str(x)+"_"+str(y)+">")
        elif data[x][y] == "2":
            output.write("<Type=start,Pos="+str(x)+"_"+str(y)+">")
        elif data[x][y] == "3":
            output.write("<Type=goal,Pos="+str(x)+"_"+str(y)+">")
    output.write("\n")
"""
output.close()
