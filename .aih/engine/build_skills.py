#!/usr/bin/env python3
"""Explicit release-time skill bundling/catalog creation; read-only discovery API."""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
from skill_helpers import ContractError, Workspace, check_bundle, json_bytes, schema_validate

VERSION = '1.0.0'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def metadata(package):
    path = Path(package) / 'SKILL.md'
    Workspace._reject_links(path.absolute())
    # Stop reading at the closing frontmatter boundary. Instruction bodies do not
    # enter discovery results and package code is never imported.
    with path.open(encoding='utf-8') as stream:
        if stream.readline().strip() != '---':
            raise ContractError('SKILL.md must start with YAML frontmatter')
        lines = []
        for line in stream:
            if line.strip() == '---':
                break
            lines.append(line)
            if sum(map(len, lines)) > 65536:
                raise ContractError('Skill metadata exceeds 64 KiB')
        else:
            raise ContractError('Unterminated skill frontmatter')
    raw = ''.join(lines)
    try:
        front = json.loads(raw)
    except json.JSONDecodeError:
        # Portable installed metadata supports a deliberately non-executable YAML
        # scalar subset as well as the preferred JSON-compatible YAML format.
        front, nested = {}, None
        for line in lines:
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            m = re.fullmatch(r'(  )?([a-zA-Z0-9_-]+):\s*(.*?)\s*\n?', line)
            if not m:
                raise ContractError('Use JSON-compatible YAML metadata or simple quoted scalar fields')
            indent, key, val = m.groups()
            if not indent and not val:
                front[key], nested = {}, key
                continue
            if val.startswith('"'):
                val = json.loads(val)
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1].replace("''", "'")
            if indent:
                if nested is None:
                    raise ContractError('Unexpected metadata indentation')
                front[nested][key] = val
            else:
                front[key], nested = val, None
    name = front.get('name', '')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name)>64 or name != Path(package).name:
        raise ContractError('Skill name must match its directory and Agent Skills naming rules')
    if not isinstance(front.get('description'), str) or not 1<=len(front['description'])<=1024:
        raise ContractError('Skill description must have 1..1024 characters')
    if not isinstance(front.get('metadata'), dict) or any(not isinstance(v, str) for v in front['metadata'].values()):
        raise ContractError('Agent Skills metadata must map strings to strings')
    extension = json.loads(front['metadata']['aih'])
    if extension.get('id') != name:
        raise ContractError('Metadata identity mismatch')
    return extension, sha(raw.encode())

def discover(core, config=None):
    core = Path(core)
    installed = json.loads((core/'skills/catalog.yaml').read_text()) if (core/'skills/catalog.yaml').exists() else {'skills': []}
    indexed = {x['id']: x for x in installed['skills']}
    entries, diagnostics, identities = [], [], set()
    schema = json.loads((core/'conventions/schemas.json').read_text())['skill_metadata']
    for package in sorted((core/'skills').iterdir()):
        if not package.is_dir() or not (package/'SKILL.md').exists():
            continue
        try:
            item, fingerprint = metadata(package)
            schema_validate(item, schema)
            if item['id'] in identities:
                raise ContractError('Ambiguous duplicate skill identity')
            identities.add(item['id'])
            check_bundle(package)
            resource_sha = sha((package/'resources/manifest.json').read_bytes())
            saved = indexed.get(item['id'])
            integrity = bool(saved and saved['metadata_sha256']==fingerprint and saved['resources_sha256']==resource_sha)
            issue = None if integrity else 'missing-or-stale-catalog: explicit no-open-request maintenance required before execution'
            cfg = (config or {}).get('skills', {}).get(item['id'], item['default_enabled'])
            enabled = cfg.get('enabled', item['default_enabled']) if isinstance(cfg, dict) else bool(cfg)
            missing = [dep for dep in item['dependencies'] if dep=='git' and shutil.which('git') is None]
            compatible = item['bundle_version']==VERSION and sys.version_info >= (3,11)
            item.update(package='skills/'+package.name, metadata_sha256=fingerprint, resources_sha256=resource_sha, installed=True, enabled=enabled, available=compatible and not missing and integrity, compatible=compatible, authorized=False, diagnostics=([issue] if issue else [])+(['Incompatible bundle/Python version; install a reviewed compatible package.'] if not compatible else [])+[f'Missing dependency: {x}' for x in missing])
            entries.append(item)
        except (ValueError, KeyError, OSError, ContractError) as exc:
            diagnostics.append({'package': package.name, 'error': str(exc)})
    for identity in indexed.keys()-identities:
        diagnostics.append({'package':identity,'error':'Catalog package is missing or invalid'})
    return {'schema_version':'1.0','skills':entries,'diagnostics':diagnostics}

