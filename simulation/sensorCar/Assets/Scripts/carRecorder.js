/*
	In recording-mode it retrieves the sensor information and saved it to a
	specified file in regular intervalls.
	The recording-mode is turned on with "r", and stopped with "f"
*/

import System;
import System.IO;

var filePath: String = "../dataset/";
var fileName: String = "track";
var isRecording: boolean = false;
var recordTimeInterval: float = 0.2;

var carSensor: MonoBehaviour; // TODO: get the script directly (without haveing to drag n drop it)
var carController: MonoBehaviour;

var doRecordSensors: boolean = true;
var doRecordSteerAngle: boolean = true;
var doRecordCurrentSpeed: boolean = false;
var doRecordVerticalInput: boolean = false;

function Update() {
    if (Input.GetKeyDown("f")) {
    	record(false);
    }

    if (Input.GetKeyDown("r")) {
    	record(true);
    }
}

function record(doRecord) {
	/*
		Save retrieved sensor data in a periodical interval to a textfile when
		the recording-mode is enabled by pressing "r". "f" for disable it
	*/

	var sw: StreamWriter;

	// Toggle recording
	if (doRecord && !isRecording) {
		Debug.Log("Started recording");

		// Add current ticks to the filename so that is unique
		var t: System.DateTime = System.DateTime.Now;
		var fullName = fileName + t.Ticks + ".txt";

		if (!File.Exists(filePath)) {
			Directory.CreateDirectory(filePath);
		}

		sw = new StreamWriter(filePath + fullName, true);

		isRecording = true;

		Debug.Log("Recording to: " + filePath + fullName);

	} else if (!doRecord && isRecording) {
		Debug.Log("Stopped recording");

		isRecording = false;

		sw.Close();  // error is thrown
	}

	while (isRecording) {

		var distances = carSensor.distances;
		var steerAngle = carController.CurrentSteerAngle;
		var currentSpeed = carController.CurrentSpeed;
		var verticalInput = carController.AccelInput;

		var saveString: String = "";

		if (doRecordSensors) {
			for (i = 0; i < distances.Count; i++) {
				saveString = saveString + distances[i] + ",";
			}
		}

		if (doRecordSteerAngle) {
			saveString = saveString + steerAngle + ",";
		}

		if (doRecordCurrentSpeed) {
			saveString = saveString + currentSpeed + ",";
		}

		if (doRecordSteerAngle) {
			saveString = saveString + verticalInput + ",";
		}

		if (saveString[saveString.Length - 1] == ",") {
			saveString = saveString.Substring(0, saveString.Length - 1);
		}

		sw.WriteLine(saveString);
		sw.Flush();

		Debug.Log("Added entry to file: " + saveString);

		yield WaitForSeconds(recordTimeInterval);
	}
}
