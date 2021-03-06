# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import time

import grpc

import reverse_pb2
import reverse_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(reverse_pb2_grpc.messengerServicer):

    def Send(self, request, context):
        return reverse_pb2.input_reply(message='Hello, %s!' % request.msg)
class IntegerMessage(reverse_pb2_grpc.integer_messageServicer):
    def SendInteger(self, request, context):
        temp = int(request.value)
        temp *= 2
        return reverse_pb2.replyInteger(value=temp)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reverse_pb2_grpc.add_messengerServicer_to_server(Greeter(), server)
    reverse_pb2_grpc.add_integer_messageServicer_to_server(IntegerMessage(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()