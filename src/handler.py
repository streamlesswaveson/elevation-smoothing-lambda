"""
Handler module for client elevation noise reduction
"""
import base64
import json

import numpy as np
from scipy.signal import medfilt


def _request_from_event(event):
    body = event.get('body')
    payload = body
    if event.get('isBase64Encoded'):
        payload = base64.b64decode(body, None)

    return json.loads(payload)


def _apply_filter(kernal_size, elevations):
    filtered = medfilt(elevations, kernal_size)
    deltas = np.diff(filtered)

    return filtered, deltas


def _generate_response(kernal_size, filtered, deltas):
    body = {
        "filter": kernal_size,
        "smoothed": filtered.tolist(),
        "deltas": deltas.tolist()
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }


def reduce_client_elevation_noise(event, _context):
    """
    Lambda entry point

    :param event: AWS API Gateway proxy event
    :param _context: AWS lambda context

    """
    request = _request_from_event(event)
    kernal_size = request.get('filter', 5)
    elevations = request.get('elevations', [])

    filtered, deltas = _apply_filter(kernal_size, elevations)

    return _generate_response(kernal_size, filtered, deltas)
