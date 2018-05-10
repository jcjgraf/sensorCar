// """
//	gets the distance between the sensor head an the hitted object and draws the
// 	"sensorbeam". It can also display the distance in the UI.
// """

var sensors: GameObject[];
var texts: UI.Text[];

var distances: float[];

function Update () {
	getDistance();
	displayDistances();
}

function getDistance() {
	// """
	// 	Mesure distance between sensor and hit object and return an array 
	// containg the information for all sensors
	// """

	var distancesJS = new Array();

	var sensorRange: int = 1000;  // Maximal ranging distance

	// Get distance for all sensors
	for (i = 0; i < sensors.length; i++) {	

		var hit: RaycastHit;

		var position = sensors[i].transform.position;	// Position of the sensorHead
		var angle = sensors[i].transform.eulerAngles.y * Mathf.PI / 180;	// Y Rotation in Rad

		sensorUnitVector = Vector3(Mathf.Sin(angle), 0, Mathf.Cos(angle));	// Unitvector pointing in the direction the sensor does

		// If if hits something, draw a line and get the distance between the sonsor and the hitted object
		if (Physics.Raycast(position, sensorUnitVector, hit)) {  // error: if sensor hits nothing, no value is given for this sensor -> array has not n elements

			Debug.DrawLine(position, hit.point, Color.green);

			// Get distance between sensor head and the hit object
			var distance: float = Vector3.Distance(position, hit.point);

			distancesJS.Push(distance);
		}
	}

	distances = distancesJS.ToBuiltin(float) as float[];

	return distances;
}


function displayDistances() {
	// """
	// 	Display the distance in the UI
	// """

	for (i = 0; i < texts.length; i++) {	

		// At the beginning the ui is not rendered, therefore the texts array is empty. Therefore we need a try and catch
		try {
			// TODO make work with n sensors
			if (i == 0) {
					texts[i].text = "Sensor 1: " + parseInt(distances[i]).ToString();

			} else if (i == 1) {
					texts[i].text = "Sensor 2: " + parseInt(distances[i]).ToString();

			} else if (i == 2) {
					texts[i].text = "Sensor 3: " + parseInt(distances[i]).ToString();
			}
		} catch(e) {
			// Debug.Log("Error displaying distance on textBox: " + e);
		}
	}
}
