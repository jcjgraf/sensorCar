/*
	gets the distance between the sensor head an the hitted object and draws the
	"sensorbeam". It can also display the distance in the UI.
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CarSensor : MonoBehaviour {
	/*
		gets the distance between the sensor head an the hitted object and draws the
		"sensorbeam". It can also display the distance in the UI.
	*/

	[SerializeField] private GameObject[] sensors;

	public List<float> distances;
	
	void Update() {
		/*
			Mesure distance between sensor and hit object and return an array 
			containg the information for all sensors
		*/

		RaycastHit hit;

		for (int i = 0; i < sensors.Length; i++) {

			Vector3 position = sensors[i].transform.position;	// Position of the sensorHead
			float angle = sensors[i].transform.eulerAngles.y * Mathf.PI / 180;

			Vector3 sensorUnitVector = new Vector3(Mathf.Sin(angle), 0, Mathf.Cos(angle));	// Unitvector pointing in the direction the sensor does

			// TODO use layermask to exclude sensorhead

			// If if hits something, draw a line and get the distance between the sonsor and the hitted object
			if (Physics.Raycast(position, sensorUnitVector, out hit, Mathf.Infinity)) {  // error: if sensor hits nothing, no value is given for this sensor -> array has not n elements

				Debug.DrawLine(position, hit.point, Color.green);

				// Get distance between sensor head and the hit object
				distances[i] = Vector3.Distance(position, hit.point);
			}
		}
	}
}
