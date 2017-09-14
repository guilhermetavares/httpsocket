HTTPSOCKET
----------

2) Using Python or C++, provide a single file program that:

a. Accepts an HTTP connection
b. Parses the HTTP connection data
c. If the HTTP requests the enpoint '/ws', the program will upgrade the connection to WebSocket
d. Send the following JSON through the WebSocket '{ "status" : "success" }'


Init
----

Create a socket class ``SocketHttp``, passing a full url ex ``ws://echo.websocket.org/`` for the socket connection:
    
    >>> conn = SocketHttp('ws://echo.websocket.org/')


HTTP
----

For make a http connection, uses the method ``http``:

	>>> conn = SocketHttp("https://restcountries.eu/rest/v2/region/europe")
	>>> conn.http()


To see the ``headers``:
	
	>>> print(conn.headers)
	{'Date': 'Thu, 14 Sep 2017 03:40:52 GMT', 'Server': 'Apache/2.4.25 (Debian)', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET', 'Access-Control-Allow-Headers': 'Accept, X-Requested-With', 'Cache-Control': 'public, max-age=86400', 'Content-Type': 'application/json;charset=utf-8', 'Transfer-Encoding': 'chunked'}

To see the ``status_code``:
    
    >>> print(conn.status_code)
    200


WebSocket
---------

For check, if the ``url`` is available to upgrade, just call the method ``assert_websocket``:
    
    >>> conn = SocketHttp("https://restcountries.eu/rest/v2/region/europe")
    >>> conn.assert_websocket()
    False
    >>> conn = SocketHttp("ws://echo.websocket.org/")
    True


For make a upgrade connection, uses the method ``upgrade``:

    >>> conn = SocketHttp("ws://echo.websocket.org/")
    >>> conn.upgrade()
    >>> conn.headers
    {'Connection': 'Upgrade',
	 'Date': 'Thu, 14 Sep 2017 03:55:02 GMT',
	 'Sec-WebSocket-Accept': 'f3GqT8GUCucuiz5mLwm9q+FFDmM=',
	 'Server': 'Kaazing Gateway',
	 'Upgrade': 'websocket'}


To send data, just call the method ``send``:
	
	>>> conn.send('{ "status" : "success" }')

