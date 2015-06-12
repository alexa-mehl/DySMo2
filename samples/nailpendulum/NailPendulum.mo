within ;
package NailPendulum
  import Modelica.Math.sin;
  import Modelica.Math.asin;
  import Modelica.Math.acos;
  import Modelica.Math.cos;
  import Modelica.SIunits.*;

model nail
  parameter Position x;
  parameter Position y;
  parameter Angle alpha = asin(x /(sqrt(x^2+y^2)));
end nail;

model pendulum_phi
  // pundulum with equtaions that are dependent on the angle phi

    parameter Position auf_x(fixed=false);
    parameter Position auf_y(fixed=false);
    Angle phi(start = 90*3.14/180);
    AngularVelocity dphi(start = -0.5, fixed=true);
    parameter Real g = 9.81;
    parameter Mass m=1;
    Length x;
    Length y;
    Velocity dx;
    Velocity dy;
    parameter Real D = 0.005;
    Length L;
    Force F;

equation
    der(L)=0;
    x = sin(phi)*L+auf_x;
    y = -cos(phi)*L+auf_y;
    dy = der(y);
    dx = der(x);
    dphi = der(phi);
    der(dphi) = -g/L * sin(phi) - D* g/L *der(phi);
    F =m*g*cos(phi) + m*L*dphi^2;

end pendulum_phi;

model ball
  // ball-throwing

    Real x;
    Real y;
    Real vx;
    Real vy;
    parameter Real m = 1;
    constant Real g = 9.81;
    parameter Real c0=0;
    parameter Real L = 2;

equation
    vx = der(x);
    vy = der(y);
    m*der(vx) = 0;
    m*der(vy) = -g*m;

end ball;

model ball_struc

    extends ball;
    Integer transitionId(start=0);
    nail n(x=-0.7, y=-0.7);
    Boolean long;
    parameter StateSelect stateSelect=StateSelect.never;
    Angle phi(stateSelect=stateSelect);
    AngularVelocity dphi;
    Real r;
    Real phi1(start=0);

equation
    der(phi1)=0;

    if long then
       phi = -acos(-y/sqrt(x^2 + y^2));
    else
       phi = -acos(-(y-n.y)/sqrt((x-n.x)^2 + (y-n.y)^2));
    end if;
      dphi = der(phi);

      if long then
          r =sqrt((x)^2 + (y)^2);
      else
          r =sqrt((x - n.x)^2 + (y - n.y)^2) + sqrt(n.x^2 + n.y^2);
      end if;
algorithm
      when phi>n.alpha and long==false then
        long :=true;
      end when;
      when (r>2+0.0001) then
        transitionId :=1;

        if long then
          reinit(phi1,-acos(-y/sqrt(x^2 + y^2)));
        else
          reinit(phi1,-acos(-(y-n.y)/sqrt((x-n.x)^2 + (y-n.y)^2)));
        end if;

        terminate("ball to pendulum");
      end when;

end ball_struc;

model pendulum_struc
  extends pendulum_phi;

  parameter Length Lmax = 2;
  parameter Length Lmin = Lmax-(sqrt(n.x^2+n.y^2));
  Integer transitionId(start = 0);
  nail n(x = -0.7, y = -0.7);
  Boolean long(start=true);

initial equation
    if long == true then
      L = Lmax;
      auf_x = 0;
      auf_y = 0;
    else
      L = Lmin;
      auf_x = n.x;
      auf_y = n.y;

    end if;
equation

algorithm
      when L>=Lmax and phi<n.alpha and dphi<0 then
          transitionId :=1;
          long :=false;
          reinit(dphi, dphi*Lmax/Lmin);
          terminate("test 1");
      end when;
      when L<Lmax and phi>n.alpha and dphi>0 then
          transitionId :=1;
          long :=true;
          reinit(dphi, dphi*Lmin/Lmax);
          terminate("test 2");
      end when;
      when F <= 0 then
        transitionId :=2;
        terminate("pendulum to ball");
    end when;

end pendulum_struc;

  annotation (uses(Modelica(version="3.2")));

end NailPendulum;
