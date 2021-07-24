def create_session():
    from sqlalchemy.orm import Session
    from rainman.models import engine

    return Session(engine)
