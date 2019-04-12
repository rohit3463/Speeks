import React, { Component } from 'react';
import './App.css';
import { Row, Col } from 'antd';
import Video from './components/Video';
import anime from 'animejs/lib/anime.es.js';

import * as RecordRTC from 'recordrtc';

import p5 from 'p5';
import 'p5/lib/addons/p5.sound';

const scale = (value, start1, stop1, start2, stop2) => {
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1));
}

class App extends Component {
    animateRadius; mic; recorder;

    constructor() {
        super();

        this.state = {
            stream: false,
        }
        //this.mic = new p5.AudioIn();
    }

    animate = () => {
        let micLevel = this.mic.getLevel();
        let value = scale(micLevel, 0, 1, 25, 50);
        //value -= 25 * 10;
        console.log(value);
        //value = Math.floor(value * 1.3);
        
        

        anime({
            targets: "#hello",
            r: value,
            autoplay: false,
            duration: 500,
        }).play();

        setTimeout(this.animate, 503);  
    }

    buttonClick = async (Event) => {
        //this.mic.start();
        //this.animate();

        if(this.state.stream !== false) {
            let recorder = this.recorder, blob;

            recorder.stopRecording(() => {
                blob = recorder.getBlob();
                console.log(blob);
                recorder.destroy();
            });

            let fd = new FormData();
            fd.append('audioVideoData', blob, 'recording.webm');

            fetch('https://aa1c3508-9966-40bc-9fd8-fd6451c11bd8.mock.pstmn.io/api', {method: 'post', body: fd});
        }
        
        else {
            let stream = await navigator.mediaDevices.getUserMedia({audio: {echoCancellation: true,}, video: true});
            
            this.setState({
                stream: stream,
            });

            this.recorder = RecordRTC(stream, {type: 'video'});
            this.recorder.startRecording();
        }
    }

    render() {
        //new Audio("mycanvas");

        return (
            <Row type="flex" align="middle" className="mydiv">
                <Col span={24}>
                <Row >
                    <Col span={12} offset={6}>
                        <Video stream={this.state.stream} />
                    </Col>
                </Row>
                <Row >
                    <Col span={14} offset={5} style={{marginTop: 20}}>
                        <svg width="100" height="100" xmlns="http://www.w3.org/2000/svg" >
                            <circle id="hello" cx="50" cy="50" r="25" stroke="black" strokeWidth="0" fill="red" />
                            <image x="25" y="25" width="50" xlinkHref="microphone1.svg" onClick={this.buttonClick} style={{cursor: "pointer"}} />
                        </svg>
                    </Col>
                </Row>
                </Col>
            </Row>
        );
    }
}

export default App;
