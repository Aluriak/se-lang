from selang import get_models, models_to_se


# model = Model(
    # 'My little system',
    # {
        # 'sun': (2, orbit(1)),
        # 2: ('moon', orbit(0.05)),
    # },
    # {
        # 2: ref('earth'),
    # }
# )
models = get_models('data/kalgash.json')

models_to_se(models, '~/games/space_engine/SpaceEngine/')
