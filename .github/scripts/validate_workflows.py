import glob
import sys

import yaml


def main() -> int:
    files = sorted(glob.glob('.github/workflows/*.yml') + glob.glob('.github/workflows/*.yaml'))
    if not files:
        print('No workflow files found in .github/workflows')
        return 1

    failures = []

    for path in files:
        with open(path, 'r', encoding='utf-8') as handle:
            try:
                data = yaml.safe_load(handle)
            except Exception as exc:  # pragma: no cover
                failures.append(f'{path}: invalid YAML ({exc})')
                continue

        if not isinstance(data, dict):
            failures.append(f'{path}: top-level YAML must be a mapping')
            continue

        normalized_keys = {str(key).lower() for key in data.keys()}

        if 'name' not in normalized_keys:
            failures.append(f'{path}: missing top-level key "name"')

        if 'on' not in normalized_keys and 'true' not in normalized_keys:
            failures.append(f'{path}: missing top-level key "on"')

    if failures:
        print('Workflow smoke test failed:')
        for failure in failures:
            print(f' - {failure}')
        return 1

    print(f'Validated {len(files)} workflow file(s).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
