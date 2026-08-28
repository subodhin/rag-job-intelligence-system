#from app.services.insight_service import get_job_insights
from app.services.data_service import generate_insights



def job_insights_tool():
    """
    Return job market insights.
    """
    return generate_insights()