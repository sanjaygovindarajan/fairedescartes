import shapefile
def read_shp(file,recordId,res=1,isl=1,countries=True):
    
    #Open shapefile with PySHP
    
    shp = shapefile.Reader(file)
    shapes = shp.shapes()
    svg = []
    svgPoints = []
    i = 0
    for country in shapes:
        i = i + 1
        if((shp.shapeRecord(i-1).record[recordId] in countries) or countries):
            print(i)
            main = []
            rounded = []
            for point in country.points:
                data = ','.join(str(x) for x in point)
                long = float(data.split(',')[0])
                lat = float(data.split(',')[1])
                long = long + 180
                lat = lat + 90
                data = str(long) + ',' + str(lat)
                data = data + ' '
                if data in main:
                    main.append(data)
                    pointRounded = [str(round(long*res)/res),str(round(lat*res)/res)]
                    rounded.append(pointRounded)
                    polygon = ''
                    if(len(rounded) > isl):
                        svgJson = {'Points':rounded,'Country':shp.shapeRecord(i-1).record[recordId].replace(' ','')}
                        svg.append(svgJson)
                    main = []
                    rounded = []
                else:
                    main.append(data)
                    roundedData = [str(round(long*res)/res),str(round(lat*res)/res)]
                    if not(roundedData in rounded):
                        rounded.append(roundedData)
    jsonData = {}
    jsonData['data'] = svg
    jsonData['metadata'] = {}
    return jsonData
                        

nescale = 40
netranslate = [415,190]

svgPoints = []
i = 0
for country in shapes:
    i = i + 1
    if(shp.shapeRecord(i-1).record[3] == 'United States of America'):
        print(i)
        main = []
        rounded = []
        for point in country.points:
            data = ','.join(str(x) for x in point)
            long = float(data.split(',')[0])
            lat = float(data.split(',')[1])
            long = (long + 180) * 4
            lat = 720 - ((lat + 90) * 4)
            data = str(long) + ',' + str(lat)
            data = data + ' '
            if data in main:
                main.append(data)
                rounded.append(str((round(long,3)-netranslate[0])*nescale)+','+str((round(lat,3)-netranslate[1])*nescale))
                polygon = ''
                if(len(rounded) > 3):
                    for j in rounded:
                        polygon = polygon + j
                    svgPoints.append('<polygon points="'+ polygon + '"class="'+shp.shapeRecord(i-1).record[3]+'"style="fill:rgb(180,255,180);stroke:purple;stroke-width:0.5" />\n')
                main = []
                rounded = []
            else:
                main.append(data)
                roundedData = str((round(long,3)-netranslate[0])*nescale)+','+str((round(lat,3)-netranslate[1])*nescale) + ' '
                if not(roundedData in rounded):
                    rounded.append(roundedData)
for i in svgPoints:
    svg = svg + i
location_data = open('/path/to/datafile').read().replace(',,','').replace(',\n','\n')
for i in location_data.split('\n'):
    if (len(i.split(',')) == 12):
        try:
            coordinates = i.split(',')
            long = float(coordinates[8])
            lat = float(coordinates[7])
            long = (long + 180) * 4
            lat = 720 - ((lat + 90) * 4)
            svg = svg + '<circle cx="' + str((long-netranslate[0])*nescale) + '" cy = "' + str((lat-netranslate[1])*nescale)
            if(coordinates[0][5]=='5'):
                svg = svg + '" r="4" stroke="red" stroke-width = "2" />'
            else:
                svg = svg + '" r="4" stroke="blue" stroke-width = "2" />'
        except:
            pass
for i in range(-90,90):
    coord = str((720 - ((i + 90) * 4) - netranslate[1]) * nescale)
    coordshift = str(float(coord)+5)
    svg = svg + '<line x1="0" x2="1380" y1="'+ coord + '" y2="'+coord+'" style="stroke:rgb(125,125,125);stroke-width:1;stroke-opacity:0.5" />'
    svg = svg + '<text x="1390" y="' + coordshift + '" fill="rgba(125,125,125,0.5)">'+str(i)+'</text>'
for i in range(-180,180):
    coord = str((((i + 180) * 4) - netranslate[0]) * nescale)
    coordshift = str(float(coord)-10)
    svg = svg + '<line y1="0" y2="695" x1="'+ coord + '" x2="'+coord+'" style="stroke:rgb(125,125,125);stroke-width:1;stroke-opacity:0.5" />'
    svg = svg + '<text y="715" x="' + coordshift + '" fill="rgba(125,125,125,0.5)">'+str(i)+'</text>'
svg = svg + '''
<rect x="1300" y="620" width="120" height="80" style="fill:white;stroke:black;stroke-width:5" />
<circle cx="1320" cy = "640" r="8" stroke="red" stroke-width = "4" />
<circle cx="1320" cy = "680" r="8" stroke="blue" stroke-width = "4" />
<text x="1340" y="645" fill="Red" font-size:"20">HB1805</text>
<text x="1340" y="685" fill="Blue" font-size: "20">HB1907</text>
</svg>
</body>
</html>'''
svgFile = open('svgmap5.html','w')
svgFile.write(svg)
svgFile.close()
