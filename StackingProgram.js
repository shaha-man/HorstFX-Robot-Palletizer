configuration();
{
    config("robot.horstproto", "Horst900S4Fast");
    config("tool", "Suction Schmalz");
    config("tool2", "Suction Gripper Schmalz ECBPMi 24V-DC FK");
    config("world", "H900_MRBM_LS_World");
    config("scripttype", "textual");
    config("tcp.weight", "0.5");
    config("version", "2022.07_hotfix3");
    config("io.config.file", "StackingProgram.io");
    config("io.config.checksum", "e9f51029");
}


var pose = getCurrentPose();
var x = pose.x;
var y = pose.y;
var z = pose.z;
var rx = pose.rx;
var ry = pose.ry;
var rz = pose.rz;
var q0 = pose.q0;
var q1 = pose.q1;
var q2 = pose.q2;
var q3 = pose.q3;


var bld = 5.0;
var bor = 180.0;
var pat_x = 0.430;
var pat_y = -0.050;




//test we have BOXES boxes



//{"dim_x":0.069, "dim_y":0.115, "dim_z":0.073, "x":0.00, "y":0.00, "z":0.00, "approach":9},{"dim_x":0.063, "dim_y":0.064, "dim_z":0.035, "x":0.00, "y":0.115, "z":0.00, "approach":7},{"dim_x":0.063, "dim_y":0.064, "dim_z":0.035, "x":0.00, "y":0.115, "z":0.037, "approach":7}

var Pattern1Create = 'PUTHERE';
var pjson = JSON.parse(Pattern1Create);
var boxes = pjson.length;

showHint(boxes);


/*for (var i = 0; i < boxes; i++){
	showInfo("Box dimensions \nLength: " + pjson[i].dim_x + 
	",\nWidht: " + pjson[i].dim_y + 
	",\nHeight: " + pjson[i].dim_z +
	",\nApproach: " + pjson[i].approach);
}*/
sleep(100); 

var Pattern1Text = JSON.stringify(pjson);
showHint(Pattern1Text);

dx = 0.05;
dy = 0;

for (var i = 0; i < boxes; ++i){
	
if (dx > 0.4){
dx = 0.05;
dy = pjson[0].dim_y;
}

move({
'movetype': 'JOINT',
'poserelation': 'ABSOLUTE',
'coord' : 'cartesian_basis',
'blendradius.orient' : bor,
'blendradius.xyz' : bld,
'speed.ratio': 0.75,
'targetpose.x': dx + 0.330 + pjson[i].dim_x/2,
'targetpose.y': 0.250 - pjson[i].dim_y/2 - dy,
'targetpose.z': 0.160,
'targetpose.rx': -180,
'targetpose.ry': 0,
'targetpose.rz': 180,
 }, "PickUP_Lift_position");
	

move({
	'movetype': 'LINEAR',
	'poserelation': 'ABSOLUTE',
	'coord' : 'cartesian_basis',
	'blendradius.orient' : bor,
	'blendradius.xyz' : bld,
	'speed.ratio': 0.75,
	'targetpose.x': dx + 0.330 + pjson[i].dim_x/2,
	'targetpose.y': 0.250 - pjson[i].dim_y/2 - dy,
	'targetpose.z': 0.00231 + pjson[i].dim_z,
	'targetpose.rx': -180,
	'targetpose.ry': 0,
	'targetpose.rz': 180,
 	}, "PickBox");  // To the object

//sleep(500);
	GripperSuck();  // gripper suck

	move({
	'movetype': 'LINEAR',
	'poserelation': 'RELATIVE',
	'coord' : 'cartesian_basis',
	'blendradius.orient' : bor,
	'blendradius.xyz' : bld,
	'speed.ratio': 1.0,
	'targetpose.x': 0.0,
	'targetpose.y': 0.0 ,
	'targetpose.z': 0.160,
	'targetpose.rx': 0,
	'targetpose.ry': 0,
	'targetpose.rz': 0,
 	}, "PickUP_Lift_position");

dx += pjson[i].dim_x;


	
//currentPose();

var stack_height = pjson[i].shape_z;

if (pjson[i].approach == 3){
	Approach3();
} else if (pjson[i].approach == 5){
	Approach5();
} else if (pjson[i].approach == 7){
	Approach7();
} else if (pjson[i].approach == 9){
	Approach9();
}
ApproachUp();
}


