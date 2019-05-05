using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace UnityStandardAssets.Vehicles.Car {

	[RequireComponent(typeof (CarController))]
	public class CanvasDrawer : MonoBehaviour {

		private CarController carController;
		private CarSensor carSensor;

		[SerializeField] private Text textfield;

		// Use this for initialization
		void Start () {
			carController = GetComponent<CarController>();
			carSensor = GetComponent<CarSensor>();
		}
		
		// Update is called once per frame
		void Update () {
			textfield.text = "";

			for (int i = 0; i < carSensor.distances.Count; i++) {	

				textfield.text += i + 1 + ": " + (int)carSensor.distances[i] + "\n";

			}
		}
	}
}
