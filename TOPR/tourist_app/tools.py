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
