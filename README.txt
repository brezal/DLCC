DNA Localised Circuit Compiler - DLCC v1.0

################
# Installation #
################
Requires:
- Python > 2.7
- matplotlib (http://matplotlib.org/)
- networkx (https://networkx.github.io/)
- pyparsing (https://pyparsing.wikispaces.com/)
- Prism (http://www.prismmodelchecker.org/)


################
#   Running    #
################
Run from the command line like this:   python dlcc.py tests/test1.dlin
Input files are given the .dlin extension.
Output files will be saved to a timestamped directory in the "out" folder.


######################################################
#   Compatibility Between PRISM and OSX El Capitan   #
######################################################
This bug has nothing to do with DLCC, other but is just a compatibility issue bewteen PRISM and Mac OSX El Capitan.  After installing PRISM using the install.sh script, you may get a 'Library not loaded: ../../lib/libdd.dylib' error.  This can occur when PRISM looks for java in the wrong place.  To fix it, run 'locate java' in the terminal and copy the path of your java directory.  Open the prism script (located in the bin directory) and change the value of the PRISM_JAVA variable to the correct directory.  For me, it's 'PRISM_JAVA=/Library/Java/JavaVirtualMachines/jdk1.8.0_51.jdk/Contents/Home/bin/java'.  That should fix it.  There's more information on this bug at http://stackoverflow.com/questions/33033283/prism-model-checker-library-not-loaded-lib-libdd-dylib-after-upgrading-t.


################
#   Precision  #
################
Track lengths (in anchorages) are given an upper bound of 20 (the number that you can fit on an origami tile).
If a track longer than 20 is required to meet the MCE tolerance, DLCC will give a precision error.
  

################
#Tests/Examples#
################
Sample input files are provided in the "tests" folder.

- test1.dlin
  Description: Compound propositional formula that can be readily solved with a low MCE tolerance (P(error) = 0.10).  

- test2.dlin
  Description: Example of topological refinement.  DLCC detects and eliminates a double negative to make a simpler but equivalent circuit.

- test3.dlin
  Description: Example of a problem that is difficult for a localised circuit to solve.  Even with a MCE tolerance of P(error) = 0.5, we still get very long tracks.

- test4.dlin
  Description: Very simple test/debugging case of ¬x.


################
#   Graphics   #
################
Can be buggy and sometimes you get tracks that overlap.  Since the simple representation is just to give the scale of the lengths, and not really how the track would be organised on an origami tile, we didn't put much time into the visualisation.


################
#In Development#
################
We're still working on a few features like:
- fanout
- a walker that can block a track and keep on walking, potentially blocking other tracks thereafter


####################
#Questions/Comments#
####################
Please do not hesitate to get in touch at michael.boemo@physics.ox.ac.uk.


####################
#    License       #
####################
DLCC is covered by the GNU General Public License v3 (outlined in license.txt in the top directory).

