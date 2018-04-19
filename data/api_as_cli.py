"""Show how the CLI is working under the hood."""
from selang import get_models, models_to_se
models = get_models('data/kalgash.json')
models_to_se(models, '~/games/space_engine/SpaceEngine/')
