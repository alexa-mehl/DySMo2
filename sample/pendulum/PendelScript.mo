within ;
package PendelScript
  import Modelica.Math.sin;
  import Modelica.Math.asin;
  import Modelica.Math.cos;
  import Modelica.SIunits.*;
  import Modelica.Utilities.Streams.print;
  model pendelphi
  // Pendel mit Gleichungen abhängig vom Winkel phi
    Angle phi(start = 0);
    AngularVelocity dphi(start = -2);
    parameter Real g = 9.81;
    parameter Mass m=1;
    Length x(start = 2, fixed = true);
    Length y;
    Velocity dx;
    Velocity dy;
    Real D = 0.0;
    Length L = 2;
    Force F;
  equation
    x = sin(phi)*L;
    y = -cos(phi)*L;
    dy = der(y);
    dx = der(x);
    dphi = der(phi);

    der(dphi) = -g/L * sin(phi) - D* g/L *der(phi);
    //L^2 = x^2+y^2;
    F =m*g*cos(phi) + m*L*dphi^2;

  end pendelphi;

model Ball

// Werfen des Balls
  Real x;
  Real y;
  Real vx;
  Real vy;

  parameter Real m = 1;
  constant Real g = 9.81;
  parameter Real c0=0;

  parameter Real L=2;

equation
  vx = der(x);
  vy = der(y);
  m*der(vx) = 0;
  m * der(vy) = -g*m;

end Ball;

model pendel_struc
  extends pendelphi;
  Integer switch_to(start = 0);

equation
    when F <= 0 or terminal() then
    switch_to = 2;
    terminate("Pendulum to ball");
    end when;

end pendel_struc;

model ball_struc
  extends Ball;
  Integer switch_to(start = 0);
  Angle phi;
  AngularVelocity dphi;
    Real r;
    Integer dummy(start = 0);
equation
  phi = asin(x/L);
  dphi = der(phi);
   r = sqrt(x^2+y^2);

  when r<L then
    dummy = 1;
  end when;

  when r>L and dummy >=1 then
    switch_to = 1;

   terminate("Ball to Pendulum");
  end when;
end ball_struc;
  annotation (uses(Modelica(version="3.2")), Commands(file="PendelStructur.mos"));
end PendelScript;
