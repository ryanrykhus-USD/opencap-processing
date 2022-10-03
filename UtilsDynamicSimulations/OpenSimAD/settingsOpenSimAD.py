'''
    ---------------------------------------------------------------------------
    OpenCap processing: settingsOpenSimAD.py
    ---------------------------------------------------------------------------
    Copyright 2022 Stanford University and the Authors
    
    Author(s): Antoine Falisse, Scott Uhlrich
    
    Licensed under the Apache License, Version 2.0 (the "License"); you may not
    use this file except in compliance with the License. You may obtain a copy
    of the License at http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    
    This script contains settings of the trajectory optimization problem that
    we found worked well for a set of activities. We encourage users to play
    around with these settings until they are satisfied with their results. We
    cannot guarantee that the settings will 1) make your problem converge and
    2) make your problem converge to a biomechanically meaningful solution. We
    also encourage users to explore mainOpenSimAD, since many more settings can
    be tuned and are not exposed here.
'''

def get_default_setup(motion_type):

    setups = {}   
    setups['other'] = {
        'ipopt_tolerance': 3,
        'weights': {
            'positionTrackingTerm': 100,
            'velocityTrackingTerm': 10,
            'accelerationTrackingTerm': 50,
            'activationTerm': 10,
            'armExcitationTerm': 0.001,
            'lumbarExcitationTerm': 0.001,
            'jointAccelerationTerm': 0.001,
            'activationDtTerm': 0.001,
            'forceDtTerm': 0.001},            
        'coordinates_toTrack': {
            'pelvis_tilt': {"weight": 10},
            'pelvis_list': {"weight": 10},
            'pelvis_rotation': {"weight": 10},
            'pelvis_tx': {"weight": 10},
            'pelvis_ty': {"weight": 10},
            'pelvis_tz': {"weight": 10}, 
            'hip_flexion_l': {"weight": 20},
            'hip_adduction_l': {"weight": 10},
            'hip_rotation_l': {"weight": 1},
            'hip_flexion_r': {"weight": 20},
            'hip_adduction_r': {"weight": 10},
            'hip_rotation_r': {"weight": 1},
            'knee_angle_l': {"weight": 10},
            'knee_angle_r': {"weight": 10},
            'ankle_angle_l': {"weight": 10},
            'ankle_angle_r': {"weight": 10},
            'subtalar_angle_l': {"weight": 10},
            'subtalar_angle_r': {"weight": 10},
            'lumbar_extension': {"weight": 10},
            'lumbar_bending': {"weight": 10},
            'lumbar_rotation': {"weight": 10},
            'arm_flex_l': {"weight": 10},
            'arm_add_l': {"weight": 10},
            'arm_rot_l': {"weight": 10},
            'arm_flex_r': {"weight": 10},
            'arm_add_r': {"weight": 10},
            'arm_rot_r': {"weight": 10},
            'elbow_flex_l': {"weight": 10},
            'elbow_flex_r': {"weight": 10},
            'pro_sup_l': {"weight": 10},
            'pro_sup_r': {"weight": 10}},
        'coordinate_constraints': {
            'pelvis_tx': {"env_bound": 0.1}},
        'ignorePassiveFiberForce': True}
    
    setups['running'] = {
        'ipopt_tolerance': 3,
        'weights': {
            'positionTrackingTerm': 100,
            'velocityTrackingTerm': 10,
            'accelerationTrackingTerm': 50,
            'activationTerm': 10,
            'armExcitationTerm': 0.001,
            'lumbarExcitationTerm': 0.001,
            'jointAccelerationTerm': 0.001,
            'activationDtTerm': 0.001,
            'forceDtTerm': 0.001},            
        'coordinates_toTrack': {
            'pelvis_tilt': {"weight": 10},
            'pelvis_list': {"weight": 10},
            'pelvis_rotation': {"weight": 10},
            'pelvis_tx': {"weight": 10},
            'pelvis_ty': {"weight": 10},
            'pelvis_tz': {"weight": 10}, 
            'hip_flexion_l': {"weight": 20},
            'hip_adduction_l': {"weight": 10},
            'hip_rotation_l': {"weight": 1},
            'hip_flexion_r': {"weight": 20},
            'hip_adduction_r': {"weight": 10},
            'hip_rotation_r': {"weight": 1},
            'knee_angle_l': {"weight": 10},
            'knee_angle_r': {"weight": 10},
            'ankle_angle_l': {"weight": 10},
            'ankle_angle_r': {"weight": 10},
            'subtalar_angle_l': {"weight": 10},
            'subtalar_angle_r': {"weight": 10},
            'lumbar_extension': {"weight": 10},
            'lumbar_bending': {"weight": 10},
            'lumbar_rotation': {"weight": 10},
            'arm_flex_l': {"weight": 10},
            'arm_add_l': {"weight": 10},
            'arm_rot_l': {"weight": 10},
            'arm_flex_r': {"weight": 10},
            'arm_add_r': {"weight": 10},
            'arm_rot_r': {"weight": 10},
            'elbow_flex_l': {"weight": 10},
            'elbow_flex_r': {"weight": 10},
            'pro_sup_l': {"weight": 10},
            'pro_sup_r': {"weight": 10}},
        'coordinate_constraints': {
            'pelvis_tx': {"env_bound": 0.1}},
        'ignorePassiveFiberForce': True}
    
    setups['walking'] = {
        'ipopt_tolerance': 3,
        'weights': {
            'positionTrackingTerm': 10,
            'velocityTrackingTerm': 10,
            'accelerationTrackingTerm': 50,
            'activationTerm': 1,
            'armExcitationTerm': 0.001,
            'lumbarExcitationTerm': 0.001,
            'jointAccelerationTerm': 0.001,
            'activationDtTerm': 0.001,
            'forceDtTerm': 0.001},            
        'coordinates_toTrack': {
            'pelvis_tilt': {"weight": 10},
            'pelvis_list': {"weight": 1},
            'pelvis_rotation': {"weight": 1},
            'pelvis_tx': {"weight": 1},
            'pelvis_ty': {"weight": 1},
            'pelvis_tz': {"weight": 1}, 
            'hip_flexion_l': {"weight": 10},
            'hip_adduction_l': {"weight": 1},
            'hip_rotation_l': {"weight": 1},
            'hip_flexion_r': {"weight": 10},
            'hip_adduction_r': {"weight": 1},
            'hip_rotation_r': {"weight": 1},
            'knee_angle_l': {"weight": 10},
            'knee_angle_r': {"weight": 10},
            'ankle_angle_l': {"weight": 10},
            'ankle_angle_r': {"weight": 10},
            'subtalar_angle_l': {"weight": 1},
            'subtalar_angle_r': {"weight": 1},
            'lumbar_extension': {"weight": 10},
            'lumbar_bending': {"weight": 1},
            'lumbar_rotation': {"weight": 1},
            'arm_flex_l': {"weight": 1},
            'arm_add_l': {"weight": 1},
            'arm_rot_l': {"weight": 1},
            'arm_flex_r': {"weight": 1},
            'arm_add_r': {"weight": 1},
            'arm_rot_r': {"weight": 1},
            'elbow_flex_l': {"weight": 1},
            'elbow_flex_r': {"weight": 1},
            'pro_sup_l': {"weight": 1},
            'pro_sup_r': {"weight": 1}},            
        'coordinate_constraints': {
            'pelvis_ty': {"env_bound": 0.1},
            'pelvis_tx': {"env_bound": 0.1}},
        'enableLimitTorques': True}
    
    
    setups['drop_jump'] = {
        'weights': {
            'positionTrackingTerm': 50,
            'velocityTrackingTerm': 10,
            'accelerationTrackingTerm': 50,
            'activationTerm': 1,
            'armExcitationTerm': 0.001,
            'lumbarExcitationTerm': 0.001,
            'jointAccelerationTerm': 0.001,
            'activationDtTerm': 0.001,
            'forceDtTerm': 0.001},            
        'coordinates_toTrack': {
            'pelvis_tilt': {"weight": 10},
            'pelvis_list': {"weight": 1},
            'pelvis_rotation': {"weight": 1},
            'pelvis_tx': {"weight": 1},
            'pelvis_ty': {"weight": 10},
            'pelvis_tz': {"weight": 1}, 
            'hip_flexion_l': {"weight": 10},
            'hip_adduction_l': {"weight": 1},
            'hip_rotation_l': {"weight": 1},
            'hip_flexion_r': {"weight": 10},
            'hip_adduction_r': {"weight": 1},
            'hip_rotation_r': {"weight": 1},
            'knee_angle_l': {"weight": 10},
            'knee_angle_r': {"weight": 10},
            'ankle_angle_l': {"weight": 10},
            'ankle_angle_r': {"weight": 10},
            'subtalar_angle_l': {"weight": 1},
            'subtalar_angle_r': {"weight": 1},
            'lumbar_extension': {"weight": 10},
            'lumbar_bending': {"weight": 1},
            'lumbar_rotation': {"weight": 1},
            'arm_flex_l': {"weight": 50},
            'arm_add_l': {"weight": 50},
            'arm_rot_l': {"weight": 50},
            'arm_flex_r': {"weight": 50},
            'arm_add_r': {"weight": 50},
            'arm_rot_r': {"weight": 50},
            'elbow_flex_l': {"weight": 50},
            'elbow_flex_r': {"weight": 50},
            'pro_sup_l': {"weight": 50},
            'pro_sup_r': {"weight": 50}},            
        'coordinate_constraints': {
            'pelvis_ty': {"env_bound": 0.02},
            'pelvis_tx': {"env_bound": 0.02},
            'pelvis_tz': {"env_bound": 0.02}},
        'ignorePassiveFiberForce': True}
    
    setups['sit_to_stand'] = {
        'ipopt_tolerance': 3,
        'weights': {
            'positionTrackingTerm': 50,
            'velocityTrackingTerm': 10,
            'accelerationTrackingTerm': 50,
            'activationTerm': 100,
            'armExcitationTerm': 0.001,
            'lumbarExcitationTerm': 0.001,
            'jointAccelerationTerm': 0.001,
            'activationDtTerm': 0.001,
            'forceDtTerm': 0.001,
            'reserveActuatorTerm': 0.001,
            },            
        'coordinates_toTrack': {
            'pelvis_tilt': {"weight": 100},
            'pelvis_list': {"weight": 10},
            'pelvis_rotation': {"weight": 1},
            'pelvis_tx': {"weight": 100},
            'pelvis_ty': {"weight": 10},
            'pelvis_tz': {"weight": 100}, 
            'hip_flexion_l': {"weight": 100},
            'hip_adduction_l': {"weight": 20},
            'hip_rotation_l': {"weight": 1},
            'hip_flexion_r': {"weight": 100},
            'hip_adduction_r': {"weight": 20},
            'hip_rotation_r': {"weight": 1},
            'knee_angle_l': {"weight": 100},
            'knee_angle_r': {"weight": 100},
            'ankle_angle_l': {"weight": 100},
            'ankle_angle_r': {"weight": 100},
            'subtalar_angle_l': {"weight": 20},
            'subtalar_angle_r': {"weight": 20},
            'lumbar_extension': {"weight": 100},
            'lumbar_bending': {"weight": 20},
            'lumbar_rotation': {"weight": 20},
            'arm_flex_l': {"weight": 50},
            'arm_add_l': {"weight": 10},
            'arm_rot_l': {"weight": 10},
            'arm_flex_r': {"weight": 50},
            'arm_add_r': {"weight": 10},
            'arm_rot_r': {"weight": 10},
            'elbow_flex_l': {"weight": 10},
            'elbow_flex_r': {"weight": 10},
            'pro_sup_l': {"weight": 10},
            'pro_sup_r': {"weight": 10}},            
        'coordinate_constraints': {
            'pelvis_ty': {"env_bound": 0.1},
            'pelvis_tx': {"env_bound": 0.1}},       
        'withReserveActuators': True,
        'reserveActuatorCoordinates': {
            'hip_rotation_l': 30, 'hip_rotation_r': 30},
        'periodicConstraints': {'Qs': ['lowerLimbJoints']},
        'ignorePassiveFiberForce': True}
    
    setups['squats'] = {
        'ipopt_tolerance': 3,
        'weights': {
            'positionTrackingTerm': 50,
            'velocityTrackingTerm': 10,
            'accelerationTrackingTerm': 50,
            'activationTerm': 100,
            'armExcitationTerm': 0.001,
            'lumbarExcitationTerm': 0.001,
            'jointAccelerationTerm': 0.001,
            'activationDtTerm': 0.001,
            'forceDtTerm': 0.001,
            'reserveActuatorTerm': 0.001},            
        'coordinates_toTrack': {
            'pelvis_tilt': {"weight": 100},
            'pelvis_list': {"weight": 10},
            'pelvis_rotation': {"weight": 1},
            'pelvis_tx': {"weight": 100},
            'pelvis_ty': {"weight": 10},
            'pelvis_tz': {"weight": 100}, 
            'hip_flexion_l': {"weight": 100},
            'hip_adduction_l': {"weight": 20},
            'hip_rotation_l': {"weight": 1},
            'hip_flexion_r': {"weight": 100},
            'hip_adduction_r': {"weight": 20},
            'hip_rotation_r': {"weight": 1},
            'knee_angle_l': {"weight": 100},
            'knee_angle_r': {"weight": 100},
            'ankle_angle_l': {"weight": 100},
            'ankle_angle_r': {"weight": 100},
            'subtalar_angle_l': {"weight": 20},
            'subtalar_angle_r': {"weight": 20},
            'lumbar_extension': {"weight": 100},
            'lumbar_bending': {"weight": 20},
            'lumbar_rotation': {"weight": 20},
            'arm_flex_l': {"weight": 50},
            'arm_add_l': {"weight": 10},
            'arm_rot_l': {"weight": 10},
            'arm_flex_r': {"weight": 50},
            'arm_add_r': {"weight": 10},
            'arm_rot_r': {"weight": 10},
            'elbow_flex_l': {"weight": 10},
            'elbow_flex_r': {"weight": 10},
            'pro_sup_l': {"weight": 10},
            'pro_sup_r': {"weight": 10}},            
        'coordinate_constraints': {
            'pelvis_ty': {"env_bound": 0.1},
            'pelvis_tx': {"env_bound": 0.1}},
        'withReserveActuators': True,
        'reserveActuatorCoordinates': {
            'hip_rotation_l': 30, 'hip_rotation_r': 30},
        'periodicConstraints': {'Qs': ['lowerLimbJoints'],
                                'Qds': ['lowerLimbJoints'],
                                'muscles': ['all'],
                                'lumbar': ['all']},
        'ignorePassiveFiberForce': True}
        
    setups['jumping'] = {
        'weights': {
            'positionTrackingTerm': 100,
            'velocityTrackingTerm': 10,
            'accelerationTrackingTerm': 50,
            'activationTerm': 1,
            'armExcitationTerm': 0.001,
            'lumbarExcitationTerm': 0.001,
            'jointAccelerationTerm': 0.001,
            'activationDtTerm': 0.001,
            'forceDtTerm': 0.001},            
        'coordinates_toTrack': {
            'pelvis_tilt': {"weight": 10},
            'pelvis_list': {"weight": 10},
            'pelvis_rotation': {"weight": 10},
            'pelvis_tx': {"weight": 10},
            'pelvis_ty': {"weight": 100},
            'pelvis_tz': {"weight": 10}, 
            'hip_flexion_l': {"weight": 20},
            'hip_adduction_l': {"weight": 10},
            'hip_rotation_l': {"weight": 10},
            'hip_flexion_r': {"weight": 20},
            'hip_adduction_r': {"weight": 10},
            'hip_rotation_r': {"weight": 10},
            'knee_angle_l': {"weight": 10},
            'knee_angle_r': {"weight": 10},
            'ankle_angle_l': {"weight": 10},
            'ankle_angle_r': {"weight": 10},
            'subtalar_angle_l': {"weight": 10},
            'subtalar_angle_r': {"weight": 10},
            'lumbar_extension': {"weight": 10},
            'lumbar_bending': {"weight": 10},
            'lumbar_rotation': {"weight": 10},
            'arm_flex_l': {"weight": 100},
            'arm_add_l': {"weight": 100},
            'arm_rot_l': {"weight": 100},
            'arm_flex_r': {"weight": 100},
            'arm_add_r': {"weight": 100},
            'arm_rot_r': {"weight": 100},
            'elbow_flex_l': {"weight": 100},
            'elbow_flex_r': {"weight": 100},
            'pro_sup_l': {"weight": 100},
            'pro_sup_r': {"weight": 100}},
        'coordinate_constraints': {
            'pelvis_tx': {"env_bound": 0.1},
            'pelvis_ty': {"env_bound": 0.1}},
        'ignorePassiveFiberForce': True,
        }
    
    setups['my_periodic_running'] = {
        'ipopt_tolerance': 3,
        'weights': {
            'positionTrackingTerm': 100,
            'velocityTrackingTerm': 10,
            'accelerationTrackingTerm': 50,
            'activationTerm': 10,
            'armExcitationTerm': 0.001,
            'lumbarExcitationTerm': 0.001,
            'jointAccelerationTerm': 0.001,
            'activationDtTerm': 0.001,
            'forceDtTerm': 0.001},            
        'coordinates_toTrack': {
            'pelvis_tilt': {"weight": 10},
            'pelvis_list': {"weight": 10},
            'pelvis_rotation': {"weight": 10},
            'pelvis_tx': {"weight": 10},
            'pelvis_ty': {"weight": 10},
            'pelvis_tz': {"weight": 10}, 
            'hip_flexion_l': {"weight": 20},
            'hip_adduction_l': {"weight": 10},
            'hip_rotation_l': {"weight": 1},
            'hip_flexion_r': {"weight": 20},
            'hip_adduction_r': {"weight": 10},
            'hip_rotation_r': {"weight": 1},
            'knee_angle_l': {"weight": 10},
            'knee_angle_r': {"weight": 10},
            'ankle_angle_l': {"weight": 10},
            'ankle_angle_r': {"weight": 10},
            'subtalar_angle_l': {"weight": 10},
            'subtalar_angle_r': {"weight": 10},
            'lumbar_extension': {"weight": 10},
            'lumbar_bending': {"weight": 10},
            'lumbar_rotation': {"weight": 10},
            'arm_flex_l': {"weight": 10},
            'arm_add_l': {"weight": 10},
            'arm_rot_l': {"weight": 10},
            'arm_flex_r': {"weight": 10},
            'arm_add_r': {"weight": 10},
            'arm_rot_r': {"weight": 10},
            'elbow_flex_l': {"weight": 10},
            'elbow_flex_r': {"weight": 10},
            'pro_sup_l': {"weight": 10},
            'pro_sup_r': {"weight": 10}},
        'coordinate_constraints': {
            'pelvis_tx': {"env_bound": 0.1}},
        'periodicConstraints': {
            # All lower limb coordinates but pelvis_tx.
            'Qs': ['pelvis_tilt', 'pelvis_list', 'pelvis_rotation', 
                   'pelvis_ty', 'pelvis_tz', 'hip_flexion_l', 
                   'hip_adduction_l', 'hip_rotation_l', 'hip_flexion_r',
                   'hip_adduction_r', 'hip_rotation_r', 'knee_angle_l',
                   'knee_angle_r', 'ankle_angle_l', 'ankle_angle_r', 
                   'subtalar_angle_l', 'subtalar_angle_r', 'mtp_angle_l',
                   'mtp_angle_r', 'lumbar_extension', 'lumbar_bending',
                   'lumbar_rotation'],
            'Qds': ['lowerLimbJoints'],
            'muscles': ['all'],
            'lumbar': ['all']},
        'ignorePassiveFiberForce': True}

    return setups[motion_type]

