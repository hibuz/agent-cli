from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ..api.models import AgentMetadata
from ..api.database import get_db, engine
from ..api.schemas import AgentRegister, AgentResponse, AgentList

# Create database tables
from ..api.models import Base
Base.metadata.create_all(bind=engine)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/agents/register", response_model=AgentResponse)
async def register_agent(agent: AgentRegister, db: Session = Depends(get_db)):
    """
    Register a new agent or update an existing one.
    """
    try:
        # Check if agent already exists
        db_agent = db.query(AgentMetadata).filter(AgentMetadata.agent_id == agent.agent_id).first()

        if db_agent:
            # Update existing agent
            db_agent.name = agent.name
            db_agent.description = agent.description
            db_agent.version = agent.version
            db_agent.input_schema = agent.input_schema
            db_agent.output_schema = agent.output_schema
            db_agent.is_active = agent.is_active
            logger.info(f"Updated agent: {agent.agent_id}")
        else:
            # Create new agent
            db_agent = AgentMetadata(
                agent_id=agent.agent_id,
                name=agent.name,
                description=agent.description,
                version=agent.version,
                input_schema=agent.input_schema,
                output_schema=agent.output_schema,
                is_active=agent.is_active
            )
            db.add(db_agent)
            logger.info(f"Registered new agent: {agent.agent_id}")

        db.commit()
        db.refresh(db_agent)

        return AgentResponse.from_orm(db_agent)

    except Exception as e:
        db.rollback()
        logger.error(f"Error registering agent {agent.agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents", response_model=List[AgentResponse])
async def list_agents(skip: int = 0, limit: int = 100, active_only: bool = True, db: Session = Depends(get_db)):
    """
    List all registered agents.
    """
    try:
        query = db.query(AgentMetadata)
        if active_only:
            query = query.filter(AgentMetadata.is_active == True)

        agents = query.offset(skip).limit(limit).all()
        return [AgentResponse.from_orm(agent) for agent in agents]

    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """
    Get a specific agent by ID.
    """
    try:
        agent = db.query(AgentMetadata).filter(AgentMetadata.agent_id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

        return AgentResponse.from_orm(agent)

    except Exception as e:
        logger.error(f"Error getting agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    """
    Delete an agent (soft delete by setting is_active to False).
    """
    try:
        agent = db.query(AgentMetadata).filter(AgentMetadata.agent_id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

        agent.is_active = False
        db.commit()
        logger.info(f"Deactivated agent: {agent_id}")

        return {"message": f"Agent {agent_id} deactivated successfully"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error deactivating agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))