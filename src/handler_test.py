# pylint: disable=C0301

"""
Handler test
"""
import json

import handler


def test_empty_request():
    """
    Empty request should return 200
    :return:
    """
    request = {'body': '{}'}
    result = handler.reduce_client_elevation_noise(request, {})

    status_code = result['statusCode']
    result_body = json.loads(result['body'])
    assert status_code == 200
    assert result_body['filter'] == 5
    assert len(result_body['smoothed']) == 0
    assert len(result_body['deltas']) == 0


def test_filter_and_inputarray():
    """
    Should process elevations with given filter
    :return:
    """
    request = {'body': '{"filter":3,"elevations":[1,2,3,4,5,6,7,8,9,10,30,30,30,30,25,20,18,13,10.4,4]}'}

    result = handler.reduce_client_elevation_noise(request, {})

    status_code = result['statusCode']
    result_body = json.loads(result['body'])
    assert status_code == 200
    assert result_body['filter'] == 3
    assert len(result_body['smoothed']) == 20
    assert len(result_body['deltas']) == 19


def test_filter_and_inputarray_base64():
    """
    Should process elevations base64-encoded
    :return:
    """
    body_base64 = 'eyJmaWx0ZXIiOjMsImVsZXZhdGlvbnMiOlsxLDIsMyw0LDUsNiw3LDgsOSwxMCwzMCwzMCwzMCwzMCwyNSwyMCwxOCwxMywxMC40LDRdfQ=='
    request = {'body': body_base64, 'isBase64Encoded': True}

    result = handler.reduce_client_elevation_noise(request, {})

    status_code = result['statusCode']
    result_body = json.loads(result['body'])
    assert status_code == 200
    assert result_body['filter'] == 3
    assert len(result_body['smoothed']) == 20
    assert len(result_body['deltas']) == 19
