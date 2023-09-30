# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from solrpi import fronius_inverter
import responses
import json

@responses.activate
def test_fronius():

    file = open('test/sample_fronius_1_response.json')
    sample_response = json.load(file)
    file.close()

    inverter = fronius_inverter.FroniusInverter()

    responses.add(responses.GET, fronius_inverter.FRONIUS_URL,
                  json=sample_response, status=200)
    
    retval = inverter.get_watt()
    assert retval == [-1166.3, 1390.1468505859375]