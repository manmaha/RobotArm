#Slider Control for Robot WebArm
#Manish Mahajan
# 2 July 2019

from flask import Flask, redirect, url_for, request, render_template
import logging
import time
import argparse
import signal
import sys
import atexit

from yaml import load, Loader




def main():
    @atexit.register
    def cleanup_arm():
        pass
    parser = argparse.ArgumentParser(description='Web Driver for RoboKar')
    parser.add_argument('--hostname', default='0.0.0.0')
    parser.add_argument('--port', default=5000)
    parser.add_argument('--testing',default=False)
    parser.add_argument('--onPi', default=False)
    args = parser.parse_args()
    url = 'http://'+args.hostname+':'+str(args.port)+'/'
    print(url)
    params = load(open('WebParams.yaml').read(), Loader=Loader)
    #initialise lists
    joint_list = params['joint_list']
    channel_list = params['channel_list']
    angle_list = params['angle_list']
    data_dict = dict(zip(joint_list,[list(i) for i in zip(channel_list,angle_list)]))
    #actuation_range_list = params['actuation_range']
    if args.onPi == True:
        from adafruit_servokit import ServoKit
        kit = ServoKit(channels=16)
        #Setup channels
        for i in range(len(channel_list)):
            kit.servo[channel].actuation_range = params['actuation_range'][i]

    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template('RobotArmSlider.html',host=url,\
        joint_list=params['joint_list'],angle_list=params['angle_list'],\
        actuation_range_list=params['actuation_range'])


    @app.route("/read_joint_val",methods = ['POST','GET'])
    def servo_control():
        #form angle command list
        joint = request.args.get("joint")
        value = request.args.get("value")
        data_dict[joint][1]=value
        print('Received Joint: ', joint, ' Angle: ', value)
        #send pwm Command
        try:
            if args.onPi == True:
                kit.servo[data_dict[joint][0]].angle = float(value)
            print('Sent Joint: ', joint, ' Angle: ', value)
        except:
            pass
        angle_list = [data[1] for data in data_dict.values()]
        return render_template('RobotArmSlider.html',host=url,\
        joint_list=params['joint_list'],angle_list=angle_list,\
        actuation_range_list=params['actuation_range'])

    @app.route("/stop")
    def stop():
        sys.exit(0)

    app.run(host=args.hostname,port=args.port,debug=args.testing)


if __name__ == '__main__':
    main()
