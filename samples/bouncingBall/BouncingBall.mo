within ;
package BouncingBall "Bouncing ball with structural changes"

  model ContactBall

  import Modelica.SIunits.*;

  parameter Mass m = 1;
  parameter Radius r = 1;
  parameter TranslationalSpringConstant c = 1e3;
  parameter TranslationalDampingConstant d = 0.6e1;
  parameter Acceleration g = 9.81;

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

    annotation (Diagram(graphics));
  end ContactBall;

  model FlyingBall

  parameter Real r = 1;
  parameter Real g=9.81;
  Real h(start=20);
  Real v;

  equation
    der(h) = v;
    der(v) = -g;

  end FlyingBall;

  model Ball_struc
    extends FlyingBall;
    Integer transitionId(start = 0);
  equation
    when h < r then
      transitionId = 1;
      terminate("kein Kontakt mit Boden");
    end when;
  end Ball_struc;

model Contact_struc
extends ContactBall;
  Integer transitionId(start = 0);
  Real h, v;
equation
  h = damper.s_rel*1;
  v = damper.v_rel *1;
  when (mass.s > r) then
    transitionId = 1;
    terminate("Kontakt mit Boden");
  end when;
end Contact_struc;

  annotation (uses(Modelica(version="3.2")),
    experiment(StopTime=5),
    __Dymola_experimentSetupOutput);
end BouncingBall;
