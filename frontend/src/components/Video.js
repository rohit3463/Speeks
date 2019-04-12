import React, {Component} from 'react';

class Video extends Component {
    constructor(props) {
        super(props);
    }

    getVideo = () => {
        return (
            <video autoPlay muted="muted" id="myVideo" style={{width: "100%"}} />
        );
    }

    render() {
        const stream = this.props.stream;

        if(stream !== false)
            document.getElementById('myVideo').srcObject = stream;
            
        return (
            <this.getVideo />
        );
    }
}

export default Video;
