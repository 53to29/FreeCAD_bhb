#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MeshGetElements.py
#
#  Copyright (C) 2016  Ulrich Brammer <ulrich1a@users.sourceforge.net>
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
#  MA  02110-1301  USA

__title__="FreeCAD mesh get element test macro"
__author__ =  "Ulrich Brammer <ulrich1a@users.sourceforge.net>"
__url__ = ["http://www.freecadweb.org"]


'''Version 2 
Select Faces from an Object and the Analysis for this Object and run the macro

The Analysis needs to have a mesh

'''

import FreeCAD
import Fem
import FemMeshTools
#import ccxInpWriter
import time
import FreeCADGui



class MeshInfo(object):
  def __init__(self, theMesh):
    # the new node dictionary with element information
    # the node_dict contains for each node its membership in elements
    # stored informatation are: 
    # element number, the number of nodes per element, the position of the node in the element.
    # The position of the node in the element is coded as a set bit at that position in bit array (integer)
    # Fixme: the number of nodes per element should be replaced by the type of the element
    # but I did not know, how to get this from the mesh.
    self.node_dict = {}
    # initialize the node-dict so we get an ordered structure
    for node in theMesh.Nodes:
      self.node_dict[node]=[]
    # print node_dict

    # The ele_dict holds later an integer (bit array) for each element, which gives us
    # the information we are searching for:
    # Is this element part of the node list (searching for elements) or
    # has this element a face we are searching for?
    # The number in the ele_dict is organized as a bit array.
    # The corresponding bit is set, if the node of the node_list 
    # is contained in the element.
    self.ele_dict = {}

    # filling the node_dict
    for ele in theMesh.Volumes:
      self.ele_dict[ele] = 0 # initializing the ele_dict, in order to get an ordered structure
      eleList = theMesh.getElementNodes(ele)
      print 'eleList: ', eleList
      theLen = len(eleList)
      pos = int(1)
      for elNode in eleList:
        self.node_dict[elNode].append([ele, theLen, pos])
        # x << n x shifted left by n bits = Multiplication
        pos = pos << 1
    print 'node_dict: ', self.node_dict
    # fuer jeden Knoten Liste [element nummer, anzahle elementknoten (10 fuer tetra10), postion (???)]
    print 'empty ele_dict: ', self.ele_dict

    # The node_dict and the initialized empty ele_dict can be reused for other searches.

  def getccx_faces(self, node_list):
    # Now we are looking for nodes inside of the Faces = filling the ele_dict
    e_dict = self.ele_dict.copy()
    for node in node_list:
      for nList in self.node_dict[node]:
        print nList
        e_dict[nList[0]] = e_dict[nList[0]] + nList[2]
    print  'e_dict: ', e_dict

    ele_list = [] # The ele_list contains the result of the search.
    for ele in e_dict:
      if (411 & e_dict[ele]) == 411:
        #print "411 Face P2: ", ele
        ele_list.append([ele, 'P2'])
      if (119 & e_dict[ele]) == 119:
        #print "119 Face P1: ", ele
        ele_list.append([ele, 'P1'])
      if (717 & e_dict[ele]) == 717:
        #print "717 Face P3: ", ele
        ele_list.append([ele, 'P3'])
      if (814 & e_dict[ele]) == 814:
        #print "814 Face P4: ", ele
        ele_list.append([ele, 'P4'])
    print "found Faces: ", len(ele_list)
    print "ele_list: ", ele_list
    return ele_list


mylist = FreeCADGui.Selection.getSelectionEx()
mat_list = None
print 'The Selection: ',mylist
print 'count of Selections: ', mylist.__len__()

theFaceList = []

for o in FreeCADGui.Selection.getSelectionEx():
  print o.ObjectName

  if hasattr(o.Object,"Shape"):
    print 'The Object ', o.ObjectName, ' has a Shape.'
    if hasattr(o.Object.Shape,"Solids"):
      print 'The Object has ', len(o.Object.Shape.Solids), ' Solids.'
      theShape = o.Object.Shape.Solids[0]
    if hasattr(o.Object.Shape,"Faces"):
      print 'The Object has ', len(o.Object.Shape.Faces), ' Faces.'
      #theFaceList = o.Object.Shape.Faces

      for s in o.SubElementNames:
        print "SubElementName: ",s
      for s in o.SubObjects:
        print "object: ",s
        theFaceList.append(s)
      print 'theFaceList: ', theFaceList


  if o.ObjectName == 'Analysis':
    print 'found an Analysis'
    for s in o.Object.OutList:
      if s.TypeId == "App::MaterialObjectPython":
        print 'found a material: '
        if mat_list:
          mat_list.append(s)
        else:
          mat_list = [s]

      if s.TypeId == "Fem::FemMeshShapeNetgenObject":
        theMesh = s.FemMesh



if theMesh:
    ## This is the call of code of the current FEM-workbench
    # it measures the time to get the required node_list 
    nodeStart = time.clock()
    node_list = []
    if len(theFaceList) >0:
        for anFace in theFaceList:
            node_list = node_list + theMesh.getNodesByFace(anFace)
            print 'len(node_list): ', len(node_list)
            print 'the Face: ', anFace
    node_list = set(node_list) # This is needed to delete duplicates!
    #else:
        #node_list = theMesh.Nodes
    nodeEnd = time.clock()
    nodeTime = nodeEnd - nodeStart
    print 'node_list: ', node_list

    startZeit = time.clock()

    M_info = MeshInfo(theMesh)

    ccx_faces = M_info.getccx_faces(node_list)

    endZeit = time.clock()
    print 'node search time: ', nodeTime, ' Face search time: ', endZeit - startZeit


    startFemTime = time.clock()
    # here is the original code from FemMeshTools used to create the Volumes with Face info for ccx
    ref_face_volume_elements = []
    for ref_face in theFaceList:
        ref_face_volume_elements = ref_face_volume_elements + theMesh.getccxVolumesByFace(ref_face)
    print 'Original method faces: ', len(ref_face_volume_elements)
    endFemTime = time.clock()
    print 'Original method face search time: ', endFemTime - startFemTime



