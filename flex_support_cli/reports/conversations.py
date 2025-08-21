def get_conv_default_service(client):
    return client.conversations.v1.configuration().fetch().default_chat_service_sid

def fetch_conv_addresses(client):
    return client.conversations.v1.address_configurations.stream()