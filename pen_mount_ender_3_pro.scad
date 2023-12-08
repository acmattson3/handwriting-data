$fn=30;

screw_hole_dist=14.4;
screw_hole_dia=3.3;
screw_hole_rad=screw_hole_dia/2;
total_body_width=12.5;

pen_rad=4;
gap_size=0.4;

module screw_hole(dist, rad, height) {
    cylinder(h=height, r=rad);
}

module screw_holes(dist, rad, height) {
    translate([0,height/2,0]) 
    rotate([90,0,0]) {
        translate([dist/2,0,0])
        screw_hole(dist, rad, height);
        translate([-dist/2,0,0])
        screw_hole(dist, rad, height);
    }
}

screw_wall_thick=4;
module mount_body(body_width) {
    difference() {
    hull()
    screw_holes(screw_hole_dist, screw_hole_rad+screw_wall_thick, body_width);
    screw_holes(screw_hole_dist, screw_hole_rad, 30);
    }
}

module body_half(body_width) {
    difference() {
    mount_body(body_width);
    translate([0,body_width/2,-50/2])
    cylinder(h=50, r=4+gap_size);
    }
}

module parts_together() {
    translate([0,-(total_body_width/2/2+gap_size)])
    body_half(total_body_width/2);
    rotate([180,0,0])
    translate([0,-(total_body_width/2/2+gap_size)])
    body_half(total_body_width/2);
}

module print_parts() {
    translate([0,-total_body_width,0])
    rotate([90,0,0])
    body_half(total_body_width/2);
    translate([0,total_body_width,0])
    rotate([90,0,0])
    body_half(total_body_width/2);
}

print_parts();
