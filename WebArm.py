from flask import Flask, redirect, url_for, request, render_template
import logging
import time
import argparse
import signal
import sys
import atexit
from adafruit_servokit import ServoKit
from yaml import load, Loader




def main():
    @atexit.register
    def cleanup_arm():
        pass
    parser = argparse.ArgumentParser(description='Web Driver for RoboKar')
    parser.add_argument('--hostname', default='0.0.0.0')
    parser.add_argument('--port', default=5000)
    parser.add_argument('--testing',default=False)
    args = parser.parse_args()
    url = 'http:/'+args.hostname+':'+str(args.port)+'/'
    print(url)
    params = load(open('WebParams.yaml').read(), Loader=Loader)


    kit = ServoKit(channels=16)

    app = Flask(__name__)

    @app.route("/")
    def index():
        #initialise angle_list
        angle_list = [0.0 for i in params['joint_list']]
        return render_template('WebArm.html',host=url,joint_list=params['joint_list'],angle_list=angle_list)


    @app.route("/",methods = ['POST','GET'])
    def servo_control():
        #form angle command list
        angle_list = [request.form[i] for i in params['joint_list']]
        print(angle_list)
        #send pwm Commands
        for i in range(len(angle_list)):
            try:
                kit.servo[params['channel_list'][i]].angle = float(angle_list[i])
                print('sent ',angle_list[i],' to ',params['channel_list'][i])
            except:
                pass

        return render_template('WebArm.html',host=url,joint_list=params['joint_list'],angle_list=angle_list)

    app.run(host=args.hostname,port=args.port,debug=args.testing)


if __name__ == '__main__':
    main()