def build(core):
    from installation import core_maintenance
    with core_maintenance(core) as selected:
        return _build(selected)

def _build(core):
    core=Path(core)
    entries=[]
    schema=json.loads((core/'conventions/schemas.json').read_text())['skill_metadata']
    for package in sorted((core/'skills').iterdir()):
        if not package.is_dir() or not (package/'SKILL.md').exists():
            continue
        item,fingerprint=metadata(package)
        schema_validate(item,schema)
        (package/'scripts').mkdir(exist_ok=True)
        (package/'resources').mkdir(exist_ok=True)
        (package/'references').mkdir(exist_ok=True)
        sources = {'scripts/helper.py':core/'engine/skill_helpers.py','scripts/exchange.py':core/'engine/exchange.py','scripts/contracts.py':core/'engine/contracts.py','scripts/portable_process.py':core/'engine/portable_process.py','scripts/portable_edits.py':core/'engine/portable_edits.py','scripts/product_edits.py':core/'engine/product_edits.py','scripts/execution.py':core/'engine/execution.py','scripts/security.py':core/'engine/security.py','scripts/storage.py':core/'engine/storage.py','resources/schemas.json':core/'conventions/schemas.json','resources/coverage.json':core/'conventions/coverage.json','resources/runtime.schema.json':core/'conventions/runtime.schema.json','references/workspace.md':core/'conventions/workspace.md','references/records.md':core/'conventions/records.md','references/execution.md':core/'conventions/execution.md','references/questionnaires.md':core/'conventions/questionnaires.md','references/documentation.md':core/'conventions/documentation.md','references/semantic-results.md':core/'conventions/semantic-results.md'}
        manifest={}
        for target,source in sources.items():
            content=source.read_bytes()
            (package/target).write_bytes(content)
            manifest[target]=sha(content)
        for target in ['references/standalone.md'] + sorted(p.relative_to(package).as_posix() for p in (package/'resources').glob('example-*.json')) + (['references/planning.md'] if (package/'references/planning.md').exists() else []):
            manifest[target]=sha((package/target).read_bytes())
        info={'schema_version':'1.0','bundle_version':VERSION,'helper_version':VERSION,'conventions_version':'1.0','files':manifest}
        (package/'resources/manifest.json').write_bytes(json_bytes(info))
        item.update(package='skills/'+package.name,metadata_sha256=fingerprint,resources_sha256=sha((package/'resources/manifest.json').read_bytes()))
        entries.append(item)
    catalog={'schema_version':'1.0','bundle_version':VERSION,'skills':entries}
    (core/'skills/catalog.yaml').write_bytes(json_bytes(catalog))
    lines=['# Installed AIH skills','', 'Generated from package metadata; core version '+VERSION+'. Ordinary discovery is read-only. Installed, enabled, available and authorized are separate states. Seven core skills default enabled; Git is optional and disabled. Enabling a skill grants no product, Git, publication or deployment authority.','', '| Skill | When to use | Outputs / boundaries | Default |','|---|---|---|---|']
    for e in entries:
        lines.append(f"| [{e['display_name']}]({e['id']}/SKILL.md) | {e['purpose']} | {e['output_summary']} {'; '.join(e['excludes'])}. | {'Enabled' if e['default_enabled'] else 'Disabled'} |")
    lines+=['','Copy any package folder to a permitted ordinary workspace folder and read its [standalone contract](clarify-requirements/references/standalone.md). Each package includes its own contracts, helpers and examples; no AIH installation or fixed product-state path is required. Run `python -B <package>/scripts/helper.py integrity` before use. Metadata/resource changes are diagnosed; reconcile catalogs only through explicit maintenance with no open request or execution owner.','', 'The official format reference is https://agentskills.io/specification. Package/helper portability tests do not establish observed compliance by a semantic agent.']
    (core/'skills/README.md').write_text('\n'.join(lines)+'\n')
    return catalog

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--core',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--build',action='store_true',help='Explicit release/catalog maintenance; refuses any open request or execution owner')
    a=p.parse_args()
    print(json.dumps(build(a.core) if a.build else discover(a.core),indent=2))
if __name__=='__main__':main()
