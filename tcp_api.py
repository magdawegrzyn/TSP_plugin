# -*- coding: utf-8 -*-
from urllib2 import Request, urlopen
import json

class tcp_api:
    def __init__(self,routingMode,travelMode,apiKey = '58d904a497c67e00015b45fc07b5026cf1ff4264bdcec8fbc6623caa'):
        self.api_key = apiKey
        if routingMode == 'shortest route':
            self.preference = 'shortest'
            self.metrics = 'distance'
        elif routingMode == 'fastest route':
            self.preference = 'fastest'
            self.metrics = 'duration'
        else:
            raise ValueError("zla wartosc dla routingMode. typ:%s wartosc:%s" % (type(routingMode), routingMode))
        if travelMode == 'car':
            self.profile = 'driving-car'
        elif travelMode == 'bicycle':
            self.profile = 'cycling-regular'
        elif travelMode == 'pedestrian':
            self.profile = 'foot-walking'
        else:
            raise ValueError("zla wartosc dla travelMode. typ:%s wartosc:%s" % (type(travelMode), travelMode))

    headers = {
        'Accept': 'text/json; charset=utf-8'
    }

    sources = 'all'
    destinations = 'all'
    resolve_locations = ''
    units = 'm'

    format = 'geojson'
    language = 'en'
    geometry = 'true'
    geometry_format = 'encodedpolyline'
    geometry_simplify = ''
    instructions = 'true'
    instructions_format =''
    roundabout_exits = ''
    attributes = ''
    maneuvers = ''
    radiuses = ''
    bearings = ''
    continue_straight = ''
    elevation = ''
    extra_info = ''
    options = ''
    id = ''
    def GetMatrix(self,locationsString):
        url = 'https://api.openrouteservice.org/matrix?api_key=%s&profile=%s&locations=%s&sources=%s&destinations=%s&metrics=%s&resolve_locations=%s&units=%s&optimized=true' % \
              (self.api_key,self.profile,locationsString, self.sources, self.destinations, self.metrics,self.resolve_locations,self.units)

        #raise Exception(url)
        request = Request(url,headers=self.headers)
        jsonObj = json.load(urlopen(request))

        return jsonObj

    def GetDirections(self,locationsString):

        #force ORS to use legal pedestrian roots
        if self.profile == 'foot-walking':
            self.preference = 'fastest'

        url = 'https://api.openrouteservice.org/directions?api_key=%s&coordinates=%s&profile=%s&preference=%s&format=%s&units=%s&language=%s&geometry=%s&geometry_format=%s&geometry_simplify=%s&instructions=%s&instructions_format=%s&roundabout_exits=%s&attributes=%s&maneuvers=%s&radiuses=%s&bearings=%s&continue_straight=%s&elevation=%s&extra_info=%s&optimized=false&options=%s&id=%s' % \
              (self.api_key,locationsString,self.profile,self.preference,self.format,self.units,self.language,self.geometry,self.geometry_format,self.geometry_simplify,self.instructions,self.instructions_format,self.roundabout_exits,self.attributes,self.maneuvers,self.radiuses,self.bearings,self.continue_straight,self.elevation,self.extra_info,self.options,self.id)
        request = Request(url,headers=self.headers)
        #raise Exception(url)
        jsonObj = json.load(urlopen(request))
        return jsonObj

    def DistMatrix(self,locationsString):

        jsonObj = self.GetMatrix(locationsString)
        try:
            return list(jsonObj["durations"])
        except:
            return list(jsonObj["distances"])

def main():
    tcp = tcp_api()
    print (tcp.DistMatrix('21.0,52.0|22.0,52.0|21.5,51.4'))
    directionsJson = tcp.GetDirections('21.0,52.0|22.0,52.0|21.5,51.4')
    print (str(directionsJson))

if __name__ == '__main__':
  main()