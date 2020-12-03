import pytest
from iplib3 import IPAddress, IPv4, IPv6, _ipv4_validator, _ipv6_validator # pylint: disable=import-error

def test_ipv4():
    assert str(IPAddress(25601440).as_ipv4) == '1.134.165.160'
    assert str(IPAddress('192.168.1.1')) == '192.168.1.1'
    assert str(IPv4('192.168.1.1')) == '192.168.1.1'
    assert str(IPAddress('1.1.1.1:8080')) == '1.1.1.1:8080'
    assert str(IPv4('1.1.1.1:8080')) == '1.1.1.1:8080'
    assert str(IPAddress(0xDEADBEEF).as_ipv4) == '222.173.190.239'
    assert str(IPAddress(0xDEADBEEF, port_num=80).as_ipv4) == '222.173.190.239:80'


def test_ipv4_port_initialisation():

    foo = IPv4('222.173.190.239:80')
    bar = IPv4('222.173.190.239', 80)
    baz = IPv4('222.173.190.239', port_num=80)
    spam = IPv4('222.173.190.239:25565', port_num=80) # Argument-given ports should be preferred

    assert foo == bar == baz == spam
    assert str(baz) == '222.173.190.239:80'


def test_ipv6():
    assert str(IPAddress(25601440).as_ipv6) == '0:0:0:0:0:0:186:A5A0'
    assert str(IPAddress('2606:4700:4700::1111')) == '2606:4700:4700::1111'
    assert str(IPv6('2606:4700:4700::1111')) == '2606:4700:4700::1111'
    assert str(IPAddress('[2606:4700:4700::1111]:8080')) == '[2606:4700:4700::1111]:8080'
    assert str(IPv6('[2606:4700:4700::1111]:8080')) == '[2606:4700:4700::1111]:8080'
    assert str(IPAddress(0xDEADBEEF).as_ipv6) == '0:0:0:0:0:0:DEAD:BEEF'


def test_ipv6_full():
    assert IPAddress(25601440).num_to_ipv6(shorten=False) == '0000:0000:0000:0000:0000:0000:0186:A5A0'


def test_ipv6_remove_zeroes():
    assert IPAddress(25601440).num_to_ipv6(remove_zeroes=True) == '::186:A5A0'
    assert IPAddress(0xDEADBEEF).num_to_ipv6(remove_zeroes=True) == '::DEAD:BEEF'


def test_ipv6_port_initialisation():

    foo = IPv6('[::1337:1337:1337:1337]:25565')
    bar = IPv6('::1337:1337:1337:1337', 25565)
    baz = IPv6('::1337:1337:1337:1337', port_num=25565)
    spam = IPv6('[::1337:1337:1337:1337]:80', port_num=25565) # Argument-given ports should be preferred

    assert foo == bar == baz == spam
    assert str(baz) == '[::1337:1337:1337:1337]:25565'


def test_chaining():
    assert str(IPAddress(25601440).as_ipv6.as_ipv4) == '1.134.165.160'


def test_hex_output():

    base = IPAddress(0xDEADBEEF)
    v4 = base.as_ipv4
    v6 = base.as_ipv6

    assert base.hex == '0xDEADBEEF'
    assert v4.hex == '0xDEADBEEF'
    assert v6.hex == '0xDEADBEEF'


def test_ipv4_validator():
    assert _ipv4_validator('1.1.1.1') is True
    assert _ipv4_validator('0.0.0.0') is True
    assert _ipv4_validator('255.255.255.255') is True

    assert _ipv4_validator('192.168.0.1:8080') is True
    assert _ipv4_validator('12.123.234.345') is False
    assert _ipv4_validator('FF.FF.FF.FF') is False
    assert _ipv4_validator('1.1.1.1:314159') is False
    assert _ipv4_validator('12.23.34.45.56') is False
    assert _ipv4_validator('12.23.34.45.56', strict=False) is False

    assert _ipv4_validator('1337.1337.1337.1337') is False
    assert _ipv4_validator('1337.1337.1337.1337:314159') is False
    assert _ipv4_validator('1337.1337.1337.1337', strict=False) is True
    assert _ipv4_validator('1337.1337.1337.1337:314159', strict=False) is True


def test_ipv6_validator():
    assert _ipv6_validator('0:0:0:0:0:0:0:0') is True
    assert _ipv6_validator('FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF') is True
    assert _ipv6_validator('[0:0:0:0:0:0:0:0]:80') is True
    assert _ipv6_validator('[FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF]:65535') is True
    assert _ipv6_validator('::12') is True
    assert _ipv6_validator('314::') is True
    assert _ipv6_validator('2606:4700:4700::1111') is True
