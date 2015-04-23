within ;
package dominospiel
import Modelica.SIunits.*;
constant Real pi= Modelica.Constants.pi;
  model dominostein
    import Modelica.SIunits.*;
    //parameter Real D=0.046/2;
    parameter Real X=0.008;
    parameter Real Y=0.024;
    parameter Real Z=0.046;
    Angle phi;
    Real phi_deg;
    parameter Real m=0.01;
    constant Real g=9.81;
    parameter Real theta=m*(X^2 + Z^2)/3;
    AngularVelocity omega(start=0.0316, fixed = true);
    parameter Real R=0.5*sqrt(X^2 + Z^2);
    Real T;
    Real x;
    Real z;
    //Real L;
  equation
    Modelica.Math.sin(phi) = x/Z;
    Modelica.Math.cos(phi) = z/Z;
    theta*der(omega) = T;
    der(phi) = omega;
    phi_deg = phi*180/pi;

    if phi < 90/180*pi then
      T = m*g*R*Modelica.Math.sin(phi);
    else
      T = 0;
    end if;

    when phi >= 90/180*3.1416 then
      reinit(omega,0);
    end when;

  end dominostein;

  model stones
    parameter Real D=0.011; // Abstand der Steine
    parameter Integer active=1, fallen=0, gesamt=5; // Steine
    parameter Integer rest=gesamt - fallen - active; // Gesamtanzahl
    dominostein stones[active]; // Array aktive Steine
    Integer transitionId; // Transitions ID
  algorithm
    // Stein wird angestoßen
    when stones[active].x > D and rest > 0 then
      transitionId := 1;
      terminate("crash");
    end when;
    // Stein ist gefallen
    when stones[1].phi_deg > 90 and active > 1 then
      transitionId := 2;
      terminate("ground");
    end when;
    // Ende der Simulation
     when stones[1].phi_deg > 90 and active == 1 then
      transitionId := 3;
      terminate("simulation end");
    end when;

  end stones;

  annotation (uses(Modelica(version="3.2")),
    version="1",
    conversion(noneFromVersion=""));
end dominospiel;
