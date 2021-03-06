package org.firstinspires.ftc.teamcode.opModes.Tests;

import static org.firstinspires.ftc.teamcode.modules.HardwareConfig.LINE_SENSOR_BACK;
//import static org.firstinspires.ftc.teamcode.modules.HardwareConfig.LINE_SENSOR_MID;

import com.acmerobotics.dashboard.FtcDashboard;
import com.acmerobotics.dashboard.config.Config;
import com.acmerobotics.dashboard.telemetry.TelemetryPacket;
import com.qualcomm.hardware.rev.Rev2mDistanceSensor;
import com.qualcomm.hardware.rev.RevColorSensorV3;
import com.qualcomm.robotcore.eventloop.opmode.TeleOp;
import com.qualcomm.robotcore.eventloop.opmode.Disabled;
import com.qualcomm.robotcore.eventloop.opmode.LinearOpMode;
import com.qualcomm.robotcore.hardware.AnalogInput;
import com.qualcomm.robotcore.hardware.ColorSensor;
import com.qualcomm.robotcore.hardware.DigitalChannel;
import com.qualcomm.robotcore.hardware.DistanceSensor;
import com.qualcomm.robotcore.util.ElapsedTime;

import org.firstinspires.ftc.robotcontroller.external.samples.SensorDIO;
import org.firstinspires.ftc.robotcore.external.Telemetry;
import org.firstinspires.ftc.robotcore.external.navigation.DistanceUnit;
import org.firstinspires.ftc.teamcode.Robot21;
import org.firstinspires.ftc.teamcode.misc.AmperkaProximitySensor;

@Config
@TeleOp(group = "Sensor")
public class SensorTest extends LinearOpMode {
//    private AnalogInput input;
//    private AnalogInput backline, midline;
//    private AmperkaProximitySensor distanceSensor;
    private RevColorSensorV3 distanceSensor;
//    public static double midvalue = 0.35;
    public static double backvalue = 0.35;
    public static double offset = 60;
    private FtcDashboard dashboard;

    @Override
    public void runOpMode() throws InterruptedException {
//        Robot21 R = new Robot21();
//        R.attachGamepads(gamepad1, gamepad2);
//        R.init(this);
        distanceSensor = hardwareMap.get(RevColorSensorV3.class, "distance_sensor");

        dashboard = FtcDashboard.getInstance();
        dashboard.setTelemetryTransmissionInterval(25);
        telemetry.setDisplayFormat(Telemetry.DisplayFormat.HTML);
//        distanceSensor = hardwareMap.get(AmperkaProximitySensor.class, "distance_sensor");
//        distanceSensor.addTelemetry(telemetry);
//        distanceSensor.initialize();
//        while (distanceSensor.init()) {
//            telemetry.addData("Distance sensor init error!", null);
//            telemetry.update();
//        }
////        distanceSensor.setDefaultSettings();
//        input = hardwareMap.get(AnalogInput.class, "sensor_range");
//        backline = hardwareMap.get(AnalogInput.class, LINE_SENSOR_BACK);
//        midline = hardwareMap.get(AnalogInput.class, LINE_SENSOR_MID);

        waitForStart();

        ElapsedTime t = new ElapsedTime();
        while(opModeIsActive()) {
            TelemetryPacket packet = new TelemetryPacket();
//            R.control(false, t.milliseconds());
//            R.intake.update();
            telemetry.addData("Distance in mm", distanceSensor.getDistance(DistanceUnit.MM));
            telemetry.addData("isFull", distanceSensor.getDistance(DistanceUnit.MM) < offset);
            telemetry.addData("<font color='red'>my text here</font>", null);
            packet.addLine("Distance in mm: " + distanceSensor.getDistance(DistanceUnit.MM));
            packet.addLine("isFull: " + (distanceSensor.getDistance(DistanceUnit.MM) < offset));
//            telemetry.addData("Voltage: ", input.getVoltage());
//            telemetry.addData("isFull", R.intake.isFull());
//            telemetry.addData("isLineMid", midline.getVoltage() < midvalue);
//            telemetry.addData("isLineBack", backline.getVoltage() < backvalue);
//            telemetry.addData("BackVoltage", backline.getVoltage());
//            telemetry.addData("TiltVel", R.imu.tiltVelocity());
//            telemetry.addData("tilthead", R.imu.getTiltHeading());
            dashboard.sendTelemetryPacket(packet);
            telemetry.update();
        }
    }

}