var currentJoints = getCurrentJoints();
var j1 = currentJoints.j1;
var j6 = currentJoints.j6;

function GripperInit(){
setOutput("TOOL_OUTPUT_1", 0);
sleep(100);
setOutput("TOOL_OUTPUT_2", 0);
}

function GripperSuckpPrim(){
while (getInput("TOOL_INPUT_1") != 1){
	setOutput("TOOL_OUTPUT_1", 1);
	}
setOutput("TOOL_OUTPUT_1", 0);
}

function GripperSuck(){
setOutput("TOOL_OUTPUT_1", 1);
sleep(500);
setOutput("TOOL_OUTPUT_1", 0);
}

function GripperRelease(){
setOutput("TOOL_OUTPUT_2", 1);
sleep(300);
setOutput("TOOL_OUTPUT_2", 0);
}

function GripperCheck(){
waitfor("TOOL_INPUT_1", 1);
}

function GoBase(dx){
showHint("GoBase");
move({
'movetype': 'JOINT',
'poserelation': 'ABSOLUTE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 0.75,
'targetpose.x': dx + 0.330,
'targetpose.y': 0.250  - dy,
'targetpose.z': 0.160,
'targetpose.rx': -180,
'targetpose.ry': 0,
'targetpose.rz': 180,
 }, "PickUP_Lift_position");
//sleep(100);
/*move({
'movetype': 'JOINT',
'poserelation': 'ABSOLUTE',
'coord' : 'cartesian_basis',
'speed.ratio': 0.75,
'targetpose.x': 0.330,
'targetpose.y': 0.250 ,
'targetpose.z': 0.060,
'targetpose.rx': -180,
'targetpose.ry': 0,
'targetpose.rz': 180,
 }, "PickUP_position");*/
}

function Approach3(){
move({
'movetype': 'JOINT',
'poserelation': 'ABSOLUTE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 1.0,
'targetpose.x': pat_x + pjson[i].dim_x/2 + pjson[i].x + 0.05,
'targetpose.y': pat_y - pjson[i].dim_y/2 - pjson[i].y + 0.05,
'targetpose.z': 0.18 + pjson[i].dim_z + pjson[i].z,
'targetpose.rx': -180,
'targetpose.ry': 0,
'targetpose.rz': 180,
 }, "app31");
//sleep(100);
move({
'movetype': 'LINEAR',
'poserelation': 'RELATIVE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 1.0,
'targetpose.x': 0,
'targetpose.y': 0,
'targetpose.z': -0.13,
'targetpose.rx': 0,
'targetpose.ry': 0,
'targetpose.rz': 0,
 }, "app32");
move({
'movetype': 'LINEAR',
'poserelation': 'RELATIVE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 0.75,
'targetpose.x': -0.05,
'targetpose.y': -0.05,
'targetpose.z': 0,
'targetpose.rx': 0,
'targetpose.ry': 0,
'targetpose.rz': 0,
 }, "app32");
GripperRelease();
}

function Approach5(){
move({
'movetype': 'JOINT',
'poserelation': 'ABSOLUTE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 1.0,
'targetpose.x': pat_x + pjson[i].dim_x/2 + pjson[i].x + 0.05,
'targetpose.y': pat_y - pjson[i].dim_y/2 - pjson[i].y - 0.05,
'targetpose.z': 0.18 + pjson[i].dim_z + pjson[i].z,
'targetpose.rx': -180,
'targetpose.ry': 0,
'targetpose.rz': 180,
 }, "app51");
//sleep(100);
move({
'movetype': 'LINEAR',
'poserelation': 'RELATIVE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 0.7,
'targetpose.x': 0,
'targetpose.y': 0,
'targetpose.z': -0.13,
'targetpose.rx': 0,
'targetpose.ry': 0,
'targetpose.rz': 0,
 }, "app52");
move({
'movetype': 'LINEAR',
'poserelation': 'RELATIVE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 0.7,
'targetpose.x': -0.05,
'targetpose.y': 0.05,
'targetpose.z': 0,
'targetpose.rx': 0,
'targetpose.ry': 0,
'targetpose.rz': 0,
 }, "app52");
GripperRelease();
}


