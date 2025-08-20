

def taskrouter_workers(client=None, workspace_sid=None):
    workers = client.taskrouter.v1.workspaces(workspace_sid).workers.stream()
    return workers
    

def taskrouter_queues(client=None, workspace_sid=None):
    queues = client.taskrouter.v1.workspaces(workspace_sid).task_queues.stream()
    return queues