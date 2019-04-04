class Action:
    def __init__(self, key, duration, function, triggers, name, description):
        self.name = name
        self.key = key
        self.description = description
        self.duration = duration
        self.function = function
        self.triggers = triggers
        self.actor = None

    def __call__(self, **kwargs):
        from entity import Entity, EntityView
        for key in kwargs.keys():
            if isinstance(kwargs[key], Entity):
                kwargs[key].timer -= self.duration
                kwargs[key] = EntityView(kwargs[key], key)
        if self.actor:
            self.function(**kwargs, this=EntityView(self.actor, 'this'))
        else:
            self.function(**kwargs)

