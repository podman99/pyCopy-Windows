import os.path
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Keith Jasper"
__date__ ="$05-Feb-2014 12:52:04$"

import sys
import os
import shutil
import time


class PyCopy:
    defaultdst = "Z:\\pytest"
    dst = False
    src = False
    bytecount = 0
    skipcount = 0
    completecount = 0
    dircount = 0
    
    def __init__(self, args):
        print "argCount: ", len(args)
        print "String: ", str(sys.argv)
        self.src = sys.argv[1]
        if len(args) == 3:
            self.dst = sys.argv[2]
        else:
            self.dst = self.defaultdst
        
    
    def debug(self):
        print "Printing Destination: ", self.dst


        if self.src == False:
            print "SRC is False!"
            sys.exit(9)
            
        if self.dst == False:
            print "DST is False!"
            sys.exit(9)
    
    def checkSrc(self):
        return os.path.isdir(self.src)
    
    def checkDst(self):
        return os.path.isdir(self.dst)
       
        
    def runCopy(self):
        if self.checkSrc() == False:
            print "Src is not a directory"
            sys.exit(9)
            
        if self.checkDst() == False:
            print "Dst is not a directory"
            sys.exit(9)
            
        self.copyTree(self.src, self.dst + "\\Backup")
        
    def copyTree(self, src, dst, symlinks=False, ignore=None):
        errors = []
        
        names = os.listdir(src)
        if ignore is not None:
            ignored_names = ignore(src, names)
        else:
            ignored_names = set()

        try:
            os.makedirs(dst)
        except OSError, e:
            if e[0] != 0:
                print str(e)
        
        for name in names:
            if name in ignored_names:
                continue
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            try:
                if symlinks and os.path.islink(srcname):
                    linkto = os.readlink(srcname)
                    os.symlink(linkto, dstname)
                    print "Creating Link: ", srcname, "\t---> " , dstname
                elif os.path.isdir(srcname):
                    print "Traversing Directory: ", srcname, "\t---> " , dstname
                    self.dircount = self.dircount + 1
                    self.copyTree(srcname, dstname, symlinks, ignore)
                else:
                    srctime = time.ctime(os.path.getmtime(srcname))
                    if os.path.isfile(dstname):
                        dsttime = time.ctime(os.path.getmtime(dstname))
                    else:
                        dsttime = 0
                    if srctime != dsttime:
                        print "Copying: ", srcname, "\t---> " , dstname
                        shutil.copy2(srcname, dstname)
                        self.completecount = self.completecount + 1
                        self.bytecount = self.bytecount + os.path.getsize(srcname)
                    else:
                        self.skipcount = self.skipcount + 1
                        print "SKIPPING: ", srcname, "\t---> " , dstname, "\tFile Exists"
                # XXX What about devices, sockets etc.?
            except IOError, e:
                errors.append((srcname, dstname, str(e)))
            # catch the Error from the recursive copytree so that we can
            # continue with other files
            except OSError, e:
                errors.extend(e.args[0])
        
        if errors:
            raise Error(errors)

    def PrintFinish(self):
        print ""
        print ""
        print "-----------------------------------------------"
        print "Copied Files:\t\t", self.completecount
        print "Total Mb:\t\t", self.bytecount / 1024 / 1024
        print "Skipped Files:\t\t", self.skipcount
        print "Number of Directories:\t", self.dircount
        print "-----------------------------------------------"

if __name__ == "__main__":
    if len(sys.argv) == 3:
        copy = PyCopy(sys.argv)
        copy.debug()
        copy.runCopy()
        copy.PrintFinish()
    elif len(sys.argv) == 2:
        copy = PyCopy(sys.argv)
        copy.debug()
        copy.runCopy()
        copy.PrintFinish()
    else:
        print "Number of Arguments: ", len(sys.argv)
        print "argument list", str(sys.argv)
    
    
    
    
    