from sequence import MultiSequence 

if __name__ == '__main__':

  seq = MultiSequence()
#  seq.load_frames_from_path('/Volumes/Main/Photos/Timelapse/2012/genf1')
#  seq.load_frames_from_path('/Users/dennis/Pictures/Timelapse/Berlin/Dom/')
  seq.load_frames_from_path('/Users/dennis/Pictures/Timelapse/Kroatia/sunset2/')
#  seq.load_frames_from_path('/Volumes/Main/Photos/Timelapse/2012/20120902_saleve_paragliders/')
  seq.splitSequences()

  seq.interpolate_cropping()
  seq.interpolate_tonals()
#  seq.diff()
