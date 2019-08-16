# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 10:53:07 2019

@author: Eesh Gupta
"""
import numpy as np
from Qubit import Qubit
from GateBuilder import gates
import cmath
import math

class register(object): 
    def __init__(self, n): 
        """
        Input: Positive integer n to denote number of qubits
        """
        self.n=n
        self.qubits= self.createQubits()
        self.state_vector=self.createStateVector()
        self.updateStateVector()
        
    def createQubits(self):  
        """
        Input: Number of qubits
        Output: A list of qubit objects
        """
        qubit_list=[]
        for i in range(self.n): 
            qubit_list.append(Qubit(i))
        return qubit_list
    
    def createStateVector(self):
        """
        Output: Create a column vector representation of the tensor product of 
        n qubits
        """
#        state_vector=np.zeros((2**self.n,1))
#        updatestatevector(state_vector)
#        return state_vector
        state_vector={}
        for i in range(2**(self.n)):
            c=self.bin_spec(i)
            state_vector[c]=0.0
        return state_vector
    
    def updateStateVector(self):
        """
        Output: Updates the amplitudes of basis states of combined system
        """
        for key in self.state_vector.keys(): 
            amp=1
            for i in range(len(key)): 
                if key[i] == '0': 
                    amp = amp*(self.qubits[i].a)
                elif key[i] == '1':
                    amp = amp*(self.qubits[i].b)
            self.state_vector[key] = amp
#        
            
    def bin_spec(self, n): 
        """
        Input: int n in assumed decimal representation
        Output: A self.n digit inverted binary representation of n.
        """
        a=self.dec_to_bin(n)
        while len(a) != self.n:
            a = a + '0'
        return a
    
    def dec_to_bin(self,n):
        """
        Input: int n in assumed decimal representation
        Output: Inverted Binary representation of input n
        """
        if n==0: 
            return '0'
        elif n==1: 
            return '1'
        else: 
            return  str(n%2) + self.dec_to_bin(n//2) 
    
    def measure(self, hits): 
        """
        Input: int hits= Number of times the measurements must be performed
        Output: A list of resultant qubits with a length of # of hits
        """
        prob=[]
        keys=[]
        result=[]
        
        #List Of Probabilities
        state_vector= self.stateVector
        state_vector=state_vector.reshape((2**self.n))
        for val in state_vector:
            prob.append(abs(val)**2)
        #List of states
        for key in self.state_vector.keys(): 
            keys.append(key)
        #List of indixes of states
        indices = list(range(0, len(self.state_vector.keys())))
        #Measurement
        draw = np.random.choice(a=indices, size = hits, p=prob)
        for i in range(len(draw)): 
            result.append(keys[draw[i]])
        return result
    
    def applySingleQubitGate(self, gate, target_qubit_index, phase = None): 
        """
        Input: A single qubit gate object to be applied on an int qubit index from qubit 
        list. Input phase if gate is phase shift gate.
        Output: Transformed stateVector
        """
        newGate = gates()
        self.stateVector = newGate.buildApplyGate( gate = gate, 
                                                  target_qubit_index = target_qubit_index, 
                                                  qubits = self.n, 
                                                  stateVector = self.stateVector, 
                                                  phase = phase)
        
    def applyMultiQubitGate(self, gate, control_ind, target_ind): 
        """
        Assumes CNOT Gate
        Input: A multi qubit gate with control qubits specified by int in list 
        of control ind and target qubits specified by int in list target qubit. 
        Output: Transformed stateVector
        """
        basis_labels = []
        newGate = gates()
        
        #getting basis state labels
        for key in self.state_vector.keys(): 
            basis_labels.append(key)
        #calling gate function
        self.stateVector = newGate.CNOT(self, control_ind = control_ind, 
                                        target_ind = target_ind, 
                                        qubit_size = self.n, 
                                        basis_labels = basis_labels,
                                        stateVector = self.stateVector)
    
#getter for self.state_vector
    @property    
    def stateVector(self): 
        """
        Output: Proper array repr of state vector array
        """
        state_vector_arr= np.array([])
        values=[]
        
        #complexify the state_vector_arr
        for i in range(2**self.n): 
            state_vector_arr = np.append(state_vector_arr, [complex(0,0)])
        state_vector_arr = state_vector_arr.reshape((2**self.n, 1))
        
        #Creating repr
        for val in self.state_vector.values():
            values.append(val)
        for i in range(2**self.n):
            state_vector_arr[i,0]=values[i]
        return state_vector_arr
    
    @stateVector.setter
    def stateVector(self, state_vector): 
        """
        Input: An array of values for different basis states
        Function: Assigns those values to respective dict keys in internal
        repr of state vector
        """
        #check for normalization condition
        value = 0 
        for val in state_vector: 
            value += val**2
        if value >=0.999 and value <=1.001: 
            #initializing keys list
            keys=[]
            for key in self.state_vector.keys(): 
                keys.append(key)
            #checking length constraint
            if len(keys) == len(state_vector):
                for i in range(len(keys)): 
                    self.state_vector[keys[i]] = state_vector[i]
            else: 
                raise ValueError("Length of stateVector must be equal to " + 
                                 str(2**self.n) + ".")
        else: 
            raise ValueError("stateVector must be normalized!")

        

            
            
        

