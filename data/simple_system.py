from selang import ref, orbit, Model, model_to_se


model = Model(
    'My little system',
    {
        'sun': (2, orbit(1)),
        2: ('moon', orbit(0.05)),
    },
    {
        2: ref('earth'),
    }
)

model_to_se(model, '~/games/space_engine/SpaceEngine/')
