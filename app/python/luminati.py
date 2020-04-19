# #!/usr/bin/env python
# import sys
# print('If you get error "ImportError: No module named \'six\'" install six:\n' +
#       '$ sudo pip install six')
# print('To enable your free eval account and get CUSTOMER, YOURZONE and ' +
#       'YOURPASS, please contact sales@luminati.io')
# if sys.version_info[0] == 2:
#     import six
#     from six.moves.urllib import request
#     opener = request.build_opener(
#         request.ProxyHandler(
#             {'http': 'http://lum-customer-hl_18b66636-zone-static:sf29m4yulha4@zproxy.lum-superproxy.io:22225',
#              'https': 'http://lum-customer-hl_18b66636-zone-static:sf29m4yulha4@zproxy.lum-superproxy.io:22225'}))
#     print(opener.open('http://lumtest.com/myip.json').read())
# if sys.version_info[0] == 3:
#     import urllib.request
#     opener = urllib.request.build_opener(
#         urllib.request.ProxyHandler(
#             {'http': 'http://lum-customer-hl_18b66636-zone-static:sf29m4yulha4@zproxy.lum-superproxy.io:22225',
#              'https': 'http://lum-customer-hl_18b66636-zone-static:sf29m4yulha4@zproxy.lum-superproxy.io:22225'}))
#     print(opener.open('http://lumtest.com/myip.json').read())

#!/usr/bin/env python
import sys
print('If you get error "ImportError: No module named \'six\'" install six:\n' +
      '$ sudo pip install six')
print('To enable your free eval account and get CUSTOMER, YOURZONE and ' +
      'YOURPASS, please contact sales@luminati.io')
if sys.version_info[0] == 2:
    import six
    from six.moves.urllib import request
    opener = request.build_opener(
        request.ProxyHandler(
            {'http': '127.0.0.1:24001',
             'https': '127.0.0.1:24001'}))
    print(opener.open('http://lumtest.com/myip.json').read())
if sys.version_info[0] == 3:
    import urllib.request
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler(
            {'http': '127.0.0.1:24001',
             'https': '127.0.0.1:24001'}))
    print(opener.open('http://lumtest.com/myip.json').read())
