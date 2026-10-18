import logging
from prajna.app.graph.falkor_client import falkor_client

logger = logging.getLogger(__name__)

def seed_synthetic_overlay(tenant: str = "kirana") -> None:
    """
    Ingests DevRev & Microsoft Work IQ style cross-domain entities:
    Teams, Ownership, Features, Products, Customer Tickets, Decisions, and Permissions.
    Separated into modular statements to conform strictly to openCypher syntax.
    """
    statements = [
        # 1. Teams & Ownership
        """
        MERGE (t_core:Team {id: 'team:core-ai', name: 'Core AI Team'})
        MERGE (t_pay:Team {id: 'team:payments', name: 'Payments Team'})
        MERGE (t_sec:Team {id: 'team:security', name: 'Security Team'})
        """,
        """
        MATCH (admin:Person {id: 'person:admin'})
        MATCH (rohan:Person {id: 'person:rohan'})
        MATCH (ronit:Person {id: 'person:ronit'})
        MATCH (swati:Person {id: 'person:swati'})
        MATCH (harnish:Person {id: 'person:harnish'})
        MATCH (alice:Person {id: 'person:alice'})
        MATCH (bob:Person {id: 'person:bob'})
        MATCH (s_pay:Service {id: 'service:payments'})
        MATCH (t_core:Team {id: 'team:core-ai'})
        MATCH (t_pay:Team {id: 'team:payments'})

        MERGE (admin)-[:MEMBER_OF]->(t_core)
        MERGE (rohan)-[:MEMBER_OF]->(t_core)
        MERGE (ronit)-[:MEMBER_OF]->(t_core)
        MERGE (swati)-[:MEMBER_OF]->(t_core)
        MERGE (harnish)-[:MEMBER_OF]->(t_core)
        MERGE (alice)-[:MEMBER_OF]->(t_pay)
        MERGE (bob)-[:MEMBER_OF]->(t_pay)

        MERGE (t_pay)-[:OWNS]->(s_pay)
        MERGE (t_core)-[:OWNS]->(s_pay)
        """,

        # 2. Products, Capabilities, Features & Services
        """
        MERGE (prod:Product {id: 'product:checkout-suite', name: 'Checkout Suite'})
        MERGE (cap:Capability {id: 'capability:payment-processing', name: 'Payment Processing'})-[:PART_OF]->(prod)
        MERGE (f_checkout:Feature {id: 'feature:checkout', name: 'Instant Checkout'})-[:PART_OF]->(cap)
        MERGE (f_auth:Feature {id: 'feature:auth', name: 'Multi-Factor Auth'})-[:PART_OF]->(cap)
        """,
        """
        MATCH (s_pay:Service {id: 'service:payments'})
        MATCH (f_checkout:Feature {id: 'feature:checkout'})
        MERGE (s_pay)-[:SERVES]->(f_checkout)
        """,

        # 3. Customer Tickets (DevRev style)
        """
        MERGE (cust_acme:Person {id: 'person:acme-corp', display_name: 'Acme Corp CTO'})
        MERGE (cust_globex:Person {id: 'person:globex', display_name: 'Globex Lead Dev'})
        MERGE (tk1:Ticket {id: 'ticket:201', title: 'Webhook fails on peak hours', status: 'resolved'})
        MERGE (tk2:Ticket {id: 'ticket:202', title: 'Payment latency exceeds 3000ms', status: 'new'})
        MERGE (cust_acme)-[:REPORTED]->(tk1)
        MERGE (cust_globex)-[:REPORTED]->(tk2)
        """,
        """
        MATCH (tk1:Ticket {id: 'ticket:201'})
        MATCH (tk2:Ticket {id: 'ticket:202'})
        MATCH (f_checkout:Feature {id: 'feature:checkout'})
        MERGE (tk1)-[:ABOUT]->(f_checkout)
        MERGE (tk2)-[:ABOUT]->(f_checkout)
        """,
        """
        MATCH (tk1:Ticket {id: 'ticket:201'})
        MATCH (iss1:Issue {id: 'issue:101'})
        MERGE (tk1)-[:ESCALATED_TO]->(iss1)
        """,

        # 4. ADRs (Decisions) & Supersedes Chain
        """
        MERGE (d1:Decision {
          id: 'decision:1',
          text: 'Migrate session storage from Redis to FalkorDB multi-tenant graphs',
          decided_at: '2026-08-01',
          status: 'superseded'
        })
        MERGE (d2:Decision {
          id: 'decision:2',
          text: 'Adopt GraphBLAS Cypher-native scoring for all knowledge agents',
          decided_at: '2026-10-12',
          status: 'active'
        })
        MERGE (d2)-[:SUPERSEDES]->(d1)
        """,
        """
        MATCH (d2:Decision {id: 'decision:2'})
        MATCH (pr101:PR {id: 'pr:101'})
        MERGE (d2)-[:BASED_ON]->(pr101)
        """,

        # 5. Permission Sources & CAN_READ edges
        """
        MERGE (src_public:Source {id: 'source:engineering-public', name: 'Public Engineering Graph'})
        MERGE (src_sec:Source {id: 'source:security-private', name: 'Confidential Security Audits'})
        """,
        """
        MATCH (admin:Person {id: 'person:admin'})
        MATCH (rohan:Person {id: 'person:rohan'})
        MATCH (ronit:Person {id: 'person:ronit'})
        MATCH (swati:Person {id: 'person:swati'})
        MATCH (harnish:Person {id: 'person:harnish'})
        MATCH (alice:Person {id: 'person:alice'})
        MATCH (bob:Person {id: 'person:bob'})
        MATCH (t_sec:Team {id: 'team:security'})
        MATCH (src_public:Source {id: 'source:engineering-public'})
        MATCH (src_sec:Source {id: 'source:security-private'})

        MERGE (admin)-[:CAN_READ]->(src_public)
        MERGE (admin)-[:CAN_READ]->(src_sec)
        MERGE (rohan)-[:CAN_READ]->(src_public)
        MERGE (ronit)-[:CAN_READ]->(src_public)
        MERGE (swati)-[:CAN_READ]->(src_public)
        MERGE (harnish)-[:CAN_READ]->(src_public)
        MERGE (alice)-[:CAN_READ]->(src_public)
        MERGE (bob)-[:CAN_READ]->(src_public)
        MERGE (t_sec)-[:CAN_READ]->(src_sec)
        """
    ]

    for stmt in statements:
        falkor_client.query(stmt, tenant=tenant)

    logger.info("Synthetic org overlay graph seeded successfully.")