def get_trial_setup(settings, motion_type, trialName):
    
    if motion_type == 'running':        
        settings['trials'], settings['trials'][trialName] = {}, {}
        settings['trials'][trialName]['filter_Qs_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qs'] = 12
        settings['trials'][trialName]['filter_Qds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qds'] = 12
        settings['trials'][trialName]['filter_Qdds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qdds'] = 12
        settings['trials'][trialName]['splineQds'] = True
        settings['trials'][trialName]['meshDensity'] = 100
        settings['trials'][trialName]['yCalcnToes'] = True
        
    elif motion_type == 'jumping':  
        settings['trials'], settings['trials'][trialName] = {}, {}
        settings['trials'][trialName]['filter_Qs_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qs'] = 20
        settings['trials'][trialName]['filter_Qds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qds'] = 20
        settings['trials'][trialName]['filter_Qdds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qdds'] = 20
        settings['trials'][trialName]['splineQds'] = True
        settings['trials'][trialName]['meshDensity'] = 50
        settings['trials'][trialName]['yCalcnToes'] = True
        
    elif motion_type == 'walking':  
        settings['trials'], settings['trials'][trialName] = {}, {}
        settings['trials'][trialName]['filter_Qs_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qs'] = 6
        settings['trials'][trialName]['meshDensity'] = 100
        
    elif motion_type == 'drop_jump':  
        settings['trials'], settings['trials'][trialName] = {}, {}
        settings['trials'][trialName]['filter_Qs_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qs'] = 30
        settings['trials'][trialName]['filter_Qds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qds'] = 30
        settings['trials'][trialName]['filter_Qdds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qdds'] = 30
        settings['trials'][trialName]['splineQds'] = True
        settings['trials'][trialName]['meshDensity'] = 100
        
    elif motion_type == 'sit_to_stand':
        settings['trials'], settings['trials'][trialName] = {}, {}
        settings['trials'][trialName]['filter_Qs_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qs'] = 4
        settings['trials'][trialName]['filter_Qds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qds'] = 4
        settings['trials'][trialName]['filter_Qdds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qdds'] = 4
        settings['trials'][trialName]['splineQds'] = True
        settings['trials'][trialName]['meshDensity'] = 50
        
    elif motion_type == 'squats':  
        settings['trials'], settings['trials'][trialName] = {}, {}
        settings['trials'][trialName]['filter_Qs_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qs'] = 4
        settings['trials'][trialName]['filter_Qds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qds'] = 4
        settings['trials'][trialName]['filter_Qdds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qdds'] = 4
        settings['trials'][trialName]['splineQds'] = True
        settings['trials'][trialName]['heel_vGRF_threshold'] = 5
        settings['trials'][trialName]['meshDensity'] = 50
        
    if motion_type == 'other':        
        settings['trials'], settings['trials'][trialName] = {}, {}
        settings['trials'][trialName]['filter_Qs_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qs'] = 30
        settings['trials'][trialName]['filter_Qds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qds'] = 30
        settings['trials'][trialName]['filter_Qdds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qdds'] = 30
        settings['trials'][trialName]['splineQds'] = True
        settings['trials'][trialName]['meshDensity'] = 100
        settings['trials'][trialName]['yCalcnToes'] = True
        
    if motion_type == 'my_periodic_running':        
        settings['trials'], settings['trials'][trialName] = {}, {}
        settings['trials'][trialName]['filter_Qs_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qs'] = 12
        settings['trials'][trialName]['filter_Qds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qds'] = 12
        settings['trials'][trialName]['filter_Qdds_toTrack'] = True
        settings['trials'][trialName]['cutoff_freq_Qdds'] = 12
        settings['trials'][trialName]['splineQds'] = True
        settings['trials'][trialName]['meshDensity'] = 100
        settings['trials'][trialName]['yCalcnToes'] = True
        
    return settings
