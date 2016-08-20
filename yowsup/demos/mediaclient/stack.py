import sys

from yowsup.stacks import  YowStackBuilder
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS, YOWSUP_PROTOCOL_LAYERS_FULL
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.network import YowNetworkLayer
# from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
# from yowsup.layers.stanzaregulator import YowStanzaRegulator
# from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
# from yowsup.layers.protocol_acks import YowAckProtocolLayer
# from yowsup.layers.logger import YowLoggerLayer
from yowsup.common import YowConstants
from yowsup.env import YowsupEnv
from yowsup import env

from .layer import SendMediaLayer


class SendMediaStack(object):

    def __init__(self, credentials, messages, encryptionEnabled = True):
        # layers = (SendMediaLayer,) + (YOWSUP_PROTOCOL_LAYERS_FULL,) + YOWSUP_CORE_LAYERS

        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(SendMediaLayer)\
            .build()

        self.stack.setProp(SendMediaLayer.PROP_MESSAGES, messages)
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, credentials)
        self.stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
        self.stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
        self.stack.setProp(YowCoderLayer.PROP_RESOURCE, YowsupEnv.getCurrent().getResource())
        self.stack.setProp(PROP_IDENTITY_AUTOTRUST, True)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)