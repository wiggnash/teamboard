from django.core.management.base import BaseCommand

from kb_entries.models import KBEntry


# Starter Q&A content. Keywords (api, database, cache, deploy, index, auth)
# intentionally overlap across categories so a single search term matches
# multiple entries.
KB_ENTRIES = [
    # --- API ---
    {
        "category": KBEntry.Category.API,
        "question": "What is a REST API?",
        "answer": "A REST API is an interface that exposes resources over HTTP using "
                  "standard methods like GET, POST, PUT, and DELETE. Clients send "
                  "requests and receive responses, commonly in JSON.",
    },
    {
        "category": KBEntry.Category.API,
        "question": "How do I authenticate requests to an API?",
        "answer": "Common API authentication methods include API keys, JWT tokens, and "
                  "OAuth2. The credential is usually sent in the Authorization header "
                  "rather than the request body.",
    },
    {
        "category": KBEntry.Category.API,
        "question": "What is the difference between PUT and PATCH in an API?",
        "answer": "PUT replaces an entire resource, while PATCH updates only the fields "
                  "you send. Use PATCH for partial updates to avoid overwriting data.",
    },
    {
        "category": KBEntry.Category.API,
        "question": "What does HTTP status code 401 mean in an API response?",
        "answer": "401 Unauthorized means the request lacks valid authentication "
                  "credentials. It differs from 403 Forbidden, where you are "
                  "authenticated but not allowed to access the resource.",
    },
    {
        "category": KBEntry.Category.API,
        "question": "How can I version a REST API?",
        "answer": "Common API versioning strategies include putting the version in the "
                  "URL path (/v1/), in a request header, or in a query parameter. URL "
                  "versioning is the most visible and widely used.",
    },

    # --- Database ---
    {
        "category": KBEntry.Category.DATABASE,
        "question": "What is a database index and why does it matter?",
        "answer": "An index is a data structure that speeds up read queries by letting "
                  "the database find rows without scanning the whole table. It costs "
                  "extra storage and slightly slower writes.",
    },
    {
        "category": KBEntry.Category.DATABASE,
        "question": "What is the difference between SQL and NoSQL databases?",
        "answer": "SQL databases are relational with fixed schemas and strong "
                  "consistency, while NoSQL databases (document, key-value, graph) "
                  "trade rigid schemas for flexibility and horizontal scaling.",
    },
    {
        "category": KBEntry.Category.DATABASE,
        "question": "What is a database transaction?",
        "answer": "A transaction groups multiple operations so they all succeed or all "
                  "fail together (atomicity). This keeps the database consistent even "
                  "if an error happens midway.",
    },
    {
        "category": KBEntry.Category.DATABASE,
        "question": "How does a foreign key work in a relational database?",
        "answer": "A foreign key links a row in one table to the primary key of another, "
                  "enforcing referential integrity so you cannot reference a record "
                  "that does not exist.",
    },
    {
        "category": KBEntry.Category.DATABASE,
        "question": "What is database connection pooling?",
        "answer": "Connection pooling reuses a set of open database connections instead "
                  "of opening a new one per request, reducing latency and load under "
                  "high traffic.",
    },

    # --- Cloud ---
    {
        "category": KBEntry.Category.CLOUD,
        "question": "What is the difference between IaaS, PaaS, and SaaS?",
        "answer": "IaaS gives you raw infrastructure (VMs, storage), PaaS gives you a "
                  "managed platform to deploy apps, and SaaS delivers finished software "
                  "over the internet. Each layer hides more of the stack.",
    },
    {
        "category": KBEntry.Category.CLOUD,
        "question": "How do I deploy an application to the cloud?",
        "answer": "Typical cloud deployment involves packaging the app (often in a "
                  "container), pushing it to a registry, and running it on a managed "
                  "service. CI/CD pipelines automate build, test, and deploy steps.",
    },
    {
        "category": KBEntry.Category.CLOUD,
        "question": "What is horizontal scaling in the cloud?",
        "answer": "Horizontal scaling adds more instances of a service to handle load, "
                  "as opposed to vertical scaling, which makes a single instance bigger. "
                  "A load balancer distributes traffic across instances.",
    },
    {
        "category": KBEntry.Category.CLOUD,
        "question": "What is a cache and why is it used in cloud systems?",
        "answer": "A cache stores frequently accessed data in fast storage (like Redis) "
                  "so repeated requests avoid hitting the database, lowering latency and "
                  "reducing load.",
    },
    {
        "category": KBEntry.Category.CLOUD,
        "question": "What is the purpose of a load balancer?",
        "answer": "A load balancer spreads incoming requests across multiple servers to "
                  "improve availability and performance, and routes traffic away from "
                  "unhealthy instances.",
    },

    # --- Framework ---
    {
        "category": KBEntry.Category.FRAMEWORK,
        "question": "What is Django and what is it used for?",
        "answer": "Django is a high-level Python web framework for building backends "
                  "quickly. It includes an ORM, an admin site, authentication, and a "
                  "structured request/response cycle.",
    },
    {
        "category": KBEntry.Category.FRAMEWORK,
        "question": "What is an ORM in a backend framework?",
        "answer": "An ORM (Object-Relational Mapper) lets you query the database using "
                  "objects and methods instead of raw SQL. Django's ORM maps model "
                  "classes to database tables.",
    },
    {
        "category": KBEntry.Category.FRAMEWORK,
        "question": "What is middleware in a web framework?",
        "answer": "Middleware is a layer that processes every request and response, used "
                  "for things like authentication, logging, and caching, before the "
                  "request reaches your view.",
    },
    {
        "category": KBEntry.Category.FRAMEWORK,
        "question": "How does Django REST Framework handle serialization?",
        "answer": "DRF uses serializers to convert model instances to JSON for API "
                  "responses and to validate incoming request data before saving it to "
                  "the database.",
    },
    {
        "category": KBEntry.Category.FRAMEWORK,
        "question": "What is a database migration in Django?",
        "answer": "A migration is a versioned file describing schema changes. "
                  "makemigrations generates it from your models, and migrate applies it "
                  "to the database.",
    },

    # --- General ---
    {
        "category": KBEntry.Category.GENERAL,
        "question": "What is the difference between authentication and authorization?",
        "answer": "Authentication verifies who you are (login), while authorization "
                  "decides what you are allowed to do (permissions). You authenticate "
                  "first, then authorization checks access.",
    },
    {
        "category": KBEntry.Category.GENERAL,
        "question": "What is an environment variable and why use one?",
        "answer": "An environment variable stores configuration (like database "
                  "credentials or API keys) outside the code, so secrets are not "
                  "hardcoded and settings can differ per environment.",
    },
    {
        "category": KBEntry.Category.GENERAL,
        "question": "What is the difference between HTTP and HTTPS?",
        "answer": "HTTPS is HTTP encrypted with TLS, protecting data in transit from "
                  "eavesdropping and tampering. APIs handling credentials should always "
                  "use HTTPS.",
    },
    {
        "category": KBEntry.Category.GENERAL,
        "question": "What is JSON and why is it used in APIs?",
        "answer": "JSON is a lightweight, text-based data format that is easy for humans "
                  "to read and machines to parse. It is the most common format for API "
                  "request and response bodies.",
    },
    {
        "category": KBEntry.Category.GENERAL,
        "question": "What does idempotent mean for an API request?",
        "answer": "An idempotent request produces the same result no matter how many "
                  "times it is sent. GET, PUT, and DELETE are idempotent; POST usually "
                  "is not.",
    },
]


class Command(BaseCommand):
    help = "Seed the knowledge base with starter Q&A entries."

    def handle(self, *args, **options):
        created_count = 0

        for entry in KB_ENTRIES:
            obj, created = KBEntry.objects.get_or_create(
                question=entry["question"],
                defaults={
                    "answer": entry["answer"],
                    "category": entry["category"],
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded KB: {created_count} new entries created, "
                f"{len(KB_ENTRIES) - created_count} already existed."
            )
        )
