"""Command line dispatcher for the modular HAI runtime."""
import argparse
import importlib
import json
from pathlib import Path
import sys
from .storage import SafetyError, checked_path, read_json

GROUPS = {'startup':'startup', 'environment':'environment', 'profiles':'environment',
          'configuration':'environment', 'activities':'activities', 'activity':'activities',
          'packages':'packages', 'agents':'packages', 'recording':'recording', 'host':'host'}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', default=None)
    parser.add_argument('--request', default=None)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('group', choices=GROUPS)
    parser.add_argument('action', nargs='?', default='')
    # parse_intermixed_args permits common options on either side of group/action.
    try:
        args = parser.parse_intermixed_args(argv)
    except SystemExit as exc:
        if exc.code == 0: return 0
        print(json.dumps({'ok':False,'status':'invalid','operation':None,'result':{},'changed_files':[], 'issues':[{'code':'invocation','message':'Invalid arguments'}]}))
        return 2
    operation = args.group + (' ' + args.action if args.action else '')
    try:
        workspace = Path(args.workspace or '.').resolve(strict=True)
        if not workspace.is_dir(): raise SafetyError('Workspace must be a directory')
        request = {}
        if args.request:
            path = Path(args.request)
            if path.is_absolute():
                try: relative = path.relative_to(workspace).as_posix()
                except ValueError: raise SafetyError('Request must be within the workspace')
            else: relative = path.as_posix()
            try:
                request = read_json(checked_path(workspace, relative, allow_missing=False))
            except SafetyError as exc:
                raise ValueError(f'Invalid request: {exc}') from exc
            if not isinstance(request, dict): raise ValueError('Request must be a JSON object')
        if args.apply and args.group in ('activity', 'activities', 'packages', 'agents'):
            from .startup import require_mutation_context
            require_mutation_context(workspace)
        module = importlib.import_module('.' + GROUPS[args.group], __package__)
        suboperation = args.group + '/' + args.action if GROUPS[args.group] == 'environment' else args.action
        result = module.handle(suboperation, workspace, request, args.apply)
        result.setdefault('result', {}); result.setdefault('changed_files', []); result.setdefault('issues', [])
        result['operation'] = operation
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0 if result.get('ok') else 2 if result.get('status') in ('invalid', 'input_error') else 1
    except SafetyError as exc:
        changed = exc.changed_files
        result = {'ok':False,'status':'partial' if changed else 'blocked','operation':operation,'result':{},'changed_files':changed, 'issues':[{'code':'runtime','message':str(exc)}]}; code = 1
    except ValueError as exc:
        result = {'ok':False,'status':'invalid','operation':operation,'result':{},'changed_files':[], 'issues':[{'code':'invocation','message':str(exc)}]}; code = 2
    except Exception as exc:
        result = {'ok':False,'status':'blocked','operation':operation,'result':{},'changed_files':[], 'issues':[{'code':'runtime','message':str(exc)}]}; code = 1
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return code
