from attribute_type import *
from xml.dom import minidom

class Frame:
  def __init__( self, index, xmp_filename ):
    self.index     = index
    self.xmp_filename = xmp_filename
    self.xmp_file  = None
    self.is_key_frame = False
    self._load_from_xmp( xmp_filename )

    self.attributes = {
        'crs:CropTop':      FloatAttribute( 'CropTop' ),
        'crs:CropRight':    FloatAttribute( 'CropRight' ),
        'crs:CropBottom':   FloatAttribute( 'CropBottom' ),
        'crs:CropLeft':     FloatAttribute( 'CropLeft' ),
        'crs:Exposure2012':   FloatAttribute( 'Exposure2012', 2 ),
        'crs:Contrast2012':   IntegerAttribute( 'Contrast2012' ),
        'crs:Highlights2012': IntegerAttribute( 'Highlights2012' ),
        'crs:Shadows2012':    IntegerAttribute( 'Shadows2012' ),
        'crs:Whites2012':     IntegerAttribute( 'Whites2012' ),
        'crs:Blacks2012':     IntegerAttribute( 'Blacks2012' ),
        'crs:Temperature':    IntegerAttribute( 'Temperature' ),
        'crs:Tint':           IntegerAttribute( 'Tint' ),
        'xmp:Rating':         UnsignedIntegerAttribute( 'Rating' )
        }


  def _load_from_xmp( self, filename ):
    self.xmp_file = minidom.parse( filename )
    self.xmp_description = self.xmp_file.getElementsByTagName( 
        'rdf:Description' )[0]


  def write( self ):
    self.xmp_file.writexml(
        open( self.xmp_filename, 'w'), '  '
        )


  def dump( self ):
    for key,attr in self.attributes.iteritems():
       print( attr['type'](
           self.xmp_description.getAttribute( key )
           ) )


  def has_attribute( self, key ):
    return self.xmp_description.hasAttribute(key)


  def get_attribute( self, key ):
    if self.has_attribute(key):
      attr = self.xmp_description.getAttribute(key)
      return self.attributes[key].str2val(attr)
    else:
      return None


  def set_attribute(self, key, value):
    # TODO: check before if this is in the list 'attributes'
    return self.xmp_description.setAttribute( 
        key, self.attributes[key].val2str(value))


