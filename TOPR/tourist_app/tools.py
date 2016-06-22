def generate_KML_for_tourists(tourists):
    header = r"""
    <kml>
    <Document>
    <Style id="tourist">
        <IconStyle>
        <scale>0.2</scale>
          <Icon>

            <href>http://maps.google.com/mapfiles/kml/paddle/grn-blank.png</href>
          </Icon>
        </IconStyle>
 </Style>
    """

    footer = r"""
    </Document>
    </kml>
    """

    placemark1stpart = r"""
        <Folder>
            <Placemark>
            <styleUrl>#tourist</styleUrl>
                <name>
    """
    placemark2ndpart = r"""</name>
                <ExtendedData>
                </ExtendedData>
                <Point>
                    <coordinates>
    """
    placemark3rdpart = r"""</coordinates>
                </Point>
            </Placemark>
            </Folder>
    """
    tourists_kmls = [placemark1stpart + tourist.numer_telefonu + placemark2ndpart +
                     str(tourist.pozycja_N) + ',' + str(tourist.pozycja_E) + ',0.0' + placemark3rdpart for tourist in
                     tourists]
    return header + ''.join(tourists_kmls) + footer
    
    
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km
