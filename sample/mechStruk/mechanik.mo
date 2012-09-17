within ;
package mechanik
    function my_term

    input Integer code;
    external "C" my_terminate(code);
    annotation(Include = "void my_terminate(int code) { modelErrorCode = code; };");
    end my_term;

  constant Real X_WALL = 10;  //Wandabstand in
  //Real VX;   //Ballbeschleunigung in x Richtung
  model wagen
    // Mechanik Beispiel mit Abhang von mir
    Real m = 1;
    Real c = 1.9;
    Real s;
    Real ds;
    Real k = 0.05;
    constant Real g = 9.81;
    parameter Real alpha = 20*3.14/180;
    Real x;
    Real y(start=20, fixed=true);
    Real R;
    Real vx;
    Real vy;
    parameter Real  wagenheight = 2;
    parameter Real wagenwidth = 4;
    parameter Real hBall = sqrt(wagenheight^2+wagenwidth^2);
  equation
    der(x) = vx;
    der(y) = vy;
    der(s)= ds;
    R = -k * sign(ds) * m*g*cos(alpha);
    der(ds)*m = R + m*g*sin(alpha);
    x = s*cos(alpha);
    y = -s*sin(alpha);
  end wagen;

  model ContactBall

  import Modelica.SIunits.*;

  parameter Mass m = 1;
  parameter Radius r = 1;
  parameter TranslationalSpringConstant c = 1e3;
  parameter TranslationalDampingConstant d = 1e1;
  parameter Acceleration g = 9.81;
  Length h;
  Velocity v;
  Length x;
  Velocity vx;

    Modelica.Mechanics.Translational.Components.Fixed fixed
      annotation (Placement(transformation(extent={{-10,-86},{10,-66}})));
    Modelica.Mechanics.Translational.Components.Spring spring(s_rel0=r, c=c)
                                                              annotation (
        Placement(transformation(
          extent={{-10,-10},{10,10}},
          rotation=90,
          origin={-20,-50})));
    Modelica.Mechanics.Translational.Components.Mass mass(m=m)
                                                          annotation (Placement(
          transformation(
          extent={{-10,-10},{10,10}},
          rotation=90,
          origin={0,-10})));
    Modelica.Mechanics.Translational.Components.Damper damper(d=d)
                                                              annotation (
        Placement(transformation(
          extent={{-10,-10},{10,10}},
          rotation=90,
          origin={20,-50})));
    Modelica.Mechanics.Translational.Sources.Force force annotation (Placement(
          transformation(
          extent={{-10,-10},{10,10}},
          rotation=270,
          origin={0,28})));
    Modelica.Blocks.Sources.Constant const(k=-m*g)
      annotation (Placement(transformation(extent={{-60,60},{-40,80}})));
  equation
    der(x)=vx;
    der(vx)=0;
    connect(spring.flange_b, mass.flange_a) annotation (Line(
        points={{-20,-40},{-20,-30},{0,-30},{0,-20},{-6.12323e-016,-20}},
        color={0,127,0},
        smooth=Smooth.None));
    connect(mass.flange_a, damper.flange_b) annotation (Line(
        points={{-6.12323e-016,-20},{0,-20},{0,-30},{20,-30},{20,-40}},
        color={0,127,0},
        smooth=Smooth.None));
    connect(spring.flange_a, fixed.flange) annotation (Line(
        points={{-20,-60},{-20,-68},{0,-68},{0,-76}},
        color={0,127,0},
        smooth=Smooth.None));
    connect(damper.flange_a, fixed.flange) annotation (Line(
        points={{20,-60},{22,-60},{22,-68},{0,-68},{0,-76}},
        color={0,127,0},
        smooth=Smooth.None));
    connect(force.flange, mass.flange_b) annotation (Line(
        points={{-1.83697e-015,18},{-1.83697e-015,0},{6.12323e-016,0}},
        color={0,127,0},
        smooth=Smooth.None));
    connect(const.y, force.f) annotation (Line(
        points={{-39,70},{2.20436e-015,70},{2.20436e-015,40}},
        color={0,0,127},
        smooth=Smooth.None));
    h = damper.s_rel*1;
    v = damper.v_rel*1;
    annotation (Diagram(graphics));
  end ContactBall;

  model FlyingBall

  parameter Real r = 1;
  parameter Real g=9.81;
  Real h(start=10);
  Real vx;
  Real x;
  Real vy;

  equation
    der(x)=vx;
    der(vx)=0;  //ballbeschleunigung in x richtung

    der(h) = vy;
    der(vy) = -g;
  end FlyingBall;

  model wagen_struc
    extends wagen;
    Integer switch_to(start = 0);
  equation
   when (y < 10) then
     switch_to = 2;
      terminate("Kontakt mit Boden");
  end when;
  end wagen_struc;

  model ball_struc
    extends FlyingBall;
    Integer switch_to(start = 0);
  algorithm
    when h < r then
     switch_to := 3;
     my_term(1);
     // terminate("Spring auf Boden");
    end when;
   // when 10 < x then
    //  switch_to = 4;
     // terminate("Spring gegen Wand");
    //end when;
  end ball_struc;

model contact_struc
extends ContactBall;
  Integer switch_to(start = 0);
equation
  when (mass.s > r) then
    switch_to = 2;
    terminate("Kontakt mit Boden");
  end when;
end contact_struc;

model to_ball_struct
  extends FlyingBall;
  Integer switch_to(start = 0);
  Boolean gegenWand(start = false);

//initial equation
  //if (gegenWand == true) then
algorithm
   when h < r then
    gegenWand := false;
    switch_to := 3;
    terminate("Spring auf Boden");
   end when;
   when x > X_WALL then
    gegenWand := true;
    switch_to := 4;
    terminate("Spring gegen Wand");
   end when;

end to_ball_struct;

model contact_wall
//mode nr. 4
  extends ContactBall;
  Integer switch_to(start = 0);
equation
  when (mass.s > r) then
    switch_to = 2;
    terminate("Kontakt mit Wand");
  end when;
end contact_wall;

  annotation (uses(Modelica(version="3.2")));

end mechanik;
