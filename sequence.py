import os, fnmatch
from frame import Frame

class Sequence:
  def __init__( self, frames=[]):
    self.frames = frames
    self.keyframe_first = None
    self.keyframe_last  = None
    self._init_config()


  def interpolate( self, attributes ):
    for attrkey in attributes:
      attr = self.keyframe_first.attributes[attrkey]
      first = self.keyframe_first.get_attribute( attrkey )
      last  = self.keyframe_last.get_attribute( attrkey )
      if first != last:
        print '   INFO: Interpolating "%s" between %s and %s (%d,%d)' % (
            attrkey, attr.val2str(first), attr.val2str(last), 
            self.keyframe_first.index, self.keyframe_last.index)
        stepsize = 1.0 * (last - first) / len(self.frames)
#        print len(self.frames), stepsize, last, first
        for f in self.frames:
          if not f.is_key_frame:
            index = f.index - self.keyframe_first.index 
            attrval = first + stepsize * index
#            print '    %d : setting attribute "%s" to %.3f' % (index, attrkey, attrval)
            f.set_attribute(attrkey, attrval)
      for f in self.frames:
        f.write()


  def interpolate_tonals(self):
    self.interpolate( [ 
        'crs:Exposure2012', 'crs:Contrast2012', 'crs:Highlights2012', 'crs:Shadows2012', 
        'crs:Whites2012', 'crs:Blacks2012', 'crs:Temperature', 'crs:Tint'
        ] )


  def interpolate_cropping( self ):
    self.interpolate( [ 
        'crs:CropLeft', 'crs:CropRight', 'crs:CropTop', 'crs:CropBottom'
        ] )


  def diff( self, attributes ):
    for a in attributes:
      first = self.keyframe_first.get_attribute( a )
      last  = self.keyframe_last.get_attribute( a )
      if first != last:
        print ( a, first, last )


  def _init_config( self ):
    self.config = {
        'filetype': 'xmp'
        }

  def load_frames_from_path( self, path ):
    index = 0
    for filename in os.listdir( path ):
      if fnmatch.fnmatch( filename, 
          '*.%s' % self.config['filetype'] ):
        self.frames.append(
            Frame( index, path + '/' + filename )
            )
        index += 1
    print '   INFO: loaded %d frames' % index
    self._load_keyframes()

  def _load_keyframes( self ):
    # this was when only the first and last frames are keyframes 
#    self.keyframe_last  = self.frames.pop( )
#    self.keyframe_first = self.frames.pop( 0 )
    self.keyframe_first = self.frames[0]
    self.keyframe_last = self.frames[-1]
    self.keyframe_first.is_key_frame = True
    self.keyframe_last.is_key_frame = True
    print '   INFO: key frames are (%d,%d)' % (
        self.keyframe_first.index,
        self.keyframe_last.index
        )

class MultiSequence(Sequence):
  def __init__( self, frames=[]):
    self.frames = frames
    self.sequences = []
    self._init_config()

  def _load_keyframes(self):
    for frame in self.frames:
      rating = frame.get_attribute('xmp:Rating')
      if rating > 0:
        print 'Recognized keyframe at %i' % frame.index
        frame.is_key_frame = True

  def splitSequences(self):
    first = 0
    last = 0
    for frame in self.frames:
      # TODO: HEREIM --- WHY IS THE SECOND FRAME NOT FILLED CORRECTLY?
      if frame.is_key_frame and frame.index > first:
          # finish previous
          last = frame.index
          s = Sequence(self.frames[first:last+1])
          s.name = 'Sequence %d' %( len(self.sequences)+1)
          s._load_keyframes()
          self.sequences.append(s)
          # generate new
          first = frame.index

    for seq in self.sequences:
      print '%s: %d frames' % (seq.name, len(seq.frames))

  def interpolate( self, attributes ):
    for s in self.sequences:
      s.interpolate(attributes)
