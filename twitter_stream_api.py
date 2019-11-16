from twython import TwythonStreamer

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print(data['text'])

    def on_error(self, status_code, data):
        print(status_code)


stream = MyStreamer( '2lqt4zKdTSyueMSosEyADkZuq', 'tQHyN0oR46GCGGn7uOTKTFdA5ivB8ixFUNYp4JB8o88rflNh6w'
,'1183084435421351937-wh2G26PTPmvfY5oM37w2CamNkVvcb1', '33ljJ3n3Mm5MxRUYcQfEgN8Zi6WPErVvCZB7PctO0i24d')

# add parameter:
stream.statuses.filter(track='terminator')