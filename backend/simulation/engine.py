import asyncio
import os
import random
from datetime import datetime, timezone
import structlog
from google.cloud import firestore # type: ignore

logger = structlog.get_logger()

# Constants
ZONES = ["north_gate", "south_gate", "food_court_a", "merch_shop_1", "vip_lounge", "medical_tent"]
INCIDENT_TYPES = ["MEDICAL", "SECURITY", "FIRE", "STRUCTURAL", "CROWD", "OTHER"]
SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

class SimulationEngine:
    def __init__(self):
        project_id = os.environ.get("GCP_PROJECT_ID", "demo-project")
        database = os.environ.get("FIRESTORE_DATABASE", "(default)")
        self.db = firestore.AsyncClient(project=project_id, database=database)
        self.running = False
        
    async def generate_crowd_update(self):
        batch = self.db.batch()
        
        for zone in ZONES:
            capacity = random.randint(1000, 5000)
            current = random.randint(0, capacity)
            percentage = (current / capacity) * 100
            
            level = "LOW"
            if percentage > 90:
                level = "CRITICAL"
            elif percentage > 75:
                level = "HIGH"
            elif percentage > 50:
                level = "MODERATE"
            doc_ref = self.db.collection("crowd_density").document()
            data = {
                "zone_id": zone,
                "current_occupancy": current,
                "capacity": capacity,
                "percentage": percentage,
                "level": level,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            batch.set(doc_ref, data)
            
        await batch.commit()
        logger.info("simulate.crowd", status="updated", zones=len(ZONES))
        
    async def generate_incident(self):
        # 10% chance per cycle to generate an incident
        if random.random() > 0.10:
            return
            
        doc_ref = self.db.collection("incidents").document()
        data = {
            "type": random.choice(INCIDENT_TYPES),
            "description": "Simulated automatic event from Simulation Engine.",
            "zone_id": random.choice(ZONES),
            "severity": random.choice(SEVERITIES),
            "status": "OPEN",
            "reporter_id": "simulation_engine",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "assigned_to": None,
            "ai_summary": "Automatic simulation trigger. System must respond."
        }
        await doc_ref.set(data)
        logger.info("simulate.incident", status="created", incident_type=data["type"], zone=data["zone_id"])

    async def run(self, delay_seconds: int = 5):
        self.running = True
        logger.info("simulation.start", delay=delay_seconds)
        try:
            while self.running:
                await self.generate_crowd_update()
                await self.generate_incident()
                await asyncio.sleep(delay_seconds)
        except asyncio.CancelledError:
            logger.info("simulation.cancelled")
        finally:
            self.running = False
            logger.info("simulation.stop")

async def main():
    import argparse
    parser = argparse.ArgumentParser(description="NEXOVA Simulation Engine")
    parser.add_argument("--interval", type=int, default=5, help="Interval in seconds between updates")
    args = parser.parse_args()
    
    engine = SimulationEngine()
    await engine.run(args.interval)

if __name__ == "__main__":
    asyncio.run(main())
