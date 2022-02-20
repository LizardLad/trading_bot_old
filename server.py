import os
import json
import http.server
from gi.repository import GLib

trade_confidence = 90.0

class RequestHandlerParent(http.server.BaseHTTPRequestHandler):
	_shared_borg_state = {}

class RequestHandler(RequestHandlerParent):
	def log_request(self, code):
		pass	
	
	def do_GET(self):
		if(self.path in self.__class__._shared_borg_state.get('valid_get_paths', [])):
			#Send to path handler
			cb_idx = self.__class__._shared_borg_state.get('valid_get_paths', []).index(self.path)
			#print('Handler: {}'.format(self.__class__._shared_borg_state.get('get_callbacks', [])[cb_idx]))
			self.__class__._shared_borg_state.get('get_callbacks', [])[cb_idx](self) #Pass the RequestHandler to the path handler
		elif(os.path.splitext(self.path)[1][1:] == 'jsx' or os.path.splitext(self.path)[1][1:] == 'js'):
			handle_get_file(self)
		else:
			self.send_response(418)
			self.send_header('Content-type', 'text/text')
			self.end_headers()
			self.wfile.write(b'Refusing to brew coffee because I am, permanently, a teapot. Serving tea now...')
	
	def do_POST(self):
		if(self.path in self.__class__._shared_borg_state.get('valid_post_paths', [])):
			#Send to path handler
			cb_idx = self.__class__._shared_borg_state.get('valid_post_paths', []).index(self.path)
			content_length = int(self.headers['Content-Length'])
			data = self.rfile.read(content_length).decode('utf-8')
			data = json.loads(data)
			#Pass the RequestHandler to the path handler
			self.__class__._shared_borg_state.get('post_callbacks', [])[cb_idx](self, data)	
		else:
			print(self.path)
			self.send_response(404)
			self.send_header('Content-type', 'text/text')
			self.end_headers()
			self.wfile.write('Unknown endpoint: {}'.format(self.path).encode('utf-8'))

class Server:
	def __init__(self, port):
		self.__httpd = http.server.HTTPServer(('', port), RequestHandler)
		self.handler_class = RequestHandler
		GLib.io_add_watch(self.__httpd.fileno(), GLib.IO_IN, self.__handle_request)

	def register_path_cb(self, paths, cbs, get=True):
		if(get):
			valid_paths = self.handler_class._shared_borg_state.get('valid_get_paths', [])
			callbacks = self.handler_class._shared_borg_state.get('get_callbacks', [])
		else:
			valid_paths = self.handler_class._shared_borg_state.get('valid_post_paths', [])
			callbacks = self.handler_class._shared_borg_state.get('post_callbacks', [])
		
		if(isinstance(paths, list)):
			valid_paths.extend(paths)
			callbacks.extend(cbs)
		else:
			valid_paths.append(paths)
			callbacks.append(cbs)

		if(get):
			self.handler_class._shared_borg_state['valid_get_paths'] = valid_paths
			self.handler_class._shared_borg_state['get_callbacks'] = callbacks
		else:
			self.handler_class._shared_borg_state['valid_post_paths'] = valid_paths
			self.handler_class._shared_borg_state['post_callbacks'] = callbacks

	def __handle_request(self, fd, event):
		self.__httpd.handle_request()
		return True

def handle_get_status(request: RequestHandler):
	status = 'No status to report'
	data = json.dumps(status).encode('utf-8')
	request.send_response(200)
	request.send_header('Content-type', 'application/json')
	request.end_headers()
	request.wfile.write(data)

