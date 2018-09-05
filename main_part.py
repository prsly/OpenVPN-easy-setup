def main_part(portn, portl, cipher):
    conf = open('/etc/openvpn/server.conf', 'a')
    conf.write('port {i}\n'.format(i=portn) +
               'proto {i}\n'.format(i=portl) +
               'dev tun\n\n#for cert revoke check\n' +
               'crl-verify /etc/openvpn/easy-rsa/keys/crl.pem\n\n' +
               'server 10.1.0.0 255.255.255.0\ntopology subnet\n' +
               'push "redirect-gateway def1 bypass-dhcp"\n\n' +
               '#duplicate-cn\n\npush "dhcp-option DNS 8.8.8.8"\n' +
               'push "dhcp-option DNS 8.8.4.4"\n\ncomp-lzo adaptive\n' +
               'push "comp-lzo adaptive"\n\nmssfix 0\npush "mssfix 0"\n\n' +
               '#management 0.0.0.0 7000 /etc/open-vpn/management-password\n' +
               '\n#duplicate-cn\nkeepalive 10 120\ntls-timeout 160\nhand-' +
               'window 160\n\ncipher {i}\n'.format(i=cipher) +
               'auth SHA256\n\n#uncomment for 2.4.x feature to disable ' +
               'automatically negotiate in AES-256-GCM\n#ncp-disable\n\n' +
               '#max-clients 300\n\n#user nobody\n#group nobody\n\n' +
               'persist-key\npersist-tun\n\nstatus /etc/openvpn/logs/openvpn' +
               '-status.log\nlog-append /etc/openvpn/logs/openvpn.log\n\n' +
               'verb 2\n#reneg-sec 864000\nmute 3\ntls-server\n' +
               '#script-security 3\n\n#buffers\nsndbuf 393216\n' +
               'rcvbuf 393216\npush "sndbuf 393216"\npush "rcvbuf 393216"\n')
    conf.close()
