// Selected items 
var keyPressed = false;
var canvas=document.getElementById("canvas");
var ctx=canvas.getContext("2d");
var map = {
    87:false,//'w',
    83:false,//'s',
    65:false,//'a',
    68:false,//'d'
}

var colorPlate = {

}
//Event listeners 
window.addEventListener("DOMContentLoaded",init);
document.body.onkeydown=KeyDown;
document.body.onkeyup=KeyUp;

//Functions 

function init(){
    canvas.width=1600;
    canvas.height=800;
    c = new Car(200,200,'green');
    setInterval(nextAnimationFrame,10);
}

function KeyDown(e){
    if(e.keyCode in map){
        map[e.keyCode]=true;

    }
}

function KeyUp(e){
    if(e.keyCode in map){
        map[e.keyCode]=false;
    }
}

function Move(){
     if(map[87]&&map[65]){
        c.moveCar(1);
        c.rotateCar(-1);
    } else if(map[87]&&map[68]){
        c.moveCar(1);
        c.rotateCar(1);
    } else if(map[83]&&map[65]){
        c.moveCar(-1);
        c.rotateCar(-1);
    } else if(map[83]&&map[68]){
        c.moveCar(-1);
        c.rotateCar(1);
    } else if(map[83]){ //s
        c.moveCar(-1);
    } else if(map[65]){  //a
        c.rotateCar(-1);
    } else if(map[68]){ // d
        c.rotateCar(1);
    }
    else if(map[87]) // w 
    {
        c.moveCar(1);
    }
    
}

function nextAnimationFrame(){
    
    ctx.clearRect(0,0,canvas.width,canvas.height);
    // if(!isEmpty(map))
    // {
    //     c.rotateCar(0);
    // } else {
    //     Move();
    // }
    if(!map[87]&&!map[83]&&!map[68]&&!map[65])
    {
        c.rotateCar(0);
    } else {
        Move();
    }
    
}

class Car {
    
    constructor (posX,posY,color){
        this.angle=0;
        this.posX=posX;
        this.posY=posY;
        this.color=color;
        this.velocity=1;
        this.rotateCar(0);
    }

    drawCar(){
        //Draw body
        this.drawRectangle(this.posX,this.posY,40,20,this.color);

        //Draw wheels
        this.drawRectangle(this.posX,this.posY-5,10,5,'black');
        this.drawRectangle(this.posX,this.posY+20,10,5,'black');
        this.drawRectangle(this.posX+30,this.posY-5,10,5,'black');
        this.drawRectangle(this.posX+30,this.posY+20,10,5,'black');

        //Draw front window 
        this.drawRectangle(this.posX+25,this.posY+2,10,16,'#add8e6')

        //Draw lights 
        this.drawRectangle(this.posX+35,this.posY+3,5,5,'yellow');
        this.drawRectangle(this.posX+35,this.posY+12,5,5,'yellow');
    }

    moveCar(direction){
        this.velocity=this.velocity;
        this.posX=this.posX+direction*this.velocity*Math.cos(this.angle*Math.PI/180);
        this.posY=this.posY+direction*this.velocity*Math.sin(this.angle*Math.PI/180);
        this.rotateCar(0);
    }

    rotateCar(direction){
        this.angle=this.angle+direction;
        ctx.save();
        var rad = this.angle*Math.PI/180;
        ctx.translate(this.posX+20,this.posY+10);
        ctx.rotate(rad);
        ctx.translate(-(this.posX+20),-(this.posY+10));
        this.drawCar(this.angle);
        ctx.restore();
    }

    drawRectangle(x,y,w,h,color){

        //Draw body 
        ctx.fillStyle=color;
        ctx.beginPath();
        ctx.moveTo(x,y);
        ctx.lineTo(x+w,y);
        ctx.lineTo(x+w,y+h);
        ctx.lineTo(x,y+h);
        ctx.lineTo(x,y);
        ctx.fill();
        ctx.moveTo(-x,-y);
        ctx.stroke();
    }
}

function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}