def handle_get_file(request: RequestHandler, base_path='gui/'):
	path = request.path
	if(path == '/'):
		path = '/index.html'
	else:
		pass

	path = os.path.join(base_path, path[1:]) #Remove the leading /

	if(os.path.splitext(path)[1][1:] == 'jsx' or os.path.splitext(path)[1][1:] == 'js'):
		#Check it exists first
		if(not os.path.isfile(path)):
			print('Does not exist {}'.format(path))
			request.send_response(418)
			request.send_header('Content-type', 'text/text')
			request.end_headers()
			request.wfile.write(b'Refusing to brew coffee because I am, permanently, a teapot. Serving tea now...')
			return

	fp = open(path, 'r')
	data = fp.read().encode('utf-8')
	fp.close()
	request.send_response(200)	
	ext = os.path.splitext(path)[1][1:]
	#Support 4 file types atm (html, css, js, text)
	if(ext == 'html'):
		mime = 'text/html'
	elif(ext == 'css'):
		mime = 'text/css'
	elif(ext == 'js'):
		mime = 'application/javascript'
	elif(ext == 'jsx'):
		mime = 'text/babel'
		mime = 'application/javascript'
		mime = 'text/jsx'
	else:
		#Unknown ext
		print(ext)
		mime = 'text/text'	
	request.send_header('Content-type', mime)
	request.end_headers()
	request.wfile.write(data)

def set_confidence(request, data):
	global trade_confidence
	if(data.get('confidence', None) is None):
		pass
	else:
		trade_confidence = float(data['confidence'])
		trade_confidence = max(min(trade_confidence, 1), 0.34)
	request.send_response(200)
	request.send_header('Content-type', 'text/text')
	request.end_headers()
	request.wfile.write('Set trade confidence: {}'.format(trade_confidence).encode('utf-8'))

def get_confidence_threshold(request):
	request.send_response(200)
	request.send_header('Content-type', 'text/text')
	request.end_headers()
	request.wfile.write(str(trade_confidence).encode('utf-8'))

def get_api_key(request):
	request.send_response(200)
	request.send_header('Content-type', 'text/text')
	request.end_headers()
	request.wfile.write('api_key_server'.encode('utf-8'))

def get_token(request):
	request.send_response(200)
	request.send_header('Content-type', 'text/text')
	request.end_headers()
	request.wfile.write('token_default_server'.encode('utf-8'))

def get_trades(request):
	request.send_response(200)
	request.send_header('Content-type', 'application/javascript')
	request.end_headers()

	data = [{
		'asset_id': 'ETH',
		'asset_name': 'Ethereum',
		'asset_count': 0.5, 
		'buy_time': '2:00pm 01/01/2022', 
		'buy_aud_value': 1500, 
		'sell_time': '4:00pm 01/01/2022', 
		'sell_aud_value': 1700
	}]

	request.wfile.write(json.dumps(data).encode('utf-8'))

def get_positions(request):
	request.send_response(200)
	request.send_header('Content-type', 'application/javascript')
	request.end_headers()

	data = [{
			'asset_id': 'ETH',
			'asset_name': 'Ethereum',
			'asset_count': 2.002,
			'aud_value': 10000.00,
			'percentage_change': 10
		},
		{
			'asset_id': 'BTC',
			'asset_name': 'Bitcoin',
			'asset_count': 0.05,
			'aud_value': 3000.00,
			'percentage_change': -2
		}]
	request.wfile.write(json.dumps(data).encode('utf-8'))

def get_upcoming_trades(request):
	request.send_response(200)
	request.send_header('Content-type', 'application/javascript')
	request.end_headers()

	data = [
		{
			'asset_id': 'ETH', 
			'asset_count': 2.002, 
			'aud_value': 10000.00, 
			'timer': 30
		}
	]
	request.wfile.write(json.dumps(data).encode('utf-8'))

if(__name__ == '__main__'):
	server = Server(8080)
	valid_get_paths = ['/status', '/', '/main.js', '/styles/main.css', 
	'/styles/base.css', '/styles/icons.css', '/index.html', '/positions.js', 
	'/api/get/confidence_threshold', '/api/get/api_key', '/api/get/token',
	'/api/get/trades', '/api/get/positions', '/api/get/upcoming_trades']
	get_callbacks = [handle_get_status, handle_get_file, handle_get_file, handle_get_file, 
	handle_get_file, handle_get_file, handle_get_file, handle_get_file, 
	get_confidence_threshold, get_api_key, get_token,
	get_trades, get_positions, get_upcoming_trades]

	valid_post_paths = ['/api/set/confidence_threshold']
	post_callbacks = [set_confidence]

	server.register_path_cb(valid_get_paths, get_callbacks, get=True)
	server.register_path_cb(valid_post_paths, post_callbacks, get=False)

	loop = GLib.MainLoop()
	try:
		loop.run()
	except KeyboardInterrupt:
		pass
