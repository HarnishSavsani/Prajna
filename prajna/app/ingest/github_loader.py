import logging
from prajna.app.graph.falkor_client import falkor_client

logger = logging.getLogger(__name__)

def seed_github_data(tenant: str = "kirana") -> None:
    """
    Ingests GitHub-style engineering data: Services, Modules, Files, PRs, Persons, Releases.
    Idempotent using MERGE.
    """
    cypher = """
    // Persons / Engineers
    MERGE (admin:Person {id: 'person:admin'})
      SET admin.display_name = 'Admin', admin.email = 'admin@prajna.ai', admin.role = 'System Administrator', admin.is_restricted = false
    MERGE (rohan:Person {id: 'person:rohan'})
      SET rohan.display_name = 'Rohan Gaikwad', rohan.email = 'rohan@prajna.ai', rohan.role = 'Lead Architect', rohan.is_restricted = false
    MERGE (ronit:Person {id: 'person:ronit'})
      SET ronit.display_name = 'Ronit Munde', ronit.email = 'ronit@prajna.ai', ronit.role = 'Senior Backend Engineer', ronit.is_restricted = false
    MERGE (swati:Person {id: 'person:swati'})
      SET swati.display_name = 'Swati Gangurde', swati.email = 'swati@prajna.ai', swati.role = 'Staff Graph Engineer', swati.is_restricted = false
    MERGE (harnish:Person {id: 'person:harnish'})
      SET harnish.display_name = 'Harnish Savsani', harnish.email = 'harnish@prajna.ai', harnish.role = 'Founding AI Engineer', harnish.is_restricted = false
    MERGE (alice:Person {id: 'person:alice'})
      SET alice.display_name = 'Alice Chen', alice.email = 'alice@prajna.ai', alice.role = 'Staff Engineer', alice.is_restricted = false
    MERGE (bob:Person {id: 'person:bob'})
      SET bob.display_name = 'Bob Taylor', bob.email = 'bob@prajna.ai', bob.role = 'Senior Engineer', bob.is_restricted = false
    MERGE (charlie:Person {id: 'person:charlie'})
      SET charlie.display_name = 'Charlie Davis', charlie.email = 'charlie@prajna.ai', charlie.role = 'Junior Engineer', charlie.is_restricted = false
    MERGE (eve:Person {id: 'person:eve'})
      SET eve.display_name = 'Eve Secret', eve.email = 'eve@contractor.com', eve.role = 'External Contractor', eve.is_restricted = true

    // Services
    MERGE (s_pay:Service {id: 'service:payments', name: 'payments-service', tier: 'tier-1'})
    MERGE (s_auth:Service {id: 'service:auth', name: 'auth-service', tier: 'tier-1'})
    MERGE (s_ord:Service {id: 'service:orders', name: 'orders-service', tier: 'tier-2'})
    MERGE (s_notif:Service {id: 'service:notifications', name: 'notifications-service', tier: 'tier-3'})

    // Dependencies (CALLS / DEPENDS_ON)
    MERGE (s_ord)-[:CALLS]->(s_pay)
    MERGE (s_pay)-[:CALLS]->(s_auth)
    MERGE (s_notif)-[:CALLS]->(s_auth)

    // Modules & Files
    MERGE (m_gate:Module {id: 'module:gateway', name: 'gateway'})
    MERGE (m_settle:Module {id: 'module:settlement', name: 'settlement'})
    MERGE (m_gate)-[:PART_OF]->(s_pay)
    MERGE (m_settle)-[:PART_OF]->(s_pay)

    MERGE (f1:File {id: 'file:gateway.py', name: 'gateway.py', path: 'src/gateway.py'})-[:PART_OF]->(m_gate)
    MERGE (f2:File {id: 'file:settle.py', name: 'settle.py', path: 'src/settle.py'})-[:PART_OF]->(m_settle)

    // Pull Requests & Contributions
    MERGE (pr101:PR {id: 'pr:101', title: 'Implement Stripe gateway adapter', merged_at: '2026-09-01T12:00:00Z'})
    MERGE (pr102:PR {id: 'pr:102', title: 'Add idempotent refund webhooks', merged_at: '2026-09-15T15:00:00Z'})
    MERGE (pr103:PR {id: 'pr:103', title: 'Optimize settlement ledger lock', merged_at: '2026-10-01T10:00:00Z'})
    MERGE (pr104:PR {id: 'pr:104', title: 'Add FalkorDB GraphBLAS multi-hop inference', merged_at: '2026-10-14T10:00:00Z'})

    MERGE (pr101)-[:TOUCHES]->(f1)
    MERGE (pr102)-[:TOUCHES]->(f1)
    MERGE (pr103)-[:TOUCHES]->(f2)
    MERGE (pr104)-[:TOUCHES]->(f1)

    MERGE (harnish)-[:AUTHORED]->(pr104)
    MERGE (rohan)-[:REVIEWED]->(pr104)
    MERGE (swati)-[:REVIEWED]->(pr104)
    MERGE (ronit)-[:AUTHORED]->(pr103)
    MERGE (alice)-[:AUTHORED]->(pr101)
    MERGE (alice)-[:AUTHORED]->(pr102)
    MERGE (bob)-[:REVIEWED]->(pr101)
    MERGE (bob)-[:AUTHORED]->(pr103)

    // Releases & Issues
    MERGE (rel1:Release {id: 'release:v1.4.0', released_at: '2026-10-10T00:00:00Z'})
    MERGE (iss1:Issue {id: 'issue:101', title: 'Timeout on high-volume webhook refunds', state: 'closed'})
    MERGE (rel1)-[:CONTAINS]->(pr102)
    MERGE (pr102)-[:FIXES]->(iss1)
    """
    falkor_client.query(cypher, tenant=tenant)
    logger.info("GitHub engineering graph seeded.")
