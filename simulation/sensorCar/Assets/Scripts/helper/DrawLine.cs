using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DrawLine : MonoBehaviour {

	[SerializeField] private GameObject lineGeneratorPrefab;
	[SerializeField] private Transform car;
	[SerializeField] private float deltaRecordTime;

	private List<Vector3> pointPositions;

	private GameObject lineGenerator;
	private LineRenderer lineRenderer;


	private void Start() {
		lineGenerator = Instantiate (lineGeneratorPrefab);
		lineRenderer = lineGenerator.GetComponent<LineRenderer> ();

		pointPositions = new List<Vector3> ();

		InvokeRepeating("drawLineSegment", 0, deltaRecordTime);
	}

	private void drawLineSegment() {
		
		pointPositions.Add (car.position);

		lineRenderer.positionCount = pointPositions.Count;

		lineRenderer.SetPosition (pointPositions.Count - 1, car.position);
	}
}
