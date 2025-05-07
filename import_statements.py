import json
from app import create_app
from app.models import db, Statement

app = create_app()

with app.app_context():
    with open('data/actiontype_statements.json') as f:
        statements = json.load(f)

    for s in statements:
        new_statement = Statement(
            statement_number=s['statement_number'],
            choice_1_text=s['statement_choices'][0]['choice_text'],
            choice_2_text=s['statement_choices'][1]['choice_text']
        )
        db.session.add(new_statement)

    db.session.commit()
    print(f"✅ Imported {len(statements)} statements!")
