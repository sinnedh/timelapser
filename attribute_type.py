class Attribute:
  def __init__( self, key, datatype, strformat ):
    self.key = key
    self.datatype = datatype
    self.strformat = strformat

  def str2val( self, str_value ):
    return self.datatype( str_value )


  def val2str( self, value ):
    return self.strformat % value


class IntegerAttribute( Attribute ):
  def __init__( self, key ):
    Attribute.__init__( self, key, int, '%+d' )

class UnsignedIntegerAttribute( Attribute ):
  def __init__( self, key ):
    Attribute.__init__( self, key, int, '%d' )


class FloatAttribute( Attribute ):
  def __init__( self, key, digits=None ):
    if digits is None:
      Attribute.__init__( self, key, float, '%f' )
    else:
      Attribute.__init__( self, key, float, '%.'+str('%d'%digits)+'f' )


