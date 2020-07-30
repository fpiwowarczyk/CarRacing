// SSELECTING AND DECLARING ITEMS 
var keyPressed = false;
var canvas=document.getElementById("canvas");
var ctx=canvas.getContext("2d");
var img = new Image();
img.src = 'tree.png';
var map = {
    87:false,//'w'
    83:false,//'s'
    65:false,//'a'
    68:false,//'d'
}
var velocityFlag=0;

var colorPlate = [

]
//==========EVENT LISTENERS
window.addEventListener("DOMContentLoaded",init);
document.body.onkeydown=KeyDown;
document.body.onkeyup=KeyUp;
//Functions 

function init(){
    canvas.width=1600;
    canvas.height=800;
    c = new Car(200,200,'green');
    world = new World();
    setInterval(nextAnimationFrame,10);
}


 // ================= KEYBOARD USAGE 
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
     if(map[87]&&map[65]){ // w a
        c.moveCar(1,true);
        c.rotateCar(-1);
    } else if(map[87]&&map[68]){ // w d
        c.moveCar(1,true);
        c.rotateCar(1);
    } else if(map[83]&&map[65]){ // s a
        c.moveCar(-1,true);
        c.rotateCar(-1);
    } else if(map[83]&&map[68]){ // s d
        c.moveCar(-1,true);
        c.rotateCar(1);
    }else if(c.velocity>0&&map[65]){
        c.moveCar(1,false);
        c.rotateCar(-1)
    }else if(c.velocity>0&&map[68]){
        c.moveCar(1,false);
        c.rotateCar(1)
    } else if(map[83]){ //s
        c.moveCar(-1,true);
    } else if(map[65]){ //a
        c.rotateCar(-1);
    } else if(map[68]){ //d
        c.rotateCar(1);
    } else if(map[87]){ //w   
        c.moveCar(1,true);
    }else {
        c.moveCar(1,false);
    }
}

 // ================= 

 // ===== GAME LOOP
function nextAnimationFrame(){
    
    ctx.clearRect(0,0,canvas.width,canvas.height);
    world.drawMap();
    if(!map[87]&&!map[83])
    {
        c.rotateCar(0);
        Move();
    }else {
        Move();
    }
    
}
//===================

//=========== UTILS
function isEmpty(obj) {  // Checking if object is empty 
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}
 //==================
// Our car 
class Car {
    
    constructor (posX,posY,color){
        this.angle=0;
        this.posX=posX;
        this.posY=posY;
        this.color=color;
        this.velocity=0;
        this.rotateCar(0);
    }

    drawCar(){ // Making a car from rectangles 
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

    moveCar(direction,engineOn=true){
        if(engineOn===true&&this.velocity<4&&direction>0){
            this.velocity = Math.pow(0.1,velocityFlag)+velocityFlag;
            velocityFlag=velocityFlag+0.01;
        }else if(engineOn===true&&this.velocity>0&&direction <0){
            this.velocity = this.velocity- 0.09;
            velocityFlag=velocityFlag-0.01;
        } else if(engineOn===false&&this.velocity>=0.1){
            this.velocity = this.velocity - 0.01;
            velocityFlag=velocityFlag-0.01;
        } else if(this.velocity <0.1){
            console.log('4');
            velocityFlag=0;
            this.velocity=0;
        }
        console.log('v='+this.velocity);
        // If some problems show up 
        if(this.velocity>4.5){
            this.velocity=0;
            velocityFlag=0;
            this.posX=200;
            this.posY=200;
        }
        this.posX=this.posX+Math.pow(direction,2)*this.velocity*Math.cos(this.angle*Math.PI/180);
        this.posY=this.posY+Math.pow(direction,2)*this.velocity*Math.sin(this.angle*Math.PI/180);
        this.rotateCar(0);
    }

    rotateCar(direction){  // Rotating a car i have to be saved and restored
        this.angle=this.angle+direction;
        ctx.save();
        var rad = this.angle*Math.PI/180;
        ctx.translate(this.posX+20,this.posY+10);
        ctx.rotate(rad);
        ctx.translate(-(this.posX+20),-(this.posY+10));
        this.drawCar(this.angle);
        ctx.restore();
    }

    drawRectangle(x,y,w,h,color){ // Own rectangle drawing i didnt have to do that but i made it during testing and stayed
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

/// How to put images into canvas ?
class World{
    constructor (){
        this.posX =0;
        this.posY=0;
        this.rangeX=canvas.width;
        this.rangeY=canvas.height;
        this.drawMap();    
    }

    drawMap(){
        ctx.fillStyle='rgba(50,200,50,0.6)';
        ctx.fillRect(this.posX,this.posY,canvas.width,canvas.height)
        this.drawTree();
    }

    drawTree(){
        for(let i=1; i<20;i++){
            ctx.fillStyle='rgba(100,0,100,0.5)';
            ctx.fillRect(40+i*50,100,20,20);
            ctx.fillRect(40+20*50,50+i*50,20,20);
            ctx.fillRect(40+i*50,50+14*50,20,20);
            ctx.fillRect(40,50+i*50,20,20);
        }
    }
}

