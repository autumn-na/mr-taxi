#!/usr/bin/env python

import rospy, time, cv2, math

from linedetector import LineDetector
from obstacledetector import ObstacleDetector
from motordriver import MotorDriver

class AutoDrive: 
    def __init__(self):
        
        self.start_time = 0
        self.cur_time = 0
        
        self.lastAngle = 0
        rospy.init_node('xycar_driver')
        self.line_detector = LineDetector('/usb_cam/image_raw', )
        self.obstacle_detector = ObstacleDetector('/ultrasonic')
        self.driver = MotorDriver('/xycar_motor_msg')

        self.angle_threshold = 10 #minus abs of angle while steering
        self.angle_is_go = 10		# < 2, go straight
        self.angle_change_speed = 15	# angle > 5, change speed (lower)

        self.curve_radius = 10000 #230

        self.is_stop = False

        self.lastObs = [-1, -1, -1]
        
        self.obs_list_num = 5
        self.obs_l_list = []
        self.obs_m_list = []
        self.obs_r_list = []

    def trace(self):
        obs_l, obs_m, obs_r = self.obstacle_detector.get_distance()
        print(obs_l, obs_m, obs_r)  

        self.lastObs = [obs_l, obs_m, obs_r] 	

        angle = self.steer(self.line_detector.detect_angle())
        speed = self.accelerate(angle, obs_l, obs_m, obs_r)

        #print('Angle:', angle, ' Speed:', speed)
        self.driver.drive(angle + 90, speed + 90)

    def steer(self, _angle):
        if _angle == -99:
            return self.lastAngle #lastangle

        angle_ret = _angle
        angle_ret = max(-50, min(angle_ret, 50))

        angle_weight = self.curve_radius - math.sqrt(self.curve_radius * self.curve_radius - angle_ret * angle_ret)
        #print(angle_weight)
        
        if angle_ret > 0: 
            angle_ret -= angle_weight 
        else:
            angle_ret += angle_weight
        
        self.lastAngle = angle_ret
        return angle_ret

    def accelerate(self, angle, left, mid, right):
        if len(self.obs_l_list) < 5:
            if left != 0:
                self.obs_l_list.append(left)
            if mid != 0:
                self.obs_m_list.append(mid)
            if right != 0:
                self.obs_r_list.append(right)
        else:
            if left != 0:
                self.obs_l_list = self.obs_l_list[:3]
                self.obs_l_list.append(left)
            if mid != 0:
                self.obs_m_list = self.obs_m_list[:3]
                self.obs_r_list.append(mid)
            if right != 0:   
                self.obs_r_list = self.obs_r_list[:3]
                self.obs_r_list.append(right) 
        
        #left = sum(self.obs_l_list) / len(self.obs_l_list)
        #mid = sum(self.obs_m_list) / len(self.obs_m_list)
        #right = sum(self.obs_r_list) / len(self.obs_r_list)
        
        if self.start_time == 0:
            self.start_time = time.time()
        self.cur_time = time.time()
        print(self.cur_time - self.start_time)
        
        if mid < 90 and ((self.cur_time - self.start_time) >= 73.5):
            self.is_stop = True
            print('stop')
        else:
            pass
            
        if self.is_stop:
            return 0
            
        if angle < -self.angle_change_speed or angle > self.angle_change_speed:
            speed = 41
        else:
            speed = 50
        return speed

    def exit(self):
        print('finished')

if __name__ == '__main__':
    car = AutoDrive()
    time.sleep(3)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        car.trace()
        rate.sleep()
    rospy.on_shutdown(car.exit)
