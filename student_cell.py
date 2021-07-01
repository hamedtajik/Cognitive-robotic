# -*- coding: utf-8 -*-
"""
implementation of a grid cell using the log odds/logit approach from the lecture
"""
from __future__ import print_function, division

import numpy as np



def logit(event):
    """returns log odds with constraints

    Parameters
    ----------
    event : float
        Probability of a cell being occupied when a certain observation is made

    Returns
    -------
    float
        log odds value.

    float : -inf
        If np.log() is used and 1 is passed

    Notes
    -----

    The function is defined on an open interval from 0 to 1 (0, 1). As such,
    all values should be in range 0 < x < 1!
    Ignoring this constraints will result in mathematical errors, e.g. division
    by zero and the like.

    Use test_cell.py to test this function for additional information!

    Raises
    ------
    ZeroDivisionError
        Passed argument is 1.
    ValueError
        Passed argument is 0 and standard math log is used.

    Examples
    --------
    Passing 0 as argument.

    >>> logit(0)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File ".../student_cell.py", line 71, in logit
    ValueError: math domain error

    Passing 1 as argument.

    >>> logit(1)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File ".../student_cell.py", line 71, in logit
    ZeroDivisionError: float division by zero

    Passing 0.1, 0.25, 0.5, 0.75, 0.9 as argument.

    >>> [np.around(logit(x),3) for x in [0.1, 0.25, 0.5, 0.75, 0.9]]
    [-2.1970000000000001, -1.099, 0.0, 1.099, 2.1970000000000001]
    """
    # (i)   Use the log odds transformation for the passed "event" argument.
    #       Hint:   See KSR chapter "4.1 Kartierung" or
    #               https://en.wikipedia.org/wiki/Logit
    res = 0   #TODO: add your code here
    if event>0 and event<1:
     res = np.log(event/(1-event))
     if res != 1.0:
      return res
     
    
    


def inv_logit(logodds):
    """Inverse of the logit function

    Parameters
    ----------
    logodds : float
        The value in logodds transformation.

    Returns
    -------
    float
        Occupation as probability between 0 and 1.

    Raises
    ------
    OverflowError
        When values the values are below -700 and the standard math library is
        used. NumPy is able to handle this without an exception and emits a
        RuntimeWarning instead.

    Examples
    --------
    Passing -711 as argument

    >>> inv_logit(-711)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File ".../student_cell.py", line 122, in inv_logit
    OverflowError: math range error

    Using NumPy:

    >>> inv_logit(-711)
    .../student_cell.py:115: RuntimeWarning: overflow encountered in exp
    0.0

    Passing -100, -2.2, -1.1, 0.0, 1.1, 2.2, 100 as argument.

    >>> [np.around(inv_logit(x),3) for x in [-100, -2.2, -1.1, 0.0, 1.1, 2.2, 100]]
    [0.0, 0.10000000000000001, 0.25, 0.5, 0.75, 0.90000000000000002, 1.0]

    """
    # (ii)  Invert the log odds function to get the event value
    #       Hint:   See (i).
    res = 0  #TODO: add your code here
    res = 1 - (1/(1+np.exp(logodds)))

    return res


class Cell(object):
    """Simple grid cell

    The grid cell is a major component for a grid-based map approach. The cell
    holds the probability for being occupied or free respectively. This is done
    by using the logit or log odds transformation.

    In the initial state, the cell's occupation probability is 0.5 since it
    is not known whether it is occupied or not. Additionally, a threshold
    parameter is added to keep the value in the valid range (otherwise an
    overflow error may occur when trying to invert the transformation).

    Attributes
    ----------
    occ_logit : float
        Occupation probability expressed in its logit form. Initial value is
        logit(0.5).
    logit_threshold : int
        Threshold which is needed because the inv_logit can not handle
        parameters below a certain value.
    """

    def __init__(self):
        self.occ_logit = logit(0.5)
        self.logit_threshold = 100

    def __str__(self):
        return "Cell: P={}".format(inv_logit(self.occ_logit))

    def __repr__(self):
        return str(self)

    def update(self, probability):
        """Update formula

        Parameters
        ----------
        probability : float
            The probability of this cell being occupied.

        Notes
        -----
        In the update step, the logit transformation is applied to the given
        value and is added to the current accumulated value.

        A threshold is applied to avoid overflow errors from the inv_logit()
        function

        Examples
        --------
        Making updates on an initialized cell with 0.6, 0.9, 0.1 and 0.1.

        >>> my_cell = Cell()
        >>> my_cell.occ_logit
        0.0
        >>> my_cell.update(0.6)
        >>> my_cell.occ_logit
        0.4054651081081642
        >>> my_cell.update(0.9)
        >>> my_cell.occ_logit
        2.6026896854443837
        >>> my_cell.update(0.1)
        >>> my_cell.occ_logit
        0.4054651081081646
        >>> my_cell.update(0.1)
        >>> my_cell.occ_logit
        -1.7917594692280545

        Hitting maximum.

        >>> my_cell = Cell()
        >>> my_cell.occ_logit = 99
        >>> my_cell.update(0.9)
        >>> my_cell.occ_logit
        100
        >>> my_cell.update(0.9)
        >>> my_cell.occ_logit
        100

        Hitting minimum.

        >>> my_cell = Cell()
        >>> my_cell.occ_logit = -99
        >>> my_cell.occ_logit
        -99
        >>> my_cell.update(0.1)
        >>> my_cell.occ_logit
        -100
        >>> my_cell.update(0.1)
        >>> my_cell.occ_logit
        -100

        """
        # (iii) Implement the log odds update formula given in the lecture
        #       Hint:   See KSR chapter "4.2 Mapping for Occupancy Grid Maps"
        pass   #TODO: add your code here
        saver= 0
        for i in parameter:
         saver += logit(i)
        parameter = saver
         
        

        # (iv) Apply the threshold value to the probability to keep the value
        #      in a range where the inverse log odds do not result in an
        #      overflow exception
        pass   #TODO: add your code here
        
        if parameter > 100 :
            parameter = 100
        elif parameter < -100:
            parameter = -100
        return parameter
            
            

    def set_probability(self, prop=0.5):
        """Function to manually set the cell value.

        Parameters
        ----------
        prop : float, optional
            The probability that the current cell is occupied.

        Notes
        -----
        This function is needed to read a map from file. If this is not the
        case, this function may not be needed in this exercise.
        """
        self.occ_logit = logit(prop)

    def probability(self):
        """Applies the inverse logit function to the member variable.

        Returns
        -------
        float
            Returns the actual probability of the cell being occupied
        """
        return inv_logit(self.occ_logit)
