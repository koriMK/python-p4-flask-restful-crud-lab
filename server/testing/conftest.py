#!/usr/bin/env python3

import pytest
from app import app
from models import db, Plant

@pytest.fixture(autouse=True)
def setup_database():
    with app.app_context():
        db.create_all()
        
        # Add test data
        if not Plant.query.first():
            plants = [
                Plant(name="Aloe", image="./images/aloe.jpg", price=11.50, is_in_stock=True),
                Plant(name="ZZ Plant", image="./images/zz-plant.jpg", price=25.98, is_in_stock=True),
            ]
            for plant in plants:
                db.session.add(plant)
            db.session.commit()
        
        yield
        
        db.session.remove()
        db.drop_all()

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))
