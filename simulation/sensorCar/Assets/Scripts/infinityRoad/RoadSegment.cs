using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class RoadSegment {

	public GameObject prefab;
	public Vector3 standardPosition;
	public Vector3 standardRotation;
	public Vector3 standardScale;

	public Vector3 deltaEndPosition;
	public Vector3 deltaEndRotation;
	public Vector3 deltaEndScale;
}
