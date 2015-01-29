Any Transform you write should have the basic form of:

def prototypeTransform(EEGpackage):
  #Do your maths.
  return features[]

-------------------------------------------------------------------------------------------------------------------
The epilepsyTools Module contains:


object EEGpackage(): # THis is a class to keep track of any .mat file read in, create one by using "PackageName = readMatReturnPackage(filename)", where "filename" is the name of the .mat file you want to read in and Package is what you want to call the EEGPackage object 
    contains:
    self.packet = 16 x numberOfTimesteps numpy array
    self.duration = float, duration of package
    self.frequency = float, frequency of samples
    self.probeNames = List of string variables of name
    self.index = integer, index of this mat file (only for training data)
    self.name = string, filename of this file

    self.preictal = logical, if preictal == True, else == False *IMMUTABLE*
    self.interictal = logical, if interictal == True, else == False *IMMUTABLE*
    self.test = logical, if test == True, else == False *IMMUTABLE*
    self.fileKind = either "preictal", "interictal" or "test" as a text field. *IMMUTABLE*

    object methods:
    .plotPacket(self, endval = -1, startval = 0): Chucks out a rough and ready plot of EEG Squibs

    .applyTransform(transform): returns transform(EEGpackage)

    .fiveSpawn(): returns a list of five 'new' EEGpackages, each containing 2 minute 
        sections of the squibs in the original. Produces objects with name altered to have _1 through _5

    .combineToNew(EEGpackage): returns the 'child' of self and other after confirming that these two can be combined
        the child is defined as the second half of the first packages' packet (self) and the first half of the other package
        returns the baby of these two iff the sequences and the rest align. produces object with nameOfOriginal with .5 appended

    .compatibleForCombine(EEGpackage): Helper method to assist with combineToNew, compares all internal variables except the packet and the index. Checks filename.

    .downsample(divisor): Downsamples the packet by the divisor. So if you have a 400Hz packet, and call EEGpackage.downsample(2), you will now have a 200Hz packet.
    this routine requires an integer divisor and updates the Package.frequency in the object.


other methods:

readMatReturnPackage(filename, transformer = ""): Accepts a matlab filename, returns the EEG package with data transformed by the transformer, if applicable 
  Automagically works out the file kind (preictal, interictal, test) from the data file names in the .mat file

readDirectoryAndReturnTransformedList(directory, stub, component, transform): Version 0.1 had a "readTrainingDirectoryAndReturnPackageList", this is 
    insane on memory usage when all I need  is a list of lists. Where column0 is the filename, columns 1:[-1] are the X features and column[-1] is the dependent variable
    Until I think of a better way, this subroutine will take the directory, the stub, the component and the transform function and return
  the list of lists of transformed data. The "better way" will work for training and then test- probably by a "read training method", which will
  call this twice and a read test method.

readDirectoryAndReturnTransformedTrainingList(directory, stub, transform): Returns same as above, but with both interictal and preictal files. 

pretendTransform(package): Just returns a list of ten 1s. Useful for checking method syntax and whatnot.

testTransform(transform): Lets you test your own transform code by reading in some default .mat files and applying your transform. This is
                very useful for checking syntax and algorithmic errors. Tests your transform by reading in some sample ictal .mat files as generated by P.Collins and 
                applying this code. If the result is plotable, it will call matplotlib and show you the result of the transform. 
                It returns a list of the resultant feature vectors of the tests.

return_roc_auc(name, dataDirectory, listOfScans, transform, classifier, KFold = False, preprocess= None, verbose = False, cv_ratio = 0.5, smartPreictal = True, fiveSplit = False, generatePreictal = False, generateInterictal = False)
                Returns the ROC_AUC score for this transform using this classifier specified. You can choose KFold or CV, etc.

finalPredict(name, dataDirectory, listOfScans, transform, clf, preprocess= None, fiveSplit = False):
                Reads in, carrys out predictions and posts to a csv file. needs work.

predictThis(trainData, testData, clf, preprocess= None, fiveSplit = False):
                Carries out a predition for a sepcific scan / classifier set.


------------------------------------------------------------------------------------------------------------------------------

Neat programs you can quickly write:
Apply transform list and write out (I can now do this one file at a time and minimize memory usage by deleting each entry)
Apply breeding, then transform, then writeout, then delete.
Apply fiveSplit then transform
Apply breeding, then fiveSplit on each.

Per classifier:
CV with selected preictals, return roc_auc