function Approach7(){
move({
'movetype': 'JOINT',
'poserelation': 'ABSOLUTE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 1.0,
'targetpose.x': pat_x + pjson[i].dim_x/2 + pjson[i].x - 0.05,
'targetpose.y': pat_y - pjson[i].dim_y/2 - pjson[i].y - 0.05,
'targetpose.z': 0.18 + pjson[i].dim_z + pjson[i].z,
'targetpose.rx': -180,
'targetpose.ry': 0,
'targetpose.rz': 180,
 }, "app71");
//sleep(100);
move({
'movetype': 'LINEAR',
'poserelation': 'RELATIVE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 0.7,
'targetpose.x': 0,
'targetpose.y': 0,
'targetpose.z': -0.13,
'targetpose.rx': 0,
'targetpose.ry': 0,
'targetpose.rz': 0,
 }, "app72");
move({
'movetype': 'LINEAR',
'poserelation': 'RELATIVE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 0.7,
'targetpose.x': 0.05,
'targetpose.y': 0.05,
'targetpose.z': 0,
'targetpose.rx': 0,
'targetpose.ry': 0,
'targetpose.rz': 0,
 }, "app73");
GripperRelease();
}

function Approach9(){
move({
'movetype': 'JOINT',
'poserelation': 'ABSOLUTE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 1.0,
'targetpose.x': pat_x + pjson[i].dim_x/2 + pjson[i].x - 0.05,
'targetpose.y': pat_y - pjson[i].dim_y/2 - pjson[i].y + 0.05,
'targetpose.z': 0.18 + pjson[i].dim_z + pjson[i].z,
'targetpose.rx': -180,
'targetpose.ry': 0,
'targetpose.rz': 180,
 }, "app91");
//sleep(100);
move({
'movetype': 'LINEAR',
'poserelation': 'RELATIVE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 0.7,
'targetpose.x': 0,
'targetpose.y': 0,
'targetpose.z': -0.13,
'targetpose.rx': 0,
'targetpose.ry': 0,
'targetpose.rz': 0,
 }, "app92");
move({
'movetype': 'LINEAR',
'poserelation': 'RELATIVE',
'coord' : 'cartesian_basis',
'blendradius.orient' : 180.0,
'blendradius.xyz' : bld,
'speed.ratio': 0.7,
'targetpose.x': 0.05,
'targetpose.y': -0.05,
'targetpose.z': 0,
'targetpose.rx': 0,
'targetpose.ry': 0,
'targetpose.rz': 0,
 }, "app93");
GripperRelease();
}

function ApproachUp(){
move({
'movetype': 'LINEAR',
'poserelation': 'RELATIVE',
'coord' : 'cartesian_basis',
'blendradius.orient' : bor,
'blendradius.xyz' : bld,
'speed.ratio': 0.75,
'targetpose.x': 0.00,
'targetpose.y': 0.00,
'targetpose.z': 0.13,
'targetpose.rx': 0,
'targetpose.ry': 0,
'targetpose.rz': 0,
 }, "appUP");
}

function currentPose(){
var pose = getCurrentPose();
var x = pose.x;
var y = pose.y;
var z = pose.z;
var rx = pose.rx;
var ry = pose.ry;
var rz = pose.rz;
var q0 = pose.q0;
var q1 = pose.q1;
var q2 = pose.q2;
var q3 = pose.q3;
showInfo(z)
}


function MoveStart(){
move({
'movetype': 'JOINT',
'poserelation': 'ABSOLUTE',
'coord' : 'cartesian_basis',
'speed.ratio': 0.75,
'targetpose.x': 0.330,
'targetpose.y': 0.250,
'targetpose.z': 0.16043,
'targetpose.rx': 0,
'targetpose.ry': 0,
'targetpose.rz': 0,
 }, "moveSt");

}
