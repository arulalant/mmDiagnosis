import xml.etree.ElementTree as ET
from cdms2 import CDMLParser
import cdms2
import sys
import os


def updateCdmlFile(ufilepath, inputxml, outputxml=None):
    """
    ufilepath - update file path absolute/relative path
    inputxml - existing cdml file
    outputxml - updated xml file will be stored. By default
                it takes None. In that case, it will over write
                the inputxml file itself.

    Written By : Arulalan.T

    Date : 09.10.2013

    """

    tree = ET.parse(inputxml)
    root = tree.getroot()

    ufilepath = os.path.relpath(ufilepath)

    f = cdms2.open(ufilepath)
    fvariables = f.listvariables()

    # convert the datafile variables list string into lower case str
    #fvariables = str(fvariables).lower()[1:-1]
    ## again convert it back to list itself
    #fvariables = fvariables.split(',')

    root_attributes = root.attrib
    directory = root_attributes.get('directory', "")

    if not directory in ufilepath:
        sys.exit()
  
    if directory:
        filepath = ufilepath.split(directory)[-1]
    else:
        filepath = ufilepath

    cdms_filemap_entry = root_attributes.get('cdms_filemap')
    # get the fist close braket index
    close_brak_idx = cdms_filemap_entry.find("]")
    # get the vars as string
    cdms_filemap_vars = cdms_filemap_entry[3:close_brak_idx]
    # get the vars as list contains string variables
    cdms_filemap_vars = cdms_filemap_vars.split(',')

    # get the difference b/w cdms_filemap_vars and datafile variables
    diff_vars = set(cdms_filemap_vars).symmetric_difference(set(fvariables))
    if diff_vars:
        # write code here for get the difference is in either fvariables or
        # in cdms_filemap_vars.. then proceed further
        print diff_vars
        sys.exit()

    firstvar = fvariables[0]
    ftime = f[firstvar].getTime().asComponentTime()

    newlength = ''
    partition_extend = ''
    root.findall("./variable/domain/domElem[@name='time']")

    for axis in root.findall("./axis[@id='time']"):
        units = axis.get('units', '')
        # get the time index of the update/new datafile
        newTimeIdx = int(ftime[0].torel(units).value)
        length = int(axis.get('length', 0))
        newlength = str(length + 1)
        # update the axis length
        axis.attrib['length'] = newlength

        partition = axis.get('partition')
        partition_extend = [str(newTimeIdx), str(newTimeIdx + 1)]
        partition = partition[:-1] + ' ' + ' '.join(partition_extend) + ']'
        # update the partition
        axis.attrib['partition'] = partition

        tindex = axis.text.strip()
        tindex = tindex[:-1] + '  ' + str(newTimeIdx) + '.' + ']'
        # update the text (actual time index)
        axis.text = tindex
    # end of for axis in root.findall(...):

    for domElem in root.findall("./variable/domain/domElem[@name='time']"):
        domElem.attrib['length'] = newlength
    # end of for domElem in root.findall(...):

    newentry = '[' + ','.join(partition_extend) + ',-,-,-,' + filepath + "]]]]"
    if newentry in cdms_filemap_entry:
        print "Already directory path '%s' is exists in cdms_filemap", newentry
        print "So not going to create/update xml file"
        #sys.exit()
    else:    
        cdms_filemap_entry = cdms_filemap_entry[:-3] + ',' + newentry
        # assign the updated cdms_filemap with new file path entry...
        root_attributes['cdms_filemap'] = cdms_filemap_entry

        p = CDMLParser.CDMLParser()
        p.feed(ET.tostring(root))
        if outputxml:
            p.root.dump(outputxml)
            print "Created updated cdml file", outputxml
        else:
            p.root.dump(inputxml)
            print "Updated cdml file", inputxml
        # end of if outputxml:
        p.close()
    # end of if newentry in cdms_filemap_entry:
# end of def updateCdmlFile(ufilepath, inputxml, outputxml=None):

if __name__ == '__main__':

    ufilepath = sys.argv[1]
    infile = sys.argv[2]
    updateCdmlFile(ufilepath, infile)
# end of if __name__ == '__main__':







