

def taskrouter_workers(client=None, workspace_sid=None):
    print("Listing TaskRouter workers...")
    return client.taskrouter.v1.workspaces(workspace_sid).workers.stream()
    

def taskrouter_queues(client=None, workspace_sid=None):
    print("Listing TaskRouter queues...")
    return client.taskrouter.v1.workspaces(workspace_sid).task_queues.stream()