from sqlalchemy import create_engine, Column, String, Text,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import func
from sqlalchemy import DateTime

# Database connection
#DATABASE_URL = "sqlite:///database.db"
DATABASE_URL = "sqlite:////app/database.db"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True logs SQL statements for debugging
# Session = sessionmaker(bind=engine)
# Use scoped_session for thread-safe session management
Session = scoped_session(sessionmaker(bind=engine))
#session = Session()

# Base class for models
Base = declarative_base()

# Define the Issue model
class Issue(Base):
    __tablename__ = 'issues'

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    predicted_label = Column(String, nullable=False)
    corrected_label = Column(String)
    confidence = Column(Float)
    

# Initialize the database
def initialize_database():
    Base.metadata.create_all(engine)  # Creates the tables based on models
    print("Database initialized!")

def save_prediction(issue_id, title, body, predicted_label,confidence):
    """Save the predicted issue to the database."""
    session = Session()
    issue = Issue(id=issue_id, title=title, body=body, predicted_label=predicted_label,confidence=confidence)
    session.add(issue)
    session.commit()
    session.close()

def update_corrected_label(issue_id, corrected_label):
    """Update the corrected label for the given issue ID."""
    session = Session()
    issue = session.query(Issue).filter(Issue.id == issue_id).first()
    if issue:
        issue.corrected_label = corrected_label
        session.commit()
    session.close()

'''def fetch_issue(issue_id):
    """Fetch an issue by its ID."""
    return session.query(Issue).filter(Issue.id == issue_id).first()'''
def fetch_issue(issue_id):
    """Fetch an issue by its ID."""
    session = Session() 
    issue = session.query(Issue).filter(Issue.id == issue_id).first()
    session.close()
    return {
        "id": issue.id,
        "title": issue.title,
        "body": issue.body,
        "predicted_label": issue.predicted_label,
        "confidence": issue.confidence,
        "corrected_label": issue.corrected_label
    } if issue else None






