// SSELECTING AND DECLARING ITEMS 
const hex=['0','1','2','3','4','5','6','7','8','9',"A","B","C","D","E","F"];
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
    37:false,//left 
    38:false,//up
    39:false,//right
    40:false//down 
}

var velocityFlag=0;

var colorPlate = [

]
//==========EVENT LISTENERS
window.addEventListener("DOMContentLoaded",init);
document.body.onkeydown=KeyDown;
document.body.onkeyup=KeyUp;
window.addEventListener('click',function(e){
    var x = e.clientX-80;
    var y = e.clientY-80;
    console.log('x:'+x);
    console.log('y:'+y);
});
//Functions 

function init(){
    
    canvas.width=1600;
    canvas.height=800;
    color=getRandomColor();
    c = new Car(200,200,color);
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
     if((map[87]&&map[65])||(map[38]&&map[37])){ // w a || up left 
        c.moveCar(1,true);
        c.rotateCar(-1);
    } else if(map[87]&&map[68]||(map[38]&&map[39])){ // w d  || up right 
        c.moveCar(1,true);
        c.rotateCar(1);
    } else if(map[83]&&map[65]||(map[40]&&map[37])){ // s a || down left 
        c.moveCar(-1,true);
        c.rotateCar(-1);
    } else if(map[83]&&map[68]||(map[38]&&map[39])){ // s d  || down right 
        c.moveCar(-1,true);
        c.rotateCar(1);
    }else if(c.velocity>0&&map[65]||(c.velocity>0&&map[37])){  // speed and left 
        c.moveCar(1,false);
        c.rotateCar(-1)
    }else if(c.velocity>0&&map[68]||(c.velocity>0&&map[39])){  // speed right 
        c.moveCar(1,false);
        c.rotateCar(1)
    } else if(map[83]||map[40]){ //s  || down
        c.moveCar(-1,true);
    } else if(map[65]||map[37]){ //a  || lef t 
        c.rotateCar(-1);
    } else if(map[68]||map[39]){ //d  || right 
        c.rotateCar(1);
    } else if(map[87]||map[38]){ //w  || up 
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

function getRandomColor(){
    let hexColor='#';
    for(let i =0;i<6;i++){
        hexColor += hex[Math.floor(Math.random()*hex.length)];
    }
    return hexColor;
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
            velocityFlag=0;
            this.velocity=0;
        }
        //If some problems show up || any pushing w cheat 
        if(this.velocity>4.5){
            this.velocity=0;
            velocityFlag=0;
            this.posX=200;
            this.posY=200;
        }
        if(this.posX>canvas.width){
            this.velocity=0;
            velocityFlag=0;
            this.posX=this.posX-50;
        }
        if(this.posX<0){
            this.velocity=0;
            velocityFlag=0;
            this.posX=this.posX+50;
        }
        if(this.posY>canvas.height){
            this.velocity=0;
            velocityFlag=0;
            this.posY=this.posY-50;
        }
        if(this.posY<0){
            this.velocity=0;
            velocityFlag=0;
            this.posY=this.posY+50;
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
        this.drawRoad();
        for(let i =0;i<10;i++){
            this.drawTree(canvas.width-50,80*i);
        }
        for(let i =0;i<20;i++){
            this.drawTree(100*i,0);
        }

    }
    drawTree(x,y){

        ctx.beginPath();
        ctx.fillStyle='	rgba(139,69,19,0.9)'
        ctx.fillRect(x+10,y+40,20,40);
        ctx.fillStyle='rgba(0,200,0,1)';
        ctx.arc(x,y,20,0,Math.PI + (Math.PI * 2) / 2,0);
        ctx.arc(x+30,y,20,0,Math.PI + (Math.PI * 2) / 2,0);
        ctx.arc(x,y+30,20,0,Math.PI + (Math.PI * 2) / 2,0);
        ctx.arc(x+30,y+30,20,0,Math.PI + (Math.PI * 2) / 2,0);
        ctx.arc(x+50,y+30,20,0,Math.PI + (Math.PI * 2) / 2,0);
        ctx.arc(x+50,y+10,20,0,Math.PI + (Math.PI * 2) / 2,0);
        ctx.arc(x+60,y+20,20,0,Math.PI + (Math.PI * 2) / 2,0);
        ctx.arc(x+30,y+10,20,0,Math.PI + (Math.PI * 2) / 2,0);
        ctx.arc(x+40,y+10,20,0,Math.PI + (Math.PI * 2) / 2,0);
        ctx.arc(x-20,y+20,20,0,Math.PI + (Math.PI * 2) / 2,0);
        ctx.fill();
 
    }

    drawRoad(){
        ctx.fillStyle='rgba(100,0,100,0.5)';
        for(let i=1; i<29;i++){  // Horizontal Border
            ctx.fillRect(40+i*50,100,20,20);
            ctx.fillRect(40+i*50,50+14*50,20,20);
        }
        for(let i =1;i<20;i++){ // Vertical Border  
            ctx.fillRect(40+29*50,50+i*50,20,20);
            ctx.fillRect(40,50+i*50,20,20);
        }
        this.roundedRect(ctx,100,150,1350,550,40);
        ctx.fill();
        this.roundedRect(ctx,200,250,1150,350,40);
        ctx.fillStyle='rgba(50,200,50,0.6)'
        ctx.fill();

    }

    roundedRect(ctx,x,y,width,height,radius){
        ctx.beginPath();
        ctx.moveTo(x, y + radius);
        ctx.lineTo(x, y + height - radius);
        ctx.arcTo(x, y + height, x + radius, y + height, radius);
        ctx.lineTo(x + width - radius, y + height);
        ctx.arcTo(x + width, y + height, x + width, y + height-radius, radius);
        ctx.lineTo(x + width, y + radius);
        ctx.arcTo(x + width, y, x + width - radius, y, radius);
        ctx.lineTo(x + radius, y);
        ctx.arcTo(x, y, x, y + radius, radius);
        ctx.stroke();
    }
}

