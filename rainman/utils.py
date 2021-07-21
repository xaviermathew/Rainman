def create_session():
    from sqlalchemy.orm import Session
    from rainman.models import engine

    return Session(engine)


def all_subclasses(cls):
    all_classes = cls.__subclasses__()
    all_classes.extend([sub_class
                        for klass in cls.__subclasses__()
                        for sub_class in all_subclasses(klass)])
    return list(set(all_classes))


def discover_fetchers():
    from rainman.fetcher import BaseFetcher
    return [klass for klass in all_subclasses(BaseFetcher) if not klass.IS_ABSTRACT]
