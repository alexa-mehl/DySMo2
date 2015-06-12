within ;
model pipe

record globalInfo

parameter Modelica.SIunits.ThermalConductivity lambda=401
      "Specific Thermal Conductance";
  parameter Modelica.SIunits.SpecificHeatCapacity c=386
      "Specific Thermal Capacity";
  parameter Modelica.SIunits.Density rho=8960 "Density";

  parameter Modelica.SIunits.Temperature T0=298 "Initial Temperature";
  parameter Modelica.SIunits.Temperature Th=390 "Heating Temperatur";
  parameter Modelica.SIunits.Area A=0.01^2*Modelica.Constants.pi "Surface";

end globalInfo;

  model elements2 "Conduction demo"

  import Modelica.Thermal.HeatTransfer.*;

    parameter Real ns=2 "Number of Segments";

    parameter Modelica.SIunits.Length l=1 "Length of copper rod";
    parameter Modelica.SIunits.HeatCapacity C=global.c*global.rho*global.A*dx
      "Thermal Capacity";
    parameter Modelica.SIunits.Length dx=l/ns "Length of Segment";
    parameter Modelica.SIunits.ThermalResistance theta= dx/(global.lambda*global.A)
      "Thermal Resistance";
    parameter Modelica.SIunits.ThermalConductance G = 1/theta;

    globalInfo global;

  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature
                        InpT0 annotation(Placement(visible = true, transformation(origin={-350.5,
              -90.5},                                                                                      extent = {{15,-15},{-15,15}}, rotation=270)));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor
                   c1(G = G) annotation(Placement(visible = true, transformation(origin={-349,-23},   extent = {{15,-15},{-15,15}}, rotation=270)));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor
                   c2(G = G) annotation(Placement(visible = true, transformation(origin={-316.735,
              44.238},                                                                                         extent = {{-15,-15},{15,15}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor
                m1(C = C, T(start = 298.15, fixed = true)) annotation(Placement(visible = true, transformation(origin={-350.235,
              77.738},                                                                                                    extent = {{-20,-20},{20,20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor
                m2(C = C, T(start = 298.15, fixed = true)) annotation(Placement(visible = true, transformation(origin={-263.039,
              96.898},                                                                                                  extent = {{-20,-20},{20,20}}, rotation = 0)));
  Real transitionId;
  equation
  connect(c1.port_b,m1.port) annotation(Line(points={{-349,-8},{-350.235,-8},{
            -350.235,57.738}}));
  connect(InpT0.port,c1.port_a) annotation(Line(points={{-350.5,-75.5},{-350.5,-38},
            {-349,-38}}));
  connect(m1.port,c2.port_a) annotation(Line(points={{-350.235,57.738},{-350.235,44.238},
            {-331.735,44.238}}));
  connect(c2.port_b,m2.port) annotation(Line(points={{-301.735,44.238},{-263.039,44.238},
            {-263.039,76.898}}));

  InpT0.T = if time < 3000 then 298.15 else if time < 40000 then 390 else if time < 70000 then 290 else 390;

  when abs(c1.dT) <= 90 then
    transitionId = 1;
      terminate("end");
  end when;

  annotation (Diagram(coordinateSystem(preserveAspectRatio=false, extent={{-380,-120},
              {320,120}}),       graphics), Icon(coordinateSystem(extent={{-380,
              -120},{320,120}})));
  end elements2;

  model elements10 "Conduction demo"

  import Modelica.Thermal.HeatTransfer.*;
    parameter Real ns=10 "Number of Segments";

    parameter Modelica.SIunits.Length l=1 "Length of copper rod";
    parameter Modelica.SIunits.HeatCapacity C=global.c*global.rho*global.A*dx
      "Thermal Capacity";
    parameter Modelica.SIunits.Length dx=l/ns "Length of Segment";
    parameter Modelica.SIunits.ThermalResistance theta= dx/(global.lambda*global.A)
      "Thermal Resistance";
    parameter Modelica.SIunits.ThermalConductance G = 1/theta;

    globalInfo global;

  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature
                        InpT0 annotation(Placement(visible = true, transformation(origin={-350.5,
              -90.5},                                                                                      extent = {{15,-15},{-15,15}}, rotation=270)));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor
                   c1(G = G) annotation(Placement(visible = true, transformation(origin={-349,-23},   extent = {{15,-15},{-15,15}}, rotation=270)));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor
                   c2(G = G) annotation(Placement(visible = true, transformation(origin={-316.735,
              44.238},                                                                                         extent = {{-15,-15},{15,15}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor
                   c3(G = G) annotation(Placement(visible = true, transformation(origin={-227.021,
              44.131},                                                                                         extent = {{-15,-15},{15,15}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor
                   c4(G = G) annotation(Placement(visible = true, transformation(origin={-144.021,
              42.631},                                                                                        extent = {{-15,-15},{15,15}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor
                   c5(G = G) annotation(Placement(visible = true, transformation(origin={-55.521,
              41.631},                                                                                       extent = {{-15,-15},{15,15}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor
                   c6(G = G) annotation(Placement(visible = true, transformation(origin={25.979,
              42.131},                                                                                        extent = {{-15,-15},{15,15}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor
                   c7(G = G) annotation(Placement(visible = true, transformation(origin={105.979,
              44.131},                                                                                        extent = {{-15,-15},{15,15}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.ThermalConductor
                   c8(G = G) annotation(Placement(visible = true, transformation(origin={190.479,
              39.631},                                                                                        extent = {{-15,-15},{15,15}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor
                m1(C = C, T(start = 298.15, fixed = true)) annotation(Placement(visible = true, transformation(origin={-350.235,
              77.738},                                                                                                    extent = {{-20,-20},{20,20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor
                m2(C = C, T(start = 298.15, fixed = true)) annotation(Placement(visible = true, transformation(origin={-263.039,
              96.898},                                                                                                  extent = {{-20,-20},{20,20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor
                m3(C = C, T(start = 298.15, fixed = true)) annotation(Placement(visible = true, transformation(origin={-187.306,
              88.559},                                                                                                    extent = {{-20,-20},{20,20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor
                m4(C = C, T(start = 298.15, fixed = true)) annotation(Placement(visible = true, transformation(origin={-99.806,
              95.059},                                                                                                    extent = {{-20,-20},{20,20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor
                m5(C = C, T(start = 298.15, fixed = true)) annotation(Placement(visible = true, transformation(origin={-17.806,
              94.559},                                                                                                    extent = {{-20,-20},{20,20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor
                m6(C = C, T(start = 298.15, fixed = true)) annotation(Placement(visible = true, transformation(origin={65.694,
              87.559},                                                                                                    extent = {{-20,-20},{20,20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor
                m7(C = C, T(start = 298.15, fixed = true)) annotation(Placement(visible = true, transformation(origin={140.194,
              93.059},                                                                                                    extent = {{-20,-20},{20,20}}, rotation = 0)));
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor
                m8(C = C, T(start=298.15, fixed=true))     annotation(Placement(visible = true, transformation(origin={224.5,93},   extent = {{-20,-20},{20,20}}, rotation = 0)));
  Real transitionId;
  equation
  connect(c1.port_b,m1.port) annotation(Line(points={{-349,-8},{-350.235,-8},{
            -350.235,57.738}}));
  connect(InpT0.port,c1.port_a) annotation(Line(points={{-350.5,-75.5},{-350.5,-38},
            {-349,-38}}));
  connect(m7.port,c8.port_a) annotation(Line(points={{140.194,73.059},{140.194,39.631},
            {175.479,39.631}}));
  connect(m1.port,c2.port_a) annotation(Line(points={{-350.235,57.738},{-350.235,44.238},
            {-331.735,44.238}}));
  connect(c5.port_b,m5.port) annotation(Line(points={{-40.521,41.631},{-17.806,41.631},
            {-17.806,74.559}}));
  connect(m4.port,c5.port_a) annotation(Line(points={{-99.806,75.059},{-99.806,41.631},
            {-70.521,41.631}}));
  connect(c2.port_b,m2.port) annotation(Line(points={{-301.735,44.238},{-263.039,44.238},
            {-263.039,76.898}}));
  connect(c3.port_b,m3.port) annotation(Line(points={{-212.021,44.131},{-187.306,44.131},
            {-187.306,68.559}}));
  connect(m2.port,c3.port_a) annotation(Line(points={{-263.039,76.898},{-263.039,44.131},
            {-242.021,44.131}}));
  connect(c7.port_b,m7.port) annotation(Line(points={{120.979,44.131},{140.194,44.131},
            {140.194,73.059}}));
  connect(m6.port,c7.port_a) annotation(Line(points={{65.694,67.559},{65.694,44.131},
            {90.979,44.131}}));
  connect(c6.port_b,m6.port) annotation(Line(points={{40.979,42.131},{65.694,42.131},
            {65.694,67.559}}));
  connect(m5.port,c6.port_a) annotation(Line(points={{-17.806,74.559},{-17.806,42.131},
            {10.979,42.131}}));
  connect(c4.port_b,m4.port) annotation(Line(points={{-129.021,42.631},{-99.806,42.631},
            {-99.806,75.059}}));
  connect(m3.port,c4.port_a) annotation(Line(points={{-187.306,68.559},{-187.306,42.631},
            {-159.021,42.631}}));
  InpT0.T = if time < 3000 then 298.15 else if time < 40000 then 390 else if time < 70000 then 290 else 390;

    connect(c8.port_b, m8.port) annotation (Line(
        points={{205.479,39.631},{222.74,39.631},{222.74,73},{224.5,73}},
        color={191,0,0},
        smooth=Smooth.None));

  when c1.dT <=0.01 then
      transitionId = 1;
    terminate("ende");
  end when;

  annotation (Diagram(coordinateSystem(preserveAspectRatio=false, extent={{-380,-120},
              {320,120}}),       graphics), Icon(coordinateSystem(extent={{-380,
              -120},{320,120}})));
  end elements10;

  annotation (uses(Modelica(version="3.2")));
end pipe;
