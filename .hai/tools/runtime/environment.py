"""Explicit environment, profile and installed-agent configuration operations."""
import copy
import sys
from pathlib import Path
from environment_paths import STATE, PROFILES, INSTRUCTIONS, legacy_entries
from .storage import SafetyError, checked_path, read_json, fingerprint, write_bytes, write_json, lock
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'startup'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'agents'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'configuration'))
import startup_check as startup
import agent_tools
import configuration_tools as config

def provenance(request):
    value = request.get('provenance')
    if not isinstance(value, dict) or set(value) != {'source', 'reason'} or any(not isinstance(v, str) or not v.strip() for v in value.values()):
        raise ValueError('Mutation requires provenance with nonblank source and reason')

def outcome(result, changes, apply, issues=None):
    return {'ok': True, 'status': 'applied' if apply and changes else 'planned' if changes else 'unchanged',
            'result': result, 'changed_files': changes if apply else [], 'issues': issues or []}

def _parents(root, relative, changed):
    current = Path(root)
    for part in relative.split('/')[:-1]:
        current /= part
        rel = current.relative_to(root).as_posix()
        checked_path(root, rel)
        if not current.exists():
            current.mkdir()
            changed.append(rel + '/')

def handle(operation, workspace, request, apply):
    workspace = Path(workspace)
    group, _, action = operation.partition('/')
    changed = []
    if group == 'environment' and action == 'migrate-layout':
        provenance(request)
        if set(request) != {'provenance'}:
            raise ValueError('Layout migration accepts provenance only')
        from .layout_migration import migrate
        return migrate(workspace, request, apply)
    if apply and not (group == 'environment' and action in ('initialize', 'init')):
        context = startup.check(workspace)
        if (context['environment'] != 'valid' or context['instructions_status'] != 'loaded'
                or (context.get('state_format_version') != 3 and action != 'migrate-specification')):
            raise SafetyError('Valid core state and readable mandatory instructions are required for mutation; migrate older state first')
    if group == 'environment' and action in ('initialize', 'init'):
        provenance(request)
        if legacy_entries(workspace) or checked_path(workspace, '.hai_env/config/layout-migration.json').exists():
            raise SafetyError('Legacy layout exists; explicitly run environment migrate-layout instead of initialization')
        if set(request) != {'provenance'}: raise ValueError('Initialization accepts provenance only')
        statepath = checked_path(workspace, STATE)
        instructions = checked_path(workspace, INSTRUCTIONS)
        if statepath.exists(): raise SafetyError('Core state already exists')
        if instructions.exists(): fingerprint(instructions)
        template = read_json(checked_path(workspace, '.hai/templates/state.json', allow_missing=False))
        document = {'state_format_version': startup.state_contract()['current_state_format_version'], **template}
        startup.state_context(workspace, document, template, startup.state_contract())
        plan = [STATE] + ([] if instructions.exists() else [INSTRUCTIONS])
        if apply:
            try:
                env = checked_path(workspace, '.hai_env')
                if not env.exists(): env.mkdir(); changed.append('.hai_env/')
                with lock(workspace):
                    if statepath.exists() or legacy_entries(workspace) or checked_path(workspace, '.hai_env/config/layout-migration.json').exists(): raise SafetyError('State or legacy layout appeared since preview')
                    _parents(workspace, STATE, changed)
                    write_json(workspace, STATE, document); changed.append(STATE)
                    if not instructions.exists():
                        write_bytes(workspace, INSTRUCTIONS, b''); changed.append(INSTRUCTIONS)
            except Exception as exc:
                changed.extend(getattr(exc, 'changed_files', []))
                return {'ok': False, 'status': 'partial' if changed else 'blocked', 'result': {'planned_files': plan}, 'changed_files': changed, 'issues': [{'code':'write', 'message':str(exc)}]}
        return outcome({'planned_files': plan}, changed if apply else plan, apply)
    if group == 'environment' and action == 'configure':
        provenance(request)
        if set(request) != {'provenance', 'changes'} or not isinstance(request['changes'], dict) or not request['changes']:
            raise ValueError('Provide explicit named changes')
        changes = request['changes']; allowed = {'activities.location', 'features.chronicles.enabled', 'features.chronicles.record_every_prompts'}
        if not set(changes) <= allowed: raise ValueError('Unknown environment change')
        rel = STATE; path = checked_path(workspace, rel, allow_missing=False); before = fingerprint(path); state = read_json(path)
        template = read_json(checked_path(workspace, '.hai/templates/state.json', allow_missing=False)); contract = startup.state_contract()
        startup.state_context(workspace, state, template, contract)
        candidate = copy.deepcopy(state)
        for name, value in changes.items():
            parts = name.split('.'); obj = candidate
            for part in parts[:-1]: obj = obj[part]
            obj[parts[-1]] = value
        old_chronicles = state['features']['chronicles']
        new_chronicles = candidate['features']['chronicles']
        if old_chronicles['enabled'] != new_chronicles['enabled']:
            revision = old_chronicles.get('enablement_revision', 0)
            if type(revision) is not int or revision < 0:
                raise SafetyError('Invalid chronicle enablement revision')
            new_chronicles['enablement_revision'] = revision + 1
        startup.state_context(workspace, candidate, template, contract)
        owner = startup.check(workspace)['agent_configurations']['specification-manager']
        if owner.get('status') in ('configured', 'defaulted'):
            location = owner.get('settings', {}).get('location')
            if location and startup.overlaps(startup.safe_path(workspace, location), startup.safe_path(workspace, candidate['activities']['location'])):
                raise SafetyError('Activity location overlaps installed Specification-manager location')
        plan = [] if candidate == state else [rel]
        if apply and plan:
            with lock(workspace): write_json(workspace, rel, candidate, before)
        return outcome({'changes': changes, 'planned_files': plan}, plan, apply)
    if group == 'profiles':
        rel = PROFILES; path = checked_path(workspace, rel)
        if action in ('check', 'read'):
            if request or apply: raise ValueError('Profiles check takes no request or apply')
            if not path.exists(): return outcome({'status':'absent'}, [], False)
            fingerprint(path); data = agent_tools.read_profiles(path)
            return outcome({'status':'valid', 'profiles':data, 'runtime_availability':'not_checked'}, [], False)
        if action != 'configure': raise ValueError('Unsupported profiles operation')
        provenance(request)
        if set(request) != {'provenance', 'changes'} or not isinstance(request['changes'], dict) or not request['changes'] or not set(request['changes']) <= {'light','standard','advanced'}:
            raise ValueError('Profiles changes must name light, standard, or advanced')
        before = fingerprint(path); data = read_json(path) if before else {'format_version':1, 'models':{}}
        if before: agent_tools.read_profiles(path)
        candidate = copy.deepcopy(data); candidate['models'].update(request['changes'])
        if type(candidate.get('format_version')) is not int or candidate['format_version'] != 1 or any(not isinstance(candidate['models'].get(k), str) or not candidate['models'][k].strip() for k in ('light','standard','advanced')):
            raise ValueError('Profiles require nonblank light, standard and advanced model IDs')
        plan = [] if candidate == data and before else [rel]
        if apply and plan:
            with lock(workspace): write_json(workspace, rel, candidate, before)
        return outcome({'profiles':candidate, 'planned_files':plan}, plan, apply)
    if group == 'configuration':
        agent = request.get('agent')
        if not isinstance(agent, str) or not agent_tools.NAMES.fullmatch(agent): raise ValueError('A canonical agent name is required')
        contract_rel = f'.hai_env/agents/{agent}/configuration/contract.json'
        contract_path = checked_path(workspace, contract_rel, allow_missing=False); contract_fp = fingerprint(contract_path)
        contract = config.load_contract(contract_path, agent)
        current = config.read_configuration(workspace, agent, contract)
        if action == 'read':
            if set(request) != {'agent'} or apply: raise ValueError('Configuration read accepts agent only')
            return {'ok':current['status'] in ('configured','defaulted'), 'status':current['status'], 'result':current, 'changed_files':[], 'issues':current['issues']}
        if action != 'update': raise ValueError('Unsupported configuration operation')
        provenance(request)
        if set(request) != {'agent','provenance','changes'} or not isinstance(request['changes'], dict) or not request['changes']:
            raise ValueError('Configuration update requires named changes')
        if current['status'] not in ('defaulted','configured'): raise SafetyError('Current configuration is invalid')
        rel = f'.hai_env/config/agents/{agent}.json'; target = checked_path(workspace, rel); before = fingerprint(target)
        document = read_json(target) if before else {'config_format_version': contract['current_config_format_version'], 'settings': {}}
        settings = document['settings']
        for name, value in request['changes'].items():
            if name not in contract['settings']: raise ValueError(f'Unknown setting: {name}')
            parts = name.split('.')
            node = settings
            for part in parts[:-1]:
                if part not in node: node[part] = {}
                if not isinstance(node[part], dict): raise SafetyError(f'Invalid setting container: {part}')
                node = node[part]
            node[parts[-1]] = value
        config._effective_settings(contract, settings, workspace)
        plan = [rel] if before is None or read_json(target) != document else []
        if apply and plan:
            try:
                with lock(workspace):
                    if fingerprint(contract_path) != contract_fp: raise SafetyError('Contract changed')
                    _parents(workspace, rel, changed)
                    config.configuration_path(workspace, agent)
                    write_json(workspace, rel, document, before); changed.append(rel)
            except Exception as exc:
                changed.extend(getattr(exc, 'changed_files', []))
                return {'ok':False,'status':'partial' if changed else 'blocked','result':{'planned_files':plan},'changed_files':changed,'issues':[{'code':'write','message':str(exc)}]}
        return outcome({'settings':settings,'planned_files':plan}, changed if apply else plan, apply)
    if group == 'environment' and action == 'migrate-specification':
        provenance(request)
        if set(request) != {'provenance'}: raise ValueError('Migration accepts provenance only')
        import migrate_specification_configuration as migration
        if apply:
            with lock(workspace): result = migration.migrate(workspace, True)
        else: result = migration.migrate(workspace, False)
        changed = [result[k]['path'] for k in ('backup','configuration') if result.get(k,{}).get('created')]
        if result.get('state_updated'): changed.append(STATE)
        changed += result.get('created_directories', [])
        return {'ok':result['ok'], 'status':result['status'], 'result':result, 'changed_files':changed, 'issues':result['issues']}
    raise ValueError('Unsupported operation')
