"""Run with python -B test_agent_tools.py; all parsing uses the standard library."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from agent_tools import (HEADINGS, Invalid, audit, contained, decode_cell, load_json,
                         read_definition, read_profiles, resolve, unique_pairs, validate, parse_frontmatter, UnsupportedYAML)



class AgentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hai-agent-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.definition = ".hai/agents/worker/SKILL.md"
        self.description = "Call to inspect café & pipes | paths \\ and report."
        self.write_definition()
        encoded = self.description.replace("&", "&amp;").replace("\\", "&#92;").replace("|", "&#124;")
        self.catalogue = ("# Agents\n\n| Agent | Selection guide | Definition |\n| --- | --- | --- |\n"
                          f"| `worker` | {encoded} | [SKILL.md](worker/SKILL.md) |\n")
        self.write(".hai/agents/catalogue.md", self.catalogue)
        self.profiles = {"format_version": 1, "models": {"light": "small", "standard": "normal", "advanced": "large"}}
        self.write(".hai_env/model_profiles.json", json.dumps(self.profiles))
        self.runtime = {"models": {"small": ["low", "high"], "normal": ["high"], "large": ["high", "ultra"]}}

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8"))
        return target

    def write_definition(self, name="worker", metadata=None, extra=""):
        metadata = metadata or 'metadata:\n  hai-model-class: "light"\n  hai-reasoning-effort: "high"\n'
        text = (f'---\nname: {name}\ndescription: {json.dumps(self.description)}\n'
                + metadata + extra + '---\n\n' + ''.join(f"## {h}\n\nNone.\n\n" for h in HEADINGS))
        return self.write(self.definition, text)

    def test_audit_exact_decoding_unicode_and_crlf(self):
        for path in self.root.rglob("*.md"):
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        result = audit(self.root)
        self.assertTrue(result["ok"], result)
        self.assertEqual(len(result["agents"]), 1)

    def test_exact_supported_pair(self):
        result = resolve(self.root, self.definition, self.runtime)
        self.assertTrue(result["ok"])
        self.assertEqual(result["request"]["model"], "small")
        self.assertEqual(result["request"]["reasoning_effort"], "high")

    def test_validate_registered_and_unregistered_without_other_context(self):
        self.assertTrue(validate(self.root, self.definition)["ok"])
        (self.root / ".hai/agents/catalogue.md").unlink()
        self.write(".hai_env/state.json", "not JSON")
        self.write(".hai_env/model_profiles.json", "not JSON")
        self.write(".hai_env/agents/catalogue.md", "not a catalogue")
        result = validate(self.root, self.definition)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["agent"], "worker")
        self.assertFalse((self.root / ".hai/agents/catalogue.md").exists())

    def test_validate_either_origin_without_initialized_environment(self):
        content = (self.root / self.definition).read_bytes()
        for origin in (".hai", ".hai_env"):
            with self.subTest(origin=origin), tempfile.TemporaryDirectory(prefix="hai-definition-") as temporary:
                isolated = Path(temporary).resolve()
                relative = f"{origin}/agents/worker/SKILL.md"
                target = isolated / relative
                target.parent.mkdir(parents=True)
                target.write_bytes(content)
                self.assertTrue(validate(isolated, relative)["ok"])
                self.assertFalse((isolated / ".hai_env/state.json").exists())
                self.assertFalse((isolated / origin / "agents/catalogue.md").exists())
                if origin == ".hai":
                    self.assertFalse((isolated / ".hai_env").exists())

    def test_validate_format_findings(self):
        path = self.root / self.definition
        original = path.read_text(encoding="utf-8")
        invalid_contents = (
            original.replace('name: worker', 'name: other'),
            original.replace('metadata:', 'name: worker\nmetadata:'),
            original.replace('hai-model-class: "light"', 'hai-model-class: true'),
            original.replace('## Scope', '## Purpose'),
        )
        for content in invalid_contents:
            with self.subTest(content=content):
                path.write_text(content, encoding="utf-8")
                result = validate(self.root, self.definition)
                self.assertFalse(result["ok"])
                self.assertEqual(result["issues"][0]["code"], "definition")

    def test_validate_leader_without_profiles_or_execution_metadata(self):
        self.definition = ".hai/agents/leader/SKILL.md"
        self.write_definition(name="leader", metadata="\n")
        (self.root / ".hai_env/model_profiles.json").unlink()
        self.assertTrue(validate(self.root, self.definition)["ok"])
        self.write_definition(name="leader")
        self.assertFalse(validate(self.root, self.definition)["ok"])

    def test_validate_rejects_legacy_conflict(self):
        self.write(".hai/agents/worker/knowledge.md", "preserve legacy")
        result = validate(self.root, self.definition)
        self.assertFalse(result["ok"])
        self.assertIn("legacy", result["issues"][0]["message"])

    def test_validate_rejects_alias_to_differently_named_definition(self):
        original = self.root / self.definition
        other = self.write(".hai/agents/other/SKILL.md",
                           original.read_text(encoding="utf-8").replace('name: worker', 'name: other'))
        original.unlink()
        try:
            original.symlink_to(other)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        result = validate(self.root, self.definition)
        self.assertFalse(result["ok"])
        self.assertIn("identity", result["issues"][0]["message"])

    def test_validate_rejects_unsafe_or_noncanonical_paths(self):
        for relative in ("../outside/SKILL.md", "/tmp/SKILL.md", "C:/SKILL.md",
                         "other/SKILL.md", ".hai/agents/worker/../worker/SKILL.md",
                         ".hai\\agents\\worker\\SKILL.md", ".hai/agents/worker/SKILL.md#part",
                         ".hai/agents/worker/SKILL.md?query", ".hai/agents/worker"):
            with self.subTest(relative=relative), self.assertRaises(Invalid):
                validate(self.root, relative)

    def run_cli(self, *arguments, workspace=None, isolated=False):
        # Disable site-packages to prove the real parser needs no third-party library.
        flags = ["-I", "-S"] if isolated else []
        return subprocess.run(
            [sys.executable, *flags, "-B", str(Path(__file__).with_name("agent_tools.py")),
             "--workspace", str(workspace or self.root), *arguments],
            capture_output=True, text=True, encoding="utf-8", check=False)

    def test_unique_pairs_rejects_duplicate_or_nonstring_keys(self):
        self.assertEqual(unique_pairs([("first", 1), ("second", 2)]), {"first": 1, "second": 2})
        for pairs in ([('a', 1), ('a', 2)], [(1, 'value')]):
            with self.subTest(pairs=pairs), self.assertRaises(Invalid):
                unique_pairs(pairs)

    def test_catalogue_entities_decode_once_without_unrelated_html(self):
        self.assertEqual(decode_cell('café &amp; &#92; &#124;'), 'café & \\ |')
        self.assertEqual(decode_cell('&amp;#124; &amp;amp; &lt; &#x7c;'),
                         '&#124; &amp; &lt; &#x7c;')

    def test_json_bom_unicode_and_nested_duplicates(self):
        path = self.root / 'sample.json'
        path.write_bytes(b'\xef\xbb\xbf' + '{"name":"café"}'.encode('utf-8'))
        self.assertEqual(load_json(path), {'name': 'café'})
        path.write_text('{"nested":{"a":1,"a":2}}', encoding='utf-8')
        with self.assertRaises(Invalid):
            load_json(path)
        path.write_text('{broken}', encoding='utf-8')
        with self.assertRaises(Invalid):
            load_json(path)

    def test_profiles_preserve_extra_values_and_reject_missing_mappings(self):
        path = self.root / '.hai_env/model_profiles.json'
        self.profiles['notes'] = {'source': 'human'}
        path.write_text(json.dumps(self.profiles), encoding='utf-8')
        before = path.read_bytes()
        self.assertEqual(read_profiles(path), self.profiles)
        self.assertEqual(path.read_bytes(), before)
        for models in ({'light': 'small'}, {'light': 'small', 'standard': ' ', 'advanced': 'large'}):
            with self.subTest(models=models):
                path.write_text(json.dumps({'format_version': 1, 'models': models}), encoding='utf-8')
                with self.assertRaises(Invalid):
                    read_profiles(path)

    def test_contained_paths_allow_absent_descendants_but_reject_root_and_foreign_syntax(self):
        self.assertEqual(contained(self.root, 'future/child'), self.root / 'future/child')
        for relative in ('', '.', '..', '../escape', 'C:/escape', '//server/share',
                         '/absolute', 'folder\\child', 'folder?query', 'folder#part'):
            with self.subTest(relative=relative), self.assertRaises(Invalid):
                contained(self.root, relative)

    def empty_catalogue(self):
        return '\n'.join(self.catalogue.splitlines()[:4]) + '\n'

    def test_empty_catalogue_and_profile_audit_need_no_yaml(self):
        self.write('.hai/agents/catalogue.md', self.empty_catalogue())
        result = self.run_cli('audit', isolated=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output, {'ok': True, 'agents': [], 'profiles': 'valid', 'issues': []})
        (self.root / '.hai_env/model_profiles.json').unlink()
        output = audit(self.root)
        self.assertTrue(output['ok'])
        self.assertEqual(output['profiles'], 'absent')
        self.assertFalse((self.root / '.hai_env/agents/catalogue.md').exists())

    def test_malformed_catalogues_report_structural_errors_isolated(self):
        invalid = ('not a table', self.empty_catalogue().replace('Selection guide', 'Wrong'),
                   self.empty_catalogue() + '\n' + self.empty_catalogue())
        for content in invalid:
            with self.subTest(content=content):
                self.write('.hai/agents/catalogue.md', content)
                result = self.run_cli('audit', isolated=True)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(json.loads(result.stdout)['issues'][0]['code'], 'catalogue')

    def test_duplicate_catalogue_rows_rejected_before_definition_parsing(self):
        self.write('.hai/agents/catalogue.md', self.catalogue + self.catalogue.splitlines()[-1] + '\n')
        result = self.run_cli('audit', isolated=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output['agents'], [])
        self.assertEqual(len(output['issues']), 2)
        self.assertTrue(all(issue['code'] == 'agent' and 'duplicate' in issue['message']
                            for issue in output['issues']))

    def test_cli_help_available_isolated(self):
        result = self.run_cli('--help', isolated=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('validate', result.stdout)
        self.assertIn('resolve', result.stdout)

    def test_isolated_validate_and_resolve_parse_real_yaml_without_writes(self):
        runtime = self.write('runtime.json', json.dumps(self.runtime))
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        for args in (('validate', '--definition', self.definition),
                     ('resolve', '--definition', self.definition, '--runtime', str(runtime))):
            with self.subTest(args=args):
                result = self.run_cli(*args, isolated=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                output = json.loads(result.stdout)
                self.assertTrue(output['ok'])
                self.assertEqual(output['issues'], [])
        after = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_isolated_audit_parses_real_yaml_without_writes(self):
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = self.run_cli('audit', isolated=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertTrue(output['ok'])
        self.assertEqual(output['agents'], [{'name': 'worker', 'definition': self.definition}])
        self.assertEqual(output['issues'], [])
        self.assertEqual(output['profiles'], 'valid')
        after = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_isolated_file_and_frontmatter_errors(self):
        path = self.root / self.definition
        for content in ('', '# Missing frontmatter', '---\nname: worker\n'):
            with self.subTest(content=content):
                path.write_text(content, encoding='utf-8')
                result = self.run_cli('validate', '--definition', self.definition, isolated=True)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(json.loads(result.stdout)['issues'][0]['code'], 'definition')
        path.unlink()
        result = self.run_cli('validate', '--definition', self.definition, isolated=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)['issues'][0]['code'], 'input')
        result = self.run_cli('validate', '--definition', '../escape/SKILL.md', isolated=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)['issues'][0]['code'], 'input')

    def test_validate_cli_success_and_format_exit_codes(self):
        result = self.run_cli("validate", "--definition", self.definition)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["ok"])
        path = self.root / self.definition
        path.write_text(path.read_text(encoding="utf-8").replace('## Scope', '## Purpose'), encoding="utf-8")
        result = self.run_cli("validate", "--definition", self.definition)
        self.assertEqual(result.returncode, 1, result.stderr)
        output = json.loads(result.stdout)
        self.assertFalse(output["ok"])
        self.assertEqual(output["issues"][0]["code"], "definition")

    def test_validate_cli_input_exit_codes(self):
        for relative in (".hai/agents/missing/SKILL.md", "../outside/SKILL.md", "other/SKILL.md"):
            with self.subTest(relative=relative):
                result = self.run_cli("validate", "--definition", relative)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(json.loads(result.stdout)["issues"][0]["code"], "input")
        path = self.root / self.definition
        path.write_bytes(b"\xff\xfeinvalid UTF-8")
        result = self.run_cli("validate", "--definition", self.definition)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)["issues"][0]["code"], "input")
        path.unlink()
        path.mkdir()
        result = self.run_cli("validate", "--definition", self.definition)
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_validate_cli_requires_definition_argument(self):
        result = self.run_cli("validate")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--definition", result.stderr)

    def test_validate_cli_unicode_workspace_without_environment(self):
        isolated = self.root / "café workspace"
        target = isolated / self.definition
        target.parent.mkdir(parents=True)
        target.write_bytes((self.root / self.definition).read_bytes())
        result = self.run_cli("validate", "--definition", self.definition, workspace=isolated)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["agent"], "worker")
        self.assertFalse((isolated / ".hai_env").exists())

    def test_existing_audit_and_resolve_cli_dispatch(self):
        result = self.run_cli("audit")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["agents"]), 1)
        runtime = self.write("runtime.json", json.dumps(self.runtime))
        result = self.run_cli("resolve", "--definition", self.definition, "--runtime", str(runtime))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["request"]["model"], "small")

    def test_validate_success_and_failure_do_not_mutate_files(self):
        self.write(".hai_env/state.json", '{"unrelated":"preserve"}\n')
        path = self.root / self.definition
        for invalid in (False, True):
            with self.subTest(invalid=invalid):
                if invalid:
                    path.write_text(path.read_text(encoding="utf-8").replace('## Scope', '## Purpose'), encoding="utf-8")
                before = {str(p.relative_to(self.root)): p.read_bytes()
                          for p in self.root.rglob("*") if p.is_file()}
                result = self.run_cli("validate", "--definition", self.definition)
                self.assertEqual(result.returncode, 1 if invalid else 0, result.stderr)
                after = {str(p.relative_to(self.root)): p.read_bytes()
                         for p in self.root.rglob("*") if p.is_file()}
                self.assertEqual(before, after)

    def test_unavailable_effort_never_substitutes(self):
        self.runtime["models"]["small"] = ["low"]
        result = resolve(self.root, self.definition, self.runtime)
        self.assertFalse(result["ok"])
        self.assertEqual(result["request"]["reasoning_effort"], "high")
        self.assertEqual(result["request"]["model"], "small")

    def test_unavailable_model_never_substitutes(self):
        del self.runtime["models"]["small"]
        self.assertFalse(resolve(self.root, self.definition, self.runtime)["ok"])

    def test_missing_profiles_valid_audit_but_no_normal_resolution(self):
        (self.root / ".hai_env/model_profiles.json").unlink()
        self.assertTrue(audit(self.root)["ok"])
        self.assertFalse(resolve(self.root, self.definition, self.runtime)["ok"])
        self.assertFalse((self.root / ".hai_env/model_profiles.json").exists())

    def test_duplicate_json_and_boolean_version_rejected(self):
        path = self.write(".hai_env/model_profiles.json", '{"format_version":1,"format_version":1}')
        with self.assertRaises(Invalid):
            read_profiles(path)
        self.profiles["format_version"] = True
        path.write_text(json.dumps(self.profiles))
        with self.assertRaises(Invalid):
            read_profiles(path)

    def test_duplicate_yaml_and_nonstring_metadata_rejected(self):
        for extra in ('name: worker\n', 'metadata:\n  hai-model-class: true\n  hai-reasoning-effort: high\n'):
            with self.subTest(extra=extra):
                path = self.write_definition(extra=extra)
                with self.assertRaises(Invalid):
                    read_definition(path)
        self.write_definition(metadata='metadata:\n  hai-model-class: true\n  hai-reasoning-effort: high\n')
        self.assertFalse(audit(self.root)["ok"])

    def test_folded_yaml_description_is_canonical_decoded_value(self):
        path = self.write_definition()
        path.write_text(path.read_text().replace('description: ' + json.dumps(self.description),
                                                'description: >-\n  Call to inspect\n  and report.'))
        self.assertEqual(read_definition(path)["description"], "Call to inspect and report.")

    def test_quoted_strings_comments_unicode_and_plain_punctuation(self):
        parsed = parse_frontmatter('''single: 'It''s # literal: text' # comment
double: "caf\\u00e9 \\x41 \\U0001f600 \\t \\\" \\\\"
plain: https://example.test/a#part # removed
"quoted key" : 'value'
''')
        self.assertEqual(parsed, {'single': "It's # literal: text", 'double': 'caf\u00e9 A \U0001f600 \t " \\',
                                  'plain': 'https://example.test/a#part', 'quoted key': 'value'})

    def test_duplicate_keys_detected_after_decoding_at_each_depth(self):
        for source in ('name: worker\n"name": other\n',
                       'metadata:\n  key: one\n  "k\\u0065y": two\n',
                       "metadata:\n  'it''s': one\n  \"it's\": two\n"):
            with self.subTest(source=source), self.assertRaisesRegex(Invalid, 'duplicate.*'):
                parse_frontmatter(source)

    def test_metadata_implicit_types_never_become_valid_strings(self):
        for value in ('true', 'False', 'yes', 'OFF', 'null', '~', '42', '-2', ''):
            with self.subTest(value=value):
                self.write_definition(metadata='metadata:\n  hai-model-class: light\n'
                                      '  hai-reasoning-effort: high\n  extra: ' + value + '\n')
                result = validate(self.root, self.definition)
                self.assertFalse(result['ok'])
                self.assertIn('strings', result['issues'][0]['message'])
        for value in ('1.5', '01', '0xFF', '1e3', '.inf', '2026-10-23', '12:30:00'):
            with self.subTest(value=value), self.assertRaises(UnsupportedYAML):
                parse_frontmatter('extra: ' + value + '\n')

    def test_arbitrary_string_metadata_and_optional_strings_are_preserved(self):
        path = self.write_definition(metadata='metadata:\n  hai-model-class: light\n'
                                     '  hai-reasoning-effort: high\n  custom: "false"\n',
                                     extra="license: 'MIT'\ncompatibility: Works here\nallowed-tools: Read Write\n")
        result = read_definition(path)
        self.assertEqual(result['metadata']['custom'], 'false')
        self.assertEqual(result['allowed-tools'], 'Read Write')

    def test_block_folding_literal_chomping_and_terminal_break(self):
        cases = {
            'key: >-\n  one\n  two\n': 'one two',
            'key: >-\n  one\n\n  two\n': 'one\ntwo',
            'key: >-\n\n  one\n': '\none',
            'key: >-\n  one\n    code\n  two\n': 'one\n  code\ntwo',
            'key: |-\n  one\n  two\n\n': 'one\ntwo',
            'key: |\n  one\n\n': 'one\n',
            'key: |+\n  one\n\n': 'one\n\n',
            'key: |\n  one': 'one',
            'key: >+\n  one\n\n': 'one\n\n',
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(parse_frontmatter(source)['key'], expected)

    def test_terminal_frontmatter_break_is_preserved_for_blocks(self):
        path = self.write_definition(extra='license: |\n  MIT\n')
        self.assertEqual(read_definition(path)['license'], 'MIT\n')

    def test_unsupported_yaml_is_reported_without_validating_definition(self):
        values = ('&anchor value', '*alias', '!!str value', '[one, two]', '{key: value}',
                  '{"key": "value"}', '>2-\n  indented', '"multiline\n  string"')
        for value in values:
            with self.subTest(value=value), self.assertRaisesRegex(UnsupportedYAML, 'line'):
                parse_frontmatter('key: ' + value + '\n')
        for source in ('<<: *base\n', '? complex\n: value\n', '- sequence\n',
                       'key:\n  - one\n', 'key: >-\n  one\n    code\n\n  two\n'):
            with self.subTest(source=source), self.assertRaises(UnsupportedYAML):
                parse_frontmatter(source)

    def test_unsupported_cli_results_and_audit_exclusion(self):
        self.write_definition(extra='license: &named MIT\n')
        runtime = self.write('runtime.json', json.dumps(self.runtime))
        cases = ((('validate', '--definition', self.definition), 1),
                 (('audit',), 1),
                 (('resolve', '--definition', self.definition, '--runtime', str(runtime)), 2))
        for args, expected_exit in cases:
            with self.subTest(args=args):
                result = self.run_cli(*args, isolated=True)
                self.assertEqual(result.returncode, expected_exit, result.stderr)
                output = json.loads(result.stdout)
                self.assertFalse(output['ok'])
                self.assertEqual(output['issues'][0]['code'], 'unsupported')
                self.assertEqual(output.get('agents', []), [])

    def test_malformed_supported_syntax_never_partially_parses(self):
        for source in ('key: "value" trailing\n', 'key: "bad\\q"\n',
                       'key: "bad\\u00G0"\n', 'key: text: value\n',
                       'key: |\n    one\n   two\n', 'key: "bad\\U00110000"\n'):
            with self.subTest(source=source), self.assertRaisesRegex(Invalid, 'line'):
                parse_frontmatter(source)

    def test_unsupported_indentation_continuations_and_unicode_linebreaks(self):
        for source in ('key: value\n  continuation\n', 'key:\n\tchild: value\n',
                       '  key: value\n', 'key: before\u2028after\n'):
            with self.subTest(source=source), self.assertRaises(UnsupportedYAML):
                parse_frontmatter(source)

    def test_comment_cannot_supply_mapping_delimiter(self):
        with self.assertRaisesRegex(Invalid, 'comment'):
            parse_frontmatter('description # ignored: Looks valid\n')

    def test_unicode_spaces_are_scalar_content_not_yaml_separation(self):
        self.assertEqual(parse_frontmatter('description: a\u00a0b\u00a0\n')['description'], 'a\u00a0b\u00a0')
        self.assertEqual(parse_frontmatter('description: a\u00a0#literal\n')['description'], 'a\u00a0#literal')
        with self.assertRaises(UnsupportedYAML):
            parse_frontmatter('name:\u00a0demo\n')

    def test_raw_nonprintable_characters_rejected(self):
        for character in ('\x81', '\ufffe', '\x00', '\x7f'):
            with self.subTest(character=character), self.assertRaises(Invalid):
                parse_frontmatter('key: "before' + character + 'after"\n')

    def test_empty_block_keep_chomping_preserves_actual_breaks(self):
        for marker in ('|+', '>+'):
            for tail in ('next: value\n', ''):
                with self.subTest(marker=marker, tail=tail):
                    self.assertEqual(parse_frontmatter('custom: ' + marker + '\n\n\n' + tail)['custom'], '\n\n')
        self.assertEqual(parse_frontmatter('custom: |+\n\n')['custom'], '\n')
        self.assertEqual(parse_frontmatter('custom: |\n\n')['custom'], '')

    def test_wrong_name_sections_and_h1_rejected(self):
        path = self.write_definition()
        original = path.read_text()
        for text in (original.replace('name: worker', 'name: other'),
                     original.replace('## Scope', '## Purpose'), original + '# Worker\n'):
            path.write_text(text)
            with self.assertRaises(Invalid):
                read_definition(path)

    def test_leader_must_omit_execution_metadata(self):
        self.definition = ".hai/agents/leader/SKILL.md"
        path = self.write_definition(name="leader")
        with self.assertRaises(Invalid):
            read_definition(path)
        self.write_definition(name="leader", metadata="\n")
        self.assertEqual(read_definition(path)["name"], "leader")
        with self.assertRaises(Invalid):
            resolve(self.root, self.definition, self.runtime)

    def test_stale_copy_rejected(self):
        self.write(".hai/agents/catalogue.md", self.catalogue.replace('Call to inspect', 'Call to write'))
        self.assertFalse(audit(self.root)["ok"])

    def test_duplicate_rows_and_workspace_collisions(self):
        self.write(".hai_env/agents/catalogue.md", self.catalogue)
        result = audit(self.root)
        self.assertFalse(result["ok"])
        self.assertEqual(len(result["agents"]), 1)
        self.write(".hai/agents/catalogue.md", self.catalogue + self.catalogue.splitlines()[-1] + '\n')
        self.assertFalse(audit(self.root)["agents"])

    def test_legacy_registration_preserved_and_independent_entry_kept(self):
        text = self.catalogue + '| `old` | Call to help. | [knowledge.md](old/knowledge.md) |\n'
        path = self.write(".hai/agents/catalogue.md", text)
        result = audit(self.root)
        self.assertFalse(result["ok"])
        self.assertEqual(len(result["agents"]), 1)
        self.assertEqual(result["issues"][0]["agent"], "old")
        self.assertEqual(path.read_text(), text)

    def test_old_new_conflict_rejected(self):
        self.write(".hai/agents/worker/knowledge.md", "# Old worker\n")
        self.assertFalse(audit(self.root)["ok"])
        with self.assertRaises(Invalid):
            resolve(self.root, self.definition, self.runtime)

    def test_escaping_symlink_rejected(self):
        with tempfile.TemporaryDirectory(prefix="hai-external-") as external:
            path = self.root / self.definition
            path.unlink()
            outside = Path(external) / "SKILL.md"
            outside.write_text("do not read")
            try:
                path.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks unavailable")
            self.assertFalse(audit(self.root)["ok"])
            with self.assertRaises(Invalid):
                resolve(self.root, self.definition, self.runtime)
            with self.assertRaises(Invalid):
                validate(self.root, self.definition)

    def test_dangling_profile_is_invalid_not_absent(self):
        self.write(".hai/agents/catalogue.md", '\n'.join(self.catalogue.splitlines()[:4]) + '\n')
        path = self.root / ".hai_env/model_profiles.json"
        path.unlink()
        try:
            path.symlink_to(self.root / "missing-profile.json")
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        result = audit(self.root)
        self.assertFalse(result["ok"])
        self.assertEqual(result["profiles"], "invalid")

    def test_traversal_and_noncanonical_selected_path_rejected(self):
        for path in ("../outside/SKILL.md", "/tmp/SKILL.md", "C:/SKILL.md", "other/SKILL.md"):
            with self.subTest(path=path), self.assertRaises(Invalid):
                resolve(self.root, path, self.runtime)

    def test_no_mutations_to_state_or_catalogue(self):
        state = self.write(".hai_env/state.json", '{"unrelated":"preserve"}\n')
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        audit(self.root)
        resolve(self.root, self.definition, self.runtime)
        after = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(state.read_text(), '{"unrelated":"preserve"}\n')


if __name__ == "__main__":
    unittest.main()
