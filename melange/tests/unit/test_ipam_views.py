# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from melange import tests
from melange.ipam import models
from melange.ipam import views
from melange.tests.factories import models as factory_models


class TestIpConfigurationView(tests.BaseTest):

    def test_data_returns_block_ip_info(self):
        block1 = factory_models.IpBlockFactory()
        block2 = factory_models.IpBlockFactory()
        interface = factory_models.InterfaceFactory(vif_id_on_device="123")
        ip1 = factory_models.IpAddressFactory(ip_block_id=block1.id,
                                              interface_id=interface.id)
        ip2 = factory_models.IpAddressFactory(ip_block_id=block2.id,
                                              interface_id=interface.id)
        expected_ip1_config = _ip_data(ip1, block1)
        expected_ip2_config = _ip_data(ip2, block2)

        ip_configuration_view = views.IpConfigurationView(ip1, ip2)

        self.assertEqual(expected_ip1_config, ip_configuration_view.data()[0])
        self.assertEqual(expected_ip2_config, ip_configuration_view.data()[1])

    def test_data_returns_deallocated_ip_info(self):
        block = factory_models.IpBlockFactory()
        interface = factory_models.InterfaceFactory(vif_id_on_device="123")
        ip = factory_models.IpAddressFactory(ip_block_id=block.id,
                                              interface_id=interface.id)
        ip.deallocate()
        deallocated_ip = models.IpAddress.find(ip.id)
        expected_ip_config = _ip_data(deallocated_ip, block)
        ip_configuration_view = views.IpConfigurationView(deallocated_ip)

        self.assertEqual(expected_ip_config, ip_configuration_view.data()[0])

    def test_data_returns_route_info(self):
        block = factory_models.IpBlockFactory()
        interface = factory_models.InterfaceFactory(vif_id_on_device="123")
        route1 = factory_models.IpRouteFactory(source_block_id=block.id)
        route2 = factory_models.IpRouteFactory(source_block_id=block.id)
        ip = factory_models.IpAddressFactory(ip_block_id=block.id,
                                             interface_id=interface.id)
        expected_ip_config_routes = [_route_data(route1), _route_data(route2)]

        ip_configuration_view = views.IpConfigurationView(ip).data()[0]
        ip1_config_routes = ip_configuration_view['ip_block'].pop('ip_routes')

        self.assertItemsEqual(expected_ip_config_routes, ip1_config_routes)


def _ip_data(ip, block):
    return {
        'id': ip.id,
        'interface_id': ip.virtual_interface_id,
        'address': ip.address,
        'version': ip.version,
        'ip_block': {
            'id': block.id,
            'cidr': block.cidr,
            'broadcast': block.broadcast,
            'gateway': block.gateway,
            'netmask': block.netmask,
            'dns1': block.dns1,
            'dns2': block.dns2,
            'ip_routes': [],
            },
        }


def _route_data(route):
    return {
        'id': route.id,
        'destination': route.destination,
        'gateway': route.gateway,
        'netmask': route.netmask,
        }


class TestInterfaceConfigurationView(tests.BaseTest):

    def test_data_returns_mac_address(self):
        interface = factory_models.InterfaceFactory()
        mac = models.MacAddress.create(interface_id=interface.id,
                                       address="ab-bc-cd-12-23-34")

        data = views.InterfaceConfigurationView(interface).data()

        self.assertEqual(data['mac_address'], mac.eui_format)
        self.assertEqual(data['id'], interface.virtual_interface_id)

    def test_data_returns_ip_address_configuration_information(self):
        interface = factory_models.InterfaceFactory()

        ip1 = factory_models.IpAddressFactory(interface_id=interface.id)
        ip2 = factory_models.IpAddressFactory(interface_id=interface.id)

        data = views.InterfaceConfigurationView(interface).data()

        self.assertEqual(len(data['ip_addresses']), 2)
        self.assertItemsEqual(data['ip_addresses'],
                              views.IpConfigurationView(ip1, ip2).data())
