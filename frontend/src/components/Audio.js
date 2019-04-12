import p5 from 'p5';
import 'p5/lib/addons/p5.sound';

class Audio {
    constructor(parent = "p5sketch") {
        this.myp5 = new p5(this.sketch, parent);
    }

    sketch(p) {
        let mic; let volhistory = Array(0);

        p.setup = function() {
            p.createCanvas(200, 200);
            p.angleMode(p5.DEGREES);

            mic = new p5.AudioIn();
            mic.start();
        }

        
        p.draw = function() {
            p.background(0);

            let vol = mic.getLevel();
            volhistory.push(vol);
            p.noFill();
            p.stroke(255);

            p.translate(p.width / 2, p.height / 2);

            p.beginShape();
            for(let i=0 ; i < 360 ; i++) {
                let r = p.map(volhistory[i], 0, 1, 10, 100);
                let x = r * p.cos(i);
                let y = r* p.sin(i);
                p.vertex(x, y);
            }
            p.endShape();

            if(volhistory.length > 360) 
                volhistory.splice(0, 1);

            //let h = p.map(vol, 0, 1 , p.height, 0);
            //p.ellipse(p.width/2, h - 25, 50, 50);
        }
    }
}

export default Audio;

