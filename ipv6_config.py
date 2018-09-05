import os
import openvpnsetup as ovs

def ipv6_config(enable, ip, portl6):
    if enable == 1:
        ipv6forward = ovs.subcall('sysctl net.ipv6.conf.all.forwarding ' +
                                  '| grep 0', 1)
        if ipv6forward == 0:
            ovs.subcall('sysctl -w net.ipv6.conf.all.forwarding=1', 1)
            conf = open('/etc/sysctl.conf',
                        'a').write('net.ipv6.conf.all.forwarding = 1').close()
        else:
            print('IPv6 forwarding is already enabled')
        conf = open('/etc/openvpn/server.conf', 'w')
        conf.write('#IPv6 config\n' +
                   'server-ipv6 fd6c:62d9:eb8c::/112\n' +
                   'proto {i}\n'.format(i=portl6) +
                   'tun-ipv6\n' +
                   'push tun-ipv6\n' +
                   'push "route-ipv6 2000::/3"\n' +
                   'push "redirect-gateway ipv6"\n')
        conf.close()
    else:
        conf = open('/etc/openvpn/server.conf',
                    'w').write('local {i}'.format(i=ip).close())
