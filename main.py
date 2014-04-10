from sequence import MultiSequence 

if __name__ == '__main__':
    # create sequence object
    seq = MultiSequence()
    # load all xmp files in the given path
    seq.load_frames_from_path('PATH_TO_FOLDER_THAT_CONTAINS_XMP_FILES')
    # generate sequence 
    seq.splitSequences()
    # interpolate the cropping between the sequence keyframes
    seq.interpolate_cropping()
    # interpolate the tonals between the sequence keyframes
    seq.interpolate_tonals()
    # print the differences (does not yet wirk with multi-sequences)
    #seq.diff()
