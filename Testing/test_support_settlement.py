# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 D. Craig Brinck, SE; tamalone1

From:
Structural Analysis, 3rd Edition
Aslam Kassimali
Example 13.14
"""

import unittest
from PyNite import FEModel3D
import math
import sys
from io import StringIO

class Test_Support_Settlement(unittest.TestCase):
    ''' Test for support settlements. '''

    def setUp(self):
        # Suppress printed output temporarily
        sys.stdout = StringIO()

    def tearDown(self):
        # Reset the print function to normal
        sys.stdout = sys.__stdout__

    def test_support_settlement(self):

        # Create a new beam
        beam = FEModel3D()

        # Add nodes
        beam.AddNode('A', 0, 0, 0)
        beam.AddNode('B', 20*12, 0, 0)
        beam.AddNode('C', 40*12, 0, 0)
        beam.AddNode('D', 60*12, 0, 0)

        # Add members
        A = 20
        E = 29000
        G = 11400
        Iy = 1000
        Iz = 7800
        J = 8800
        beam.AddMember('AB', 'A', 'B', E, G, Iy, Iz, J, A)
        beam.AddMember('BC', 'B', 'C', E, G, Iy, Iz, J, A)
        beam.AddMember('CD', 'C', 'D', E, G, Iy, Iz, J, A)

        # Provide supports
        beam.DefineSupport('A', True, True, True, True, False, False)
        beam.DefineSupport('B', False, True, True, False, False, False)
        beam.DefineSupport('C', False, True, True, False, False, False)
        beam.DefineSupport('D', False, True, True, False, False, False)

        # Add a uniform load to the beam
        beam.AddMemberDistLoad('AB', 'Fy', -2/12, -2/12)
        beam.AddMemberDistLoad('BC', 'Fy', -2/12, -2/12)
        beam.AddMemberDistLoad('CD', 'Fy', -2/12, -2/12)

        # Add support settlements
        beam.AddNodeDisplacement('B', 'DY', -5/8)
        beam.AddNodeDisplacement('C', 'DY', -1.5)
        beam.AddNodeDisplacement('D', 'DY', -0.75)

        # Analyze the beam
        beam.Analyze()

        # Below are the textbook reactions given in the back of the textbook
        textbook_rxns = [('A', -1.098),
                         ('B',  122.373),
                         ('C', -61.451),
                         ('D',  60.176)]

        # Check each textbook value against the PyNite calculated value
        for name, text_rxn in textbook_rxns:

            # The `subTest` context manager prints which, if any, of the nodes fail the test
            with self.subTest(node=name):

                # Get the reaction at the node
                PyNite_rxn = beam.Nodes[name].RxnFY['Combo 1']

                # There are some known rounding errors in the "textbook values" listed above. These
                # rounding errors cause up to a 7.6% difference from the theoretical solution.
                # Check that the PyNite reactions are within 7.6% of the textbook values
                self.assertLess(abs(PyNite_rxn/text_rxn - 1), 0.076)
