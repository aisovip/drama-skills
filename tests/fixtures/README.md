# Synthetic forward-test inputs

These fixtures are newly written test material. They contain no private project
text, source identifier, URL, filesystem path, production prompt, or expected
creative answer.

- `journeys/` contains three blind creator inputs. A run may read the brief,
  request, and constraints, but it must not receive an expected beat map, asset
  list, shot list, or prompt.
- `invalid/` contains one isolated input per craft layer. The directory tells the
  harness that the artifact needs review; the fixture does not prescribe a
  finding, verdict, rewrite, or correction.

Evaluate generated text only with the shipped evidence rubrics. These fixtures
do not test rendered-media quality, acting quality, or market performance.
