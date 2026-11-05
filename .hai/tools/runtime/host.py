"""Report only caller-supplied host capability evidence."""
from .activities import envelope

def handle(operation, workspace, request, apply):
    op = operation.split('.')[-1].split('/')[-1]
    if not isinstance(request,dict) or (op == 'check' and set(request) - {'models','model','effort'}): return envelope(operation,'input_error',issues=['Unknown or invalid request fields'])
    if apply: return envelope(operation,'input_error',issues=['Host check is read-only'])
    if op != 'check':
        return envelope(operation, 'unsupported', issues=['Host invocation and capability discovery are not integrated'])
    models = request.get('models'); model = request.get('model'); effort = request.get('effort')
    if not isinstance(models,dict) or any(not isinstance(k,str) or not isinstance(v,list) or any(not isinstance(x,str) for x in v) for k,v in models.items()) or not isinstance(model,str) or not isinstance(effort,str):
        return envelope(operation,'input_error',issues=['Supply a model, effort, and model-to-efforts evidence map'])
    supported = model in models and effort in models[model]
    return envelope(operation,'ok' if supported else 'blocked',{'supported': supported, 'model': model, 'effort': effort, 'evidence': 'caller supplied', 'invocation': 'unsupported'},issues=[] if supported else ['Model or effort absent from supplied evidence'])
