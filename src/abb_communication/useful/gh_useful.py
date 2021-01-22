'''
. . . . . . . . . . . . . . . . . . . . . 
.                                       .
.    <<      ><      ><       >< <<     .
.    < ><   ><<     ><<<    ><    ><<   .
.    << >< > ><    ><  ><     ><        .  
.    <<  ><  ><   ><<<<<><      ><      .
.    <<      >< ><<     ><< ><    ><<   .
.    <<      ><><<       ><<  >< <<     .
.                                       .
.             DFAB 2016/17              .
. . . . . . . . . . . . . . . . . . . . . 

Created on 22.09.2016

@author: rustr
'''

import Grasshopper as gh
from Grasshopper import DataTree as Tree
from Grasshopper.Kernel.Data import GH_Path as Path
from System import Array
import Rhino.Geometry as rg

def gh_component_timer(ghenv, run, interval):
    if interval <= 0: interval = 1
    ghComp = ghenv.Component
    ghDoc = ghComp.OnPingDocument()
    def callBack(ghDoc):
        ghComp.ExpireSolution(False)
    if run:
        ghDoc.ScheduleSolution(interval, gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack))
        
        
def list_to_tree(alist, none_and_holes=False, base_path=[0]):
    """
    Transforms nestings of lists or tuples to a Grasshopper DataTree
    Usage:
    mytree = [ [1,2], 3, [],[ 4,[5]] ]
    a = list_to_tree(mytree)
    b = list_to_tree(mytree, none_and_holes=True, base_path=[7,1])
    """
    def process_one_item(alist, tree, track):
        path = Path(Array[int](track))
        if len(alist) == 0 and none_and_holes: 
            tree.EnsurePath(path)
            return
        for i,item in enumerate(alist):
            if hasattr(item, '__iter__'): #if list or tuple
                track.append(i)
                process_one_item(item, tree, track)
                track.pop()
            else:
                if none_and_holes: 
                    tree.Insert(item, path, i)
                elif item is not None: 
                    tree.Add(item, path)
                
    tree = Tree[object]()
    if alist is not None: 
        process_one_item(alist, tree, base_path[:])
    return tree

def get_bounding_box_multiple_geometries(G):
    bbmin = []
    bbmax = []
    
    for g in G:
        bb = g.GetBoundingBox(P)
        bbmin.append(bb.Min)
        bbmax.append(bb.Max)
        
    minX = min([p.X for p in bbmin])
    minY = min([p.Y for p in bbmin])
    minZ = min([p.Z for p in bbmin])
    
    maxX = max([p.X for p in bbmax])
    maxY = max([p.Y for p in bbmax])
    maxZ = max([p.Z for p in bbmax])
    
    B = rg.BoundingBox(rg.Point3d(minX, minY, minZ), rg.Point3d(maxX, maxY, maxZ))
    return B
