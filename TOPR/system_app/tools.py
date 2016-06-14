# coding: utf-8


def generate_KML(routes):
    header = r"""<kml><Document>
    <Style id="blueLine">
      <LineStyle>
        <color>ffff0000</color>
        <width>4</width>
      </LineStyle>
    </Style>
    <Style id="redLine">
      <LineStyle>
        <color>ff0000ff</color>
        <width>4</width>
      </LineStyle>
    </Style>
    <Style id="greenLine">
      <LineStyle>
        <color>ff009900</color>
        <width>4</width>
      </LineStyle>
    </Style>
    <Style id="yellowLine">
      <LineStyle>
        <color>ff61f2f2</color>
        <width>4</width>
      </LineStyle>
    </Style>
    <Style id="blackLine">
      <LineStyle>
        <color>ff000000</color>
        <width>4</width>
      </LineStyle>
    </Style>
    """

    footer = r"""
    </Document>
    </kml>
    """
    return header + ''.join([route.KML for route in routes]) + footer