from mujoco_py import load_model_from_xml, MjSim, MjViewer, load_model_from_path
import math
import os
import numpy as np
import matplotlib.pyplot as plt

#code specific imports
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from xml.etree import ElementTree


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def tensegrity_2_xml(K=1, L=1, X=1):

    top = Element('top')

    comment = Comment('Generated for PyMOTW')
    top.append(comment)

    child = SubElement(top, 'child')
    child.text = 'This child contains text.'

    child_with_tail = SubElement(top, 'child_with_tail')
    child_with_tail.text = 'This child has regular text.'
    child_with_tail.tail = 'And "tail" text.'

    child_with_entity_ref = SubElement(top, 'child_with_entity_ref')
    child_with_entity_ref.text = 'This & that'
    return prettify(top)

def run():
    model = load_model_from_path("/Users/zachyamaoka/Documents/de3_group_project/sim/falling_bar.xml")
    # model = load_model_from_path("/Users/zachyamaoka/Documents/de3_group_project/sim/6_Bar.xml")

    sim = MjSim(model)
    viewer = MjViewer(sim)

    t = 0
    vel_data = []
    pos_data = []
    acc_data = []
    time = []
    while True:
        # sim.data.ctrl[0] = math.cos(t / 10.) * 0.01
        # sim.data.ctrl[1] = math.sin(t / 10.) * 0.01
        time.append(t*0.01)
        t += 1
        # sim.step()
        viewer.render()
        if t > 400:
            break
        if t > 100 and os.getenv('TESTING') is not None:
            break

def create_tensegrity(K,L,X):

    return 0
