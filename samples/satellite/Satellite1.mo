within ;
package Satellite
import Modelica.SIunits.*;
  constant Real g0=9.81;
 final constant Real pi=2*Modelica.Math.asin(1.0);

model Planet
parameter Real G;
parameter Real M;
  parameter Real r;
end Planet;

    model Satellite
    parameter Real M=5.976e24;
    parameter Real G=6.670*10^(-11);
    Real a;
    Real ax;
    Real ay;
    Real r;
    Real x;
    Real y(start = 6378e3 + 400000);
    Real vx(start=7670);
    Real vy;

    Real v;
    Integer loops(start=0);

    equation
    a = -G*M/(r*r);
    ax = a*x/r;
    ay = a * y/r;

    r^2 = x^2 + y^2;
    v^2 = vx^2+vy^2;
    der(vx) = ax;
    der(vy) = ay;
    der(x) = vx;
    der(y) = vy;

    when vy <= 0 then
      loops = pre(loops)+1;
    end when;

    end Satellite;

    model SatelliteChange
    parameter Real M=5.976e24;
    parameter Real G=6.670*10^(-11);

    Real a;
    Real ax;
    Real ay;
    Real r;
    Real x;
    Real y(start = 4000);
    Real vx;
    Real vy;

    Real v;
    parameter Real F = 7;

    equation
    a = -G*M/(r*r);
    ax = a*x/r - F;
    ay = a * y/r;

    r^2 = x^2 + y^2;
    v^2 = vx^2+vy^2;
    der(vx) = ax;
    der(vy) = ay;
    der(x) = vx;
    der(y) = vy;
    /*
when (der(x) > 0 and pre(aa) <= 0) then
  aa = (startX + abs(x))/2;
  epsilon = -startX/aa + 1;
end when;
*/
    annotation ();
    end SatelliteChange;

model Rocket
  parameter Real G=6.6742*10^(-11);
  parameter Real M=5.974*10^(24);
  parameter Real radius_planet=6371000;

  parameter Real m0=100000;
  Mass m(start=m0);
  Mass m_boost(start=87000);

  Velocity v(displayUnit="km/s");
  Force F_schub;
  Length h;

  Real m_srb;

  Real g;

  Real ce_srb;

  Real psi(start=90*pi/180);
  Pressure p;
  parameter Real p_0=101300;
  Real F_g;
  Real F_lw;
  parameter Real cwA=0.5;

  Real rho;

  Length x( start = -9.116406537737496E+005);
  Real Rk;
  Real Is=300;
  Length height;
  Real vx;
  Real vy;
equation
  height = h+radius_planet;

  when h > 1000 then
    reinit(psi, 84.5*pi/180);
  end when;

  der(psi) = if h < 1000 then 0 else -v/Rk;

  F_schub = m_srb*ce_srb;
  g = G*M/(radius_planet + h)^2;

  ce_srb = g0*Is;
  F_g = m*g;
  p = p_0*exp(-(1.29*g*h)/p_0);
  rho = 1.29*p/100000;
  F_lw = cwA*rho/2*v^2;

  m*der(v) = (-F_schub - F_lw) - F_g*sin(psi);
  v^2/Rk = g*cos(psi);

  vx = der(x);
  vy = der(h);
  der(h) = v*sin(psi);
  der(x) = v*cos(psi);

  m_srb = if time <= 160 then -500 else if time < 240 then -100 else if time <306 then   -30 else 0;

  when time >= 160 then
    reinit(m,13000);
  end when;

  when time >= 240 then
    reinit(m,3000);
  end when;

  der(m_boost) = m_srb;
  der(m) = der(m_boost);

end Rocket;

  model PlanetRocket
  Planet earth(M=5.976e24,G=6.670*10^(-11), r= 6371000);
  Rocket rocket(M = earth.M, G = earth.G,radius_planet = earth.r);
  Integer transitionId(start = 0);
  equation
    when time >480 then
      transitionId = 1;
      terminate("End");
    end when;
  end PlanetRocket;

  model PlanetSatellite
  Planet earth(M=5.976e24,G=6.670*10^(-11), r= 6371000);
  Satellite satellite(M = earth.M, G = earth.G);
  //satellitBahn s2(M = erde.M, G = erde.G,startX=6378e3 + 500000);

  Integer transitionId(start = 0);

  equation
  when satellite.loops == 10 then
    transitionId = 1;
    terminate("loops reached");
  end when;
  end PlanetSatellite;

  model PlanetSatelliteChange
  Planet earth(M=5.976e24,G=6.670*10^(-11), r= 6371000);
  SatelliteChange satellite(M = earth.M, G = earth.G);
  parameter Real t(fixed = false);
  Integer transitionId(start = 0);
  initial equation
    t = time;
  equation
    when time-t >=50 then
     transitionId = 1;
    terminate("test");
  end when;

  end PlanetSatelliteChange;
  annotation (uses(Modelica(version="3.2")));
end Satellite;
