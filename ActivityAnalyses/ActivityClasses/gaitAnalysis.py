# -*- coding: utf-8 -*-
"""
    ---------------------------------------------------------------------------
    OpenCap processing: gaitAnalysis.py
    ---------------------------------------------------------------------------

    Copyright 2023 Stanford University and the Authors
    
    Author(s): Antoine Falisse, Scott Uhlrich
    
    Licensed under the Apache License, Version 2.0 (the "License"); you may not
    use this file except in compliance with the License. You may obtain a copy
    of the License at http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import os
import sys
sys.path.append('../../')
                
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from utilsKinematics import kinematics
from utilsProcessing import lowPassFilter
from utilsTRC import trc_2_dict


class gait_analysis(kinematics):
    
    def __init__(self, sessionDir, trialName, leg='auto',
                 lowpass_cutoff_frequency_for_coordinate_values=-1,
                 n_gait_cycles=1):
        
        # inherit init from kinematics class
        super().__init__(sessionDir, trialName, 
                     lowpass_cutoff_frequency_for_coordinate_values=lowpass_cutoff_frequency_for_coordinate_values)
                        
        # Marker data load and filter
        trcFilePath = os.path.join(sessionDir,'MarkerData',
                                    '{}.trc'.format(trialName))
        self.markerDict = trc_2_dict(trcFilePath)
        if lowpass_cutoff_frequency_for_coordinate_values > 0:
            self.markerDict['markers'] = {
                 marker_name: lowPassFilter(self.time, data, lowpass_cutoff_frequency_for_coordinate_values) \
                 for marker_name, data in self.markerDict['markers'].items()}

        # Coordinate values            
        self.coordinateValues = self.get_coordinate_values()
        
        # Segment gait cycles
        self.gaitEvents = self.segment_walking(n_gait_cycles=n_gait_cycles,leg=leg)
        self.nGaitCycles = np.shape(self.gaitEvents['ipsilateralIdx'])[0]
        
        # determine treadmill speed (0 if overground)
        self.treadmillSpeed = self.compute_treadmill_speed()
        
        # Compute COM trajectory and gait frame...used in multiple scalar computations
        self.comValues = self.get_center_of_mass_values()
        self.R_world_to_gait = self.compute_gait_frame()
                
    def compute_scalars(self,scalarNames):
               
        # verify that scalarNames are methods in gait_analysis        
        method_names = [func for func in dir(self) if callable(getattr(self, func))]
        possibleMethods = [entry for entry in method_names if 'compute_' in entry]
        
        if scalarNames is None:
            print('No scalars defined, these methods are available:')
            print(*possibleMethods)
            return
        
        nonexistant_methods = [entry for entry in scalarNames if 'compute_' + entry not in method_names]
        
        if len(nonexistant_methods) > 0:
            raise Exception(str(['compute_' + a for a in nonexistant_methods]) + ' not in gait_analysis class.')
        
        scalarDict = {}
        for scalarName in scalarNames:
            thisFunction = getattr(self, 'compute_' + scalarName)
            scalarDict[scalarName] = thisFunction()
        
        return scalarDict
    
    def compute_stride_length(self):

        # get calc positions based on self.gaitEvents['leg'] from self.markerDict
        if self.gaitEvents['ipsilateralLeg'] == 'r':
            leg = 'r'
        else:
            leg = 'L'
        calc_position = self.markerDict['markers'][leg + '_calc_study']

        # find stride length on treadmill
        # difference in ipsilateral calcaneus position at heel strike + treadmill speed * time
        strideLength = np.linalg.norm(calc_position[self.gaitEvents['ipsilateralIdx'][:,:1]] - \
                           calc_position[self.gaitEvents['ipsilateralIdx'][:,2:3]], axis=2) + \
                           self.treadmillSpeed * np.diff(self.gaitEvents['ipsilateralTime'][:,(0,2)])
        
        # average across all strides
        strideLength = np.mean(strideLength)
        
        return strideLength
    
    def compute_gait_speed(self):
                           
        comValuesArray = np.vstack((self.comValues['x'],self.comValues['y'],self.comValues['z'])).T
        gait_speed = (np.linalg.norm(comValuesArray[self.gaitEvents['ipsilateralIdx'][:,:1]] - \
                           comValuesArray[self.gaitEvents['ipsilateralIdx'][:,2:3]], axis=2)) / \
                           np.diff(self.gaitEvents['ipsilateralTime'][:,(0,2)]) + self.treadmillSpeed 
        
        # average across all strides
        gait_speed = np.mean(gait_speed)
        
        return gait_speed
    
    def compute_treadmill_speed(self):
        if self.gaitEvents['ipsilateralLeg'] == 'r':
            leg = 'r'
        else:
            leg = 'L'
        foot_position = self.markerDict['markers'][leg + '_ankle_study']
        
        stanceTimeLength = np.round(np.diff(self.gaitEvents['ipsilateralIdx'][:,:2]))
        startIdx = np.round(self.gaitEvents['ipsilateralIdx'][:,:1]+.1*stanceTimeLength).astype(int)
        endIdx = np.round(self.gaitEvents['ipsilateralIdx'][:,1:2]-.3*stanceTimeLength).astype(int)
            
        # average instantaneous velocities
        dt = np.diff(self.markerDict['time'][:2])[0]
        for i in range(self.nGaitCycles):
            footVel = np.linalg.norm(np.mean(np.diff(
                foot_position[startIdx[i,0]:endIdx[i,0],:],axis=0),axis=0)/dt)
        
        treadmillSpeed = np.mean(footVel)
        
        # overground
        if treadmillSpeed < .3:
            treadmillSpeed = 0
                           
        return treadmillSpeed
    
    def compute_step_width(self):
        # get ankle joint center positions
        if self.gaitEvents['ipsilateralLeg'] == 'r':
            leg = 'r'
            contLeg = 'L'
        else:
            leg = 'L'
            contLeg = 'r'
        ankle_position_ips = (self.markerDict['markers'][leg + '_ankle_study'] + 
                          self.markerDict['markers'][leg + '_mankle_study'])/2
        ankle_position_cont = (self.markerDict['markers'][contLeg + '_ankle_study'] + 
                          self.markerDict['markers'][contLeg + '_mankle_study'])/2
        
        ankleVector = ankle_position_cont[self.gaitEvents['contralateralIdx'][:,1]] - \
                      ankle_position_ips[self.gaitEvents['ipsilateralIdx'][:,0]]
                      
        ankleVector_inGaitFrame = np.array([np.dot(ankleVector[i,:], self.R_world_to_gait[i,:,:]) \
                                            for i in range(self.nGaitCycles)])
        
        # step width is z distance
        stepWidth = np.abs(ankleVector_inGaitFrame[:,2])
        
        # average across gait cycles
        stepWidth = np.mean(stepWidth)
        
        return stepWidth
        
    def compute_gait_frame(self):
        # Create frame for each gait cycle  with x: pelvis heading, 
        # z: average vector between ASIS during gait cycle, y: cross. 
        
        # Pelvis center trajectory (for overground heading vector)
        pelvisMarkerNames = ['r.ASIS_study','L.ASIS_study','r.PSIS_study','L.PSIS_study']
        pelvisMarkers = [self.markerDict['markers'][mkr]  for mkr in pelvisMarkerNames]
        pelvisCenter = np.mean(np.array(pelvisMarkers),axis=0)
        
        # ankle trajectory (for treadmill heading vector)
        leg = self.gaitEvents['ipsilateralLeg']
        if leg == 'l': leg='L'
        anklePos = self.markerDict['markers'][leg + '_ankle_study']
        
        # vector from left ASIS to right ASIS (for mediolateral direction)
        asisMarkerNames = ['L.ASIS_study','r.ASIS_study']
        asisMarkers = [self.markerDict['markers'][mkr]  for mkr in asisMarkerNames]
        asisVector = np.squeeze(np.diff(np.array(asisMarkers),axis=0))
        
        # heading vector per gait cycle
        # if overground, use pelvis center trajectory; treadmill: ankle trajectory
        if self.treadmillSpeed == 0:
            x = np.diff(pelvisCenter[self.gaitEvents['ipsilateralIdx'][:,(0,2)],:],axis=1)[:,0,:]
            x = x / np.linalg.norm(x,axis=1,keepdims=True)
        else: 
            x = np.zeros((self.nGaitCycles,3))
            for i in range(self.nGaitCycles):
                x[i,:] = anklePos[self.gaitEvents['ipsilateralIdx'][i,2]] - \
                         anklePos[self.gaitEvents['ipsilateralIdx'][i,1]]
            x = x / np.linalg.norm(x,axis=1,keepdims=True)
            
        # mean ASIS vector over gait cycle
        z = np.zeros((self.nGaitCycles,3))
        for i in range(self.nGaitCycles):
            z[i,:] = np.mean(asisVector[self.gaitEvents['ipsilateralIdx'][i,0]: \
                             self.gaitEvents['ipsilateralIdx'][i,2]],axis=0)
        z = z / np.linalg.norm(z,axis=1,keepdims=True)
        
        # cross to get y
        y = np.cross(z,x)
        
        # 3x3xnSteps
        R_lab_to_gait = np.stack((x.T,y.T,z.T),axis=1).transpose((2, 0, 1))
        
        return R_lab_to_gait
    
    def get_coordinates_normalized_time(self):
        
        colNames = self.coordinateValues.columns
        data = self.coordinateValues.to_numpy(copy=True)
        coordValuesNorm = []
        for i in range(self.nGaitCycles):
            coordValues = data[self.gaitEvents['ipsilateralIdx'][i,0]:self.gaitEvents['ipsilateralIdx'][i,2]]
            coordValuesNorm.append(np.stack([np.interp(np.linspace(0,100,101),
                                   np.linspace(0,100,len(coordValues)),coordValues[:,i]) \
                                   for i in range(coordValues.shape[1])],axis=1))
             
        coordinateValuesTimeNormalized = {}
        # average
        coordVals_mean = np.mean(np.array(coordValuesNorm),axis=0)
        coordinateValuesTimeNormalized['mean'] = pd.DataFrame(data=coordVals_mean, columns=colNames)
        
        #return to dataframe
        coordinateValuesTimeNormalized['indiv'] = [pd.DataFrame(data=d, columns=colNames) for d in coordValuesNorm]
        
        return coordinateValuesTimeNormalized

    def segment_walking(self, n_gait_cycles=1, leg='auto', visualize=False):
        # subtract sacrum from foot
        # visually, it looks like the position-based approach will be more robust
        r_calc_rel_x = (self.markerDict['markers']['r_calc_study'] - self.markerDict[
                                     'markers']['r.PSIS_study'])[:,0]
        r_toe_rel_x = (self.markerDict['markers']['r_toe_study'] - self.markerDict[
                                    'markers']['r.PSIS_study'])[:,0]

        # repeat for left
        l_calc_rel_x = (self.markerDict['markers']['L_calc_study'] - self.markerDict[
                                     'markers']['L.PSIS_study'])[:,0]
        l_toe_rel_x = (self.markerDict['markers']['L_toe_study'] - self.markerDict[
                                    'markers']['L.PSIS_study'])[:,0]
        
        # Find HS
        rHS, _ = find_peaks(r_calc_rel_x)
        lHS, _ = find_peaks(l_calc_rel_x)
        
        # Find TO
        rTO, _ = find_peaks(-r_toe_rel_x)
        lTO, _ = find_peaks(-l_toe_rel_x)
        
        if visualize==True:
            import matplotlib.pyplot as plt
            plt.close('all')
            plt.figure(1)
            plt.plot(self.markerDict['time'],r_toe_rel_x,label='toe')
            plt.plot(self.markerDict['time'],r_calc_rel_x,label='calc')
            plt.scatter(self.markerDict['time'][rHS], r_calc_rel_x[rHS], color='red', label='rHS')
            plt.scatter(self.markerDict['time'][rTO], r_toe_rel_x[rTO], color='blue', label='rTO')
            plt.legend()

            plt.figure(2)
            plt.plot(self.markerDict['time'],l_toe_rel_x,label='toe')
            plt.plot(self.markerDict['time'],l_calc_rel_x,label='calc')
            plt.scatter(self.markerDict['time'][lHS], l_calc_rel_x[lHS], color='red', label='lHS')
            plt.scatter(self.markerDict['time'][lTO], l_toe_rel_x[lTO], color='blue', label='lTO')
            plt.legend()

        # find the number of gait cycles for the foot of interest
        if leg=='auto':
            # find the last HS of either foot
            if rHS[-1] > lHS[-1]:
                leg = 'r'
            else:
                leg = 'l'
        
        # find the number of gait cycles for the foot of interest
        if leg == 'r':
            hsIps = rHS
            toIps = rTO
            hsCont = lHS
            toCont = lTO
        elif leg == 'l':
            hsIps = lHS
            toIps = lTO
            hsCont = rHS
            toCont = rTO

        n_gait_cycles = np.min([n_gait_cycles, len(hsIps)-1])
        gaitEvents_ips = np.zeros((n_gait_cycles, 3),dtype=np.int)
        gaitEvents_cont = np.zeros((n_gait_cycles, 2),dtype=np.int)
        if n_gait_cycles <1:
            raise Exception('Not enough gait cycles found.')

        for i in range(n_gait_cycles):
            # ipsilateral HS, TO, HS
            gaitEvents_ips[i,0] = hsIps[-i-2]
            gaitEvents_ips[i,2] = hsIps[-i-1]
            
            # iterate in reverse through ipsilateral TO, finding the one that is within the range of gaitEvents_ips
            toIpsFound = False
            for j in range(len(toIps)):
                if toIps[-j-1] > gaitEvents_ips[i,0] and toIps[-j-1] < gaitEvents_ips[i,2] and not toIpsFound:
                    gaitEvents_ips[i,1] = toIps[-j-1]
                    toIpsFound = True

            # contralateral TO, HS
            # iterate in reverse through contralateral HS and TO, finding the one that is within the range of gaitEvents_ips
            hsContFound = False
            toContFound = False
            for j in range(len(toCont)):
                if toCont[-j-1] > gaitEvents_ips[i,0] and toCont[-j-1] < gaitEvents_ips[i,2] and not toContFound:
                    gaitEvents_cont[i,0] = toCont[-j-1]
                    toContFound = True
                    
            for j in range(len(hsCont)):
                if hsCont[-j-1] > gaitEvents_ips[i,0] and hsCont[-j-1] < gaitEvents_ips[i,2] and not hsContFound:
                    gaitEvents_cont[i,1] = hsCont[-j-1]
                    hsContFound = True
            
            # making contralateral gait events optional
            if not toContFound or not hsContFound:                   
                raise Warning('Could not find contralateral gait event within ipsilateral gait event range.')
                gaitEvents_cont[i,0] = np.nan
                gaitEvents_cont[i,1] = np.nan
            
            # convert gaitEvents to times using self.markerDict['time']
            gaitEventTimes_ips = self.markerDict['time'][gaitEvents_ips]
            gaitEventTimes_cont = self.markerDict['time'][gaitEvents_cont]
                            
        gaitEvents = {'ipsilateralIdx':gaitEvents_ips,
                      'contralateralIdx':gaitEvents_cont,
                      'ipsilateralTime':gaitEventTimes_ips,
                      'contralateralTime':gaitEventTimes_cont,
                      'eventNamesIpsilateral':['HS','TO','HS'],
                      'eventNamesContralateral':['TO','HS'],
                      'ipsilateralLeg':leg}
        
        return gaitEvents       