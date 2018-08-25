# -*- coding: utf-8 -*-
from urllib2 import Request, urlopen
import json, time
from qgis.core import QgsPoint

class tcp_api:
    def __init__(self, routingMode, travelMode, apiKey='AIzaSyDhIhhDcPsvjFO-NUKXHuCfh72iKognbTk'):
        self.api_key = apiKey

        if routingMode == 'shortest route':
            self.type = 'distance'
        elif routingMode == 'fastest route':
            self.type = 'duration'
        else:
            raise ValueError("zla wartosc dla routingMode. typ:%s wartosc:%s" % (type(routingMode), routingMode))

        if travelMode == 'car':
            self.mode = 'driving'
        elif travelMode == 'bicycle':
            self.mode = 'bicycling'
        elif travelMode == 'pedestrian':
            self.mode = 'walking'
        else:
            raise ValueError("zla wartosc dla travelMode. typ:%s wartosc:%s" % (type(travelMode), travelMode))

    headers = {
        'Accept': 'text/json; charset=utf-8'
    }


    def GetMatrix(self,locationsString):
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?mode=%s&origins=%s&destinations=%s&key=%s' % \
              (self.mode,locationsString,locationsString,self.api_key)

        #raise Exception(url)
        request = Request(url,headers=self.headers)

        jsonObj = json.load(urlopen(request))

        return jsonObj

    def GetDirections(self,locationsString):
        locationsString = self.swapXY(locationsString)
        locs = locationsString.split("|")
        origin = locs.pop(0)
        destination = locs.pop(-1)
        waypoints = "|".join(locs)
        url = 'https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&waypoints=optimize:false|%s&mode=%s&key=%s' % \
              (origin,destination,waypoints,self.mode,self.api_key)

       # raise Exception(url)
        request = Request(url, headers=self.headers)
        jsonObj = json.load(urlopen(request))

        return jsonObj

    def DistMatrix(self,locationsString):
        locationsString = self.swapXY(locationsString)
        matrix =[]
        attempts = 0
        success = False
        jsonObj = dict()
        while success != True and attempts < 3:
            jsonObj = self.GetMatrix(locationsString = locationsString)
            attempts += 1
            if jsonObj["status"] == "OVER_QUERY_LIMIT":
                time.sleep(2)
                # retry
                continue
            success = True

        if jsonObj["status"] == "OK":
            for row in jsonObj["rows"]:
                mRow = []
                for item in row["elements"]:
                    try:
                        cost = item[self.type]["value"]
                    except:
                        return item["status"] + " " + " Google error." #return error message
                    mRow.append(cost)
                matrix.append(mRow)
            return matrix
        else:
            #return error message
            try:
                return "Daily limit has been reached. ERROR CODE:" + jsonObj["status"] + "  " + jsonObj["error_message"]
            except:
                return "Daily limit has been reached. ERROR CODE:" + jsonObj["status"]

    def swapXY(self,locationsString):
        yxLocs = []
        xyLocs = locationsString.split("|")
        for xyStr in xyLocs:
            xy = xyStr.split(",")
            yxStr = xy[1]+","+xy[0]
            yxLocs.append(yxStr)
        return "|".join(yxLocs)

    def decodePolyline(self, polyline_str):
        index, lat, lng = 0, 0, 0
        coordinates = []
        changes = {'latitude': 0, 'longitude': 0}

        # Coordinates have variable length when encoded, so just keep
        # track of whether we've hit the end of the string. In each
        # while loop iteration, a single coordinate is decoded.
        while index < len(polyline_str):
            # Gather lat/lon changes, store them in a dictionary to apply them later
            for unit in ['latitude', 'longitude']:
                shift, result = 0, 0

                while True:
                    byte = ord(polyline_str[index]) - 63
                    index+=1
                    result |= (byte & 0x1f) << shift
                    shift += 5
                    if not byte >= 0x20:
                        break

                if (result & 1):
                    changes[unit] = ~(result >> 1)
                else:
                    changes[unit] = (result >> 1)

            lat += changes['latitude']
            lng += changes['longitude']

            coordinates.append(QgsPoint(lng / 100000.0,lat / 100000.0))

        return coordinates

def main():
    tcp = tcp_api("fastest route","car")
    #print tcp.DistMatrix('52.6655101,21.89188|52.7655101,21.99188|52.3655101,21.39188')
    directionsJson = tcp.GetDirections('52.6655101,21.89188|52.7655101,21.99188|52.3655101,21.39188')
    encodedPath =  directionsJson['routes'][0]['overview_polyline']['points']
    print (tcp.decodePolyline(encodedPath))

if __name__ == '__main__':
  main()